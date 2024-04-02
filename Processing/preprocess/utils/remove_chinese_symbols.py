import re


def remove_chinese_symbols(text):
    chinese_pattern = "[\u4e00-\u9FFF|\u3400-\u4DBF|\U00020000-\U0002A6DF|\U0002A700-\U0002B73F|\U0002B740-\U0002B81F|\U0002B820-\U0002CEAF|\uF900-\uFAFF|\U0002F800-\U0002FA1F]"
    without_chinese = re.sub(chinese_pattern, '', text)
    without_chinese = ' '.join(without_chinese.split())
    return without_chinese
