import pandas as pd

import requests
from bs4 import BeautifulSoup
import logging
<<<<<<< HEAD

from ScrapingTool.Generic.connection_status_code import get_response_code

=======
from ScrapingTool.Models.sqlite3_read_write import Get_Keywards_List
>>>>>>> 4a22629009c0354d2ba1bab748442ab853033545

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




