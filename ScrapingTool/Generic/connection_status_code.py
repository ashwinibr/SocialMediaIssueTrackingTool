import urllib

def get_response_code(url):
    try:
        conn = urllib.request.urlopen(url)
        return conn.getcode()
    except ConnectionRefusedError as e:
        return e