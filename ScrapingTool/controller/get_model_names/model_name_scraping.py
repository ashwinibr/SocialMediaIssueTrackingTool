import logging
import re
from collections import defaultdict

from ScrapingTool.Generic.constant import GSMARENA_URL, MODEL_NAME_DICT_KEY, ANNOUNCED_YEAR_DICT_KEY, \
    MODEL_LINK_DICT_KEY, MODEL_NAME_DATABASE_TABLE, ANDROID_PIT_FORUM_URL
from ScrapingTool.Generic.parser import parse
import ScrapingTool.Models.mongo_read_write as mongo

def get_models_names_from_gsmarena(req_id,soup,url):

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
                mobile_model_name = l.find("span")
                model_links = l.find("a")
                if split_year is not None:
                    pattern = re.compile(r"(\w+)$")
                    year = pattern.search(split_year.group(1))
                    mobile_model_year_list.append(year.group(0))
                    mobile_model_name_list.append(mobile_model_name.text)
                    mobile_model_links_list.append(model_links.attrs['href'])

                else:
                    mobile_model_year_list.append("Other")
                    mobile_model_name_list.append(mobile_model_name.text)
                    mobile_model_links_list.append(model_links.attrs['href'])

    model_dictionary = {ANNOUNCED_YEAR_DICT_KEY:mobile_model_year_list,
                      MODEL_NAME_DICT_KEY:mobile_model_name_list,
                      MODEL_LINK_DICT_KEY:mobile_model_links_list}

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

    collection_name = MODEL_NAME_DATABASE_TABLE + req_id
    mongo.Write_to_DB(model_dictionary, collection_name)

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


def get_models_names_from_android_forum(req_id,soup):
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
    model_dictionary = {ANNOUNCED_YEAR_DICT_KEY: mobile_model_year_list,
                        MODEL_NAME_DICT_KEY: mobile_model_name_list,
                        MODEL_LINK_DICT_KEY: mobile_model_links_list}

    collection_name = MODEL_NAME_DATABASE_TABLE + req_id
    mongo.Write_to_DB(model_dictionary, collection_name)

    i = 0
    for key in mobile_model_year_list:
        dic_year[key].append(mobile_model_name_list[i])
        i += 1

    j = 0
    for mobile_name_key in mobile_model_name_list:
        dic_model_name[mobile_name_key].append(mobile_model_links_list[j])
        j += 1
    return dic_year,dic_model_name


def get_models_names_from_android_pit_forum(req_id,soup,url):
    mobile_model_name_list = []
    mobile_model_links_list = []
    mobile_model_year_list = []
    dic_model_name = defaultdict(list)
    dic_year = defaultdict(list)
    sub_cat_link = []
    if soup.find("a", class_="forumSubcategory"):
        for subCatLink in soup.find_all("a", class_="forumSubcategory"):
            sub_cat_link.append(ANDROID_PIT_FORUM_URL + subCatLink.attrs["href"])

    if not sub_cat_link:
        soup = parse(url)
        product = soup.find("div", class_="forumHeadingWithFavorite")
        product_name = product.find("h1")
        mobile_model_name_list.append(product_name.text)
        mobile_model_links_list.append(url)
        mobile_model_year_list.append("All")

    else:
        for forumLink in sub_cat_link:
            soup = parse(forumLink)
            product = soup.find("div", class_="forumHeadingWithFavorite")
            product_name_head = product.find("h1")
            if soup.find("a", class_ = "forumSubcategory"):
                for subCatLink in soup.find_all("a", class_ = "forumSubcategory"):
                    product_name = subCatLink.find("h3")
                    if "/" in product_name.text:
                        mobile_model_name_list.append(product_name_head.text)
                        mobile_model_links_list.append(subCatLink.attrs["href"])
                        mobile_model_year_list.append("All")
                    else:
                        mobile_model_name_list.append(product_name.text)
                        mobile_model_links_list.append(ANDROID_PIT_FORUM_URL +subCatLink.attrs["href"])
                        mobile_model_year_list.append("All")
            else:
                soup = parse(forumLink)
                product = soup.find("div", class_ = "forumHeadingWithFavorite")
                product_name = product.find("h1")

                mobile_model_name_list.append(product_name.text)
                mobile_model_links_list.append(forumLink)
                mobile_model_year_list.append("All")

    model_dictionary = {ANNOUNCED_YEAR_DICT_KEY: mobile_model_year_list,
                        MODEL_NAME_DICT_KEY: mobile_model_name_list,
                        MODEL_LINK_DICT_KEY: mobile_model_links_list}

    collection_name = MODEL_NAME_DATABASE_TABLE + req_id
    mongo.Write_to_DB(model_dictionary, collection_name)

    i = 0
    for key in mobile_model_year_list:
        dic_year[key].append(mobile_model_name_list[i])
        i += 1

    j = 0
    for mobile_name_key in mobile_model_name_list:
        dic_model_name[mobile_name_key].append(mobile_model_links_list[j])
        j += 1
    return dic_year, dic_model_name



