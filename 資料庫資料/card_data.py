import pymysql
connection = pymysql.connect(host='127.0.0.1',
                             user='*******',
                             password='******',
                             db='ucard',
                            )

import pandas as pd
df = pd.read_excel("資料庫資料整理V5.xlsx",sheet_name="卡片")
print(len(df))#總比數
for i in range(len(df)):
    if len(str(df["銀行"][i]))==2:
        bank=("0"+str(df["銀行"][i]))
    else:
        bank=str(df["銀行"][i])
    
    category=str(df["發行商"][i])
    
    if len(str(df["號碼"][i]))==1:
        id="00"+ str(df["號碼"][i])
    elif len(str(df["號碼"][i]))==2:
          id="0"+ str(df["號碼"][i])
    else :  
        id=str(df["號碼"][i])

    name=str(df["名稱"][i])
    address=str(df["網址"][i])
 


    try:
            cursor = connection.cursor()
            query = "INSERT INTO cards (`bank_id`,category,`card_id`,card_name,link) VALUES (%s,%s, %s, %s, %s)"
            cursor.execute(query, (bank,category,id,name,address))
            connection.commit()
            for i in cursor:
                print(i)
    except pymysql.connect.Error as e:
                print("Error: Could not make connecion to the MySQL database")
                print(e)
        
    #print (bank,c,id,name,address)
