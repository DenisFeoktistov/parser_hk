import re


def get_dimensions(value):
        res = re.findall(r'\d+(?:\.\d+)?', value)

        single_value = len(res) == 1

        if len(res) == 1:
            res = res[0]
        elif "-" in value and len(res) == 2:
            res = "-".join(res)
        elif "*" in value:
            res = " x ".join(res)
        elif ";" in value:
            res = ";".join(res)
        else:
            res = " x ".join(res)

        if "above" in value.lower():
            res += "+"

        if "mm" in value.lower():
            if single_value:
                res += "mm"
            else:
                res += " mm"
        elif "cm" in value.lower():
            if single_value:
                res += "CM"
            else:
                res += " CM"
        elif "inch" in value.lower():
            res += " Inch"
        elif "meters" in value.lower():
            if single_value:
                res += "m"
            else:
                res += " m"

        if single_value and "half" in value.lower():
            res = "Длина половины " + res

        if "removable" in value.lower() and single_value:
            res += " (Уменьшается)"
        elif "adjustable" in value.lower() and single_value:
            res += " (Увеличивается)"

        return res
