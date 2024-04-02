import copy

from Processing.constants import ADJACENT_BRAND_SIZE_TABLES


def get_skus_with_filter_size(skus, brand, category_simplified, gender, main_table_row):
    skus_updated = copy.deepcopy(skus)

    for sku in skus_updated:
        sku["filter_sizes"] = [sku["stripped_name"]]

        if not (brand in ADJACENT_BRAND_SIZE_TABLES and category_simplified == "Обувь"
                and main_table_row == "EU" or main_table_row == "FR"):
            continue

        if sku["stripped_name"] in ADJACENT_BRAND_SIZE_TABLES[brand][gender[0]]:
            sku["filter_sizes"].extend(ADJACENT_BRAND_SIZE_TABLES[brand][gender[0]][sku["stripped_name"]])

    return skus_updated
