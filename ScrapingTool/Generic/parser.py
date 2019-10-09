import pandas as pd

import requests
from bs4 import BeautifulSoup
import logging
from ScrapingTool.Models.sqlite3_read_write import Get_Keywards_List

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
        soup = ""
        logging.error("Raised Exception while parsing URL %s ", e)
    return soup



