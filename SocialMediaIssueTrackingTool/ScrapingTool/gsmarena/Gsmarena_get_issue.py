import datetime
import re

import pandas as pd

import requests
from bs4 import BeautifulSoup

from ScrapingTool.file_read_write import fileReaderWriter


def main_method(model_link_list,list_of_dates):

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
    data_dictionary=get_issue_from_gsmarena(pagination_link_list,list_of_dates)
    print(data_dictionary)
    return data_dictionary


def pagination_for_user_comment_links(review_opinion_link_list):
    pagination_list = []

    for links in review_opinion_link_list:
        http_request = requests.get("https://www.gsmarena.com/" + links)
        soup = BeautifulSoup(http_request.content, "html.parser")

        number = []
        for link in soup.find_all("div", class_="sub-footer no-margin-bottom"):
            print(link)
            for l in link.find_all("div", class_="nav-pages"):

                if l.find("a"):
                    for pagination_links in l.find_all("a"):
                        number.append(pagination_links.text)
                        
                    page = number[-2]
                    print(page)
                    for i in range(1, int(page) + 1):
                        pagination_list.append(links[:-4] + "p" + str(i) + ".php")
                else:
                    pagination_list.append(links)


    return pagination_list


def get_issue_from_gsmarena(pagination_link_list,selected_date_list):
    date_list=[]
    user_comment=[]
    thread_list=[]
    product_list=[]
    data_dictionary={}
    category_list = []

    excel_file = 'D:\Q& CS\Social media\social_keywords.xlsx'
    dataset = pd.read_excel(excel_file)
    df = pd.DataFrame(dataset)
    data = df.get("Category")

    #Fetching issue content from given link
    for li in pagination_link_list:
        complete_url="https://www.gsmarena.com/"+li
        http_request = requests.get(complete_url)
        soup = BeautifulSoup(http_request.content, "html.parser")

        for html_container in soup.find_all("div", class_="article-info-line page-specs light border-bottom"):
            product_name=html_container.find("h1", class_="specs-phone-name-title")

            for issue_container in soup.find_all("div", class_="user-thread"):
                #thread_list.append(complete_url)
                #product_list.append(product_name.text)

                #Fetching date,the issue was posted
                posted_date = issue_container.find("li", class_="upost")
                post_date = posted_date.text
                word_list = post_date.split()  # list of words
                hour = word_list[-1]
                hour_list = ["ago"]
                #If issue posted today,then get todays date by using the last word in date,as date is (1 minute ago)
                if hour in hour_list:
                    prod_date = datetime.date.today()
                    match = re.search('\d{4}-\d{2}-\d{2}', str(prod_date))
                    product_date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
                    modified_date =  product_date.strftime('%m/%d/%Y')
                    print("modified",modified_date)
                else:
                    time_date = datetime.datetime.strptime(post_date, '%d %b %Y')
                    prod_date= time_date.strftime('%Y-%m-%d')
                    match = re.search('\d{4}-\d{2}-\d{2}', prod_date)
                    product_date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
                    modified_date = product_date.strftime('%m/%d/%Y')
                #If no date selected by user
                if not selected_date_list:
                    thread_list.append(complete_url)
                    product_list.append(product_name.text)
                    date_list.append(modified_date)
                    comment = issue_container.find("p", class_="uopin")
                    if comment:
                        issue_data = comment.text
                        user_comment.append(issue_data)
                        key = []
                        for keyword in data:
                            main = re.findall((r'\b' + keyword + r'\b'), issue_data, re.IGNORECASE)
                            if main:
                                key.append(keyword)
                            else:
                                pass
                        if key:
                            category_list.append(key)
                        else:
                            category_list.append("other")
                #if date selected by user
                else:
                    for date in selected_date_list:
                        if date == modified_date:
                            thread_list.append(complete_url)
                            product_list.append(product_name.text)
                            date_list.append(modified_date)
                            comment = issue_container.find("p", class_="uopin")
                            if comment:
                                issue_data = comment.text
                                user_comment.append(issue_data)
                                key = []
                                for keyword in data:
                                    main = re.findall((r'\b' + keyword + r'\b'), issue_data, re.IGNORECASE)
                                    if main:
                                        key.append(keyword)
                                    else:
                                        pass
                                if key:
                                    category_list.append(key)
                                else:
                                    category_list.append("other")

        data_dictionary={"Product":product_list, "date":date_list,"Thread":thread_list,"Category":category_list,"comment":user_comment}

    #data_frame = pd.DataFrame.from_dict(data_dictionary)
    #print("data frame",data_frame)
    if not product_list:
        data_dictionary={}
    else:
        file_writer = fileReaderWriter()
        # Call write_data_using_pandas() function to write scraped dat from dictionary to excel sheet
        file_writer.write_data_using_pandas(data_dictionary)

    return data_dictionary

