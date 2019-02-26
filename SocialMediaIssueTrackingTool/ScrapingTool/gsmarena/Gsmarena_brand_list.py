import requests
from bs4 import BeautifulSoup


def get_brand_names():
    url="https://www.gsmarena.com/"
    http_request = requests.get(url)
    soup = BeautifulSoup(http_request.content ,"html.parser")

    mobile_brand_list=[]
    mobile_brand_links_list=[]

    for mobile_brand_container in soup.find_all("div", class_="brandmenu-v2 light l-box clearfix"):

        for list_of_brands in mobile_brand_container.find_all("li"):
            mobile_brand_list.append(list_of_brands.text)
            for brand_links in list_of_brands.find_all("a"):
                mobile_brand_links_list.append(brand_links.attrs['href'])

        return mobile_brand_list,mobile_brand_links_list