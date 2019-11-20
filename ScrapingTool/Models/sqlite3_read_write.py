import sqlite3
import pandas as pd
from collections import defaultdict

from ScrapingTool.Generic.constant import DATABASE_NAME, MOBILE_BRANDS_DATABASE_TABLE

def Write_to_DB(dictionary,table_name):
    conn = sqlite3.connect(DATABASE_NAME)
    data_frame = pd.DataFrame.from_dict(dictionary)
    data_frame.to_sql(table_name, conn, if_exists="append", index=False)
    with conn:
        cur = conn.cursor()
    sql_query ="""CREATE TABLE temp_table as SELECT DISTINCT * FROM {};""".format(table_name)
    cur.execute(sql_query)
    sql_query ="""DELETE FROM {};""".format(table_name)
    cur.execute(sql_query)
    sql_query ="""INSERT INTO {} SELECT * FROM temp_table;""".format(table_name)
    cur.execute(sql_query)
    sql_query ="""DROP TABLE temp_table;"""
    cur.execute(sql_query)
    conn.commit()
    conn.close()

def Get_Chart_Prod_List():
    conn = sqlite3.connect(DATABASE_NAME)
    with conn:
        cur = conn.cursor()
    
    sql_query = """SELECT Product FROM Issues_Count_By_Keyword GROUP by Product;"""  
    cur.execute(sql_query)
    result = cur.fetchall()
    prod_list = []
    for r in result:
        prod_list.append(r[0])
    return prod_list

def Get_RequestID(url, brand, models_list):
    conn = sqlite3.connect("db.sqlite3")
    with conn:
        cur = conn.cursor()

    models_list_str =""
    for model in models_list:
        if(models_list_str==""):
            models_list_str = model
        else:
            models_list_str = models_list_str+","+model   

    cur.execute("INSERT INTO Request_Data VALUES(NULL,?,?,?)",(url,brand,models_list_str))
    req_id = cur.lastrowid
    conn.commit()
    conn.close()
    return req_id

def Delete_Issue_Count():
    conn = sqlite3.connect(DATABASE_NAME)
    with conn:
        cur = conn.cursor()
    
    sql_query = """DELETE FROM Issues_Count_By_Keyword;"""  
    cur.execute(sql_query)
    conn.commit()
    conn.close()

def Update_Issue_Count_For_Key(key):
    conn = sqlite3.connect(DATABASE_NAME)
    with conn:
        cur = conn.cursor()
    
    sql_query = """SELECT Product, Date, count(Product) FROM Exported_Data WHERE Category like "%{}%" GROUP by Date,Product;""".format(key)  
    cur.execute(sql_query)
    result = cur.fetchall()
    issue_dict = {'Product':[],'Date':[],'Category':[],'NrOfIssues':[]}
    for r in result:
        issue_dict['Product'].append(r[0])
        issue_dict['Date'].append(r[1])
        issue_dict['Category'].append(key)        
        issue_dict['NrOfIssues'].append(r[2])

    data_frame = pd.DataFrame.from_dict(issue_dict)
    data_frame.to_sql('Issues_Count_By_Keyword', conn, if_exists="append", index=False)
    conn.commit()
    conn.close()


def Get_Keywards_List():
    conn = sqlite3.connect(DATABASE_NAME)
    with conn:
        cur = conn.cursor()
    
    sql_query = """SELECT Category FROM Issue_Keywords;"""
    cur.execute(sql_query)
    result = cur.fetchall()
    keywords = []
    for key in result:
        keywords.append(key[0])
    return keywords

def GetData_In_Dict(table_name, selected_url):
    conn = sqlite3.connect(DATABASE_NAME)
    with conn:
        cur = conn.cursor() 

    dictionary = {}
    query = 'SELECT * FROM {} WHERE URL="{}"'.format(table_name, selected_url)
    cur.execute(query)
    result = cur.fetchall()
    for URL, Brand_Name, Link in result:
        dictionary[Brand_Name] = Link
    conn.close()
    return dictionary

def Check_Existing_Data(selected_url):
    conn = sqlite3.connect(DATABASE_NAME)
    with conn:
        cur = conn.cursor() 

    dictionary = {}
    query = 'SELECT Brand_Name, Link FROM {} WHERE URL="{}"'.format(MOBILE_BRANDS_DATABASE_TABLE, selected_url)
    cur.execute(query)
    result = cur.fetchall()
    brand_list = []
    mobile_brand = []
    brand_url = []
    for r in result:
        mobile_brand.append(r[0])
        brand_url.append(r[1])
    if mobile_brand:
        brand_list = [mobile_brand, brand_url] 
    conn.close()
    return brand_list

def GetData_In_Tuple(table_name, selected_url, selected_brand):
    brand = selected_brand[0]
    conn = sqlite3.connect(DATABASE_NAME)
    with conn:
        cur = conn.cursor() 

    data_tuple=()
    mobile_model_year_list = []
    mobile_model_name_list = []
    mobile_model_links_list = []
    

    query = 'SELECT * FROM {} WHERE URL="{}" AND Brand_Name="{}"'.format(table_name, selected_url, brand)
    cur.execute(query)
    result = cur.fetchall()

    for URL, Brand_Name, Announced_Year, Model_Name, Model_Link in result:
        mobile_model_name_list.append(Model_Name)
        mobile_model_links_list.append(Model_Link)
        mobile_model_year_list.append(Announced_Year)


    dic_year = defaultdict(list)
    dic_model_name=defaultdict(list)

    i = 0
    for key in mobile_model_year_list:
        dic_year[key].append(mobile_model_name_list[i])
        i += 1

    j = 0
    for mobile_name_key in mobile_model_name_list:
        dic_model_name[mobile_name_key].append(mobile_model_links_list[j])
        j += 1

    conn.close()
    data_tuple = (dic_year,dic_model_name)
    return data_tuple
