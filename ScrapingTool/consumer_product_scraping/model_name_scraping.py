import re
from collections import defaultdict

from ScrapingTool.common import GSMARENA_URL
from ScrapingTool.parser import parse
from ScrapingTool.sqlite3_read_write import Write_to_DB


def get_models_names_from_gsmarena(soup,url):

    list_page = pagination_for_mobile_brand_list_from_gsmarena(soup,url)

    mobile_model_name_list = []
    mobile_model_links_list = []
    mobile_model_year_list = []

    for l in list_page:
        url = GSMARENA_URL+l
        soup = parse(url)
        for mobile_model_container in soup.find_all("div", class_="makers"):
            for l in mobile_model_container.find_all("li"):
                mobile_model_year = l.find("img")
                year_string = mobile_model_year.attrs["title"]
                split_year = re.search("\.?([^\.]*Announced[^\.]*)", year_string)
                if split_year is not None:
                    pattern = re.compile(r"(\w+)$")
                    has = pattern.search(split_year.group(1))
                    mobile_model_year_list.append(has.group(0))
                    mobile_model_name= l.find("span")
                    mobile_model_name_list.append(mobile_model_name.text)
                    model_links = l.find("a")
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

    Write_to_DB(model_dictionary,"Model_Names")

    return dic_year,dic_model_name

def pagination_for_mobile_brand_list_from_gsmarena(soup,url):
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
    return pagination_list


def get_models_names_from_android_forum(soup):
    mobile_model_name_list = []
    mobile_model_links_list = []
    mobile_model_year_list = []
    dic_model_name = defaultdict(list)
    dic_year = defaultdict(list)

    for mobile_model_container in soup.find_all("ol", class_="deviceList uix_nodeStyle_3 section"):
        for l in mobile_model_container.find_all("h3", class_="nodeTitle"):
            mobile_model_name_list.append(l.text)
            mobile_model_year_list.append("All")
            model_links = l.find("a")
            mobile_model_links_list.append(model_links.attrs['href'])
    print(mobile_model_name_list)
    print(mobile_model_links_list)
    model_dictionary = {"Announced_Year": mobile_model_year_list, "Model_Name": mobile_model_name_list,
                        "Model_Link": mobile_model_links_list}

    Write_to_DB(model_dictionary, "Model_Names")

    i = 0
    for key in mobile_model_year_list:
        dic_year[key].append(mobile_model_name_list[i])
        i += 1

    j = 0
    for mobile_name_key in mobile_model_name_list:
        dic_model_name[mobile_name_key].append(mobile_model_links_list[j])
        j += 1
    return dic_year,dic_model_name



