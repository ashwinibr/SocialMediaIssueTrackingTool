import sqlite3
def run():
    conn = sqlite3.connect("db.sqlite3")
    with conn:
        cur = conn.cursor()
    
    key = 'Screen issue'
    insert_query = """SELECT Product, Date, count(Product) FROM Exported_Data WHERE Category like '%{}%' GROUP by Date,Product;""".format(key)  
    cur.execute(insert_query)
    result = cur.fetchall()
    issue_dict = {'Product':[],'Date':[],'Category':[],'NrOfIssues':[]}
    for r in result:
        issue_dict['Product'].append(r[0])
        issue_dict['Date'].append(r[1])
        issue_dict['Category'].append(key)        
        issue_dict['NrOfIssues'].append(r[2])
        
    return issue_dict


x = run()
print(x)
