import copy
import json

from ApiProvider import ApiProvider
from Processing.preprocess.process_functions.process_details.get_final_categories import get_final_categories_and_name
from Processing.preprocess.process_functions.process_details.process_details import process_details
from Processing.preprocess.process_functions.process_parameters.process_parameters import process_parameters
from Processing.preprocess.process_functions.sku_sizes_and_tables.connect_with_filter_tables import connect_with_filter_tables
from Processing.preprocess.process_functions.sku_sizes_and_tables.get_tables import get_tables
from Processing.preprocess.process_functions.sku_sizes_and_tables.skus_with_filter_size import get_skus_with_filter_size
from Processing.preprocess.process_functions.utils.category_simplify import category_simplify
from Processing.preprocess.process_functions.utils.get_color import get_color
from Processing.preprocess.process_to_uniform.prices_and_deliveries.add_deliveries import add_deliveries
from Processing.preprocess.process_to_uniform.sku_sizes_and_tables.add_stripped_name import add_stripped_name
from Processing.preprocess.process_to_uniform.prices_and_deliveries.add_zh_prices import add_zh_prices
from Processing.preprocess.process_to_uniform.prices_and_deliveries.remove_extra_info import remove_extra_info
from Processing.preprocess.process_to_uniform.sku_sizes_and_tables.table_to_uniform import to_default_view


def extract_info(spu_detail_data):
    result = dict()

    result["skus"] = spu_detail_data["skus"]

    details = spu_detail_data["detail"]

    result["title"] = details["title"]
    result["main_brand_id"] = str(details["brandId"])
    result["brand_ids_list"] = list(map(lambda x: x["brandId"], spu_detail_data["baseProperties"]["brandList"]))

    result["main_category_id"] = details["categoryId"]
    result["manufacturer_sku"] = details["articleNumber"]
    result["images"] = list(map(lambda x: x["url"], spu_detail_data["spuImage"]["images"]))

    parameters_list = spu_detail_data["baseProperties"]["list"]
    result["parameters"] = dict()

    for infoDict in parameters_list:
        result["parameters"][infoDict["key"]] = infoDict["value"]

    return result


async def process_sku(sku):
    search_result = await ApiProvider.async_search(sku=sku)
    product = search_result["data"]["productList"][0]

    if product["articleNumber"] != sku:
        return dict()

    spuId = product['spuId']

    spu_detail_result = await ApiProvider.async_spu_detail(spuId=spuId)
    table_result = await ApiProvider.async_table(spuId=spuId)

    # save(product_result, search_result, spu_detail_result, table_result)

    search_parameters = get_search_parameters(search_result)

    spu_detail_data = spu_detail_result["data"]
    info_dict = extract_info(spu_detail_data)

    table_data = table_result["data"]
    tables_uniform = to_default_view(table_data)

    skus = info_dict["skus"]
    skus_with_prices = add_zh_prices(skus)
    skus_with_deliveries = add_deliveries(skus_with_prices)

    main_table_row = get_main_table_row(tables_uniform)

    skus_with_stripped_name = add_stripped_name(skus_with_deliveries, main_table_row)
    skus_without_extra_info = remove_extra_info(skus_with_stripped_name)

    merged_parameters = merge_parameters(info_dict["parameters"], search_parameters)
    processed_parameters = process_parameters(merged_parameters)

    processed_details = process_details(
        title=info_dict["title"],
        main_brand_id=info_dict["main_brand_id"],
        brand_ids_list=info_dict["brand_ids_list"],
        manufacturer_sku=info_dict["manufacturer_sku"],
        category_id=info_dict["main_category_id"],
        parameters=merged_parameters
    )

    tables = get_tables(
        size_table=tables_uniform,
        brand=processed_details["brands"][0],
        line=processed_details["lines"][-1] if processed_details["lines"] else list(),
        category_simplified=category_simplify(processed_details["categories"][0]),
        gender=processed_details["gender"],
        skus=skus_without_extra_info
    )

    skus_with_filter_sizes = get_skus_with_filter_size(
        brand=processed_details["brands"][0],
        category_simplified=category_simplify(processed_details["categories"][0]),
        gender=processed_details["gender"],
        main_table_row=main_table_row,
        skus=skus_without_extra_info
    )

    skus_with_filter_info = connect_with_filter_tables(
        category_simplified=category_simplify(processed_details["categories"][0]),
        gender=processed_details["gender"],
        main_table_row=main_table_row,
        skus=skus_with_filter_sizes
    )

    skus_with_final_naming = get_skus_with_final_naming(skus_with_filter_info,
                                                        category_simplify(processed_details["categories"][0]))

    skus_merged = get_merged_skus(skus_with_final_naming)

    final_categories, final_model = get_final_categories_and_name(
        category_id=product["categoryId"],
        title=product["title"],
        categories=processed_details["categories"],
        gender=processed_details["gender"],
        lines=processed_details["lines"],
        parameters=merged_parameters,
        skus=skus_merged,
        model=processed_details["model"]
    )

    result = dict()

    for key, value in processed_details.items():
        result[key] = value

    result["categories"] = final_categories
    result["model"] = final_model
    result["skus"] = skus_merged
    result["tables"] = tables
    result["processed_parameters"] = processed_parameters
    result["tables"] = tables

    result["skus"] = skus_with_final_naming

    return result


def get_merged_skus(skus):
    count_d = dict()

    for sku in skus:
        if sku["stripped_name"] in count_d:
            count_d[sku["stripped_name"]] += 1
        else:
            count_d[sku["stripped_name"]] = 1

    new_skus = list()
    added_names = set()

    for sku in skus:
        if sku["stripped_name"] in added_names:
            continue

        if count_d[sku["stripped_name"]] == 0:
            new_skus.append(sku)
            added_names.add(sku["stripped_name"])
            continue

        sku_to_add = sku

        for sku1 in skus:
            if sku_to_add["stripped_name"] != sku1["stripped_name"]:
                continue

            if "zh_price" in sku1 and "zh_price" not in sku_to_add:
                sku_to_add = sku1
            elif "zh_price" not in sku1:
                continue
            elif "zh_price" in sku1 and "zh_price" in sku_to_add:
                if sku1["zh_price"] and sku_to_add["zh_price"] and sku_to_add["zh_price"] > sku1["zh_price"]:
                    sku_to_add = sku1

        new_skus.append(sku)
        added_names.add(sku_to_add["stripped_name"])

    return copy.deepcopy(new_skus)


def get_skus_with_final_naming(skus, category_simplified):
    new_skus = copy.deepcopy(skus)

    if category_simplified == "Обувь":
        return new_skus

    colors = set()
    for sku in new_skus:
        color = get_color(sku["propertyDesc"])
        colors.add(color)

        if color:
            sku["stripped_name"] = f'{color} {sku["stripped_name"]}'

    if len(colors) == 1:
        color = colors.pop()

        for sku in new_skus:
            sku["stripped_name"] = sku["stripped_name"].lstrip(f"{color} ")
    else:
        for sku in new_skus:
            if sku["stripped_name"] != "Один размер" and "Один размер" in sku["stripped_name"]:
                sku["stripped_name"] = sku["stripped_name"].replace("Один размер", "").strip()

    return new_skus


def merge_parameters(parameters: dict, search_parameters: dict):
    merged_parameters = dict()

    for key, value in (list(search_parameters.items()) + list(parameters.items())):
        if not isinstance(value, list) and len(value.split(", ")) > 1:
            merged_parameters[key] = value.split(", ")
        if isinstance(value, list):
            merged_parameters[key] = value
        else:
            merged_parameters[key] = [value]

    return merged_parameters


def get_search_parameters(search_result):
    search_parameters = dict()

    for infoDict in search_result["data"]["facets"]:
        search_parameters[infoDict["key"]] = list()

        for item in infoDict["items"]:
            search_parameters[infoDict["key"]].append(item["name"])

    return search_parameters


def get_main_table_row(table_uniform):
    main_table_row = ""
    if len(table_uniform) >= 1:
        main_table_row = list(table_uniform[0].keys())[0]

    return main_table_row


def save(product_result, search_result, spu_detail_result, table_result):
    with open("search_result.json", "w") as search_result_file:
        search_result_file.write(json.dumps(search_result, ensure_ascii=False, indent=4))

    with open("spu_detail_result.json", "w") as spu_detail_result_file:
        spu_detail_result_file.write(json.dumps(spu_detail_result, ensure_ascii=False, indent=4))

    with open("table_shoes.json", "w") as table_result_file:
        table_result_file.write(json.dumps(table_result, ensure_ascii=False, indent=4))

    with open("product_result.json", "w") as product_result_file:
        product_result_file.write(json.dumps(product_result, ensure_ascii=False, indent=4))
