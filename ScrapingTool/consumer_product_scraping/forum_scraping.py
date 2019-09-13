from ScrapingTool.common import *
from ScrapingTool.consumer_product_scraping.brand_name_scraping import \
    get_brand_name_from_gsmarena, get_brand_name_from_androidforum
from ScrapingTool.consumer_product_scraping.get_review_from_forum.Gsmarena_get_issue import gsmarena_get_issue
from ScrapingTool.consumer_product_scraping.get_review_from_forum.android_forum_get_issue import android_forum_get_issue
from ScrapingTool.consumer_product_scraping.model_name_scraping import \
    get_models_names_from_gsmarena, get_models_names_from_android_forum


from ScrapingTool.parser import parse


def get_brand_names(url):

    if ANDROID_FORUM_STRING in url:
        url = url+"devices/list/"

    soup = parse(url)
    mobile_brand_list=[]
    mobile_brand_links_list=[]

    if GSMARRENS_STRING in url:
        get_brand_name_from_gsmarena(soup,mobile_brand_list,mobile_brand_links_list)
    elif ANDROID_FORUM_STRING in url:
        get_brand_name_from_androidforum(soup,mobile_brand_list,mobile_brand_links_list)

    return mobile_brand_list,mobile_brand_links_list


def get_models_names(url):
    model_name_dic=()

    if "/devices/list" in url:
        url = ANDROID_FORUM_URL+url
    else:
        url= GSMARENA_URL+url

    soup = parse(url)

    if GSMARRENS_STRING in url:
        model_name_dic = get_models_names_from_gsmarena(soup,url)
    elif ANDROID_FORUM_STRING in url:
        model_name_dic = get_models_names_from_android_forum(soup)
    return model_name_dic


def get_data_from_url(url,selected_model_url,selected_dates):
    data_dictionary = {}
    if ANDROID_FORUM_STRING in url:
        data_dictionary = android_forum_get_issue(selected_model_url, selected_dates)
    elif GSMARRENS_STRING in url:
        data_dictionary = gsmarena_get_issue(selected_model_url, selected_dates)

    return data_dictionary

