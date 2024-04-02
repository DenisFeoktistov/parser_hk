from Processing.constants import CATEGORY_NAMES


def category_simplify(category):
    path = CATEGORY_NAMES[category]["path"]

    value_in_to_return_value = {
        "Обувь": "Обувь",
        "Одежда": "Одежда",
        "Сумки": "Сумки",
        "Ремни": "Ремни",
        "Головные уборы": "Головные уборы",
        "Перчатки": "Перчатки",
        "Оправы для очков": "Очки",
        "Солнцезащитные очки": "Очки"
    }

    for value_in in value_in_to_return_value.keys():
        if value_in in path:
            return value_in_to_return_value[value_in]

    return CATEGORY_NAMES[category]["path"][-1]
