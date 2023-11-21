import pymysql
connection = pymysql.connect(
                            )
import pandas as pd
df = pd.read_excel("資料庫資料整理V6.xlsx",sheet_name="長期")
print(len(df))#總比數
for i in range(len(df)):
            if len(str(df["銀行別"][i]))==2:
                bank=("0"+str(df["銀行別"][i]))
            else:
                bank=str(df["銀行別"][i])
            

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
            if note=="nan":
                 note=None

            auto=str(df["自動扣繳"][i])
            if auto=="nan":
                auto=0
            elif auto=="0":
                auto=0
            else:
                 auto=df["自動扣繳"][i]

            bill=str(df["電子帳單"][i])
            if bill=="nan":
                 bill=0
            elif bill=="0":
                 bill=0
            else:
                 bill=df["自動扣繳"][i]

            print(note)
            

            try:
                cursor = connection.cursor()
                query = "INSERT INTO basic (bank_id,category,card_id,feedback,kind,basic_remark,auto_debit,e_bill) VALUES (%s, %s, %s, %s, %s, %s,%s,%s)"
                cursor.execute(query, (bank,category,id,back,typee,note,auto,bill))
                connection.commit()
                for i in cursor:
                    print(i)
            except pymysql.connect.Error as e:
                    print("Error: Could not make connecion to the MySQL database")
                    print(e)


        