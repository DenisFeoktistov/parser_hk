def capitalize_first_letter(s):
    for i, char in enumerate(s):
        if char.isalpha():
            return s[:i] + char.upper() + s[i + 1:]
    return s
