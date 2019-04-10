import sqlite3
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
x = Get_Chart_Prod_List()
print(x)
