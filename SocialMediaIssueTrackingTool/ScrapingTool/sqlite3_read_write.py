import sqlite3
import pandas as pd
from collections import defaultdict

def Write_to_DB(dictionary,table_name):
    conn = sqlite3.connect("db.sqlite3")
    data_frame = pd.DataFrame.from_dict(dictionary)
    data_frame.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()

def Get_Chart_Prod_List():
    conn = sqlite3.connect("db.sqlite3")
    with conn:
        cur = conn.cursor()
    
    insert_query = """SELECT Product FROM Issues_Count_By_Keyword GROUP by Product;"""  
    cur.execute(insert_query)
    result = cur.fetchall()
    prod_list = []
    for r in result:
        prod_list.append(r[0])
    return prod_list

def Delete_Issue_Count():
    conn = sqlite3.connect("db.sqlite3")
    with conn:
        cur = conn.cursor()
    
    insert_query = """DELETE FROM Issues_Count_By_Keyword;"""  
    cur.execute(insert_query)
    conn.commit()
    conn.close()

def Update_Issue_Count_For_Key(key):
    conn = sqlite3.connect("db.sqlite3")
    with conn:
        cur = conn.cursor()
    
    insert_query = """SELECT Product, Date, count(Product) FROM Exported_Data WHERE Category like "%{}%" GROUP by Date,Product;""".format(key)  
    cur.execute(insert_query)
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


def GetData_In_Dict(table_name):
    conn = sqlite3.connect("db.sqlite3")
    with conn:
        cur = conn.cursor() 

    dictionary = {}
    query = 'SELECT * FROM {}'.format(table_name)
    cur.execute(query)
    result = cur.fetchall()
    for Brand_Name, Link in result:
        dictionary[Brand_Name] = Link
    conn.close()
    print(dictionary)
    return dictionary

def GetData_In_Tuple(table_name):
    conn = sqlite3.connect("db.sqlite3")
    with conn:
        cur = conn.cursor() 

    data_tuple=()
    mobile_model_year_list = []
    mobile_model_name_list = []
    mobile_model_links_list = []
    

    query = 'SELECT * FROM {}'.format(table_name)
    cur.execute(query)
    result = cur.fetchall()
    print(result)
    for Announced_Year, Model_Name, Model_Link in result:
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
