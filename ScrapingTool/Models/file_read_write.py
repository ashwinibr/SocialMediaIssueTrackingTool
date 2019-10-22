'''
FileReaderWriter class is to Read and write all data from excel
'''
import logging
import sqlite3
import pandas as pd
from pandas import ExcelWriter
from openpyxl.workbook import Workbook
import ScrapingTool.Models.mongo_read_write as mongo
from ScrapingTool.Generic.constant import EXPORTED_DATA_DATABASE_TABLE, FILE_PATH, FILE_NAME, XLSX

class fileReaderWriter:
#Writing all the details which is scaped from website in excel
    def write_data_using_pandas(self, request, data):
        try:
            req_id = request.session.get('req_id')

            file_path = 'ScrapingTool/Generic/files/'
            file_name = "Request_ID-"+str(request.session.get('req_id'))+'_'+request.session.get('brand')+'.xlsx'

            exported_data = EXPORTED_DATA_DATABASE_TABLE + str(req_id)
            mongo.Write_to_DB(data,exported_data)

            writer = pd.ExcelWriter(file_path+file_name)
            # Load spreadsheet
            data_frame = pd.DataFrame.from_dict(data)
            data_frame.to_excel(writer, 'Sheet1', index=False)
            writer.save()
            logging.info("data is saved in excel")

            # Create Issues_Count_By_Keyword Table in MongoDB
            new_table_name = 'Issues_Count_By_Keyword' + str(req_id)
            mongo.Update_Issue_Count_For_Key(exported_data,new_table_name)

        except IOError as e:
            logging.error('An error occurred when trying to write the file {0} : {1}.'.format(writer, str(e)))

