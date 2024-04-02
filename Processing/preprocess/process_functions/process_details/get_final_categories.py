import copy
import pydash as _

from Processing.constants import CATEGORY_FULL_PROCESS, CATEGORY_NAMES


def get_final_categories_and_name(category_id, title, categories, gender, lines, parameters, skus, model):
    # category_id = str(product["preprocessed_data"]["categoryId"])
    # title = product["preprocessed_data"]["title"].lower()
    # categories_new = product["processed_api_data"]["categories"]
    # gender = product["processed_api_data"]["gender"]
    # lines = product["processed_api_data"]["lines"]
    # parameters = product["product_info_from_parameters"]
    categories_new = copy.deepcopy(categories)
    category_id = str(category_id)

    min_price = 1000000000
    for sku in skus:
        if "zh_price" in sku and sku["zh_price"]:
            min_price = min(min_price, sku["zh_price"])
    # for propertyId in product["units_of_propertyIds_dict"]:
    #     for unit in product["units_of_propertyIds_dict"][propertyId]["units"]:
    #         for offer in unit["offers"]:
    #             min_price = min(min_price, offer["price"])

    category_full_process = copy.deepcopy(_.get(CATEGORY_FULL_PROCESS, category_id, dict()))

    for category_to_add_by_title in _.get(category_full_process, "categories_to_add_by_title", []):
        if any(subtitle.lower() in title for subtitle in category_to_add_by_title["any_subtitles"]):
            categories_new = [category for category in categories_new if
                                   category not in category_to_add_by_title["main_names_to_delete"]]
            categories_new.extend(category_to_add_by_title["main_names_to_add"])

    for category_to_add_by_gender in _.get(category_full_process, "categories_to_add_by_gender", []):
        if any(gender_in_cat in gender for gender_in_cat in category_to_add_by_gender["genders"]):
            categories_new = [category for category in categories_new if
                                   category not in category_to_add_by_gender["main_names_to_delete"]]
            categories_new.extend(category_to_add_by_gender["main_names_to_add"])

    for category_to_add_by_parameters in _.get(category_full_process, "categories_to_add_by_parameters", []):
        for parameter in category_to_add_by_parameters["any_parameters"]:
            if any(param in map(lambda x: x.lower(), _.get(parameters, parameter, list())) for param in
                   category_to_add_by_parameters["any_parameters"][parameter]):
                categories_new = [category for category in categories_new if
                                       category not in category_to_add_by_parameters["main_names_to_delete"]]
                categories_new.extend(category_to_add_by_parameters["main_names_to_add"])

    for category_to_add_by_min_price in _.get(category_full_process, "categories_to_add_by_min_price", []):
        if min_price >= category_to_add_by_min_price["min_price"]:
            categories_new = [category for category in categories_new if
                                   category not in category_to_add_by_min_price["main_names_to_delete"]]
            categories_new.extend(category_to_add_by_min_price["main_names_to_add"])

    seen = set()
    result = []

    for item in categories_new:
        if item not in seen:
            seen.add(item)
            result.append(item)

    categories_new = result

    categories_copy = copy.copy(categories_new)

    for i in range(len(categories_copy)):
        categories_copy[i] = copy.copy(CATEGORY_NAMES[categories_copy[i]]["path"])

    categories_copy = list(sorted(categories_copy, key=len))

    for i in range(len(categories_copy)):
        count = 0
        temp_cat_list = [item for item in categories_copy[i] if not item.startswith(("Вся", "Все", "Всё"))]
        for j in range(len(categories_copy)):
            if all(sub_cat in categories_copy[j] for sub_cat in temp_cat_list):
                count += 1
        if count > 1:
            categories_new.remove(categories_copy[i][-1])

    order = ["Сумки хобо", "Сумки тоут", "Сумки вёдра", "Клатчи", "Рюкзаки", "Сумки на грудь", "Сумки на пояс",
             "Сумки через плечо", "Сумки на плечо", "Сумки с ручками"]

    if not lines:
        model = CATEGORY_NAMES[categories_new[0]]["singular_russian_name"]
        for i in order:
            if i in categories_new:
                model = CATEGORY_NAMES[i]["singular_russian_name"]
                break

    return categories_new, model
