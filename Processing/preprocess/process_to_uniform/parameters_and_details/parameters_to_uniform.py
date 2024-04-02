import pydash as _


def parameters_to_uniform(baseProperties):
    parameters_formatted = dict()

    for infoDict in _.get(baseProperties, "list", list()):
        if "key" not in infoDict or "value" not in infoDict:
            continue

        key = infoDict["key"]
        value = infoDict["value"]

        parameters_formatted[key] = value

    return parameters_formatted
