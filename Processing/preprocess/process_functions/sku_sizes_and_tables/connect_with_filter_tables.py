import copy

from Processing.constants import FILTER_SIZE_TABLES

FILTER_TABLE_COMBINATIONS = {
    ("Обувь", "M"): "Shoes_Adults",
    ("Обувь", "F"): "Shoes_Adults",
    ("Обувь", "K"): "Shoes_Kids",

    ("Ремни", None): "Belts",
    ("Головные уборы", None): "Hats",
    ("Очки", None): "Glasses",
    ("Перчатки", None): "Gloves",

    ("Одежда", "M"): "Clothes_Men",
    ("Одежда", "F"): "Clothes_Women",
    ("Одежда", "K"): "Clothes_Kids"
}


def connect_with_filter_tables(category_simplified, gender, main_table_row, skus):
    new_skus = copy.deepcopy(skus)

    table_name = None

    for filter_table_combination in FILTER_TABLE_COMBINATIONS:
        if (category_simplified == filter_table_combination[0] and
                (filter_table_combination[1] in gender or
                 not filter_table_combination[1])):
            table_name = FILTER_TABLE_COMBINATIONS[filter_table_combination]

            break

    if table_name:
        filter_table = FILTER_SIZE_TABLES[table_name]

        tables_rows = None
        if main_table_row in filter_table:
            tables_rows = [main_table_row]
        else:
            tables_rows = list(filter_table.keys())

        for table_row in tables_rows:
            if all(map(lambda sku: any(map(lambda size: size in filter_table[table_row],
                                           sku["filter_sizes"])), new_skus)):
                table_row = table_row

                for sku in new_skus:
                    sku["filter_sizes"] = list(filter(lambda size: size in filter_table[table_row],
                                                      sku["filter_sizes"]))

                    sku["filter_table_name"] = table_name
                    sku["filter_table_row_name"] = table_row

                    sku["view_name"] = sku["stripped_name"]
                    if table_row != "INT":
                        sku["view_name"] += " " + table_row

                break
        else:
            for sku in new_skus:
                for table_row in tables_rows:
                    if not any(map(lambda size: size in filter_table[table_row],
                                   sku["filter_sizes"])):
                        continue

                    sku["filter_sizes"] = list(filter(lambda size: size in filter_table[table_row],
                                                      sku["filter_sizes"]))
                    sku["filter_table_name"] = table_name
                    sku["filter_table_row_name"] = table_row

                    sku["view_name"] = sku["stripped_name"]
                    if table_row != "INT":
                        sku["view_name"] += " " + table_row
    else:
        for sku in new_skus:
            sku["filter_sizes"] = ["Один размер"]
            sku["filter_table_name"] = ""
            sku["filter_table_row_name"] = ""

            sku["view_name"] = sku["stripped_name"]

    return new_skus
