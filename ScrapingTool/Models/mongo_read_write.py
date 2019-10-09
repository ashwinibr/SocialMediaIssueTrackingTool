import pandas as pd
from collections import defaultdict
from pymongo import MongoClient
from datetime import datetime

#Create and Connect to MongoDB Database and Collections
def Connect_To_Mongodb():
    client = MongoClient('mongodb://localhost:27017')
    return client

def Create_Mongodb_Collection(collection_name):
    client = Connect_To_Mongodb()
    db = client['master_data']
    collection = db[collection_name]
    return collection

# Write Data To MongoDB Database and Collections
def Create_Request_ID():
    collection = Create_Mongodb_Collection('User_Requests')
    now = datetime.now()
    dt_string  = now.strftime(r"%d/%m/%Y %H:%M:%S")
    req_id = collection.find().count()+1
    mongo_data = {'RequestID':req_id, 'DateTime':dt_string}
    collection.insert_one(mongo_data)
    return req_id

def Write_to_DB(dictionary,table_name):
    collection = Create_Mongodb_Collection(table_name)
    d = dictionary
    k = list(d.keys())
    if(len(k)==2):
        converted_dict = [{k[0]: v1, k[1]: v2} 
                    for v1, v2 in zip(d[k[0]], d[k[1]])]
    elif(len(k)==3):
        converted_dict = [{k[0]: v1, k[1]: v2, k[2]: v3} 
                    for v1, v2, v3 in zip(d[k[0]], d[k[1]], d[k[2]])]
    elif(len(k)==4):
        converted_dict = [{k[0]: v1, k[1]: v2, k[2]: v3, k[3]: v4} 
                    for v1, v2, v3, v4 in zip(d[k[0]], d[k[1]], d[k[2]], d[k[3]])]
    elif(len(k)==5):
        converted_dict = [{k[0]: v1, k[1]: v2, k[2]: v3, k[3]: v4, k[4]: v5} 
                    for v1, v2, v3, v4, v5 in zip(d[k[0]], d[k[1]], d[k[2]], d[k[3]], d[k[4]])]
    elif(len(k)==6):
        converted_dict = [{k[0]: v1, k[1]: v2, k[2]: v3, k[3]: v4, k[4]: v5, k[5]: v6} 
                    for v1, v2, v3, v4, v5, v6 in zip(d[k[0]], d[k[1]], d[k[2]], d[k[3]], d[k[4]], d[k[5]])]
    elif(len(k)==7):
        converted_dict = [{k[0]: v1, k[1]: v2, k[2]: v3, k[3]: v4, k[4]: v5, k[5]: v6, k[6]: v7} 
                    for v1, v2, v3, v4, v5, v6, v7 in zip(d[k[0]], d[k[1]], d[k[2]], d[k[3]], d[k[4]], d[k[5]], d[k[6]])]
    elif(len(k)==8):
        converted_dict = [{k[0]: v1, k[1]: v2, k[2]: v3, k[3]: v4, k[4]: v5, k[5]: v6, k[6]: v7, k[7]: v8} 
                    for v1, v2, v3, v4, v5, v6, v7, v8 in zip(d[k[0]], d[k[1]], d[k[2]], d[k[3]], d[k[4]], d[k[5]], d[k[6]], d[k[7]])]
    else:
        converted_dict =[]

    document_nums = []
    if converted_dict:
        for mongo_data in converted_dict: 
            result = collection.insert_one(mongo_data)
            obj_id = "ObjectId({})".format("\""+str(result.inserted_id)+"\"")
            document_nums.append(obj_id)
    return document_nums

def Update_Issue_Count_For_Key(exported_data,new_table_name):
    collection = Create_Mongodb_Collection(exported_data)
    query = [{"$match" : {"Category": {'$regex': '.*'}}},{"$group" : {"_id": {"Date": "$Date","Product": "$Product", "Category" : "$Category"},"NrOfIssues": {"$sum": 1}}},{"$sort": {"NrOfIssues": -1}}]
    
    result = collection.aggregate(query)
    try:
        collection = Create_Mongodb_Collection(new_table_name)
        collection.insert(result)
    except:
        pass

# Read Data From MongoDB Database and Collections
def Get_Chart_Prod_List(table_name):
    collection = Create_Mongodb_Collection(table_name)

    result = collection.aggregate([{"$group" : {"_id": {"Product": "$Product"},"NrOfIssues": {"$sum": 1}}},{"$sort": {"NrOfIssues": -1}}])
    prod_list = []
    for r in result:
        prod_list.append(r['_id']['Product'])
    return prod_list

def Get_Chart_Data(table_name,group_by_column):
    collection = Create_Mongodb_Collection(table_name)

    result = collection.aggregate([{"$group" : {"_id": {str(group_by_column): "$"+str(group_by_column)},"NrOfIssues": {"$sum": 1}}},{"$sort": {"NrOfIssues": -1}}])
    result_list = []
    for r in result:
        temp_dict = r['_id']
        temp_dict['NrOfIssues'] = r['NrOfIssues'] 
        result_list.append(temp_dict)
    return result_list

def GetData_In_Dict(table_name):
    collection = Create_Mongodb_Collection(table_name)

    result = collection.find({})
    dictionary = {}
    for obj in result:
        dictionary[obj['Brand_Name']]=obj['Link']
    return dictionary

def GetData_In_Tuple(table_name):
    collection = Create_Mongodb_Collection(table_name)

    data_tuple=()
    mobile_model_year_list = []
    mobile_model_name_list = []
    mobile_model_links_list = []
    
    result = collection.find({})

    for obj in result:
        mobile_model_name_list.append(obj['Model_Name'])
        mobile_model_links_list.append(obj['Model_Link'])
        mobile_model_year_list.append(obj['Announced_Year'])


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

    data_tuple = (dic_year,dic_model_name)
    return data_tuple
