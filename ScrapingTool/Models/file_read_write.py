'''
FileReaderWriter class is to Read and write all data from excel
'''
import logging
import sqlite3
import pandas as pd
from ScrapingTool.Models.sqlite3_read_write import Update_Issue_Count_For_Key, Delete_Issue_Count, Get_Keywards_List

class fileReaderWriter:
#Writing all the details which is scaped from website in excel
    def write_data_using_pandas(self, request, data):
        try:
            conn = sqlite3.connect("db.sqlite3")
            file_path = 'ScrapingTool/Generic/files/'
            file_name = "Request_ID-"+str(request.session.get('req_id'))+'_'+request.session.get('brand')+'.xlsx'
            writer = pd.ExcelWriter(file_path+file_name)
            data_frame = pd.DataFrame.from_dict(data)
            data_frame.to_sql("Exported_Data",conn, if_exists="append", index=False)
            data_frame.to_excel(writer, 'Sheet1', index=False)
            logging.info("data is saved in excel")

            data["Request_ID"]=str(request.session.get('req_id'))
            data_frame = pd.DataFrame.from_dict(data)
            data_frame.to_sql("Exported_Data",conn, if_exists="append", index=False)
            writer.save()
            conn.commit()

            data = Get_Keywards_List()
            Delete_Issue_Count()
            for keyward in data:
                Update_Issue_Count_For_Key(keyward)
            conn.commit()
            conn.close()

        except IOError as e:
            logging.error('An error occurred when trying to write the file {0} : {1}.'.format(writer, str(e)))

