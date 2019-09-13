import re

from ScrapingTool.parser import get_category


def generic_category_filter(child_node):
    categories = get_category()
    issue_data = ""
    if child_node.text:
        issue_data = (child_node.text).strip()
    key = ''
    for keyword in categories:
        main = re.findall((r'\b' + keyword + r'\b'), issue_data, re.IGNORECASE)
        if main:
            key = str(keyword) + ',' + str(key)
        else:
            pass
    if key:
        category = key
    else:
        category = "other"

    return issue_data,category