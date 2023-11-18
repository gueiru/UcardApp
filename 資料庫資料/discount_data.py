import pymysql
import math
connection = pymysql.connect(
                            )
import pandas as pd
df = pd.read_excel("短期資料整理.xlsx",sheet_name="短期合檔")
#print(df)
#print(len(df))#總比數
for i in range(len(df)):
    if df["銀行別"][i]== 13:
            bank=("0"+str(df["銀行別"][i]))

            category=str(df["發卡商"][i])

            if len(str(df["號碼"][i]))==1:
                id="00"+ str(df["號碼"][i])
            elif len(str(df["號碼"][i]))==2:
                id="0"+ str(df["號碼"][i])
            else :  
                id=str(df["號碼"][i])
            
            back=float(df["金額"][i])

            title=str(df["標題"][i])

            start=str(df["開始"][i])

            
            end=str(df["結束"][i])

            condition=float(df["條件"][i])
            if math.isnan(condition ):
                 condition=None

            restriction=float(df["上限"][i])
            if math.isnan(restriction) :
                restriction=None

            store=str(df["店家"][i])


            note=str(df["備註"][i])
            if note=="nan":
                 note=None

            address=str(df["網址"][i])

            state=str(df["狀態"][i])

            #print("輸出",id,category,back,bank,title,start,end,condition,limit,store,note,address,state)
    #print("cond型態",type(condition))
    #print("cond值",type(condition))
    #print("lim",type(limit))
    #print("lim輸出",limit)


            try:
                cursor = connection.cursor()
                query = "INSERT INTO activity (bank_id,category,card_id,title,start,end,`back`,restriction,`condition`,store,note,address,state) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(query, (bank,category,id,title,start,end,back,restriction,condition,store,note,address,state))
                connection.commit()
                for i in cursor:
                    print(i)
            except pymysql.connect.Error as e:
                    print("Error: Could not make connecion to the MySQL database")
                    print(e)




        
    #print (bank,c,id,name,address)
