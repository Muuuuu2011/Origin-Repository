from flask import *
import json
import mysql.connector
from mysql.connector import pooling
from mysql.connector import Error
import os
from dotenv import load_dotenv

history_api = Blueprint('history_api',__name__)

load_dotenv()
#資料庫參數設定
connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name = os.getenv('db_pool_name'),
        pool_size = int(os.getenv('db_pool_size')),
        host = os.getenv('db_host'),
        pool_reset_session=True,
        user = os.getenv('db_user'),
        password = os.getenv('db_password'),
        database = os.getenv('db_name')
)



@history_api.route("/api/history/<email>")
def getHistory(email):
    #取得使用者狀態
    check_user_status =  session.get('email')
    if check_user_status == None:
        return json.dumps({"error":True,"message":"未登入系統，拒絕存取"}),403
    

    mydb = connection_pool.get_connection()
    mycursor = mydb.cursor(buffered=True)

    mycursor.execute("SELECT * FROM orders_data WHERE email = %s",(email,))
    check_history = mycursor.fetchall()

    list1=[]
    for i in check_history:
        data_dic={
            "id":str(i[0]),
            "attrcationId":str(i[1]),
            "date":i[2],
            "time":i[3],
            "price":str(i[4]),
            "email":i[5],
            "name":i[6],
            "phone":i[7],
            "order_number":i[9],
            "image":str(i[12]).split(",")[0],
            "attraction_name":i[13],
            "address":i[14],
        }
        data_dic=data_dic.copy()
        list1.append(data_dic)
        if(len(list1)==0):
            result={
                "error":True,
                "message":"查無資料"
            }
            mydb.close()
            return json.dumps(result),500
    mydb.close()		
    return json.dumps({"ok":True,"data":list1}),200
    