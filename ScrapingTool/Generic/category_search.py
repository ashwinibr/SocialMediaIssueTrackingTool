import re
from ScrapingTool.Models.sqlite3_read_write import Get_Keywards_List

def generic_category_filter(child_node):
    categories = Get_Keywards_List()
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