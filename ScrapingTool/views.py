 # Create your views here.
import datetime
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import logging

from ScrapingTool.GoogleCharts.GoogleCharts import CreateChart
from ScrapingTool.consumer_product_scraping.forum_scraping import \
    get_brand_names, get_models_names, get_data_from_url
from ScrapingTool.file_read_write import fileReaderWriter
from ScrapingTool.logics.DateFormateClass import date_format_change, dateFormat
from ScrapingTool.sonyforum.get_issue_links import getIssueLinks
from ScrapingTool.sonyforum.product_name_and_links import getProductNamesAndLinks
from ScrapingTool.sqlite3_read_write import GetData_In_Dict, GetData_In_Tuple, \
    Get_Chart_Prod_List

logging.basicConfig(filename='error.log', level=logging.DEBUG)


@csrf_exempt
def homepage_view(request):
    """
    This function is to dispay URL dropdown which user can select required URL.
    :param request:
    :return: rendering homepage html to display user support view
    """
    homepage_template = loader.get_template('homepage.html')
    logging.info("<<<<<<<<< Rendering in to the Home Page View >>>>>>>>>>>")
    return HttpResponse(homepage_template.render())


@csrf_exempt
def brand_view(request):
    """
    This function is to display  mobile brand names for user selected URL.
    :param request:
    :return: Returning responce to the user
    """
    if request.POST.get('back_button'):
        logging.info("<<<<<<<<< BackButton clicked in Series page  >>>>>>>>>>>")
        response = redirect('homepage')
        logging.info("<<<<<<<<< Redirecting from Series Page to Home Page View >>>>>>>>>>>")
        return response

    if request.POST.get('home_button'):
        logging.info("<<<<<<<<< BackButton clicked in Series page  >>>>>>>>>>>")
        response = redirect('homepage')
        logging.info("<<<<<<<<< Redirecting from Series Page to Home Page View >>>>>>>>>>>")
        return response

    if request.POST.get('homepage_submit_btn'):
        logging.info("<<<<<<<<< Onclick of Submit button in homepage view >>>>>>>>>>>")
        main_url = request.POST.get('mainurl')
        logging.debug("Onclick of Submit button from Homepage View we are getting URL which is selcted from USER %s"
                      , main_url)
        status_code = fileReaderWriter.get_response_code(main_url)
        logging.debug("Status code : %s", status_code)

        if status_code == 200:
            with open("ScrapingTool/files/mainurl.txt", "w") as file:
                file.write(main_url)
        else:
            error_message = "Invalid URL"
            logging.error("handling an error message for status code : %s", error_message)
            return render(request, "homepage.html",
                          {"errorvalue": error_message})

    file_read = fileReaderWriter()
    file = open("ScrapingTool/files/mainurl.txt", "r")
    main_url = file_read.read_links_from_text_file(file)

    if main_url:
        brand_list = get_brand_names(main_url)
        logging.info("<<<<<<<List of Mobile Brand names >>>>>>> %s", brand_list[0])
        logging.info("Rendering to brandselection.html page to display brand names from user selcted URL")
        return render(request, "brandselection.html", {"brandlist": brand_list[0]})
    else:
        error_message = "Invalid URL"
        logging.error("Handling an error message for empty brand name : %s", error_message)
        return render(request, "homepage.html", {"errorvalue": error_message})


@csrf_exempt
def mobile_view(request):
    """
       This function is to display  mobile model names for user selected brands and to fetch the review comments from
       the user.
       :param request:
       :return: Returning responce to the user
       """

    error_message = ""
    info_msg = ""
    successmsg = ""
    now = datetime.datetime.now()
    mobile_list_display = []
    announced_year = []
    

    if request.POST.get('back_button'):
        print(request.session.get('session'))
        if(request.session.get('session')=='mobile-view'):
            response = redirect('brand/')
            logging.info("<<<<<<<<< BackButton clicked in mobile model name page to brand page view  >>>>>>>>>>>")
            return response
        else:
            filter_value = 'Latest Released'
            mobile_list = GetData_In_Tuple("Model_Names")
            announced_year = ['Latest Released']

            for year in mobile_list[0]:
                announced_year.append(year)

            if (filter_value) == 'Latest Released':
                yearlist = [str(now.year), str(now.year - 1), str(now.year - 2)]
            else:
                yearlist = [filter_value]

            if "All" in announced_year:
                mobile_list_display.extend(mobile_list[0]["All"])
            else:
                for year in yearlist:
                    mobile_list_display.extend(mobile_list[0][year])
            successmsg = "Data extracted successfully, Click download to get data in excel"
            request.session['session']='mobile-view' 
            return render(request, "socialmediascraping.html",
                    {"errorvalue": error_message, "productname": mobile_list_display, "successmsg": successmsg,
                    "infomsg": info_msg, 'announcedyear': announced_year})


    if request.POST.get('home_button'):
        logging.info("<<<<<<<<< BackButton clicked in Series page  >>>>>>>>>>>")
        response = redirect('homepage')
        logging.info("<<<<<<<<< Redirecting from Mobile Page to Home Page View >>>>>>>>>>>")
        return response

    if request.POST.get('brand_submit'):
        request.session['session']='mobile-view' 
        logging.info("<<<<<<<<< Onclick of Submit button in brandselection view >>>>>>>>>>>")
        brand_dict = GetData_In_Dict("Mobile_Brands")

        selected_brand = request.POST.getlist('brand[]')
        logging.info("<<<<<<<<< User selected Brand name >>>>>>>>>>>%s", selected_brand[0])
        brand_url = brand_dict[selected_brand[0]]

        with open("ScrapingTool/files/series.txt", "w") as file:
            file.write(brand_url)

        logging.info("<<<<<<<<< Get mobile names from User selected Brand name >>>>>>>>>>>")
        #Model list contains year and model name
        mobile_list = get_models_names(brand_url)

        # Getting year from the list
        for key in mobile_list[0].keys():
            announced_year.append(key)

        yearlist = [str(now.year), str(now.year - 1), str(now.year - 2)]

        if "All" in announced_year:
            mobile_list_display.extend(mobile_list[0]["All"])
        else:
            for year in yearlist:
                mobile_list_display.extend(mobile_list[0][year])

    if request.POST.get('updatelist'):
        logging.info("<<<<<<<<< Onclick of update list >>>>>>>>>>>")
        filter_value = request.POST.get('years')
        mobile_list = GetData_In_Tuple("Model_Names")
        announced_year = ['Latest Released']

        for year in mobile_list[0]:
            announced_year.append(year)

        if (filter_value) == 'Latest Released':
            yearlist = [str(now.year), str(now.year - 1), str(now.year - 2)]
        else:
            yearlist = [filter_value]

        if "All" in announced_year:
            mobile_list_display.extend(mobile_list[0]["All"])
        else:
            for year in yearlist:
                mobile_list_display.extend(mobile_list[0][year])

    if request.POST.get('dashboard_button'):
        ProdList = Get_Chart_Prod_List()
        request.session['session']='dashboard-view' 
        print(request.session.get('session'))
        return render(request, "dashboard.html", {"product_list": ProdList})

    if request.POST.get('social_media_button'):
        logging.info("onclick of social media submit button")
        mobile_list = GetData_In_Tuple("Model_Names")
        mobile_dict = mobile_list[1]

        announced_year = ['Latest Released']
        for key in mobile_list[0]:
            announced_year.append(key)

        yearlist = [str(now.year), str(now.year - 1), str(now.year - 2)]
        if "All" in announced_year:
            mobile_list_display.extend(mobile_list[0]["All"])
        else:
            for year in yearlist:
                mobile_list_display.extend(mobile_list[0][year])

        file_read = fileReaderWriter()
        file = open("ScrapingTool/files/mainurl.txt", "r")
        main_url = file_read.read_links_from_text_file(file)

        todate = request.POST.get('todate')
        fromdate = request.POST.get('fromdate')

        if not fromdate and not todate and not request.POST.get("alldates") == "on":
            error_message = "Error: Please select the date"
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
                # Fetch products selected by user-checklist
                selected_model_name = request.POST.getlist('product[]')
                logging.info("<<<<<<< User selected product list : %s >>>>>>>>>>>>>>", selected_model_name)

                if selected_model_name:
                    selected_model_url = []
                    for model in selected_model_name:
                        selected_model_url.append(main_url + "/" + mobile_dict[model][0])
                    if fromdate and todate:
                        if fromdate <= todate:
                            selected_dates = date_format_change(fromdate, todate)

                            data_information = get_data_from_url(main_url,selected_model_url,selected_dates)

                            if data_information:
                                successmsg = "Data extracted successfully, Click download to get data in excel"
                                ProdList = Get_Chart_Prod_List()
                                GChart = CreateChart(ProdList[0])
                                GChart.Create_Column_Chart(ProdList[0])
                                GChart.Create_Pie_Chart(ProdList[0])
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
                        selected_dates = []
                        data_information = get_data_from_url(main_url, selected_model_url, selected_dates)

                        if data_information:
                            successmsg = "Data extracted successfully, Click download to get data in excel"
                            ProdList = Get_Chart_Prod_List()
                            GChart = CreateChart(ProdList[0])
                            GChart.Create_Column_Chart(ProdList[0])
                            GChart.Create_Pie_Chart(ProdList[0])
                            logging.info(
                                "displaying an success message after scraping data from website ")
                        else:
                            info_msg = "Info:No data for selected date"
                            logging.warning("there is no data for selected product with selected date %s",
                                            info_msg)
                    else:
                        error_message = "Error: Please select the date before submit"
                        logging.error(
                            "displaying an error message to select date  : %s",
                            error_message)
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

    if request.POST.get("gen_graph"):
        SelProduct = request.POST.get("product")
        print('Product Selected for Graph ' + SelProduct)
        GChart = CreateChart(SelProduct)
        GChart.Create_Column_Chart(SelProduct)
        GChart.Create_Pie_Chart(SelProduct)
        ProdList = Get_Chart_Prod_List()
        return render(request, "dashboard.html", {"product_list": ProdList})

    return render(request, "socialmediascraping.html",
                  {"errorvalue": error_message, "productname": mobile_list_display, "successmsg": successmsg,
                   "infomsg": info_msg, 'announcedyear': announced_year})


@csrf_exempt
def series_view(request):
    print("in series view")
    series_list = []

    if request.POST.get('back_button'):
        response = redirect('homepage')
        logging.info("redirecting series page to home page view")
        return response

    if request.POST.get('home_button'):
        logging.info("<<<<<<<<< BackButton clicked in Series page  >>>>>>>>>>>")
        response = redirect('homepage')
        logging.info("<<<<<<<<< Redirecting from Series Page to Home Page View >>>>>>>>>>>")
        return response

    if request.POST.get('homepage_submit_btn'):
        main_url = request.POST.get('mainurl')
        print(main_url)
        status_code = fileReaderWriter.get_response_code(main_url)
        logging.debug("Status code : %s", status_code)

        # if valid url entered,write it in to url.txt file
        if status_code == 200:
            with open("ScrapingTool/files/mainurl.txt", "w") as file:
                file.write(main_url)
        # else if invalid url entered,displays error
        else:
            error_message = "Unable to Connect to URL"
            logging.error("handling an error message for status code : %s", error_message)
            return render(request, "homepage.html",
                          {"errorvalue": error_message})

    # Call get_dictionary_data() method to get series names
    series = getProductNamesAndLinks()
    series_dictionary = series.get_dictionary_data()
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

    get_issue_link_obj = getIssueLinks()

    if request.POST.get('back_button'):
        response = redirect('series/')
        logging.info("redirecting form social media view to series page view")
        return response

    if request.POST.get('home_button'):
        logging.info("<<<<<<<<< BackButton clicked in Series page  >>>>>>>>>>>")
        response = redirect('homepage')
        logging.info("<<<<<<<<< Redirecting from Product Page to Home Page View >>>>>>>>>>>")
        return response

    if request.POST.get('dashboard_button'):
        ProdList = Get_Chart_Prod_List()
        return render(request, "dashboard.html", {"product_list": ProdList})

    if request.POST.get("gen_graph"):
        SelProduct = request.POST.get("product")
        print('Product Selected for Graph ' + SelProduct)
        GChart = CreateChart(SelProduct)
        GChart.Create_Column_Chart(SelProduct)
        GChart.Create_Pie_Chart(SelProduct)
        ProdList = Get_Chart_Prod_List()
        return render(request, "dashboard.html", {"product_list": ProdList})

    file_read = fileReaderWriter()
    get_product_links = getProductNamesAndLinks()

    # On click of series button
    if request.POST.get('series_button'):
        logging.info("onclick of series button")
        series_list = request.POST.getlist('series[]')
        with open("ScrapingTool/files/series.txt", "w") as file:
            # Call get_dictionary_data() method to get series link for selected series name by user
            series = getProductNamesAndLinks()
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

    # fetching product name to be displayed on webpage
    if product_data_dictionary:
        for product_names in product_data_dictionary.keys():
            logging.debug("scraping product names from website : %s", product_names)
            product_names_list.append(product_names)

        # On click of social_media_button
        if request.POST.get('social_media_button'):
            logging.info("onclick of social media submit button")

            product_links_list = []

            todate = request.POST.get('todate')
            fromdate = request.POST.get('fromdate')

            # Checking selection of dates
            # Checking if From ,To and All date is NOT selected
            if not fromdate and not todate and not request.POST.get("alldates") == "on":
                error_message = "Error: Please select the date"
                logging.error("displaying an error message if the user forgotten to select the date  : %s",
                              error_message)

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
                    # Fetch products selected by user-checklist
                    checklist = request.POST.getlist('product[]')
                    logging.debug("User selected product list : %s", checklist)

                    # Fetching product links for appropriate product name selected by user
                    for product_name, product_links in product_data_dictionary.items():
                        for checklist_product_name in checklist:
                            if checklist_product_name == product_name:
                                logging.debug("getting a selected product links %s: ", product_links)
                                product_links_list.append(product_links)
                    # If product selected and there is respective link for that enter  if condition
                    if product_links_list:
                        if fromdate and todate:
                            start_date, end_date = dateFormat(fromdate, todate)
                            if start_date <= end_date:
                                list_of_dates = date_format_change(fromdate, todate)
                                print("++++++++++++++++++listdates", list_of_dates)
                                # Fetching all the links of product pages by calling method issueLinksPagination() for selected product
                                data_dictionary = get_issue_link_obj.issueLinksPagination(list_of_dates,
                                                                                          product_links_list)

                                print(data_dictionary)

                                if data_dictionary:
                                    successmsg = "Data extracted successfully, Click download to get data in excel"
                                    ProdList = Get_Chart_Prod_List()
                                    GChart = CreateChart(ProdList[0])
                                    GChart.Create_Column_Chart(ProdList[0])
                                    GChart.Create_Pie_Chart(ProdList[0])
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
                            get_issue_link_obj.issueLinksPagination(list_of_dates, product_links_list)
                            successmsg = "Data extracted successfully, Click download to get data in excel"
                            ProdList = Get_Chart_Prod_List()
                            GChart = CreateChart(ProdList[0])
                            GChart.Create_Column_Chart(ProdList[0])
                            GChart.Create_Pie_Chart(ProdList[0])
                            logging.info(
                                "displaying an success message after scraping data from website : %s",
                                successmsg)
                        else:
                            error_message = "Error: Please select the date before submit"
                            logging.error(
                                "displaying an error message to select date  : %s",
                                error_message)
                    # Else if product not selected,displays error
                    else:
                        error_message = "Error: Please select the product"
                        logging.error(
                            "displaying an error message to select product  : %s",
                            error_message)

        # On click of download button,to download Data excel sheet
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






