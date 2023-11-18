import pymysql
connection = pymysql.connect(
                            )
import pandas as pd
df = pd.read_excel("資料庫資料整理V2.xlsx",sheet_name="長期")
print(len(df))#總比數
for i in range(len(df)):
    if df["銀行別"][i]== 13:
            bank=("0"+str(df["銀行別"][i]))

            category=str(df["發行商"][i])

            if len(str(df["號碼"][i]))==1:
                id="00"+ str(df["號碼"][i])
            elif len(str(df["號碼"][i]))==2:
                id="0"+ str(df["號碼"][i])
            else :  
                id=str(df["號碼"][i])
            
            back=float(df["回饋"][i])

            typee=str(df["種類"][i])


            note=str(df["備註"][i])
            


            try:
                cursor = connection.cursor()
                query = "INSERT INTO basic (bank,category,id,back,kind,note) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(query, (bank,category,id,back,typee,note))
                connection.commit()
                for i in cursor:
                    print(i)
            except pymysql.connect.Error as e:
                    print("Error: Could not make connecion to the MySQL database")
                    print(e)


        

'''
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
    
'''

        
    #print (bank,c,id,name,address)
