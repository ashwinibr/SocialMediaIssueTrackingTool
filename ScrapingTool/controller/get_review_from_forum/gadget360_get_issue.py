import calendar
import datetime
import re

from ScrapingTool.Generic.category_search import generic_category_filter
from ScrapingTool.Generic.parser import parse
from ScrapingTool.Models.file_read_write import fileReaderWriter


def gadget360_get_issue(request,selected_model_url, selected_dates):
    date_list = []
    user_comment_list = []
    url_list = []
    product_list = []
    category_list = []
    heading_name_list = []

    for model_url in selected_model_url:
        soup = parse(model_url)
        for html_container in soup.find_all("div", class_="_thd"):
            product_name = html_container.find("h1")
            for issue_container in soup.find_all("li", class_="parent_review li_parent_0"):
                child_node = issue_container.find("div", class_="_cmttxt _wwrap")
                #thread_name = issue_container.find("div",class_="_flx_cmttl")
                # fetching date when the issue was published
                posted_date = issue_container.find("div", class_="_cmtname")
                post_date = posted_date.find("span")
                date_expr = r"(?:%s) \d{2}, \d{4}" % '|'.join(calendar.month_abbr[1:])
                split_date = re.compile(date_expr)
                issue_date = split_date.search(str(post_date))
                if issue_date:
                    raw_date = issue_date.group(0)
                    converted_date = datetime.datetime.strptime(raw_date, '%b %d, %Y').strftime('%m/%d/%Y')
                    # if no date are selected by user
                if not selected_dates:
                    date_list.append(converted_date)
                    # child_node = issue_container.find("div", class_="_cmttxt _wwrap")
                    issue_data, category = generic_category_filter(child_node)
                    user_comment_list.append(issue_data)
                    # product_date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
                    # modified_date = product_date.strftime('%m/%d/%Y')
                    category_list.append(category)
                # if date is selected by user
                else:
                    for date in selected_dates:
                        if date == converted_date:
                            url_list.append(model_url)
                            product_list.append(product_name.text)
                            date_list.append(converted_date)
                            issue_data, category = generic_category_filter(child_node)
                            user_comment_list.append(issue_data)
                            category_list.append(category)

    data_dictionary = {"Product": product_list, "date": date_list, "Category": category_list,
                       "Link": url_list, "comment": user_comment_list}

    print(data_dictionary)

    if not product_list:
        data_dictionary = {}
    else:
        file_writer = fileReaderWriter()
        file_writer.write_data_using_pandas(request,data_dictionary)

    return data_dictionary
