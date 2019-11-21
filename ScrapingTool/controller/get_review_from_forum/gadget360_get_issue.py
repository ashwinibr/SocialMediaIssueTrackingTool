import calendar
import datetime
import re
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from ScrapingTool.Generic.category_search import generic_category_filter
from ScrapingTool.Generic.parser import parse
from ScrapingTool.Models.file_read_write import fileReaderWriter

CHROMEDRIVER_PATH = r"ScrapingTool\controller\get_review_from_forum\chromedriver_win32\chromedriver.exe"
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--incognito')
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)


def gadget360_get_issue(request, selected_model_url, selected_dates):
    date_list = []
    user_comment_list = []
    url_list = []
    product_list = []
    category_list = []
    heading_name_list = []
    brand = request.session.get('brand')
    converted_date = selected_dates
    for model_url in selected_model_url:
        driver.get(model_url)
        html_source = driver.page_source
        new_user_review_container = BeautifulSoup(html_source, 'lxml')
        for html_container in new_user_review_container.find_all("div", class_="_thd"):
            product_name = html_container.find("h1")
            for user_review_container in new_user_review_container.find_all("a", class_="_flx _rmbtn _seervw"):
                user_review_link = user_review_container.get('href')
                driver.get(user_review_link)
                more_buttons = driver.find_element_by_css_selector(".review_load_more")
                driver.find_element(By.ID, "review_rating_type").click()
                dropdown = driver.find_element(By.ID, "review_rating_type")
                dropdown.find_element(By.XPATH, "//option[. = 'Latest']").click()
                driver.find_element(By.ID, "review_rating_type").click()
                while True:
                    if(more_buttons.is_displayed()):
                        driver.execute_script("arguments[0].click();", more_buttons)
                        more_buttons = driver.find_element_by_css_selector(".review_load_more")
                        for issue_container in new_user_review_container.find_all("li", class_=" parent_review li_parent_0"):
                            posted_date = issue_container.find("div", class_="_cmtname")
                            post_date = posted_date.find("span")
                            date_expr = r"(?:%s) ?\s(\d+)\, \d{4}" % '|'.join(calendar.month_abbr[1:])
                            split_date = re.compile(date_expr)
                            issue_date = split_date.search(str(post_date))
                            if issue_date:
                                raw_date = issue_date.group(0)
                                converted_date = datetime.datetime.strptime(raw_date, '%b %d, %Y').strftime('%m/%d/%Y')
                        if converted_date<selected_dates[-1] and brand!="Google":
                            print("breaking loop")
                            break
                    else:
                        print("breaking loop")
                        break

                # Beautiful Soup Code
                html_source = driver.page_source
                new_user_review_container = BeautifulSoup(html_source, 'lxml')
                for issue_container in new_user_review_container.find_all("li", class_=" parent_review li_parent_0"):
                    posted_date = issue_container.find("div", class_="_cmtname")
                    post_date = posted_date.find("span")
                    date_expr = r"(?:%s) ?\s(\d+)\, \d{4}" % '|'.join(calendar.month_abbr[1:])
                    split_date = re.compile(date_expr)
                    issue_date = split_date.search(str(post_date))
                    if issue_date:
                        raw_date = issue_date.group(0)
                        converted_date = datetime.datetime.strptime(raw_date, '%b %d, %Y').strftime('%m/%d/%Y')
                        # if no date are selected by user
                    if not selected_dates:
                        url_list.append(model_url)
                        product_list.append(product_name.text.strip())
                        date_list.append(converted_date)
                        child_node = issue_container.find("div", class_="_cmttxt")
                        issue_data, category = generic_category_filter(child_node)
                        user_comment_list.append(issue_data)
                        category_list.append(category)
                    # if date is selected by user
                    else:
                        for date in selected_dates:
                            if date == converted_date:
                                url_list.append(model_url)
                                product_list.append(product_name.text.strip())
                                date_list.append(converted_date)
                                # fetching the issue comment
                                child_node = issue_container.find("div", class_="_cmttxt")
                                issue_data, category = generic_category_filter(child_node)
                                user_comment_list.append(issue_data)
                                category_list.append(category)

    data_dictionary = {"Product": product_list, "Date": date_list, "Link": url_list, "Category": category_list,
                       "comment": user_comment_list}

    if not product_list:
        data_dictionary = {}
    else:
        file_writer = fileReaderWriter()
        file_writer.write_data_using_pandas(request, data_dictionary)
    return data_dictionary
