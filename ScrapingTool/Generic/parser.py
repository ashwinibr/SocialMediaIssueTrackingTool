import pandas as pd

import requests
from bs4 import BeautifulSoup
import logging


from ScrapingTool.Generic.connection_status_code import get_response_code

def parse(url):
    """
    This function is to get html parsed data.
    by using BeautifulSoup library we are fetching html parsed data
    :return: soup which contain parsed html data
    """

    try:
        status_code = get_response_code(url)

        if status_code == 200:
            http_response = requests.get(url)
            soup = BeautifulSoup(http_response.content, "html.parser")
            http_response.close()
        else:
            soup = ""
            print("url is not successfully verified")

    except Exception as e:
        logging.error("Raised Exception while parsing URL %s ", e)
    return soup




