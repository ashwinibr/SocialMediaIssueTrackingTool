import datetime
import re

import pandas as pd

import requests
from bs4 import BeautifulSoup

from ScrapingTool.file_read_write import fileReaderWriter


def main_method(model_link_list,model_name_list):

    print(model_name_list)
    print("main method")
    #url = ['https://www.gsmarena.com/apple_ipad_pro_12_9_(2018)-9387.php',
           #'https://www.gsmarena.com/apple_ipad_pro_11-9386.php',
           #'https://www.gsmarena.com/apple_iphone_xs_max-9319.php']

    # url = ["https://www.gsmarena.com/samsung_galaxy_m20-9506.php"]
    review_issue = []
    for links in model_link_list:

        http_request = requests.get(links)
        soup = BeautifulSoup(http_request.content, "html.parser")

        review_opinion_link_list = []
        for review_button_container in soup.find_all("div", class_="button-links"):
            for review_button_link in review_button_container.find_all("a"):
                review_opinion_link_list.append(review_button_link.attrs['href'])
        review_issue.append(review_opinion_link_list[0])
    pagination_link_list = pagination_for_user_comment_links(review_issue)
    data_dictionary=get_issue_from_gsmarena(pagination_link_list)
    return data_dictionary


def pagination_for_user_comment_links(review_opinion_link_list):
    pagination_list = []

    for links in review_opinion_link_list:
        http_request = requests.get("https://www.gsmarena.com/" + links)
        soup = BeautifulSoup(http_request.content, "html.parser")

        number = []
        for link in soup.find_all("div", class_="sub-footer no-margin-bottom"):
            for l in link.find_all("div", class_="nav-pages"):
                for pagination_links in l.find_all("a"):
                    number.append(pagination_links.text)
        page = number[-2]
        for i in range(1, int(page) + 1):
            pagination_list.append(links[:-4] + "p" + str(i) + ".php")
    return pagination_list


def get_issue_from_gsmarena(pagination_link_list):
    date_list=[]
    user_comment=[]
    thread_list=[]
    product_list=[]

    selected_date_list = []

    for li in pagination_link_list:
        complete_url="https://www.gsmarena.com/"+li
        http_request = requests.get(complete_url)
        soup = BeautifulSoup(http_request.content, "html.parser")

        for html_container in soup.find_all("div", class_="article-info-line page-specs light border-bottom"):
            product_name=html_container.find("h1", class_="specs-phone-name-title")

            for issue_container in soup.find_all("div", class_="user-thread"):
                thread_list.append(complete_url)
                product_list.append(product_name.text)

                posted_date = issue_container.find("li", class_="upost")
                post_date = posted_date.text
                print(post_date)
                word_list = post_date.split()  # list of words
                hour = word_list[-2]
                hour_list = ["hour","hours","minute","minutes","second","seconds"]
                if hour in hour_list:
                    modified_date = datetime.date.today()
                else:
                    time_date = datetime.datetime.strptime(post_date, '%d %b %Y')
                    modified_date = time_date.strftime('%Y-%m-%d')
                if not selected_date_list:
                    date_list.append(modified_date)
                    print(modified_date)
                    comment = issue_container.find("p", class_="uopin")
                    issue_data = comment.text
                    user_comment.append(issue_data)
                    print(issue_data)
                else:
                    for date in selected_date_list:
                        if date == modified_date:
                            date_list.append(modified_date)
                            print(modified_date)
                            comment = issue_container.find("p", class_="uopin")
                            issue_data = comment.text
                            user_comment.append(issue_data)
                            print(issue_data)


    print(len(date_list),len(thread_list),len(user_comment),len(product_list))

    data_dictionary={"Product":product_list, "date":date_list,"Thread":thread_list,"comment":user_comment}
    data_frame = pd.DataFrame.from_dict(data_dictionary)
    print(data_frame)


    file_writer = fileReaderWriter()
    # Call write_data_using_pandas() function to write scraped dat from dictionary to excel sheet
    file_writer.write_data_using_pandas(data_dictionary)

<<<<<<< HEAD
"""
                date=issue_container.find("li",class_="upost")
                d=date.text
                word_list = d.split()  # list of words
                hour = word_list[-2]
                if hour == "hour" or hour == "hours":
                    date = datetime.date.today()
                    date_list.append(date)
                else:
                    s = datetime.datetime.strptime(d, '%d %b %Y')
                    date_list.append(s.strftime('%Y-%m-%d'))

                comment=issue_container.find("p", class_="uopin")
                user_comment.append(comment.text)


"""
=======
    return data_dictionary
>>>>>>> e95b10292ffbdf487c866013808d95d4e3618630
