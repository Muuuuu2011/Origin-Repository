from flask import *
import json
import mysql.connector
from mysql.connector import pooling
from mysql.connector import Error

booking_api = Blueprint('booking_api',__name__)


#資料庫參數設定
connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name = 'MySQLPool',
        pool_size = 5,
        host = "localhost",
        pool_reset_session=True,
        user = "root",
        password = "Chickenbot2011_",
        database = "website"
)



@booking_api.route("/api/booking",methods=["GET", "POST", "DELETE"])
def booking():
    try:

        #取得使用者狀態
        check_user_status =  session.get('email')
        #建立預定行程
        if request.method=="POST":
            mydb = connection_pool.get_connection()
            mycursor = mydb.cursor(buffered=True)
            if check_user_status == None:
                return json.dumps({"error":True,"message":"未登入系統，拒絕存取"}),403
            elif check_user_status != None:
                check_booking=request.get_json()#調整格式
                mycursor.execute("SELECT * FROM booking_data WHERE user_mail =(%s)",(check_user_status,))
                check_booking_status = mycursor.fetchone()
                # print(check_booking_status)
                #如果查無資料，則建立新訂單
                if check_booking_status == None:
                    sql = "INSERT INTO booking_data (attractionId,date,time,price,user_mail) VALUES (%s, %s, %s,%s,%s)"
                    val=(check_booking["attractionId"],check_booking["date"],check_booking["time"],check_booking["price"],check_user_status)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    mydb.close()
                    return json.dumps({"ok":True,"message":"建立成功"}),200
                #如果有資料存在，則修改舊訂單
                elif check_booking_status != None:
                    mycursor.execute("UPDATE booking_data SET attractionId=(%s),date=(%s),time=(%s),price=(%s) WHERE user_mail =(%s)",(check_booking["attractionId"],check_booking["date"],check_booking["time"],check_booking["price"],check_user_status,))
                    mydb.commit()
                    mydb.close()
                    return json.dumps({"ok":True,"message":"建立成功"}),200
                else:
                    return json.dumps({"error":True,"message":"建立失敗，輸入不正確或其他原因"}),400
            else:
                return json.dumps({"error":True,"message":"建立失敗，輸入不正確或其他原因"}),400
        
        #刪除預定行程
        elif request.method=="DELETE":
            mydb = connection_pool.get_connection()
            mycursor = mydb.cursor(buffered=True)
            if check_user_status == None:
                return json.dumps({"error":True,"message":"未登入系統，拒絕存取"}),403
            else:
                mycursor.execute("DELETE FROM booking_data WHERE user_mail =(%s)",(check_user_status,))
                mydb.commit()
                mydb.close()
                return json.dumps({"ok":True,"message":"刪除成功"}),200

        #確認行程資料
        elif request.method=="GET":
            mydb = connection_pool.get_connection()
            mycursor = mydb.cursor(buffered=True)
            if check_user_status == None:
                return json.dumps({"error":True,"message":"未登入系統，拒絕存取"}),403
            else:
                mycursor.execute("SELECT * FROM booking_data WHERE user_mail =(%s)",(check_user_status,))
                check_booking_data = mycursor.fetchone()
                print(check_booking_data)
                if (check_booking_data==None):
                    booking_result={
                        "data":None
                    }
                    mydb.close()
                    return json.dumps(booking_result),200
                
                else:
                    mycursor.execute("SELECT * FROM booking_data WHERE user_mail =(%s)",(check_user_status,))
                    check_booking = mycursor.fetchone()
                    mycursor.execute("SELECT * FROM attractions_data WHERE id = %s",(check_booking[1],))
                    check_booking_data = mycursor.fetchone()
                    booking_result={
                        "data":{
                            "attraction":{
                                "id":check_booking_data[0],
                                "name":check_booking_data[1],
                                "address":check_booking_data[4],
                                "image":check_booking_data[9].split(",")
                            },
                            "date":check_booking[2],
                            "time":check_booking[3],
                            "price":check_booking[4]
                        }
                    }
                    mydb.close()
                    return json.dumps(booking_result),200
            

    except:
        return json.dumps({"error":True,"message":"伺服器內部錯誤"}),500
