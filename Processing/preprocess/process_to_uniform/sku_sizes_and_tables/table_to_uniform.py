import copy
import pydash as _

from Processing.constants import TABLE_ROWS_TO_UNIFORM


def to_default_view(table_data):
    data = copy.deepcopy(table_data)

    result = list()

    for standard_table in _.get(data, "standard", list()):
        result.append(dict())
        current_table = result[-1]

        for info_dict in standard_table["details"]:
            current_table[info_dict["sizeKey"]] = info_dict["sizeValue"].split(",")

    if _.get(data, "customize", list()):
        result.append(dict())

    for customize_table in _.get(data, "customize", list()):
        # result.append(dict())
        # current_table = result[-1]
        #
        # for info_dict in customize_table:
        #     current_table[info_dict["sizeKey"]] = info_dict["sizeValue"].split(",")
        current_table = result[-1]

        current_table[customize_table["sizeKey"]] = customize_table["sizeValue"].split(",")

    result_with_uniform_rows = list()

    for table in result:
        table_with_uniform_rows = dict()

        for key in table:
            if key in TABLE_ROWS_TO_UNIFORM:
                table_with_uniform_rows[TABLE_ROWS_TO_UNIFORM[key]] = table[key]

        if table_with_uniform_rows:
            result_with_uniform_rows.append(table_with_uniform_rows)

    return result_with_uniform_rows
