import datetime
import re

from ScrapingTool.common import GSMARENA_URL
from ScrapingTool.consumer_product_scraping.get_review_from_forum.category_search import generic_category_filter
from ScrapingTool.file_read_write import fileReaderWriter
from ScrapingTool.parser import get_category, parse


def get_issue_from_gsmarena(req_id,selected_model_links,selected_dates):
    date_list = []
    user_comment_list = []
    url_list = []
    product_list = []
    category_list = []

    # Fetching issue content from given link
    for model_url in selected_model_links:
        complete_url = GSMARENA_URL + model_url
        soup = parse(complete_url)
        for html_container in soup.find_all("div", class_="article-info-line page-specs light border-bottom"):
            product_name = html_container.find("h1", class_="specs-phone-name-title")

            for issue_container in soup.find_all("div", class_="user-thread"):
                child_node = issue_container.find("p", class_="uopin")
                # Fetching date,the issue was posted
                posted_date = issue_container.find("li", class_="upost")
                post_date = posted_date.text
                word_list = post_date.split()  # list of words
                hour = word_list[-1]
                hour_list = ["ago"]
                # If issue posted today,then get todays date by using the last word in date,as date is (1 minute ago)
                if hour in hour_list:
                    prod_date = datetime.date.today()
                    match = re.search('\d{4}-\d{2}-\d{2}', str(prod_date))
                    product_date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
                    modified_date = product_date.strftime('%m/%d/%Y')
                else:
                    time_date = datetime.datetime.strptime(post_date, '%d %b %Y')
                    prod_date = time_date.strftime('%Y-%m-%d')
                    match = re.search('\d{4}-\d{2}-\d{2}', prod_date)
                    product_date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
                    modified_date = product_date.strftime('%m/%d/%Y')
                # If no date selected by user
                if not selected_dates:
                    url_list.append(complete_url)
                    product_list.append(product_name.text)
                    date_list.append(modified_date.strip('\u200e'))
                    issue_data, category = generic_category_filter(child_node)
                    user_comment_list.append(issue_data)
                    category_list.append(category)

                # if date selected by user
                else:
                    for date in selected_dates:
                        if date == modified_date.strip('\u200e'):
                            url_list.append(complete_url)
                            product_list.append(product_name.text)
                            date_list.append(modified_date.strip('\u200e'))
                            child_node = issue_container.find("p", class_="uopin")
                            issue_data, category = generic_category_filter(child_node)
                            user_comment_list.append(issue_data)
                            category_list.append(category)

        data_dictionary = {"Product": product_list, "Date": date_list, "Link": url_list, "Category": category_list,
                           "Comment": user_comment_list}

    if not product_list:
        data_dictionary = {}
    else:
        file_writer = fileReaderWriter()
        # Call write_data_using_pandas() function to write scraped dat from dictionary to excel sheet
        file_writer.write_data_using_pandas(req_id,data_dictionary)

    return data_dictionary


def gsmarena_get_issue(req_id,model_link_list,list_of_dates):
    review_issue = []
    for links in model_link_list:
        soup = parse(links)
        review_opinion_link_list = []
        for review_button_container in soup.find_all("div", class_="button-links"):
            for review_button_link in review_button_container.find_all("a"):
                review_opinion_link_list.append(review_button_link.attrs['href'])
        review_issue.append(review_opinion_link_list[0])
    pagination_link_list = pagination_for_user_comment_links(review_issue)
    data_dictionary=get_issue_from_gsmarena(req_id,pagination_link_list,list_of_dates)
    return data_dictionary


def pagination_for_user_comment_links(review_opinion_link_list):
    pagination_list = []
    for links in review_opinion_link_list:
        soup = parse(GSMARENA_URL + links)
        number = []
        for link in soup.find_all("div", class_="sub-footer no-margin-bottom"):
            for l in link.find_all("div", class_="nav-pages"):
                if l.find("a"):
                    for pagination_links in l.find_all("a"):
                        number.append(pagination_links.text)
                    page = number[-2]
                    for i in range(1, int(page) + 1):
                        pagination_list.append(links[:-4] + "p" + str(i) + ".php")
                else:
                    pagination_list.append(links)
    return pagination_list




