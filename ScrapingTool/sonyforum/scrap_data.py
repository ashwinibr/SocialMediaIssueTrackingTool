'''
Scrap Data class is to scrap user issue content
Input : Product Issue url
Output : Product name,user name,author rank,issue link,issue date,subject,content
'''
import datetime
import logging
import re
import pandas as pd

import requests
from bs4 import BeautifulSoup
from requests import RequestException
from ScrapingTool.file_read_write import fileReaderWriter

class scrapData:
    logging.basicConfig(level=logging.DEBUG)

    def get_issue_data(self,issue_link,selected_date_list):
        #creating a list to store all the details
        author_rank_list = []
        user_name_list = []
        date_list = []
        issue_list = []
        thread_name_list = []
        product_name_list = []
        thread_link_list = []
        data_dictionary={}
        category_list = []

        excel_file = 'ScrapingTool/files/social_keywords.xlsx'
        dataset = pd.read_excel(excel_file)
        df = pd.DataFrame(dataset)
        data = df.get("Category")


        #creating csv file name social_media.csv
        #f = csv.writer(open('D:\Q& CS\Social_media_tracking\Data.csv', 'w', encoding='utf-8'))
        #header = ['Product_name', 'User_name', 'Author_rank', 'Link', 'Subject', 'Date', 'Issue']
        #f.writerow(header)

        #using for loop to getting each URL
        #print("scrap data links %s", issue_link)
        #print("scrap data selected date %s",selected_date_list)

        for url in issue_link:
            #url="https://talk.sonymobile.com/t5/Xperia-XZ2-Compact/Android-9-volume/td-p/1346706/page/2"
            print("for ", url)
            try:
                http_request = requests.get(url)
                soup = BeautifulSoup(http_request.content,"html.parser")

                #Fetching user data
                for issue_container in soup.find_all("div",class_="lia-linear-display-message-view"):


                    if not selected_date_list:
                        #Issue link added
                        thread_link_list.append(url)

                        # Fetching product name
                        product_name = soup.find("a",
                                                 class_="lia-link-navigation crumb-board lia-breadcrumb-board lia-breadcrumb-forum").get_text()
                        product_name_list.append(product_name)

                        # Fetching thread name
                        thread = soup.find("span", class_="lia-link-navigation lia-link-disabled").get_text()
                        thread_name_list.append(thread)

                        # Fetching user name
                        user = issue_container.find("div", {"class": "lia-quilt-row lia-quilt-row-header"})
                        name = user.find("div", {"class": "lia-quilt-column-alley lia-quilt-column-alley-left"})
                        user_name = name.span.text
                        user_name_list.append(user_name)

                        # Fetching Author_rank
                        rank = issue_container.find('div',
                                                    class_='lia-message-author-rank lia-component-author-rank lia-component-message-view-widget-author-rank').get_text()
                        print("rank",rank)
                        author = rank.split()
                        author_rank = ""
                        for author_list in author:
                            string = author_list.strip('[]')
                            author_rank = author_rank + " " + string
                        author_rank_list.append(author_rank)

                        # Fetching Issue date
                        try:
                            local_date = issue_container.find('span', class_='local-friendly-date')
                            issue_local_date = issue_container.find('span', class_='local-date')
                            if local_date:
                                if local_date.has_attr('title'):
                                    issue_date = local_date['title'][1:11]
                                    date_list.append(issue_date)
                                else:
                                    pass
                            elif issue_local_date:
                                issue_date = issue_local_date.get_text()
                                date_list.append(issue_date)
                        except ValueError:
                            logging.error("error for scraping date in scrapData class")

                        # Fetching Issue content
                        try:
                            content = issue_container.find('div', class_='lia-message-body-content')
                            if content:
                                issue = content.get_text()
                                issue_list.append(issue)
                                print(issue)
                                # keyword fetch
                                #key = []
                                key = ''
                                for keyword in data:
                                    main = re.findall((r'\b' + keyword + r'\b'), issue, re.IGNORECASE)
                                    if main:
                                        #key.append(keyword)
                                        key = str(keyword)+ ',' + str(key)
                                    else:
                                        pass
                                if key:
                                    category_list.append(key)
                                else:
                                    category_list.append("other")
                            #If no content for particullar issue link
                            else:
                                issue = "No content refer issue thread"
                                issue_list.append(issue)
                        except:
                            logging.error('An error occurred in getting the detailed issue' + url)

                    else:
                        # Fetching Issue date
                        try:
                            local_date = issue_container.find('span', class_='local-friendly-date')

                            issue_local_date = issue_container.find('span', class_='local-date')
                            if local_date:
                                if local_date.has_attr('title'):
                                    issue_date = local_date['title'][1:11]
                                else:
                                    pass
                            elif issue_local_date:
                                    issue_date = issue_local_date.get_text()

                        except ValueError:
                            logging.error("error for scraping date in scrapData class")

                        match = re.search('\d{4}-\d{2}-\d{2}', issue_date)
                        product_date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
                        format_product_date = product_date.strftime('%m/%d/%Y')


                        for date in selected_date_list:
                            #print("url%s", url)
                            #print("formate date &s", format_product_date)
                            #print("date %s", date)
                            if date == format_product_date:

                                date_list.append(issue_date)
                                thread_link_list.append(url)

                                print("checking %s", url)

                                #Fetching product name
                                product_name = soup.find("a",class_="lia-link-navigation crumb-board lia-breadcrumb-board lia-breadcrumb-forum").get_text()
                                product_name_list.append(product_name)

                                #Fetching thread name
                                thread = soup.find("span", class_="lia-link-navigation lia-link-disabled").get_text()
                                thread_name_list.append(thread)

                                #Fetching user name
                                user = issue_container.find("div", {"class": "lia-quilt-row lia-quilt-row-header"})
                                name = user.find("div", {"class": "lia-quilt-column-alley lia-quilt-column-alley-left"})
                                user_name = name.span.text
                                user_name_list.append(user_name)

                                #Fetching Author_rank
                                rank = issue_container.find('div',
                                                            class_='lia-message-author-rank lia-component-author-rank lia-component-message-view-widget-author-rank').get_text()

                                author = rank.split()
                                author_rank = ""
                                for author_list in author:
                                    string = author_list.strip('[]')
                                    author_rank=author_rank+" "+string
                                author_rank_list.append(author_rank)


                                #Fetching Issue content
                                try:
                                    content = issue_container.find('div', class_='lia-message-body-content')
                                    if content:
                                        issue = content.get_text()
                                        issue_list.append(issue)
                                        print(issue)
                                        #keyword fetch
                                        #key = []
                                        key = ''
                                        for keyword in data:
                                            main = re.findall((r'\b' + keyword + r'\b'), issue, re.IGNORECASE)
                                            if main:
                                                #key.append(keyword)
                                                key = str(keyword)+ ',' + str(key)
                                            else:
                                                pass
                                        if key:
                                            category_list.append(key)
                                        else:
                                            category_list.append("other")
                                    else:
                                        print("else entered")
                                        issue = "No content refer issue thread"
                                        issue_list.append(issue)

                                except:
                                    logging.error('An error occurred in getting the detailed issue' + url)


                                #Write issue data in csv file
                                #f.writerow([product_name, user_name, author_rank, url, thread, issue_date, issue])

            except RequestException as e:
                logging.error('Error during requests to {0} : {1}'.format(url, str(e)))


            #Call dictionary to write the issue content
            data_dictionary = {'Product': product_name_list, 'First User Name': user_name_list,
                               'Second User Name': author_rank_list, 'Category': category_list,
                               'Thread Name': thread_name_list, "Links ": thread_link_list, 'Date': date_list,
                               "Issue Detail": issue_list}


        file_writer = fileReaderWriter()
        #Call write_data_using_pandas() function to write scraped dat from dictionary to excel sheet
        file_writer.write_data_using_pandas(data_dictionary)
        return data_dictionary



