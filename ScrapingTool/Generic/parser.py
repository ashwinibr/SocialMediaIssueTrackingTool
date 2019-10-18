import pandas as pd

import requests
from bs4 import BeautifulSoup
import logging
import time

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
            http_response.close()
            soup = BeautifulSoup(http_response.content, "html.parser")
        else:
            soup = ""    
            status_dict = {'301': 'Moved Temporarily', '401': 'Unauthorized', '403': 'Forbidden', '404': 'Not Found', '408': 'Request Timeout', '429': 'Too Many Requests', '503': 'Service Unavailable'}
            status = status_dict[str(status_code)]
            print("Connection Lost!! Status Code: "+str(status_code)+':'+status)

    except Exception as e:
        logging.error("Raised Exception while parsing URL %s ", e)
    return soup