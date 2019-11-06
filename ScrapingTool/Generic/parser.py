import pandas as pd

import requests
from bs4 import BeautifulSoup
import logging
import time
import numpy as np

from ScrapingTool.Generic.connection_status_code import get_response_code


def get_random_ua():
    random_ua = ''
    ua_file = 'ScrapingTool/Generic/files/ua_file.txt'
    try:
        with open(ua_file) as f:
            lines = f.readlines()
        if len(lines) > 0:
            prng = np.random.RandomState()
            index = prng.permutation(len(lines) - 1)
            idx = np.asarray(index, dtype=np.integer)[0]
            random_proxy = lines[int(idx)]
    except Exception as ex:
        print('Exception in random_ua')
        print(str(ex))
    finally:
        return random_ua


def parse(url):
    """
    This function is to get html parsed data.
    by using BeautifulSoup library we are fetching html parsed data
    :return: soup which contain parsed html data
    """
    try:
        delays = [7, 4, 6, 2, 10, 19]
        delay = np.random.choice(delays)
        time.sleep(delay)
        user_agent = get_random_ua()
        headers = {
                'user-agent': user_agent,
                'referrer': 'https://google.com',
            }
        http_response = requests.get(url,headers=headers)
        soup = BeautifulSoup(http_response.content, "html.parser")
        http_response.close()
    except Exception as ex:
            print(str(ex))
            user_agent = get_random_ua()
            headers = {
                    'user-agent': user_agent,
                    'referrer': 'https://google.com',
                }
            cahe_url = 'http://webcache.googleusercontent.com/search?q=cache:'+url
            http_response = requests.get(cahe_url,headers=headers)
            soup = BeautifulSoup(http_response.content, "html.parser")
            http_response.close()
    finally:
        if len(soup) > 0:
            return soup
        else:
            return None
    