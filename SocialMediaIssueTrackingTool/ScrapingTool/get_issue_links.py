'''
Fetching issue links
input : getting product pagination links from issueLinksPagination() method of views
output : Issue link for each product link
'''
from multiprocessing import pool

import requests
from bs4 import BeautifulSoup
from requests import RequestException
import re,datetime

from ScrapingTool.scrap_data import scrapData


class getIssueLinks:

    def get_issue_link(self,product_links_list,Date_list):
        issue_links_list = []
        try:
            for url in product_links_list:
                req = requests.get(url)
                    #parsing html code using html parser with the BeautifulSoup object
                soup = BeautifulSoup(req.content, "html.parser")

                '''
                Fetching Issue links using tag,id
                Input : Html tag and id
                Output : Issue links for each product link
                '''
                for product_container in soup.findAll("div", {"class": "lia-component-messages-column-message-info"}):
                        product_cont = product_container.find("a", {"class":"page-link lia-link-navigation lia-custom-event"})
                        product_links = product_cont.attrs["href"]
                        issue_url ="https://talk.sonymobile.com"+product_links


                        for Check_date in product_container.findAll('span', {"class": "local-friendly-date"}):
                            issue_dates = Check_date['title'][1:11]
                            product_date = datetime.datetime.strptime(issue_dates, '%Y-%m-%d').date()
                            format_product_date = product_date.strftime('%m/%d/%Y')
                            #If From and To date selected by user
                            if Date_list:
                                for date in Date_list:
                                    if date == format_product_date:
                                        # Pagination code: If each issue has more than one page enter this code
                                        if product_container.find("ul", class_="lia-list-standard-inline"):
                                            issue_request = requests.get(issue_url)
                                            issue_soup = BeautifulSoup(issue_request.content, "html.parser")
                                            page_url = issue_url + "/page/%s"
                                            issue_link = issue_soup.find("div", {"class": "lia-quilt-row lia-quilt-row-main"})
                                            page_link = issue_link.find("div", {
                                                "class": "lia-paging-full-wrapper lia-paging-pager lia-paging-full-left-position lia-discussion-page-message-pager lia-component-message-pager"})
                                            if page_link:
                                                last_pages = page_link.find("ul", {"class": "lia-paging-full-pages"})
                                                #get page number from the above html tag
                                                page_text = last_pages.text
                                                number_list = re.findall(r'\d+', page_text)
                                                #Get the last number from the list of numbers
                                                list_number = number_list[-1]
                                                for i in range(1, int(list_number) + 1):
                                                    urls = page_url % i  # make a url list and iterate over it
                                                    issue_links_list.append(urls)
                                            else:
                                                pass
                                        else:
                                            issue_links_list.append(issue_url)
                            #if all dates selected option by user
                            else:
                                if product_container.find("ul", class_="lia-list-standard-inline"):
                                    issue_request = requests.get(issue_url)
                                    issue_soup = BeautifulSoup(issue_request.content, "html.parser")
                                    page_url = issue_url + "/page/%s"
                                    issue_link = issue_soup.find("div", {"class": "lia-quilt-row lia-quilt-row-main"})
                                    page_link = issue_link.find("div", {
                                        "class": "lia-paging-full-wrapper lia-paging-pager lia-paging-full-left-position lia-discussion-page-message-pager lia-component-message-pager"})
                                    if page_link:
                                        last_pages = page_link.find("ul", {"class": "lia-paging-full-pages"})
                                        page_text = last_pages.text
                                        number_list = re.findall(r'\d+', page_text)
                                        list_number = number_list[-1]
                                        for i in range(1, int(list_number) + 1):
                                            urls = page_url % i  # make a url list and iterate over it
                                            issue_links_list.append(urls)
                                    else:
                                        pass
                                else:
                                    issue_links_list.append(issue_url)

            #Fetch scrap data
            scrap_data=scrapData()
            print("link_list %s ",issue_links_list)
            get_value_from_scrap_data=scrap_data.get_issue_data(getIssueLinks().remove_dupilcate_link(issue_links_list),Date_list)
            return get_value_from_scrap_data

        except RequestException as e:
            print('Error during requests to {0} : {1}'.format(url, str(e)))


#function to remove duplicate links
    def remove_dupilcate_link(self, duplicate):
            final_links_list = []
            for link in duplicate:
                if link not in final_links_list:
                    final_links_list.append(link)
            print("after duplicate remove %s", final_links_list)
            return final_links_list
