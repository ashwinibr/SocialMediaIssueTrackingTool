import datetime
import re
from collections import defaultdict

from ScrapingTool.Generic.constant import ANDROID_FORUM_URL
from ScrapingTool.Generic.category_search import generic_category_filter
from ScrapingTool.Models.file_read_write import fileReaderWriter
from ScrapingTool.Generic.parser import parse


def android_forum_get_issue(selected_model_links,selected_dates):

    date_list = []
    url_list = []
    product_list = []
    category_list = []
    user_comment_list = []
    heading_name_list = []
    for model_url in selected_model_links:
        pagination_url_list=[]
        pagination_list = pagination_for_user_comment_links(model_url)
        if pagination_list:
            for url in pagination_list:
                pagination_url_list.append(url)
        else:
            pagination_url_list.append(model_url)

        dic_thread_name = get_thread_link_from_android_forum(pagination_url_list)
        for thread_url, thread_name in dic_thread_name.items():
            complete_url = ANDROID_FORUM_URL + thread_url
            soup = parse(complete_url)
            for node in soup.find_all("div",class_="messageInfo primaryContent"):

                child_node_date = node.find("a", class_="datePermalink")
                comment_date = child_node_date.text

                strip_date=comment_date.strip()
                pattern = re.compile(
                    "(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\s+\d{1,2},\s+\d{4}")
                date = pattern.search(strip_date).group()
                converted_date = datetime.datetime.strptime(date, '%b %d, %Y').strftime('%m/%d/%Y')

                child_node = node.find("div", class_="messageContent")
                if not selected_dates:
                    date_list.append(converted_date.strip('\u200e'))
                    heading_name_list.append(thread_name[0])
                    product_list.append(thread_name[1])
                    url_list.append(complete_url)
                    issue_data, category=generic_category_filter(child_node)
                    user_comment_list.append(issue_data)
                    category_list.append(category)

                else:
                    for date in selected_dates:
                        if date == converted_date:
                            date_list.append(converted_date.strip('\u200e'))
                            heading_name_list.append(thread_name[0])
                            product_list.append(thread_name[1])
                            url_list.append(complete_url)
                            issue_data, category = generic_category_filter(child_node)
                            user_comment_list.append(issue_data)
                            category_list.append(category)

    data_dictionary = {"Product": product_list, "date": date_list, "Category": category_list,"Thread":heading_name_list,
                       "Link":url_list,"comment": user_comment_list}

    if not product_list:
        data_dictionary={}
    else:
        file_writer = fileReaderWriter()
        file_writer.write_data_using_pandas(data_dictionary)

    return data_dictionary


def get_thread_link_from_android_forum(pagination_url_list):
    thread_link_list = []
    thread_name_list = []
    product_name_list = []
    dic_thread_name = defaultdict(list)

    for url in pagination_url_list:
        soup = parse(url)
        product_name = (soup.find("div", class_="channel_title")).get_text()
        for thread in soup.find_all("div", class_="listBlock main"):
            for link in thread.find_all("a",class_="PreviewTooltip"):
                thread_link_list.append(link.attrs['href'])
                thread_name_list.append(link.get_text())
                product_name_list.append(product_name)
    i = 0
    for key in thread_link_list:
        dic_thread_name[key].append(thread_name_list[i])
        dic_thread_name[key].append(product_name_list[i])
        i += 1

    return dic_thread_name


def pagination_for_user_comment_links(model_url):
    pagination_list = []
    soup = parse(model_url)

    for node in soup.find_all("div", class_="PageNav"):
        child_node = node.find("span", class_="pageNavHeader")
        page_header_text = (child_node.text).split(" ")
        page_number = page_header_text[len(page_header_text)-1]
        for num in range(int(page_number)):
            num = num + 1
            url = model_url + "page-" + str(num)
            pagination_list.append(url)

    return pagination_list
