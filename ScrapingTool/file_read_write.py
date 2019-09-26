'''
FileReaderWriter class is to Read and write all data from excel
'''
import logging
import urllib
import sqlite3
import pandas as pd
from pandas import ExcelWriter
from openpyxl.workbook import Workbook
#from ScrapingTool.sqlite3_read_write import Update_Issue_Count_For_Key, Delete_Issue_Count
import ScrapingTool.mongo_read_write as mongo

class fileReaderWriter:
    logging.basicConfig(level=logging.DEBUG)

#Writing all the details which is scaped from website in excel
    def write_data_using_pandas(self, req_id, data):
        try:
            writer = pd.ExcelWriter("ScrapingTool/files//FinalData.xlsx")

            # Load to MongoDB
            exported_data = 'Exported_Data' + req_id
            mongo.Write_to_DB(data,exported_data)

            # Load to spreadsheet 
            data_frame = pd.DataFrame.from_dict(data)
            data_frame.to_excel(writer, 'Sheet1', index=False)
            writer.save()
            logging.info("data is saved in excel")

            # # Load to SQL DB
            # conn = sqlite3.connect("db.sqlite3")
            # data_frame.to_sql("Exported_Data",conn, if_exists="replace", index=False)
            # conn.commit()

            # # Create Issues_Count_By_Keyword Table in SQL
            # excel_file = 'ScrapingTool/files/social_keywords.xlsx'
            # dataset = pd.read_excel(excel_file)
            # df = pd.DataFrame(dataset)
            # data = df.get("Category")
            # Delete_Issue_Count()
            # for keyward in data:
            #     Update_Issue_Count_For_Key(keyward)
            # conn.commit()
            # conn.close()

            # Create Issues_Count_By_Keyword Table in MongoDB
            new_table_name = 'Issues_Count_By_Keyword' + req_id
            mongo.Update_Issue_Count_For_Key(exported_data,new_table_name)

        except IOError as e:
            logging.error('An error occurred when trying to write the file {0} : {1}.'.format(writer, str(e)))


#Fetching data fron passed(argument) text file
    def read_links_from_text_file(self, file_name):
        for url in file_name:
           return url


    def get_response_code(url):
        try:
            conn = urllib.request.urlopen(url)
            return conn.getcode()
        except:
            logging.error("status code check")
            pass
