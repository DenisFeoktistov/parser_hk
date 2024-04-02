from Processing.constants import COLORS


def get_color(value):
    value = value.lower()

    for color in sorted(COLORS.keys(), key=lambda x: -len(x)):
        if color.lower() in value:
            return COLORS[color]["view_name"]

    return ""
