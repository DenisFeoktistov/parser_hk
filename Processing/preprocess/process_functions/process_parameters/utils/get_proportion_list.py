import re


def get_proportion_list(value):
    res = re.findall(r'\d+%', value)
    res.extend(re.findall("\d+:\d+", value))

    return res
