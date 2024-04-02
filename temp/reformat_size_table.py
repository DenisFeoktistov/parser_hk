import json

with open("Processing/constants/size_table.json") as tables_old_file:
    tables_old = json.loads(tables_old_file.read())

tables_new = dict()

for table_old in tables_old:
    table_name = table_old["name"]

    table = dict()

    for key, value in table_old["all_sizes"].items():
        if key != "default_size":
            table[value["size_table_row_name"]] = value["sizes"]

            for i, size in enumerate(table[value["size_table_row_name"]]):
                table[value["size_table_row_name"]][i] = (size.replace(" 1/2", ".5")
                                                          .replace(" 1/3", " ⅓")
                                                          .replace(" 2/3", " ⅔"))

    tables_new[table_old["name"]] = table

with open("../Processing/constants/files/scripted_size_tables.json", "w") as tables_new_file:
    tables_new_file.write(json.dumps(tables_new, ensure_ascii=False, indent=4))
