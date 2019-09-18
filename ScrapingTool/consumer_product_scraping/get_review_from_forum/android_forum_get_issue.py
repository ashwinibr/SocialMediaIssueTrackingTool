import datetime
import requests

from bs4 import BeautifulSoup
from ScrapingTool.common import ANDROID_FORUM_URL
from ScrapingTool.consumer_product_scraping.get_review_from_forum.category_search import generic_category_filter
from ScrapingTool.file_read_write import fileReaderWriter
from ScrapingTool.parser import parse


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
                complete_url = ANDROID_FORUM_URL + url
                pagination_url_list.append(complete_url)
        else:
            pagination_url_list.append(model_url)

        thread_list=get_thread_link_from_android_forum(pagination_url_list)
        for url in thread_list[0]:
            complete_url = ANDROID_FORUM_URL + url
            soup = parse(complete_url)
            soup_node = soup.find("div", class_="mainContainer_noSidebar")
            thread_name =""
            for node in soup_node.find_all("h1"):
                thread_name = node.text
            for node in soup.find_all("div",class_="messageInfo primaryContent"):
                child_node_date = node.find("a", class_="datePermalink")
                comment_date = child_node_date.text
                strip_date=comment_date.strip()
                remove_time = strip_date[0:12]
                converted_date = datetime.datetime.strptime(remove_time, '%b %d, %Y').strftime('%m/%d/%Y')
                child_node = node.find("div", class_="messageContent")
                if not selected_dates:
                    date_list.append(converted_date.strip('\u200e'))
                    heading_name_list.append(thread_name)
                    product_list.append(thread_list[1][0])
                    url_list.append(complete_url)
                    issue_data, category=generic_category_filter(child_node)
                    user_comment_list.append(issue_data)
                    category_list.append(category)

                else:
                    for date in selected_dates:
                        if date == converted_date.strip('\u200e'):
                            date_list.append(converted_date.strip('\u200e'))
                            heading_name_list.append(thread_name)
                            product_list.append(thread_list[1][0])
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
    product_name_list = []

    for url in pagination_url_list:
        soup = parse(url)
        product_name = ((soup.find("div", class_="titleBar")).text).strip()
        for thread in soup.find_all("div", class_="listBlock main"):
            for link in thread.find_all("a",class_="PreviewTooltip"):
                thread_link_list.append(link.attrs['href'])
                product_name_list.append(product_name)
    return thread_link_list,product_name_list


def pagination_for_user_comment_links(model_url):
    pagination_list = []
    http_request = requests.get(model_url)
    soup = BeautifulSoup(http_request.content, "html.parser")

    for node in soup.find_all("div", class_="PageNav"):
        child_node = node.find("span", class_="pageNavHeader")
        page_header_text = (child_node.text).split(" ")
        page_number = page_header_text[len(page_header_text)-1]
        for num in range(int(page_number)):
            num = num + 1
            url = model_url + "page-" + str(num)
            pagination_list.append(model_url)

    return pagination_list



