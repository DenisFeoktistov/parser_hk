import json


with open("Processing/constants/files/adjacent_brand_size_tables.json", encoding='utf-8') as f:
    ADJACENT_BRAND_SIZE_TABLES = json.load(f)

with open("Processing/constants/files/catanal.json", encoding='utf-8') as f:
    CATANAL = json.load(f)

with open("Processing/constants/files/categories.json", encoding='utf-8') as f:
    CATEGORIES = json.load(f)

with open("Processing/constants/files/categories_singular.json", encoding='utf-8') as f:
    CATEGORIES_SINGULAR = json.load(f)

with open("Processing/constants/files/categories_weights.json", encoding='utf-8') as f:
    CATEGORIES_WEIGHTS = json.load(f)

with open("Processing/constants/files/category_full_process.json", encoding='utf-8') as f:
    CATEGORY_FULL_PROCESS = json.load(f)

with open("Processing/constants/files/category_hierarchy.json", encoding='utf-8') as f:
    CATEGORY_HIERARCHY = json.load(f)

with open("Processing/constants/files/category_ids.json", encoding='utf-8') as f:
    CATEGORY_IDS = json.load(f)

with open("Processing/constants/files/category_names.json", encoding='utf-8') as f:
    CATEGORY_NAMES = json.load(f)

with open("Processing/constants/files/colors.json", encoding='utf-8') as f:
    COLORS = json.load(f)

with open("Processing/constants/files/correct_name_of_rows.json", encoding='utf-8') as f:
    CORRECT_NAME_OF_ROWS = json.load(f)

with open("Processing/constants/files/filter_size_tables.json", encoding='utf-8') as f:
    FILTER_SIZE_TABLES = json.load(f)

with open("Processing/constants/files/genders.json", encoding='utf-8') as f:
    GENDERS = json.load(f)

with open("Processing/constants/files/short_to_filter_size_table_name_row_converter.json", encoding='utf-8') as f:
    SHORT_TO_FILTER_SIZE_TABLE_NAME_ROW_CONVERTER = json.load(f)

with open("Processing/constants/files/scripted_size_tables.json", encoding='utf-8') as f:
    SCRIPTED_SIZE_TABLES = json.load(f)

with open("Processing/constants/files/size_table_rows.json", encoding='utf-8') as f:
    SIZE_TABLE_ROWS = json.load(f)

with open("Processing/constants/files/size_table_rows_values.json", encoding='utf-8') as f:
    SIZE_TABLE_ROWS_VALUES = json.load(f)

with open("Processing/constants/files/spu_change_lines.json", encoding='utf-8') as f:
    SPU_CHANGE_LINES = json.load(f)

with open("Processing/constants/files/titling.json", encoding='utf-8') as f:
    TITLING = json.load(f)

with open("Processing/constants/files/title_translations.json", encoding='utf-8') as f:
    TITLE_TRANSLATIONS = json.load(f)

with open("Processing/constants/files/translations.json", encoding='utf-8') as f:
    TRANSLATIONS = json.load(f)

with open("Processing/constants/files/table_rows_to_uniform.json", encoding='utf-8') as f:
    TABLE_ROWS_TO_UNIFORM = json.load(f)

with open("Processing/constants/files/parameters.json") as file:
    PARAMETERS = json.loads(file.read())

with open("Processing/constants/files/materials.json") as file:
    MATERIALS = json.loads(file.read())
