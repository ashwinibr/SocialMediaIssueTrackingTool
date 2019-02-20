import re

import requests
from bs4 import BeautifulSoup


def pagination_for_mobile_brand_list(url):
    #url="apple-phones-48.php"
    #url="samsung-phones-9.php"

    http_request = requests.get("https://www.gsmarena.com/"+url)
    soup = BeautifulSoup(http_request.content, "html.parser")

    pagination_list=[]

    number=[]
    for link in soup.find_all("div", class_="nav-pages"):
        for pagination_links in link.find_all("a"):
            number.append(pagination_links.text)

    number_of_page=number[-1]
    search_digit = re.findall(r'\d+', url)
    url = re.sub(search_digit[0], '', url)
    for i in range(1,int(number_of_page)+1):
        pagination_list.append(url[:-4]+"f-"+search_digit[0]+"-0-p"+str(i)+".php")
    data_tuple = get_models_names(pagination_list)
    return data_tuple

def get_models_names(list_page):
    mobile_model_name_list = []
    mobile_model_links_list = []
    mobile_model_year_list=[]

    for l in list_page:
        print("https://www.gsmarena.com/"+l)
        http_request = requests.get("https://www.gsmarena.com/"+l)
        soup = BeautifulSoup(http_request.content ,"html.parser")

        for mobile_model_container in soup.find_all("div", class_="makers"):


            for mobile_model in mobile_model_container.find_all("span"):
                mobile_model_name_list.append(mobile_model.text)
            for model_links in mobile_model_container.find_all("a"):
                mobile_model_links_list.append(model_links.attrs['href'])

    print(mobile_model_year_list)
    print(mobile_model_name_list)
    data_tuple =(mobile_model_name_list,mobile_model_links_list)
    return data_tuple


