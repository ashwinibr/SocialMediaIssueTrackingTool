import logging
import requests


def get_response_code(url):
    try:
        response = requests.head(url)
        return response.status_code
    except ConnectionRefusedError as e:
        logging.error("ConnectionRefusedError :%s", e)
        pass
