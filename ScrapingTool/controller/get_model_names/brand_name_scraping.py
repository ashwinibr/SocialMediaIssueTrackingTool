#from ScrapingTool.sqlite3_read_write import Write_to_DB
import ScrapingTool.mongo_read_write as mongo
from ScrapingTool.Generic.constant import BRAND_NAME_DICT_KEY, BRAND_LINK_DICT_KEY, MOBILE_BRANDS_DATABASE_TABLE

def get_brand_name_from_gsmarena(req_id,soup,mobile_brand_list,mobile_brand_links_list):

    for mobile_brand_container in soup.find_all("div", class_="brandmenu-v2 light l-box clearfix"):
        for list_of_brands in mobile_brand_container.find_all("li"):
            mobile_brand_list.append(list_of_brands.text)
            for brand_links in list_of_brands.find_all("a"):
                mobile_brand_links_list.append(brand_links.attrs['href'])

    brand_dict = {BRAND_NAME_DICT_KEY: mobile_brand_list, BRAND_LINK_DICT_KEY: mobile_brand_links_list}
    collection_name = MOBILE_BRANDS_DATABASE_TABLE + req_id
    mongo.Write_to_DB(brand_dict,collection_name)
    return mobile_brand_list,mobile_brand_links_list


def get_brand_name_from_androidforum(req_id,soup,mobile_brand_list,mobile_brand_links_list):
    for mobile_brand_container in soup.find_all("div", class_="nodeInfo forumNodeInfo featuredNode brandNode"):
        for list_of_brands in mobile_brand_container.find_all("h3"):

            for brand_name in list_of_brands.find_all("span"):
                mobile_brand_list.append(brand_name.text)
                mobile_brand_links_list.append(brand_name.attrs['href'])

    brand_dict = {BRAND_NAME_DICT_KEY: mobile_brand_list, BRAND_LINK_DICT_KEY: mobile_brand_links_list}
    collection_name = MOBILE_BRANDS_DATABASE_TABLE + req_id
    mongo.Write_to_DB(brand_dict, collection_name)
    return mobile_brand_list, mobile_brand_links_list


def get_brand_name_from_androidpit_forum(req_id,soup,mobile_brand_list,mobile_brand_links_list):
    string = ["General", "AndroidPIT Support (ONLY for the AndroidPIT site, AndroidPIT app and Buzzinga app)","Android",
              "Android Developer","Other Android Devices and Services (Chromecast, Google Fit etc)","Android Tablets",
              "Other Android Tablets","Wearable Android Devices","Miscellaneous"]

    for forum_a_links in soup.find_all("a", {"class": "forumOverviewCategoryListLink"}):
        for forum_name in forum_a_links.find_all("h2"):
            if (forum_name.text).strip() not in string:
                mobile_brand_list.append(forum_name.text)
                mobile_brand_links_list.append(forum_a_links.attrs['href'])
    brand_dict = {BRAND_NAME_DICT_KEY: mobile_brand_list, BRAND_LINK_DICT_KEY: mobile_brand_links_list}
    collection_name = MOBILE_BRANDS_DATABASE_TABLE + req_id
    mongo.Write_to_DB(brand_dict, collection_name)
    return mobile_brand_list, mobile_brand_links_list