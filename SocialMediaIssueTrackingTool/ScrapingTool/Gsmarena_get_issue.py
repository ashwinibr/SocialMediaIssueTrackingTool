import requests
from bs4 import BeautifulSoup
from ScrapingTool.file_read_write import fileReaderWriter


def main_method(url):

    #url="https://www.gsmarena.com/samsung_galaxy_m20-9506.php"
    #url="https://www.gsmarena.com/apple-phones-48.php"

    http_request = requests.get(url)
    soup = BeautifulSoup(http_request.content ,"html.parser")

    review_opinion_link_list=[]

    for review_button_container in soup.find_all("div", class_="button-links"):
        for review_button_link in review_button_container.find_all("a"):
            review_opinion_link_list.append(review_button_link.attrs['href'])

    get_issue(review_opinion_link_list[0])
#print(review_opinion_link_list[0])


def get_issue(issue_url):
    http_request = requests.get("https://www.gsmarena.com/"+issue_url)
    soup = BeautifulSoup(http_request.content, "html.parser")

    for issue_container in soup.find_all("div", class_="user-thread"):
        #print(issue_container)
        date_list=issue_container.find("li",class_="upost")
        print(date_list.text)

        user_comment=issue_container.find("p", class_="uopin")
        print(user_comment.text)

