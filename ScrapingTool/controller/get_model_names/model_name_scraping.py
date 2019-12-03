import logging
import re
from collections import defaultdict

from ScrapingTool.Generic.constant import *
from ScrapingTool.Generic.parser import parse
from ScrapingTool.Models.mongo_read_write import Write_to_DB


def get_models_names_from_sonyforum(request, soup):
    mobile_model_name_list = []
    mobile_model_links_list = []
    mobile_model_year_list = []
    main_url = []
    mobile_brand = request.session.get('brand')
    brand_list = []

    for mobile_model_container in soup.find_all("a", class_="lia-link-navigation lia-message-unread"):
        brand_list.append(mobile_brand)
        mobile_model_name_list.append(mobile_model_container.text)
        mobile_model_links_list.append(mobile_model_container.attrs['href'])
        main_url.append(SONY_FORUM_URL)
        mobile_model_year_list.append("All")

    model_dictionary = {MAIN_URL_KEY: main_url, BRAND_NAME_KEY: brand_list,
                        ANNOUNCED_YEAR_DICT_KEY: mobile_model_year_list,
                        MODEL_NAME_DICT_KEY: mobile_model_name_list,
                        MODEL_LINK_DICT_KEY: mobile_model_links_list}
    dic_year = defaultdict(list)
    dic_model_name = defaultdict(list)

    i = 0
    for key in mobile_model_year_list:
        dic_year[key].append(mobile_model_name_list[i])
        i += 1

    j = 0
    for mobile_name_key in mobile_model_name_list:
        dic_model_name[mobile_name_key].append(mobile_model_links_list[j])
        j += 1

    Write_to_DB(model_dictionary, MODEL_NAME_DATABASE_TABLE)

    return dic_year, dic_model_name

def get_models_names_from_gsmarena(request,soup,url):

    list_page = pagination_for_mobile_brand_list_from_gsmarena(soup,url)

    mobile_model_name_list = []
    mobile_model_links_list = []
    mobile_model_year_list = []
    main_url = []
    mobile_brand = request.session.get('brand')
    brand_list = []

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
                    main_url.append(GSMARENA_URL)
                    brand_list.append(mobile_brand)
                    mobile_model_year_list.append(year.group(0))
                    mobile_model_name_list.append(mobile_model_name.text)
                    mobile_model_links_list.append(model_links.attrs['href'])

                else:
                    main_url.append(GSMARENA_URL)
                    brand_list.append(mobile_brand)
                    mobile_model_year_list.append("Other")
                    mobile_model_name_list.append(mobile_model_name.text)
                    mobile_model_links_list.append(model_links.attrs['href'])

    model_dictionary = {MAIN_URL_KEY:main_url, BRAND_NAME_KEY: brand_list,
                      ANNOUNCED_YEAR_DICT_KEY:mobile_model_year_list,
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
    Write_to_DB(model_dictionary,MODEL_NAME_DATABASE_TABLE)

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


def get_models_names_from_android_forum(request,soup):
    mobile_model_name_list = []
    mobile_model_links_list = []
    mobile_model_year_list = []
    dic_model_name = defaultdict(list)
    dic_year = defaultdict(list)
    main_url = []
    mobile_brand = request.session.get('brand')
    brand_list = []

    for mobile_model_container in soup.find_all("ol", class_="deviceList uix_nodeStyle_3 section"):
        for l in mobile_model_container.find_all("h3", class_="nodeTitle"):
            brand_list.append(mobile_brand)
            mobile_model_name_list.append(l.text)
            mobile_model_year_list.append("All")
            model_links = l.find("a")
            mobile_model_links_list.append(model_links.attrs['href'])
            main_url.append(ANDROID_FORUM_URL)

    model_dictionary = {MAIN_URL_KEY:main_url, BRAND_NAME_KEY: brand_list,
                        ANNOUNCED_YEAR_DICT_KEY: mobile_model_year_list,
                        MODEL_NAME_DICT_KEY: mobile_model_name_list,
                        MODEL_LINK_DICT_KEY: mobile_model_links_list}

    Write_to_DB(model_dictionary, MODEL_NAME_DATABASE_TABLE)

    i = 0
    for key in mobile_model_year_list:
        dic_year[key].append(mobile_model_name_list[i])
        i += 1

    j = 0
    for mobile_name_key in mobile_model_name_list:
        dic_model_name[mobile_name_key].append(mobile_model_links_list[j])
        j += 1
    return dic_year,dic_model_name


def get_models_names_from_android_pit_forum(request,soup,url):
    mobile_model_name_list = []
    mobile_model_links_list = []
    mobile_model_year_list = []
    dic_model_name = defaultdict(list)
    dic_year = defaultdict(list)
    sub_cat_link = []
    main_url = []
    mobile_brand = request.session.get('brand')
    brand_list = []

    if soup.find("a", class_="forumSubcategory"):
        for subCatLink in soup.find_all("a", class_="forumSubcategory"):
            sub_cat_link.append(ANDROID_PIT_FORUM_URL + subCatLink.attrs["href"])

    if not sub_cat_link:
        soup = parse(url)
        product = soup.find("div", class_="forumHeadingWithFavorite")
        product_name = product.find("h1")
        brand_list.append(mobile_brand)
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
                        main_url.append(ANDROID_PIT_FORUM_URL)
                        brand_list.append(mobile_brand)
                        mobile_model_name_list.append(product_name_head.text)
                        mobile_model_links_list.append(subCatLink.attrs["href"])
                        mobile_model_year_list.append("All")
                    else:
                        main_url.append(ANDROID_PIT_FORUM_URL)
                        brand_list.append(mobile_brand)
                        mobile_model_name_list.append(product_name.text)
                        mobile_model_links_list.append(ANDROID_PIT_FORUM_URL +subCatLink.attrs["href"])
                        mobile_model_year_list.append("All")
            else:
                soup = parse(forumLink)
                product = soup.find("div", class_ = "forumHeadingWithFavorite")
                product_name = product.find("h1")

                main_url.append(ANDROID_PIT_FORUM_URL)
                brand_list.append(mobile_brand)
                mobile_model_name_list.append(product_name.text)
                mobile_model_links_list.append(forumLink)
                mobile_model_year_list.append("All")

    model_dictionary = {MAIN_URL_KEY:main_url, BRAND_NAME_KEY: brand_list,
                        ANNOUNCED_YEAR_DICT_KEY: mobile_model_year_list,
                        MODEL_NAME_DICT_KEY: mobile_model_name_list,
                        MODEL_LINK_DICT_KEY: mobile_model_links_list}

    Write_to_DB(model_dictionary, MODEL_NAME_DATABASE_TABLE)

    i = 0
    for key in mobile_model_year_list:
        dic_year[key].append(mobile_model_name_list[i])
        i += 1

    j = 0
    for mobile_name_key in mobile_model_name_list:
        dic_model_name[mobile_name_key].append(mobile_model_links_list[j])
        j += 1
    return dic_year, dic_model_name


def get_models_names_from_gadgets360(request,soup):

    mobile_model_name_list = []
    mobile_model_links_list = []
    mobile_model_year_list = []
    dic_model_name = defaultdict(list)
    dic_year = defaultdict(list)
    main_url = []
    mobile_brand = request.session.get('brand')
    brand_list = []

    for mobile_model_container in soup.find_all("ul", class_="clearfix margin_t20"):
        for link in mobile_model_container.find_all("a"):
            l = link.get('href')
            for product_name in link.find_all("strong"):
                brand_list.append(mobile_brand)
                mobile_model_links_list.append(l)
                mobile_model_name_list.append(product_name.text)
                main_url.append(GADGETS_FORUM_URL)

                #year_request = requests.get(l)
                #year_soup = bs4.BeautifulSoup(year_request.content, "html.parser")
                #for release_date_container in year_soup.findAll("ul", class_="_flx _dt"):
                    #for release_date in release_date_container.findAll("li"):
                        #split_year = re.compile(r'\d{4}')
                        #year = split_year.search(str(release_date))
                        #if year:
                            #mobile_model_year_list.append(year.group(0))
                            #prev_year = year.group(0)
                            #break
                    #if year is None:
                        #mobile_model_year_list.append(prev_year)
                mobile_model_year_list.append("All")

    model_dictionary = {MAIN_URL_KEY:main_url, BRAND_NAME_KEY: brand_list,
                        ANNOUNCED_YEAR_DICT_KEY: mobile_model_year_list,
                        MODEL_NAME_DICT_KEY: mobile_model_name_list,
                        MODEL_LINK_DICT_KEY: mobile_model_links_list}

    Write_to_DB(model_dictionary, MODEL_NAME_DATABASE_TABLE)

    i = 0
    for key in mobile_model_year_list:
        dic_year[key].append(mobile_model_name_list[i])
        i += 1

    j = 0
    for mobile_name_key in mobile_model_name_list:
        dic_model_name[mobile_name_key].append(mobile_model_links_list[j])
        j += 1
    return dic_year, dic_model_name


