import pandas as pd
import re

import requests
from bs4 import BeautifulSoup

from ScrapingTool.file_read_write import fileReaderWriter


class getProductNamesAndLinks:
#Fetch series name and link
    def get_product_series(self, url):
        series_dictionary_data = {}
        try:
            # creating links to add all the product name and product links
            series_links_list = []
            series_names_list = []

            # passing URL to get the responce from website
            response = requests.get(url)
            response.close()

            # getting html code using Beautifull soup
            soup = BeautifulSoup(response.content, "html.parser")

            # Getting all the phone series links
            home_page_list = soup.find_all("a", class_="lia-link-navigation category-title")

            for t in home_page_list:
                series_names_list.append(t.text)
                series_links_list.append(t.attrs['href'])

            for i in range(len(series_names_list)):
                series_dictionary_data[series_names_list[i]] = series_links_list[i]

            return series_dictionary_data

        except:
            return series_dictionary_data



#Get product name and links for selected series
    def get_links_for_products(self, series_url):
        dictionary_data = {}

        try:
                # creating links to add all the product name and product links
                product_links_list = []
                product_name_list = []

                # passing URL to get the responce from website
                response = requests.get(series_url)
                response.close()

                # getting html code using Beautifull soup
                soup = BeautifulSoup(response.content, "html.parser")

                # getting all the product name links and appending in to the list
                home_page_list = soup.find_all("a", class_="lia-link-navigation lia-message-unread")

                type(home_page_list)
                home_page_list[0].text
                home_page_list[0].attrs['href']

                for t in home_page_list:
                    product_name_list.append(t.text)
                    product_links_list.append(t.attrs['href'])


                for i in range(len(product_name_list)):
                    dictionary_data[product_name_list[i]] = product_links_list[i]
                return dictionary_data
        except:
            return dictionary_data


#Fetch all the product page link for selected products
    def get_pagination_links(self, req_url_list):
        page_url = req_url_list + "/page/%s"
        pagination_list = []
        url_req = requests.get(req_url_list)
        soup_container = BeautifulSoup(url_req.content, "html.parser")
        if soup_container.find("ul", {"class": "lia-paging-full-pages"}):
            number_of_pages = soup_container.find("ul", {"class": "lia-paging-full-pages"})
            page_text = number_of_pages.text
            page_number_list = re.findall(r'\d+', page_text)
            list_last_page_number = page_number_list[-1]
            for i in range(1, int(list_last_page_number) + 1):
                urls = page_url % i  # make a url list and iterate over it
                pagination_list.append(urls)
        return pagination_list


# Fetch Series names and link for selected product
    def get_dictionary_data(self):
        file_read = fileReaderWriter()
        get_product_links = getProductNamesAndLinks()

        file_path = open("ScrapingTool/files/mainurl.txt", "r")
        url = file_read.read_links_from_text_file(file_path) + "/t5/Phones-Tablets/ct-p/Phones"
        series_dictionary = get_product_links.get_product_series(url)

        return series_dictionary