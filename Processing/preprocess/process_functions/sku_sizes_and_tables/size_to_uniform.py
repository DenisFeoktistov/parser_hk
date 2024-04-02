# Принимает строку с размером и превращает ее в размер стандартного вида - для дефолтных размерных таблиц
# Например, XXXXXXS = 6XS, 43 1/3 = 43, 45 2/3 = 45.5
import re

from Processing.preprocess.process_functions.process_parameters.utils.get_dimensions import get_dimensions
from Processing.preprocess.utils.remove_chinese_symbols import remove_chinese_symbols


def process_size_into_standard_view(size: str):
    if "均码" in size:
        return "Один размер"

    size = remove_chinese_symbols(size)
    size = size.replace("⅓", "")
    size = size.replace("⅔", ".5")
    size = size.replace("½", ".5")
    size = size.rstrip('-')
    lower_size = size.lower()
    if lower_size == "f" or lower_size == "os" or lower_size == "os/f" or lower_size == "-":
        return "Один размер"
    if "/" in lower_size:
        if len(lower_size.split('/')) >= 2:
            size = [process_size_into_standard_view(lower_size.split('/')[0]),
                    process_size_into_standard_view(lower_size.split('/')[1])]

            if size[0] == size[1]:
                return size[0]
            else:
                return "".join(size)
    if "-" in lower_size:
        if len(lower_size.split('-')) >= 2:
            size = [process_size_into_standard_view(lower_size.split('-')[0]),
                    process_size_into_standard_view(lower_size.split('-')[1])]

            if size[0] == size[1]:
                return size[0]
            else:
                return "".join(size)
    if "*#*" in lower_size:
        if len(lower_size.split('*#*')) >= 2:
            size = [process_size_into_standard_view(lower_size.split('*#*')[0]),
                    process_size_into_standard_view(lower_size.split('*#*')[1])]

            if size[0] == "Один размер" and size[1] != "Один размер":
                return size[1]
            if size[1] == "Один размер" and size[0] != "Один размер":
                return size[0]

            if size[0] == size[1] == "Один размер":
                return "Один размер"
            else:
                return "".join(size)
    if "s/m" in lower_size:
        return ["S", "M"]
    if "l/xl" in lower_size:
        return ["L", "XL"]
    if "xxxs" in lower_size or "3xs" in lower_size:
        return "XXXS"
    if "xxs" in lower_size or "2xs" in lower_size:
        return "XXS"
    if "xs" in lower_size:
        return "XS"
    if " s " in (" " + lower_size + " "):
        return "S"
    if " m " in (" " + lower_size + " "):
        return "M"
    if "xxxxxxxxxxl" in lower_size or "10xl" in lower_size:
        return "10XL"
    if "xxxxxxxxxl" in lower_size or "9xl" in lower_size:
        return "9XL"
    if "xxxxxxxxl" in lower_size or "8xl" in lower_size:
        return "8XL"
    if "xxxxxxxl" in lower_size or "7xl" in lower_size:
        return "7XL"
    if "xxxxxxl" in lower_size or "6xl" in lower_size:
        return "6XL"
    if "xxxxxl" in lower_size or "5xl" in lower_size:
        return "5XL"
    if "xxxxl" in lower_size or "4xl" in lower_size:
        return "4XL"
    if "xxxl" in lower_size or "3xl" in lower_size:
        return "XXXL"
    if "xxl" in lower_size or "2xl" in lower_size:
        return "XXL"
    if "xl" in lower_size:
        return "XL"
    if " l " in (" " + lower_size + " "):
        return "L"
    if get_dimensions(size):
        return get_dimensions(size)
    chinese_sizes = ["155/86a",
                     "160/80a",
                     "165/84a",
                     "170/88a",
                     "175/92a",
                     "180/96a",
                     "185/100a",
                     "190/104a",
                     "195/108a",
                     "200/112a",
                     "140/64a",
                     "145/72a",
                     "150/76a",
                     "155/80a",
                     "160/84a",
                     "165/88a",
                     "170/92a",
                     "175/96a",
                     "180/100a",
                     "185/104a",
                     "190/108a",
                     "140/60a",
                     "145/64a",
                     "150/68a",
                     "155/72a",
                     "160/76a",
                     "165/80a",
                     "170/84a",
                     "175/88a",
                     "180/92a",
                     "185/96a",
                     "190/100a",
                     ]
    if lower_size in chinese_sizes:
        return size

    # Проверка на детские размеры обуви по типу 7Y, 10C, 5K
    pattern = r'\d+(\.\d+)?[yck]'
    match = re.search(pattern, lower_size)
    if match:
        matched_substring = match.group(0).upper()
        return matched_substring

    return "Один размер"
