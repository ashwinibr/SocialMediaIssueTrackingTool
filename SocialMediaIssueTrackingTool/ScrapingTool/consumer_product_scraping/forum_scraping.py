
from SocialMediaIssueTrackingTool.ScrapingTool.consumer_product_scraping.brand_name_scraping import \
    get_brand_name_from_gsmarena, get_brand_name_from_androidforum
from SocialMediaIssueTrackingTool.ScrapingTool.consumer_product_scraping.model_name_scraping import \
    get_models_names_from_gsmarena, get_models_names_from_android_forum

from SocialMediaIssueTrackingTool.ScrapingTool.parser import parse


def get_brand_names(url):

    if "androidforums" in url:
        url=url+"devices/list/"

    soup = parse(url)
    mobile_brand_list=[]
    mobile_brand_links_list=[]

    if "gsmarena" in url:
        get_brand_name_from_gsmarena(soup,mobile_brand_list,mobile_brand_links_list)
    elif "androidforums" in url:
        get_brand_name_from_androidforum(soup,mobile_brand_list,mobile_brand_links_list)

    return mobile_brand_list,mobile_brand_links_list


def get_models_names(url):
    model_name_dic=()

    if "/devices/list" in url:
        url="https://androidforums.com/"+url
    else:
        url="https://www.gsmarena.com/"+url

    soup = parse(url)
    if "gsmarena" in url:
        model_name_dic = get_models_names_from_gsmarena(soup,url)
    elif "androidforums" in url:
        model_name_dic = get_models_names_from_android_forum(soup)
    return model_name_dic

