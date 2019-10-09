'''
FileReaderWriter class is to Read and write all data from excel
'''
import logging
import urllib
import sqlite3
import pandas as pd
from pandas import ExcelWriter
from openpyxl.workbook import Workbook
import ScrapingTool.mongo_read_write as mongo

class fileReaderWriter:
    logging.basicConfig(level=logging.DEBUG)

#Writing all the details which is scaped from website in excel
    def write_data_using_pandas(self, req_id, data):
        try:
            writer = pd.ExcelWriter("ScrapingTool/Generic/files/FinalData.xlsx")

            # Load to MongoDB
            exported_data = 'Exported_Data' + req_id
            mongo.Write_to_DB(data,exported_data)

            # Load to spreadsheet 
            data_frame = pd.DataFrame.from_dict(data)
            data_frame.to_excel(writer, 'Sheet1', index=False)
            writer.save()
            logging.info("data is saved in excel")

            # Create Issues_Count_By_Keyword Table in MongoDB
            new_table_name = 'Issues_Count_By_Keyword' + req_id
            mongo.Update_Issue_Count_For_Key(exported_data,new_table_name)

        except IOError as e:
            logging.error('An error occurred when trying to write the file {0} : {1}.'.format(writer, str(e)))

