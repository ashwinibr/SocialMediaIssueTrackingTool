# Create your views here.
import datetime
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import logging

from ScrapingTool.file_read_write import fileReaderWriter
from ScrapingTool.get_issue_links import getIssueLinks
from ScrapingTool.logics.DateFormateClass import dateFormate, dateListFunction
from ScrapingTool.product_name_and_links import getProductNamesAndLinks
from ScrapingTool.Gsmarena_brand_list import get_brand_names
from ScrapingTool.Gsmarena_models_list import pagination_for_mobile_brand_list
from ScrapingTool.Gsmarena_get_issue import main_method

logging.basicConfig(level=logging.DEBUG)

@csrf_exempt
def homepage_view(request):
    print("in home page view")
    #renders home page
    homepage_template = loader.get_template('homepage.html')
    logging.info("rendering home page view")
    return HttpResponse(homepage_template.render())


@csrf_exempt
def brand_view(request):
    brand_list = []
    brand_dict = {}
    print("In brand page")
    if request.POST.get('back_button'):
        response = redirect('homepage')
        logging.info("redirecting series page to home page view")
        return response

    if request.POST.get('homepage_submit_btn'):
        main_url = request.POST.get('mainurl')
        status_code = fileReaderWriter.get_response_code(main_url)
        logging.debug("Status code : %s",status_code)

        #if valid url entered,write it in to url.txt file
        if status_code == 200:
            with open("ScrapingTool/files/mainurl.txt", "w") as file:
                file.write(main_url)
        #else if invalid url entered,displays error
        else:
            error_message = "Invalid URL "
            logging.error("handling an error message for status code : %s",error_message)
            return render(request, "homepage.html",
                          {"errorvalue": error_message})
    file_read = fileReaderWriter()
    file = open("ScrapingTool/files/mainurl.txt", "r")
    main_url = file_read.read_links_from_text_file(file)
    
    if (main_url=="https://www.gsmarena.com/" or main_url=="https://www.gsmarena.com"):
        brand_list = get_brand_names()
        brand_dict = dict(zip(brand_list[0],brand_list[1]))
        print(brand_dict)
        print(brand_list[0])
        return render(request, "brandselection.html",
                      {"brandlist": brand_list[0]})
    else:
        error_message = "Invalid URL"
        logging.error("handling an error message for empty brand name : %s", error_message)
        return render(request, "brandselection.html",
                      {"errorvalue": error_message})



@csrf_exempt
def mobile_view(request):
    print("In Mobile View")
    mobile_list = []
    mobile_dict ={}
    error_message=""
    info_msg = ""
    successmsg = ""

    if request.POST.get('back_button'):
        response = redirect('brand/')
        logging.info("redirecting mobile page to brand page view")
        return response

    if request.POST.get('brand_submit'):
        print("Brand submit clicked") 
        brand_list = get_brand_names()
        brand_dict = dict(zip(brand_list[0],brand_list[1]))
        logging.info("onclick of brand submit button")
        selected_brand = request.POST.getlist('brand[]')
        print(selected_brand)
        brand_url = brand_dict[selected_brand[0]]
        
        with open("ScrapingTool/files/series.txt", "w") as file:
            file.write(brand_url)
        
        mobile_list = pagination_for_mobile_brand_list(brand_url)
        mobile_dict = dict(zip(mobile_list[0],mobile_list[1]))
        print(mobile_list)

    #On click of social_media_button
    if request.POST.get('social_media_button'):
        logging.info("onclick of social media submit button")
        print("Social media button clicked")

        file_read = fileReaderWriter()
        file = open("ScrapingTool/files/Series.txt", "r")
        brand_url = file_read.read_links_from_text_file(file)
        mobile_list = pagination_for_mobile_brand_list(brand_url)
        mobile_dict = dict(zip(mobile_list[0],mobile_list[1]))
        print("======================mobile dict============",mobile_dict)
        print(mobile_list)
        
        file_read = fileReaderWriter()
        file = open("ScrapingTool/files/mainurl.txt", "r")
        main_url = file_read.read_links_from_text_file(file)

        todate = request.POST.get('todate')
        fromdate = request.POST.get('fromdate')

        if not fromdate and not todate and not request.POST.get("alldates") == "on":
            error_message="Error: Please select the date"
            logging.error("displaying an error message if the user forgotten to select the date  : %s", error_message)

        else:
            if not fromdate and not request.POST.get("alldates") == "on":
                error_message = "Error: Please select the from date before submit"
                logging.error("displaying an error message if the user forgotten to select the From date  : %s",
                                  error_message)
            elif not todate and not request.POST.get("alldates") == "on":
                error_message = "Error: Please select the To date before submit"
                logging.error("displaying an error message if user forgotten to select the To date  : %s",
                                  error_message)
            else:
                #Fetch products selected by user-checklist
                checklist = request.POST.getlist('product[]')
                logging.debug("User selected product list : %s", checklist)

                if checklist:
                        if fromdate and todate:
                            if fromdate <= todate:
                                list_of_dates = dateListFunction(fromdate, todate)
                                #list_of_dates = ['02/18/2019', '02/21/2019']
                                # Fetching all the links of product pages by calling method issueLinksPagination() for selected product
                                selected_model_url = []
                                for model in checklist:
                                    selected_model_url.append(main_url + "/" + mobile_dict[model])
                                data_dictionary = main_method(selected_model_url, checklist,list_of_dates)

                                if data_dictionary:
                                    successmsg = "Data extracted successfully, Click download to get data in excel"
                                    logging.info(
                                        "displaying an success message after scraping data from website : %s",
                                        successmsg)
                                else:
                                    info_msg = "Info:No data for selected date"
                                    logging.warning("there is no data for selected product with selected date %s",
                                                    info_msg)
                            else:
                                error_message = "Error:From date should be less than or equal to To date"
                                logging.error(
                                    "displaying an error message if user selected - to date<from date  : %s",
                                    error_message)
                        elif request.POST.get("alldates") == "on":
                            print("on")
                            list_of_dates = []
                            selected_model_url = []

                            for model in checklist:
                                selected_model_url.append(main_url + "/" + mobile_dict[model])
                            main_method(selected_model_url, checklist,list_of_dates)

                            successmsg = "Data extracted successfully, Click download to get data in excel"
                            logging.info(
                                "displaying an success message after scraping data from website : %s",
                                successmsg)
                        else:
                            error_message = "Error: Please select the date before submit"
                            logging.error(
                                "displaying an error message to select date  : %s",
                                error_message)
                #Else if product not selected,displays error
                else:
                    error_message = "Error: Please select the product"
                    logging.error(
                            "displaying an error message to select product  : %s",
                            error_message)

    elif request.POST.get("douwnload_button"):
        file_name = 'ScrapingTool/files/FinalData.xlsx'  # this should live elsewhere, definitely
        with open(file_name, 'rb') as f:
            response = HttpResponse(f.read(),
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=' + file_name
            response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            return response

    return render(request, "socialmediascraping.html",
                  {"errorvalue": error_message, "productname": mobile_dict.keys, "successmsg": successmsg,
                       "infomsg": info_msg})        
                        

@csrf_exempt
def series_view(request):
    print("in series view")
    series_list = []
   
    if request.POST.get('back_button'):
        response = redirect('homepage')
        logging.info("redirecting series page to home page view")
        return response

    if request.POST.get('homepage_submit_btn'):
        main_url = request.POST.get('mainurl')
        status_code = fileReaderWriter.get_response_code(main_url)
        logging.debug("Status code : %s",status_code)

        #if valid url entered,write it in to url.txt file
        if status_code == 200:
            with open("ScrapingTool/files/mainurl.txt", "w") as file:
                file.write(main_url)
        #else if invalid url entered,displays error
        else:
            error_message = "Invalid URL "
            logging.error("handling an error message for status code : %s",error_message)
            return render(request, "homepage.html",
                          {"errorvalue": error_message})

    #Call get_dictionary_data() method to get series names
    series = getProductNamesAndLinks()
    series_dictionary =series.get_dictionary_data()
    if series_dictionary:
            for series_name in series_dictionary.keys():
                logging.debug("iterate series names : %s", series_name)
                series_list.append(series_name)
            
            return render(request, "series.html",
                      {"productseries": series_list})
    else:
        error_message = "Invalid URL"
        logging.error("handling an error message for empty series dictionary : %s", error_message)
        return render(request, "homepage.html",
                      {"errorvalue": error_message})


@csrf_exempt
def product_view(request):
    error_message = ""
    info_msg = ""
    successmsg = ""
    product_names_list = []

    get_issue_link_obj=getIssueLinks()

    if request.POST.get('back_button'):
        response = redirect('series/')
        logging.info("redirecting form social media view to series page view")
        return response

    file_read = fileReaderWriter()
    get_product_links = getProductNamesAndLinks()

    #On click of series button
    if request.POST.get('series_button'):
        logging.info("onclick of series button")
        series_list = request.POST.getlist('series[]')
        with open("ScrapingTool/files/series.txt", "w") as file:
            #Call get_dictionary_data() method to get series link for selected series name by user
            series=getProductNamesAndLinks()
            series_dictionary = series.get_dictionary_data()
            for series_name, series_links in series_dictionary.items():
                for list_of_series in series_list:
                    if list_of_series == series_name:
                        logging.debug("selected series link %s", series_links)
                        file.write(series_links)

    file = open("ScrapingTool/files/series.txt", "r")
    series_url = file_read.read_links_from_text_file(file)
    print(series_url)
    product_data_dictionary = get_product_links.get_links_for_products(series_url)

    #fetching product name to be displayed on webpage
    if product_data_dictionary:
        for product_names in product_data_dictionary.keys():
            logging.debug("scraping product names from website : %s",product_names)
            product_names_list.append(product_names)

        #On click of social_media_button
        if request.POST.get('social_media_button'):
            logging.info("onclick of social media submit button")

            product_links_list = []

            todate = request.POST.get('todate')
            fromdate = request.POST.get('fromdate')

            #Checking selection of dates
            #Checking if From ,To and All date is NOT selected
            if not fromdate and not todate and not request.POST.get("alldates") == "on":
                error_message="Error: Please select the date"
                logging.error("displaying an error message if the user forgotten to select the date  : %s", error_message)

            else:
                if not fromdate and not request.POST.get("alldates") == "on":
                    error_message = "Error: Please select the from date before submit"
                    logging.error("displaying an error message if the user forgotten to select the From date  : %s",
                                  error_message)
                elif not todate and not request.POST.get("alldates") == "on":
                    error_message = "Error: Please select the To date before submit"
                    logging.error("displaying an error message if user forgotten to select the To date  : %s",
                                  error_message)
                else:
                    #Fetch products selected by user-checklist
                    checklist = request.POST.getlist('product[]')
                    logging.debug("User selected product list : %s",checklist)

                    #Fetching product links for appropriate product name selected by user
                    for product_name, product_links in product_data_dictionary.items():
                        for checklist_product_name in checklist:
                            if checklist_product_name == product_name:
                                logging.debug("getting a selected product links %s: ", product_links)
                                product_links_list.append(product_links)
                    #If product selected and there is respective link for that enter  if condition
                    if product_links_list:
                        if fromdate and todate:
                            start_date, end_date = dateFormate(fromdate, todate)
                            if start_date <= end_date:
                                list_of_dates = dateListFunction(fromdate, todate)
                                print("++++++++++++++++++listdates",list_of_dates)
                                #Fetching all the links of product pages by calling method issueLinksPagination() for selected product
                                data_dictionary = get_issue_link_obj.issueLinksPagination(list_of_dates, product_links_list)
                                if data_dictionary:
                                    successmsg = "Data extracted successfully, Click download to get data in excel"
                                    logging.info(
                                        "displaying an success message after scraping data from website : %s",
                                        successmsg)
                                else:
                                    info_msg = "Info:No data for selected date"
                                    logging.warning("there is no data for selected product with selected date %s",info_msg)
                            else:
                                error_message = "Error:From date should be less than or equal to To date"
                                logging.error(
                                    "displaying an error message if user selected - to date<from date  : %s",
                                    error_message)

                        elif request.POST.get("alldates") == "on":
                            print("on")
                            list_of_dates = []
                            get_issue_link_obj.issueLinksPagination(list_of_dates, product_links_list)
                            successmsg = "Data extracted successfully, Click download to get data in excel"
                            logging.info(
                                "displaying an success message after scraping data from website : %s",
                                successmsg)
                        else:
                            error_message = "Error: Please select the date before submit"
                            logging.error(
                                "displaying an error message to select date  : %s",
                                error_message)
                    #Else if product not selected,displays error
                    else:
                        error_message = "Error: Please select the product"
                        logging.error(
                            "displaying an error message to select product  : %s",
                            error_message)

        #On click of download button,to download Data excel sheet
        elif request.POST.get("douwnload_button"):
            file_name = 'ScrapingTool/files/FinalData.xlsx'  # this should live elsewhere, definitely
            with open(file_name, 'rb') as f:
                response = HttpResponse(f.read(),
                                        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=' + file_name
                response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                return response

        return render(request, "socialmediascraping.html",
                      {"productname": product_names_list, "errorvalue": error_message, "successmsg": successmsg,
                       "infomsg": info_msg})

    else:
        error_message = "Invalid URL"
        logging.error("handling an error message for empty product dictionary : %s", error_message)
        return render(request, "homepage.html",
                      {"errorvalue": error_message})






