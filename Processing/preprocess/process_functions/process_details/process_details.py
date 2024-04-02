import copy

import pydash as _

from Processing.constants import TITLING, CATEGORY_NAMES, CATEGORY_FULL_PROCESS, SPU_CHANGE_LINES, TITLE_TRANSLATIONS
from Processing.preprocess.process_functions.utils.capitalize_first_letter import capitalize_first_letter
from Processing.preprocess.process_functions.utils.none_in_string import none_in_string
from Processing.preprocess.process_functions.utils.replace_substring import replace_substring
from Processing.preprocess.utils.remove_chinese_symbols import remove_chinese_symbols

spu_change_lines_copy = copy.deepcopy(SPU_CHANGE_LINES)


def process_details(title, main_brand_id, brand_ids_list, manufacturer_sku, category_id, parameters):
    # Этот словарь вернет данная ф-ция
    res = dict()

    res["is_collab"] = False
    res["collab_names"] = list()
    res["brands"] = list()
    res["model"] = remove_chinese_symbols(title)
    res["lines"] = list()

    title = " " + title.lower() + " "

    lines = get_lines(main_brand_id, title)

    collabs = get_collabs(brand_ids_list, main_brand_id, manufacturer_sku, title)
    res["brands"], res["lines"], res["collab_names"] = get_final_lines_brands_collabs(brand_ids_list, lines, collabs)
    if len(collabs) > 0 or len(brand_ids_list) > 1 or " x " in title.lower():
        res["is_collab"] = True

    res["categories"] = get_starting_categories(category_id)
    res["model"] = crop_collab(collabs, main_brand_id, res["model"])
    res["model"] = crop_lines(lines, res["model"])
    res["model"] = crop_brands(main_brand_id, res["model"])
    res["model"] = crop_model(res["model"], res["collab_names"])
    res["colorway"], res["model"] = update_colorway_and_model(res["lines"], main_brand_id, title,
                                                              res["model"], res["categories"], res["brands"])

    res["date"], res["approximate_date"] = get_date(parameters)

    res["custom"] = get_is_custom(title, manufacturer_sku)

    res["gender"] = get_gender(parameters)

    if res["gender"] == ["F"] and (main_brand_id == "13" or main_brand_id == "144") and "Обувь" in \
            CATEGORY_NAMES[res["categories"][0]]["path"]:
        res["gender"].append("M")

    if res["gender"] == ["M"] and (main_brand_id == "13" or main_brand_id == "144") and "Обувь" in \
            CATEGORY_NAMES[res["categories"][0]]["path"]:
        res["gender"].append("F")

    res["manufacturer_sku"] = remove_chinese_symbols(manufacturer_sku).strip("\\").strip("/").strip('-')
    res["formatted_manufacturer_sku"] = ''.join(
        ''.join(res["manufacturer_sku"].split()).split(
            '-')).lower()

    return res


def get_starting_categories(category_id):
    if str(category_id) in CATEGORY_FULL_PROCESS:
        return copy.deepcopy(CATEGORY_FULL_PROCESS[str(category_id)]["categories_to_add_directly"])
    else:
        return ["Другие аксессуары"]


def get_main_brand(brand_list):
    for brand_id in map(str, brand_list):
        if brand_id not in TITLING:
            continue

        return brand_id

    return ""


def get_final_lines_brands_collabs(brand_ids_list, lines, collabs):
    result_brands = list()
    result_lines = list()
    result_collab_names = list()

    for brand_id in map(str, brand_ids_list):
        if brand_id in TITLING:
            result_brands.append(TITLING[brand_id]["brand_names"][0])

    for line in lines:
        result_lines.append(line["path"])

    for collab in collabs:
        result_collab_names.append(collab)

    return result_brands, result_lines, result_collab_names


def get_is_custom(title, manufacturer_sku):
    is_custom = False

    if "定制" in title or "team" in manufacturer_sku.lower():
        is_custom = True

    return is_custom


def get_gender(parameters):
    gender = list()

    for item in parameters["fitIds"]:
        if "women" == item.lower():
            gender.append("F")
        if "men" == item.lower():
            gender.append("M")
        if "kids" == item.lower():
            gender.append("K")
        if "unisex" == item.lower():
            gender.append("M")
            gender.append("F")
    gender = list(set(gender))

    return gender


def get_date(parameters):
    date = ""
    approximate_date = ""

    if "Release Date" in parameters and parameters["Release Date"][0].split(".") == 3:
        date = ".".join(parameters["Release Date"].split(".")[::-1])

        year = parameters["Release Date"].split(".")[2]
        month = parameters["Release Date"].split(".")[1]

        month_list = ["", "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль",
                      "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
        approximate_date = month_list[int(month)] + " " + year

    return date, approximate_date


def update_colorway_and_model(lines, main_brand_id, title, model, categories, brands):
    colorway = ""

    if len(lines):
        colorway = model

        if "Другие" in lines[0][-1]:
            if lines[0][-1] == "Другие Air Jordan 1":
                model = "Air Jordan 1"
            elif lines[0][-1] == "Другие Yeezy":
                model = "Yeezy"
            else:
                model = ' '.join(lines[0][-1].split()[2:])

        elif main_brand_id == "13":
            if lines[0][-1].startswith("Air"):
                model = lines[0][-1]
            else:
                model = (lines[0][-1]).replace(brands[0], "").strip()
        else:
            model = (lines[0][-1]).replace(brands[0], "").strip()
    if not lines:
        colorway = model
        model = CATEGORY_NAMES[categories[0]]["singular_russian_name"]

    colorway = capitalize_first_letter(colorway)
    model = model.replace("(", "")
    model = model.replace(")", "")
    model = model.replace("（", "")
    model = model.replace("）", "")

    colorway = colorway.replace("(", "")
    colorway = colorway.replace(")", "")
    colorway = colorway.replace("（", "")
    colorway = colorway.replace("）", "")
    title_extra_translation = translate_title(title.lower())
    colorway = (colorway + " " + title_extra_translation).strip()

    return colorway, model


def crop_model(model, collab_names):
    result_model = model

    for collab_name in collab_names:
        for i in range(collab_name.count(" x ")):
            result_model = replace_substring(result_model, " x ")

    result_model = result_model.rstrip("#")
    result_model = result_model.replace("】", " ").replace("【", " ")
    result_model = result_model.strip("-")
    result_model = result_model.strip("-")
    result_model = result_model.strip("/")
    result_model = result_model.strip("|")
    result_model = result_model.strip("\\")
    result_model = result_model.strip(".")
    result_model = result_model.strip(",")
    result_model = " ".join(result_model.split()).strip()

    if result_model:
        result_model = result_model[0].capitalize() + result_model[1:]

    return result_model


def crop_brands(main_brand_id, model):
    result_model = model

    for brand_name in sorted(TITLING[main_brand_id]["brand_names"], key=lambda s: -len(s)):
        if brand_name.lower() in result_model.lower():
            result_model = replace_substring(result_model, brand_name)
            break

    return result_model


def crop_lines(lines, model):
    result_model = model

    for line in lines:
        for line_name in sorted(_.get(line, "line_names", list()), key=lambda s: -len(s)):
            if line_name.lower() in result_model.lower():
                for line_name_no_crop in sorted(_.get(line, "line_name_no_crop", list()), key=lambda s: -len(s)):
                    if line_name_no_crop.lower() in line_name.lower():
                        result_model = replace_substring(result_model, line_name, line_name_no_crop)
                        break
                else:
                    result_model = replace_substring(result_model, line_name)

    return result_model


def crop_collab(collabs, main_brand_id, model):
    result_model = model

    for collab in collabs:
        for collab_name in sorted(_.get(TITLING[main_brand_id]["collaborations"][collab], "collab_brand_names", list()),
                                  key=lambda s: -len(s)):
            if collab_name.lower() in result_model.lower():
                for collab_name_no_crop in sorted(
                        _.get(TITLING[main_brand_id]["collaborations"][collab], "collab_brand_names_no_crop", list()),
                        key=lambda s: -len(s)):
                    if collab_name_no_crop.lower() in collab_name.lower():
                        result_model = replace_substring(result_model, collab_name, collab_name_no_crop)
                        break
                else:
                    result_model = replace_substring(result_model, collab_name)

    return result_model


def get_collabs(brand_ids_list, main_brand_id, manufacturer_sku, title):
    collabs = list()
    for collab in _.get(TITLING[main_brand_id], "collaborations", dict()):
        if len(collabs) != 0 and not _.get(TITLING[main_brand_id], "many_collaborations", False):
            break

        collab_added = False

        for collab_name in _.get(TITLING[main_brand_id]["collaborations"][collab], "collab_brand_names", list()):
            if collab_name.lower() in title.lower() and none_in_string(title.lower(), _.get(
                    TITLING[main_brand_id]["collaborations"][collab],
                    "collab_skip_names", list())):
                collabs.append(collab)
                collab_added = True
                break

        if collab_added:
            continue

        for collab_brand_id in _.get(TITLING[main_brand_id]["collaborations"][collab], "collab_brand_ids", list()):
            if collab_brand_id in map(str, brand_ids_list):
                collabs.append(collab)
                collab_added = True
                break

        if collab_added:
            continue

        if manufacturer_sku in _.get(TITLING[main_brand_id]["collaborations"][collab], "collab_skus", list()):
            collabs.append(collab)
            collab_added = True

        if collab_added:
            continue
    return collabs


def get_lines(brand_id, title):
    lines = list()

    for line in _.get(TITLING, f"{brand_id}.lines", list()):
        for line_name in line["line_names"]:
            if line_name.lower() in title.lower() and none_in_string(title.lower(), _.get(line, "line_skip_names", [])):
                lines.append(copy.deepcopy(line))
                break

        if len(lines) != 0 and not _.get(TITLING[brand_id], "many_lines", False):
            break
    return lines


def translate_title(title):
    res = ""
    for subtitle in TITLE_TRANSLATIONS:
        if subtitle in title and TITLE_TRANSLATIONS[subtitle] not in title:
            res += TITLE_TRANSLATIONS[subtitle] + " "
    return res
