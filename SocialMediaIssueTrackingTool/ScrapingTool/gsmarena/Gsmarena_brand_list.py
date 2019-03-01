import requests
from bs4 import BeautifulSoup
import pandas as pd
from ScrapingTool.sqlite3_read_write import GetData_In_Dict, Write_to_DB

def get_brand_names():
    url="https://www.gsmarena.com/"
    http_request = requests.get(url)
    soup = BeautifulSoup(http_request.content ,"html.parser")

    mobile_brand_list=[]
    mobile_brand_links_list=[]
    brand_dict ={}
    for mobile_brand_container in soup.find_all("div", class_="brandmenu-v2 light l-box clearfix"):

        for list_of_brands in mobile_brand_container.find_all("li"):
            mobile_brand_list.append(list_of_brands.text)
            for brand_links in list_of_brands.find_all("a"):
                mobile_brand_links_list.append(brand_links.attrs['href'])
        brand_dict ={"Brand_Name":mobile_brand_list, "Link":mobile_brand_links_list}
        Write_to_DB(brand_dict,"Mobile_Brands")
        return mobile_brand_list,mobile_brand_links_list

