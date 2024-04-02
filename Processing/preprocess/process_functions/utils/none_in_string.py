def none_in_string(input_string, string_list):
    for item in string_list:
        if item.lower() in input_string.lower():
            return False
    return True
