import sqlite3
import json

def CreateJson_File():
    DB = "./db.sqlite3"

    def get_all_users( json_str = False ):
        conn = sqlite3.connect( DB )
        conn.row_factory = sqlite3.Row # This enables column access by name: row['column_name'] 
        db = conn.cursor()

        rows = db.execute('''
        SELECT Category, sum(NrOfIssues) as NrOfIssues
        from Issues_Count_By_Keyword GROUP By Category
        ORDER BY sum(NrOfIssues) DESC''').fetchall()
        conn.commit()
        conn.close()

        if json_str:
            return json.dumps( [dict(ix) for ix in rows] ) #CREATE JSON
        return rows


    data = get_all_users( json_str = True )
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

CreateJson_File()
