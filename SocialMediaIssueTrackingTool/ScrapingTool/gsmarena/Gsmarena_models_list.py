import re
from collections import defaultdict
import requests
from bs4 import BeautifulSoup
from ScrapingTool.sqlite3_read_write import GetData_In_Dict, Write_to_DB


def pagination_for_mobile_brand_list(url):
    #url="apple-phones-48.php"
    #url="samsung-phones-9.php"

    http_request = requests.get("https://www.gsmarena.com/"+url)
    soup = BeautifulSoup(http_request.content, "html.parser")

    pagination_list = []
    number = []

    if soup.find("div", class_="nav-pages"):
        for link in soup.find_all("div", class_="nav-pages"):
            for pagination_links in link.find_all("a"):
                number.append(pagination_links.text)
        number_of_page = number[-1]
        search_digit = re.findall(r'\d+', url)
        url = re.sub(search_digit[0], '', url)
        for i in range(1, int(number_of_page) + 1):
            pagination_list.append(url[:-4] + "f-" + search_digit[0] + "-0-p" + str(i) + ".php")
    else:
        pagination_list.append(url)

    data_tuple = get_models_names(pagination_list)
    return data_tuple

def get_models_names(list_page):
    mobile_model_name_list = []
    mobile_model_links_list = []
    mobile_model_year_list = []

    model_dictionary={}

    for l in list_page:
        print("https://www.gsmarena.com/"+l)
        http_request = requests.get("https://www.gsmarena.com/"+l)
        soup = BeautifulSoup(http_request.content ,"html.parser")

        for mobile_model_container in soup.find_all("div", class_="makers"):

            #print(mobile_model_container)
            for l in mobile_model_container.find_all("li"):
               # print(l)
                mobile_model_year = l.find("img")
                year_string = mobile_model_year.attrs["title"]
                split_year = re.search("\.?([^\.]*Announced[^\.]*)", year_string)
                #print(split_year)
                if split_year is not None:
                    pattern = re.compile(r"(\w+)$")
                    has = pattern.search(split_year.group(1))
                    #print(has.group(0))
                    mobile_model_year_list.append(has.group(0))

                    mobile_model_name= l.find("span")
                    #print(mobile_model_name.text)
                    mobile_model_name_list.append(mobile_model_name.text)

                    model_links = l.find("a")
                    #print(model_links.attrs['href'])
                    mobile_model_links_list.append(model_links.attrs['href'])

                else:
                    print("announced is not present in the sentence")

    model_dictionary={"Announced_Year":mobile_model_year_list, "Model_Name":mobile_model_name_list, "Model_Link":mobile_model_links_list}

    dic_year = defaultdict(list)
    dic_model_name=defaultdict(list)

    i = 0
    for key in mobile_model_year_list:
        dic_year[key].append(mobile_model_name_list[i])
        i += 1

    j = 0
    for mobile_name_key in mobile_model_name_list:
        dic_model_name[mobile_name_key].append(mobile_model_links_list[j])
        j += 1

    #print(dic_year)
    #print(dic_model_name)
    #print(len(mobile_model_year_list))
    #print(len(mobile_model_name_list))
    #print(len(mobile_model_links_list))
    

    Write_to_DB(model_dictionary,"Model_Names")

    return dic_year,dic_model_name


