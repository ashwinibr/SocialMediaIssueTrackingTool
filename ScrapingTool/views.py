 # Create your views here.
import datetime
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import logging

from ScrapingTool.Generic.connection_status_code import get_response_code
from ScrapingTool.Generic.constant import MODEL_NAME_DATABASE_TABLE, MOBILE_BRANDS_DATABASE_TABLE
from ScrapingTool.GoogleCharts.GoogleCharts import CreateChart
from ScrapingTool.controller.main_scraper_module import \
    get_brand_names, get_models_names, get_data_from_url
from ScrapingTool.Generic.DateFormateClass import date_format_change, dateFormat
from ScrapingTool.Models.sqlite3_read_write import GetData_In_Dict, GetData_In_Tuple, \
    Get_Chart_Prod_List, Get_RequestID, Check_Existing_Data

logging.basicConfig(filename='error.log', level=logging.DEBUG)


@csrf_exempt
def homepage_view(request):
    """
    This function is to dispay URL dropdown which user can select required URL.
    :param request:
    :return: rendering homepage html to display user support view
    """
    #homepage_template = loader.get_template('homepage.html')
    logging.info("<<<<<<<<< Rendering in to the Home Page View >>>>>>>>>>>")
    #return HttpResponse(homepage_template.render())
    return render(request,'homepage.html')

@csrf_exempt
def brand_view(request):
    """
    This function is to display  mobile brand names for user selected URL.
    :param request:
    :return: Returning responce to the user
    """
    if request.POST.get('back_button'):
        logging.info("<<<<<<<<< BackButton clicked in brand page  >>>>>>>>>>>")
        response = redirect('home')
        logging.info("<<<<<<<<< Redirecting from Brand Page to Home Page View >>>>>>>>>>>")
        return response

    if request.POST.get('home_button'):
        logging.info("<<<<<<<<< BackButton clicked in Brand page  >>>>>>>>>>>")
        response = redirect('home')
        logging.info("<<<<<<<<< Redirecting from Brand Page to Home Page View >>>>>>>>>>>")
        return response

    if request.POST.get('homepage_submit_btn'):
        logging.info("<<<<<<<<< Submit button clicked in homepage view >>>>>>>>>>>")
        main_url = request.POST.get('mainurl')
        print("main_url", main_url)
        logging.debug("<<<<<< Connecting to user selected URL : %s >>>>>>>>"
                      , main_url)
        status_code = get_response_code(main_url)
        logging.debug("Connection status code : %s", status_code)

        if status_code == 200:
            request.session['mainurl'] = main_url
        else:
            logging.debug("Connection status code : %s", status_code)
            error_message = "Unable to connect to URL"
            logging.error("handling an error message for status code : %s", error_message)
            messages.error(request,error_message)
            return redirect('home')

    main_url = str(request.session.get('mainurl'))
    from_url = str(request.POST.get('from-url'))
    print("main url", main_url)
    print("from url", from_url)
    if main_url:
        if(from_url=='on'):
            brand_list = get_brand_names(request)
        else:
            brand_list = Check_Existing_Data(main_url)
            if(len(brand_list)==0):
                brand_list = get_brand_names(request)

        logging.info("<<<<<<< Received List of Mobile Brand Names >>>>>>> %s", brand_list[0])
        logging.info("Rendering to brandselection.html page to display brand names from user selcted URL")
        return render(request, "brandselection.html", {"brandlist": brand_list[0]})
    else:
        error_message = "Unable to Connect to URL"
        logging.error("handling an error message for empty brand name : %s", error_message)
        messages.error(request,'Unable to connect to URL')
        return redirect('home')


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
        logging.info("Session ID: %s", request.session.get('cur_view'))
        if(request.session.get('cur_view')=='mobile-view'):
            response = redirect('brand/')
            logging.info("<<<<<<<<< BackButton clicked in Mobile page >>>>>>>>>>>")
            logging.info("<<<<<<<<< Redirecting from Mobile Page to Home Page View >>>>>>>>>>>")
            return response
        else:
            filter_value = 'Latest Released'
            main_url = str(request.session.get('mainurl'))
            from_url = str(request.POST.get('from-url'))
            mobile_list = GetData_In_Tuple(MODEL_NAME_DATABASE_TABLE,main_url, request.session.get('selected_brand'))
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
            request.session['cur_view']='mobile-view' 
            return render(request, "product.html",
                    {"errorvalue": error_message, "productname": mobile_list_display, "successmsg": successmsg,
                    "infomsg": info_msg, 'announcedyear': announced_year})


    if request.POST.get('home_button'):
        logging.info("<<<<<<<<< HomeButton clicked in Mobile Page  >>>>>>>>>>>")
        response = redirect('home')
        logging.info("<<<<<<<<< Redirecting from Mobile Page to Home Page View >>>>>>>>>>>")
        return response

    if request.POST.get('brand_submit'):
        request.session['cur_view']='mobile-view' 
        logging.info("<<<<<<<<< Submit button clicked in brandselection view >>>>>>>>>>>")
        main_url = str(request.session.get('mainurl'))
        brand_dict = GetData_In_Dict(MOBILE_BRANDS_DATABASE_TABLE, main_url)
        print(brand_dict)
        selected_brand = request.POST.getlist('brand[]')
        request.session['selected_brand'] = request.POST.getlist('brand[]')
        logging.info("<<<<<<<<< User selected Brand name >>>>>>>>>>>%s", selected_brand[0])
        brand_url = brand_dict[selected_brand[0]]
        request.session['brand']= selected_brand[0]
        logging.info("<<<<<<<<< Getting mobile names from user selected Brand name >>>>>>>>>>>")
        #Model list contains year and model name

        main_url = str(request.session.get('mainurl'))
        from_url = str(request.POST.get('from-url'))
        check_data_in_DB = GetData_In_Tuple(MODEL_NAME_DATABASE_TABLE,main_url, request.session.get('selected_brand'))
        if(from_url=='on'):
            mobile_list = get_models_names(request,brand_url)
        elif(len(check_data_in_DB[1])<=2):
            mobile_list = get_models_names(request,brand_url)
        else:
            mobile_list = GetData_In_Tuple(MODEL_NAME_DATABASE_TABLE,main_url, request.session.get('selected_brand'))


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
        logging.info("<<<<<<<<< update list button clicked >>>>>>>>>>>")
        filter_value = request.POST.get('years')
        main_url = str(request.session.get('mainurl'))
        from_url = str(request.POST.get('from-url'))
        selected_brand = request.POST.getlist('brand[]')

        mobile_list = GetData_In_Tuple(MODEL_NAME_DATABASE_TABLE,main_url, request.session.get('selected_brand'))
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
        logging.info("<<<<<<<<< dashboard button clicked >>>>>>>>>>>")
        ProdList = Get_Chart_Prod_List()
        request.session['cur_view']='dashboard-view' 
        logging.info("Current View: %s", request.session.get('cur_view'))
        return render(request, "dashboard.html", {"product_list": ProdList})

    if request.POST.get('product_submit_button'):
        logging.info("social media submit button clicked")
        main_url = str(request.session.get('mainurl'))
        from_url = str(request.POST.get('from-url'))
        mobile_list = GetData_In_Tuple(MODEL_NAME_DATABASE_TABLE,main_url, request.session.get('selected_brand'))
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

        main_url = str(request.session.get('mainurl'))

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
                sel_brand = str(request.session.get('brand'))

                req_id = Get_RequestID(main_url, sel_brand, selected_model_name, fromdate, todate)
                request.session['req_id'] = req_id
                if selected_model_name:
                    selected_model_url = []
                    for model in selected_model_name:
                        print("selected product url")
                        print(mobile_dict[model][0])
                        if "gadgets.ndtv" in main_url:
                            selected_model_url.append(mobile_dict[model][0])
                        else:
                            selected_model_url.append(main_url + "/" + mobile_dict[model][0])
                    if fromdate and todate:
                        if fromdate <= todate:
                            selected_dates = date_format_change(fromdate, todate)

                            data_information = get_data_from_url(request,main_url,selected_model_url,selected_dates)

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
                        selected_dates = []
                        data_information = get_data_from_url(request,main_url, selected_model_url, selected_dates)

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
        file_path = 'ScrapingTool/Generic/files/'
        file_name = "Request_ID-"+str(request.session.get('req_id'))+'_'+request.session.get('brand')+'.xlsx'
        with open(file_path+file_name, 'rb') as f:
            response = HttpResponse(f.read(),
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=' + file_name
            response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            return response

    if request.POST.get("gen_graph"):
        SelProduct = request.POST.get("product")
        logging.debug('Product Selected for Graph : %s', SelProduct)
        GChart = CreateChart(SelProduct)
        GChart.Create_Column_Chart(SelProduct)
        GChart.Create_Pie_Chart(SelProduct)
        ProdList = Get_Chart_Prod_List()
        return render(request, "dashboard.html", {"product_list": ProdList})

    return render(request, "product.html",
                  {"errorvalue": error_message, "productname": mobile_list_display, "successmsg": successmsg,
                   "infomsg": info_msg, 'announcedyear': announced_year})



