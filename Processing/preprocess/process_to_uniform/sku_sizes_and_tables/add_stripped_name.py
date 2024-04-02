import copy

from Processing.preprocess.process_functions.sku_sizes_and_tables.size_to_uniform import process_size_into_standard_view


def add_stripped_name(skus, main_table_row):
    new_skus = copy.deepcopy(skus)

    for sku in new_skus:
        sku["stripped_name"] = sku["propertyDesc"].strip(main_table_row).strip()

        sku["stripped_name"] = process_size_into_standard_view(sku["stripped_name"])

    return new_skus
