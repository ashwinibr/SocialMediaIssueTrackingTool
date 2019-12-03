'''
FileReaderWriter class is to Read and write all data from excel
'''
import logging
import sqlite3
import pandas as pd
from ScrapingTool.Models.mongo_read_write import Update_Issue_Count_For_Key, Delete_Issue_Count, Get_Keywards_List, Write_to_DB
from ScrapingTool.Generic.constant import *

class fileReaderWriter:
#Writing all the details which is scaped from website in excel
    def write_data_using_pandas(self, request, data):
        try:
            #Load To Database
            Write_to_DB(data, EXPORTED_DATA_DATABASE_TABLE)
            Update_Issue_Count_For_Key(EXPORTED_DATA_DATABASE_TABLE,"Issues_Count_By_Keyword")

            # Load spreadsheet
            file_path = 'ScrapingTool/Generic/files/'
            file_name = "Request_ID-"+str(request.session.get('req_id'))+'_'+request.session.get('brand')+'.xlsx'            
            writer = pd.ExcelWriter(file_path+file_name)
            data_frame = pd.DataFrame.from_dict(data)
            data_frame.to_excel(writer, 'Sheet1', index=False)
            writer.save()
            logging.info("data is saved in excel")

        except IOError as e:
            logging.error('An error occurred when trying to write the file {0} : {1}.'.format(writer, str(e)))

