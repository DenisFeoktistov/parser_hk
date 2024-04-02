from Processing.constants import PARAMETERS, MATERIALS, COLORS
from Processing.preprocess.process_functions.process_parameters.utils.get_dimensions import get_dimensions
from Processing.preprocess.process_functions.process_parameters.utils.get_proportion_list import get_proportion_list
from Processing.preprocess.process_functions.process_parameters.utils.get_weight import get_weight


def process_parameters(parameters):
    new_parameters = dict()
    filter_parameters = dict()
    filter_parameters["materials"] = list()
    filter_parameters["colors"] = list()

    for key, values in parameters.items():
        if key not in PARAMETERS:
            continue

        translation = PARAMETERS[key]["translation"]
        new_parameters[translation] = list()

        if "values" in PARAMETERS[key]:
            for value in values:
                if value.lower() in PARAMETERS[key]["values"]:
                    new_parameters[translation].append(PARAMETERS[key]["values"][value.lower()])

        type = ""
        if "type" in PARAMETERS[key]:
            type = PARAMETERS[key]["type"]
        if type == "size":
            for value in values:
                new_parameters[translation].append(get_dimensions(value))
        if type == "weight":
            for value in values:
                new_parameters[translation].append(get_weight(value))
        if type == "proportion":
            for value in values:
                new_parameters[translation].append(", ".join(get_proportion_list(value)))

        if type == "material":
            for value in values:
                value = value.lower()

                for material in sorted(MATERIALS.keys(), key=lambda x: -len(x)):
                    if material.lower() in value:
                        value = value.replace(material.lower(), "")
                        new_parameters[translation].append(MATERIALS[material]["view_name"])
                        filter_parameters["materials"].append(MATERIALS[material]["filter_name"])

        if type == "color":
            for value in values:
                value = value.lower()

                for color in sorted(COLORS.keys(), key=lambda x: -len(x)):
                    if color.lower() in value:
                        value = value.replace(color.lower(), "")
                        new_parameters[translation].append(COLORS[color]["view_name"])
                        filter_parameters["colors"].append(COLORS[color]["filter_name"])

        if translation == "Парфюмер":
            for value in values:
                new_parameters[translation].append(value)

        if translation == "Состав":
            for value in values:
                percentage = get_proportion_list(value)
                materials = list()

                for word in value.split():
                    if word.lower() in MATERIALS:
                        materials.append(MATERIALS[word.lower()]["view_name"])
                        filter_parameters["materials"].append(MATERIALS[word.lower()]["filter_name"])

                if len(percentage) == len(materials):
                    res_values = list()

                    for material, percentage in zip(materials, percentage):
                        res_values.append(f"{material}: {percentage}")

                    new_parameters[translation].append(", ".join(res_values))

        if not new_parameters[PARAMETERS[key]["translation"]]:
            del new_parameters[PARAMETERS[key]["translation"]]

    for key in new_parameters:
        new_parameters[key] = list(set(new_parameters[key]))

    for key in filter_parameters:
        filter_parameters[key] = list(set(filter_parameters[key]))

    return new_parameters, filter_parameters
