import copy


from Processing.constants import SCRIPTED_SIZE_TABLES
from Processing.preprocess.process_functions.sku_sizes_and_tables.count_missing_values import count_missing_values

SCRIPTED_TABLES_COMBINATIONS = {
    ("adidas", "M", None, True): ("adidas_Men_fractions_standard",),
    ("adidas", "F", None, True): ("adidas_Women_fractions_standard",),
    ("adidas", "K", None, True): ("adidas_Kids_mixed_standard",),

    ("adidas", "M", None, False): ("adidas_(Wo)Men_default_mixed_standard",),
    ("adidas", "F", None, False): ("adidas_(Wo)Men_default_mixed_standard",),
    ("adidas", "K", None, False): ("adidas_Kids_mixed_standard",),

    ("Nike", "M", None, False): ("Nike_Jordan_Men",),
    ("Nike", "F", None, False): ("Nike_Jordan_Women",),
    ("Nike", "K", None, False): ("Nike_Jordan_Toddler_PreSchool",),

    ("Jordan", "M", None, False): ("Nike_Jordan_Men",),
    ("Jordan", "F", None, False): ("Nike_Jordan_Women",),
    ("Jordan", "K", None, False): ("Nike_Jordan_Toddler_PreSchool",),

    ("New Balance", "M", None, False): ("NewBalance_Men", "NewBalance_Men_extra"),
    ("Nike", "F", None, False): ("NewBalance_Women",),
    ("Nike", "K", None, False): ("NewBalance_Kids",),

    ("Reebok", "M", None, False): ("Reebok_Men",),
    ("Reebok", "F", None, False): ("Reebok_Women",),
    ("Reebok", "K", None, False): ("Reebok_Kids",),

    ("Converse", "M", "Converse Chuck Taylor", False): ("Converse_Men_chuck",),
    ("Converse", "F", "Converse Chuck Taylor", False): ("Converse_Women_chuck",),
    ("Converse", "K", "Converse Chuck Taylor", False): ("Converse_Kids",),

    ("Converse", "M", None, False): ("Converse_Men_standard",),
    ("Converse", "F", None, False): ("Converse_Women_standard",),
    ("Converse", "K", None, False): ("Converse_Kids",),

    ("Asics", "M", None, False): ("Asics_Men",),
    ("Nike", "F", None, False): ("Asics_Women",),
    ("Nike", "K", None, False): ("Asics_Kids",),

    ("Vans", "M", None, False): ("Vans_Men",),
    ("Vans", "F", None, False): ("Vans_Women",),
    ("Vans", "K", None, False): ("Vans_Kids",),

    ("PUMA", "M", None, False): ("PUMA_Men", "PUMA_Men_extra"),
    ("PUMA", "F", None, False): ("PUMA_Women",),
    ("PUMA", "K", None, False): ("PUMA_Kids",),

    ("Anta", "M", None, False): ("Anta_Men",),
    ("Anta", "F", None, False): ("Anta_Women",),
    ("Anta", "K", None, False): ("Anta_Kids",),

    ("Fila", "M", None, False): ("Fila_Men",),
    ("Fila", "F", None, False): ("Fila_Women",),
    ("Fila", "K", None, False): ("Fila_Kids",),
}
SCRIPTED_DEFAULT_TABLE_COMBINATIONS = {
    ("Обувь", "M"): ("Shoes_Adults", "shoes_adults_rows_convert"),
    ("Обувь", "F"): ("Shoes_Adults", "shoes_adults_rows_convert"),
    ("Обувь", "K"): ("Shoes_Kids", "shoes_kids_rows_convert"),

    ("Ремни", None): ("Belts", "belts_rows_convert"),
    ("Головные уборы", None): ("Hats", "hats_rows_convert"),
    ("Очки", None): ("Glasses", "glasses_rows_convert"),
    ("Перчатки", None): ("Gloves", "gloves_rows_convert"),

    ("Одежда", "M"): ("Clothes_Men", "clothes_men_rows_convert"),
    ("Одежда", "F"): ("Clothes_Women", "clothes_women_rows_convert"),
    ("Одежда", "K"): ("Clothes_Kids", "clothes_kids_rows_convert")
}


def get_tables_shoes(size_table, brand, line, gender, skus):
    sizes = set([sku["stripped_name"] for sku in skus])

    fractional_sizes = {"⅓", "⅔"}
    is_frac = any([frac_size in size for size in sizes for frac_size in fractional_sizes])

    # соответствие в формате brand, gender, line, only_for_frac -> table_name

    # теперь выбираем подходящие таблицы
    table_names = None
    for scripted_table_combinations, combination_table_names in SCRIPTED_TABLES_COMBINATIONS.items():
        if scripted_table_combinations[0] == brand and \
                scripted_table_combinations[1] in gender and \
                scripted_table_combinations[2] in [None, line] and \
                scripted_table_combinations[3] in [False, is_frac]:
            table_names = combination_table_names

            break

    table_name = None

    if table_names and len(table_names) == 1:
        table_name = table_names[0]

    # выберем наиболее подходящую таблицу,
    # если есть несколько в значении по подходящей комбинации
    elif table_names and len(table_names) > 1:
        missing_values = list()

        for table_name in table_names:
            missing_values.append(count_missing_values(sizes, SCRIPTED_SIZE_TABLES[table_name]))

        for i, missing_value in enumerate(missing_values):
            if missing_value == min(missing_values):
                table_name = table_names[i]
                break

    tables = list()

    if table_name:
        scripted_size_table = SCRIPTED_SIZE_TABLES[table_name]
        tables.append(scripted_size_table)

        if count_missing_values(sizes, scripted_size_table) != 0:
            tables.append(size_table)
    else:
        extended_size_table = copy.deepcopy(size_table)

        # RU таблицу добавляем на основе EU: берем каждый размер и делаем -1 от размера (при условии, что возможно).
        if "EU" in extended_size_table:
            try:
                RU = [str(float(i) - 1) for i in extended_size_table["EU"]]
                RU = [size.replace('.0', '') for size in RU]
                extended_size_table["RU"] = RU
            except:
                pass

        tables.append(extended_size_table)

        # В качестве extra_table добавляем мою таблицу в зависимости от гендера
        if "M" in gender or "F" in gender:
            tables.append(SCRIPTED_SIZE_TABLES["Shoes_Adults"])
        else:
            tables.append(SCRIPTED_SIZE_TABLES["Shoes_Kids"])

    return tables


def get_tables_clothes(size_table, brand, line, gender, skus):
    tables = list()

    tables.append(copy.deepcopy(size_table))

    if "M" in gender:
        tables.append(copy.deepcopy(SCRIPTED_SIZE_TABLES["Clothes_Men"]))
    elif "F" in gender:
        tables.append(copy.deepcopy(SCRIPTED_SIZE_TABLES["Clothes_Women"]))
    elif "K" in gender:
        tables.append(copy.deepcopy(SCRIPTED_SIZE_TABLES["Clothes_Kids"]))

    return tables


def get_tables_belts(size_table, brand, line, gender, skus):
    tables = list()

    tables.append(copy.deepcopy(size_table))
    tables.append(copy.deepcopy(SCRIPTED_SIZE_TABLES["Belts"]))

    return tables


def get_tables_hats(size_table, brand, line, gender, skus):
    tables = list()

    tables.append(copy.deepcopy(size_table))
    tables.append(copy.deepcopy(SCRIPTED_SIZE_TABLES["Hats"]))

    return tables


def get_tables_glasses(size_table, brand, line, gender, skus):
    tables = list()

    tables.append(copy.deepcopy(size_table))
    tables.append(copy.deepcopy(SCRIPTED_SIZE_TABLES["Glasses"]))

    return tables


def get_tables_gloves(size_table, brand, line, gender, skus):
    tables = list()

    tables.append(copy.deepcopy(size_table))
    tables.append(copy.deepcopy(SCRIPTED_SIZE_TABLES["Gloves"]))

    return tables


def get_tables(size_table, brand, line, category_simplified, gender, skus):
    category_to_function = {
        "Обувь": get_tables_shoes,
        "Одежда": get_tables_clothes,
        "Ремни": get_tables_belts,
        "Головные уборы": get_tables_hats,
        "Очки": get_tables_glasses,
        "Перчатки": get_tables_gloves
    }

    if category_simplified in category_to_function:
        return category_to_function[category_simplified](size_table, brand, line, gender, skus)
    else:
        return size_table, None
