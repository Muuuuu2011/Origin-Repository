from flask import *
import json
import mysql.connector
from mysql.connector import pooling
from mysql.connector import Error

booking_api = Blueprint('booking_api',__name__)


# 資料庫參數設定
connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name = 'MySQLPool',
        pool_size = 5,
        host = "localhost",
        pool_reset_session=True,
        user = "admin",
        password = "1234",
        database = "website"
)




@booking_api.route("/api/booking",methods=["GET", "POST", "DELETE"])
def booking():
    try:
        mydb = connection_pool.get_connection()
        mycursor = mydb.cursor(buffered=True)
        #取得使用者狀態
        check_user_status =  session.get('email')
        #建立預定行程
        if request.method=="POST":
            if check_user_status == None:
                return json.dumps({"error":True,"message":"未登入系統，拒絕存取"}),403
            elif check_user_status != None:
                check_booking=request.get_json()#調整格式
                session["booking"]= check_booking
                if session["booking"]!=None:
                    print(session["booking"])
                    return json.dumps({"ok":True,"message":"建立成功"}),200
                else:
                    return json.dumps({"error":True,"message":"建立失敗，輸入不正確或其他原因"}),400
            else:
                return json.dumps({"error":True,"message":"建立失敗，輸入不正確或其他原因"}),400
        
        #刪除預定行程
        elif request.method=="DELETE":
            if check_user_status == None:
                return json.dumps({"error":True,"message":"未登入系統，拒絕存取"}),403
            else:
                session.pop("booking")
                return json.dumps({"ok":True,"message":"刪除成功"}),200

        #確認行程資料
        elif request.method=="GET":
            if check_user_status == None:
                return json.dumps({"error":True,"message":"未登入系統，拒絕存取"}),403
            else:
                if (session.get("booking")==None):
                    booking_result={
                        "data":None
                    }
                    return json.dumps(booking_result),200
                
                else:
                    mycursor.execute("SELECT * FROM attractions_data WHERE id = %s",(session["booking"]["attractionId"],))
                    check_booking_data = mycursor.fetchone()
                    booking_result={
                        "data":{
                            "attraction":{
                                "id":check_booking_data[0],
                                "name":check_booking_data[1],
                                "address":check_booking_data[4],
                                "image":check_booking_data[9].split(",")
                            },
                            "date":session["booking"]["date"],
                            "time":session["booking"]["time"],
                            "price":session["booking"]["price"]
                        }
                    }
                    mydb.close()
                    return json.dumps(booking_result),200
            

    except:
        return json.dumps({"error":True,"message":"伺服器內部錯誤"}),500
