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
        http_request = requests.get(url)
        soup = BeautifulSoup(http_request.content, "html.parser")
    except Exception as e:
        logging.error("Raised Exception while parsing URL %s ", e)
    return soup

