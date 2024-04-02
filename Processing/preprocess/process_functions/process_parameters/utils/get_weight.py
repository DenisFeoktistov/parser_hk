import re


def get_weight(value):
    res = "-".join(re.findall(r'\d+g?', value))

    return res
