import pandas as pd

import requests
from bs4 import BeautifulSoup
import logging




def parse(url):
    """
    This function is to get html parsed data.
    by using BeautifulSoup library we are fetching html parsed data
    :return: soup which contain parsed html data
    """
    try:
        print(url)
        http_response = requests.get(url)
        soup = BeautifulSoup(http_response.content, "html.parser")
        http_response.close()
    except Exception as e:
        logging.error("Raised Exception while parsing URL %s ", e)
    return soup


def get_category():
    """
       This function is to get categories from .xlsx file.
       :return: returning category list
    """
    excel_file_path = 'ScrapingTool/files/social_keywords.xlsx'
    try:
        dataset = pd.read_excel(excel_file_path)
        dataframe = pd.DataFrame(dataset)
        data = dataframe.get("Category")
    except IOError as e:
        logging.error("Raised Exception while reading xml file %s ", e)

    return data


