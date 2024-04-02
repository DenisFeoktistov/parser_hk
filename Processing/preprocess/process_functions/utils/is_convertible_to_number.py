def is_convertible_to_number(input_str):
    try:
        # Try converting to int
        int(input_str)
        return True
    except ValueError:
        try:
            # Try converting to float
            float(input_str)
            return True
        except ValueError:
            return False
