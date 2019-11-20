from ScrapingTool.Generic.constant import *
from ScrapingTool.Models.sqlite3_read_write import Write_to_DB


def get_brand_name_from_gsmarena(soup,mobile_brand_list,mobile_brand_links_list):
    main_url = []
    for mobile_brand_container in soup.find_all("div", class_="brandmenu-v2 light l-box clearfix"):
        for list_of_brands in mobile_brand_container.find_all("li"):
            mobile_brand_list.append(list_of_brands.text)
            for brand_links in list_of_brands.find_all("a"):
                mobile_brand_links_list.append(GSMARENA_URL+brand_links.attrs['href'])
                main_url.append(GSMARENA_URL)

    brand_dict = {MAIN_URL_KEY:main_url, BRAND_NAME_DICT_KEY: mobile_brand_list, BRAND_LINK_DICT_KEY: mobile_brand_links_list}
    Write_to_DB(brand_dict, MOBILE_BRANDS_DATABASE_TABLE)
    return mobile_brand_list,mobile_brand_links_list


def get_brand_name_from_androidforum(soup,mobile_brand_list,mobile_brand_links_list):
    main_url = []
    for mobile_brand_container in soup.find_all("div", class_="nodeInfo forumNodeInfo featuredNode brandNode"):
        for list_of_brands in mobile_brand_container.find_all("h3"):

            for brand_name in list_of_brands.find_all("span"):
                mobile_brand_list.append(brand_name.text)
                mobile_brand_links_list.append(ANDROID_FORUM_URL+brand_name.attrs['href'])
                main_url.append(ANDROID_FORUM_URL)

    brand_dict = {MAIN_URL_KEY:main_url, BRAND_NAME_DICT_KEY: mobile_brand_list, BRAND_LINK_DICT_KEY: mobile_brand_links_list}
    Write_to_DB(brand_dict, MOBILE_BRANDS_DATABASE_TABLE)
    return mobile_brand_list, mobile_brand_links_list


def get_brand_name_from_androidpit_forum(soup,mobile_brand_list,mobile_brand_links_list):
    string = ["General", "AndroidPIT Support (ONLY for the AndroidPIT site, AndroidPIT app and Buzzinga app)","Android",
              "Android Developer","Other Android Devices and Services (Chromecast, Google Fit etc)","Android Tablets",
              "Other Android Tablets","Wearable Android Devices","Miscellaneous"]
    main_url = []

    for forum_a_links in soup.find_all("a", {"class": "forumOverviewCategoryListLink"}):
        for forum_name in forum_a_links.find_all("h2"):
            if (forum_name.text).strip() not in string:
                mobile_brand_list.append(forum_name.text)
                mobile_brand_links_list.append(ANDROID_PIT_FORUM_URL+forum_a_links.attrs['href'])
                main_url.append(ANDROID_PIT_FORUM_URL)

    brand_dict = {MAIN_URL_KEY:main_url, BRAND_NAME_DICT_KEY: mobile_brand_list, BRAND_LINK_DICT_KEY: mobile_brand_links_list}
    Write_to_DB(brand_dict, MOBILE_BRANDS_DATABASE_TABLE)
    return mobile_brand_list, mobile_brand_links_list


def get_brand_name_from_gadget360(soup, mobile_brand_list, mobile_brand_links_list):
    main_url =[]
    for mobile_brand_container in soup.findAll("div", class_="subnav"):
        for brand in mobile_brand_container.findAll("a"):
            brand_link = brand.get('href')
            mobile_brand_list.append(brand.text)
            mobile_brand_links_list.append(brand_link)
            main_url.append(GADGETS_FORUM_URL)

    print(mobile_brand_list)
    brand_dict = {MAIN_URL_KEY:main_url, BRAND_NAME_DICT_KEY: mobile_brand_list, BRAND_LINK_DICT_KEY: mobile_brand_links_list}
    Write_to_DB(brand_dict, MOBILE_BRANDS_DATABASE_TABLE)
    return mobile_brand_list, mobile_brand_links_list


def get_brand_name_forum_sonyforum(soup, mobile_brand_list, mobile_brand_links_list):
    main_url = []

    for mobile_brand_container in soup.find_all("a", class_="lia-link-navigation category-title"):
        mobile_brand_list.append(mobile_brand_container.text)
        mobile_brand_links_list.append(mobile_brand_container.attrs['href'])
        main_url.append(SONY_FORUM_URL)

    brand_dict = {MAIN_URL_KEY: main_url, BRAND_NAME_DICT_KEY: mobile_brand_list,
                  BRAND_LINK_DICT_KEY: mobile_brand_links_list}
    Write_to_DB(brand_dict, MOBILE_BRANDS_DATABASE_TABLE)
    return mobile_brand_list, mobile_brand_links_list