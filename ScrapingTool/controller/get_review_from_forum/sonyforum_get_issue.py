from datetime import datetime
import re
from ScrapingTool.Generic.constant import SONY_FORUM_URL
from ScrapingTool.Generic.category_search import generic_category_filter
from ScrapingTool.Models.file_read_write import fileReaderWriter
from ScrapingTool.Generic.parser import parse


def sony_forum_get_issue(request,selected_model_links,selected_dates):
    date_list = []
    url_list = []
    product_list = []
    category_list = []
    user_comment_list = []
    heading_name_list = []
    for model_url in selected_model_links:
        pagination_url_list=[]
        pagination_list = pagination_for_thread_links(model_url)
        if pagination_list:
            for url in pagination_list:
                pagination_url_list.append(url)
        else:
            pagination_url_list.append(model_url)

        data_fetch_url_list =remove_dupilcate_link(get_thread_link_from_sony_forum(pagination_url_list,selected_dates))

        for url in data_fetch_url_list:
            soup=parse(url)
            for issue_container in soup.find_all("div", class_="lia-linear-display-message-view"):
                local_date = issue_container.find('span', class_='local-friendly-date')

                issue_local_date = issue_container.find('span', class_='local-date')
                issue_date = ""
                if local_date:
                    if local_date.has_attr('title'):
                        issue_date = local_date['title'][1:11]
                    else:
                        pass
                elif issue_local_date:
                    issue_date = issue_local_date.get_text()

                match = re.search('\d{4}-\d{2}-\d{2}', issue_date.strip('\u200e'))
                product_date = datetime.strptime(match.group(), '%Y-%m-%d').date()
                converted_date = product_date.strftime('%m/%d/%Y')
                cdate = datetime.strptime(converted_date, '%m/%d/%Y').date()
                sdate = datetime.strptime(selected_dates[-1], '%m/%d/%Y').date()
                s1date = datetime.strptime(selected_dates[0], '%m/%d/%Y').date()

                child_node = issue_container.find('div', class_='lia-message-body-content')

                if (cdate > sdate):
                    break
                elif (cdate < s1date):
                    pass
                else:
                    for date in selected_dates:
                        if date == converted_date:
                            date_list.append(issue_date.strip('\u200e'))
                            url_list.append(url)
                            product_name = soup.find("a",
                                                     class_="lia-link-navigation crumb-board lia-breadcrumb-board lia-breadcrumb-forum").get_text()
                            product_list.append(product_name)
                            thread = soup.find("span", class_="lia-link-navigation lia-link-disabled").get_text()
                            heading_name_list.append(thread)
                            issue_data, category = generic_category_filter(child_node)
                            user_comment_list.append(issue_data)
                            category_list.append(category)

    data_dictionary = {"Product": product_list, "Date": date_list, "Category": category_list,
                        "Thread": heading_name_list,
                        "Link": url_list, "Comment": user_comment_list}

    if not product_list:
        data_dictionary = {}
    else:
        file_writer = fileReaderWriter()
        file_writer.write_data_using_pandas(request, data_dictionary)

    return data_dictionary


def pagination_for_thread_links(model_url):
    page_url = model_url + "/page/%s"
    pagination_list = []
    soup = parse(model_url)
    if soup.find("ul", {"class": "lia-paging-full-pages"}):
        number_of_pages = soup.find("ul", {"class": "lia-paging-full-pages"})
        page_text = number_of_pages.text
        page_number_list = re.findall(r'\d+', page_text)
        list_last_page_number = page_number_list[-1]
        for i in range(1, int(list_last_page_number) + 1):
            urls = page_url % i  # make a url list and iterate over it
            pagination_list.append(urls)
    return pagination_list


def get_thread_link_from_sony_forum(pagination_url_list,selected_dates):
    issue_links_list=[]

    for url in pagination_url_list:
        soup = parse(url)
        for product_container in soup.findAll("div", {"class": "lia-component-messages-column-message-info"}):
            product_cont = product_container.find("a", {"class": "page-link lia-link-navigation lia-custom-event"})
            product_links = product_cont.attrs["href"]
            issue_url = SONY_FORUM_URL + product_links
            for Check_date in product_container.findAll('span', {"class": "local-friendly-date"}):
                issue_dates = Check_date['title'][1:11]
                product_date = datetime.strptime(issue_dates, '%Y-%m-%d').date()
                converted_date = product_date.strftime('%m/%d/%Y')
                cdate = datetime.strptime(converted_date, '%m/%d/%Y').date()
                sdate = datetime.strptime(selected_dates[-1], '%m/%d/%Y').date()
                s1date = datetime.strptime(selected_dates[0], '%m/%d/%Y').date()
                if (cdate > sdate):
                    break
                elif (cdate<s1date):
                    pass
                else:
                    for date in selected_dates:
                        if date == converted_date.strip('\u200e'):
                            # Pagination code: If each issue has more than one page enter this code
                            if product_container.find("ul", class_="lia-list-standard-inline"):
                                issue_soup = parse(issue_url)
                                page_url = issue_url + "/page/%s"
                                issue_link = issue_soup.find("div", {"class": "lia-quilt-row lia-quilt-row-main"})
                                page_link = issue_link.find("div", {
                                    "class": "lia-paging-full-wrapper lia-paging-pager lia-paging-full-left-position lia-discussion-page-message-pager lia-component-message-pager"})
                                if page_link:
                                    last_pages = page_link.find("ul", {"class": "lia-paging-full-pages"})
                                    # get page number from the above html tag
                                    page_text = last_pages.text
                                    number_list = re.findall(r'\d+', page_text)
                                    # Get the last number from the list of numbers
                                    list_number = number_list[-1]
                                    for i in range(1, int(list_number) + 1):
                                        urls = page_url % i  # make a url list and iterate over it
                                        issue_links_list.append(urls)
                                else:
                                    pass
                            else:
                                issue_links_list.append(issue_url)
    return issue_links_list


def remove_dupilcate_link(duplicate):
    final_links_list = []
    for link in duplicate:
        if link not in final_links_list:
            final_links_list.append(link)
    return final_links_list