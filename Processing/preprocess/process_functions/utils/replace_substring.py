def replace_substring(s, sub, replace=""):
    s_lower = s.lower()
    sub_lower = sub.lower()

    start = s_lower.find(sub_lower)

    if start != -1:
        end = start + len(sub)

        s = s[:start] + " ".join(map(str.capitalize, replace.split())) + s[end:]

    return s
