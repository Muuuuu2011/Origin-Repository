from typing import MutableMapping
from flask import *
import json
import mysql.connector
from mysql.connector import pooling
from mysql.connector import Error
import requests
import datetime
from flask_mail import Mail
from flask_mail import Message
from threading import Thread

orders_api = Blueprint('orders_api',__name__)

# mail = Mail(orders_api)


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

@orders_api.route("/api/orders",methods=["POST"])
def orders():
        #取得使用者狀態
        check_user_status =  session.get('email')
        if check_user_status == None:
            return json.dumps({"error":True,"message":"未登入系統，拒絕存取"}),403
        try:
            check_Orders=request.get_json()
            # print(check_Orders)
            #聯絡資料為空
            if check_Orders["order"]["contact"]["name"]=="" or check_Orders["order"]["contact"]["email"]=="" or check_Orders["order"]["contact"]["phone"]=="" :
                return json.dumps({"error":True,"message":"請輸入聯絡資料"}),400
            


            #發送請求給TayPay
            url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"

            data = {
                "prime": check_Orders["prime"],
                "partner_key": "partner_ViRs6zmvz6H4fdP2jy2MY8wiParGD8MqIpB4qaGzrEmXcp975aBrRIjZ",
                "merchant_id": "mycompany1102_TAISHIN",
                "details":"TapPay Test",
                "amount": check_Orders["order"]["price"],
                "cardholder": {
                    "phone_number":check_Orders["order"]["contact"]["phone"],
                    "name": check_Orders["order"]["contact"]["name"],
                    "email": check_Orders["order"]["contact"]["email"],
                    "zip_code": "100",
                    "address": "test",
                    "national_id": "test"
                },
                "remember": False
            }
            headers = {
                'content-type': 'application/json',
                'x-api-key': "partner_ViRs6zmvz6H4fdP2jy2MY8wiParGD8MqIpB4qaGzrEmXcp975aBrRIjZ"
            }
            response = requests.post(url,data=json.dumps(data),headers=headers)
            res = response.json()
            # print(res)

            #建立訂單
            mydb = connection_pool.get_connection()
            mycursor = mydb.cursor(buffered=True)

            #訂單編號生成
            time=str(datetime.date.today())
            time_1 = time.split("-")
            order_number= time_1[0]+ time_1[1]+ time_1[2]+str(check_Orders["order"]["trip"]["attraction"]["id"])+check_Orders["order"]["contact"]["phone"]
            

            mycursor.execute("SELECT * FROM orders_data WHERE order_number = %s",(order_number,))
            check_order_number = mycursor.fetchone()
            #確認訂單編號是否已存在
            if check_order_number == None: 

                sql = "INSERT INTO orders_data (attractionId,date,time,price,email,name,phone,payment_status,order_number,bank_transaction_id) VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s,%s)"
                val=(check_Orders["order"]["trip"]["attraction"]["id"],
                    check_Orders["order"]["trip"]["date"],
                    check_Orders["order"]["trip"]["time"],
                    check_Orders["order"]["price"],
                    check_Orders["order"]["contact"]["email"],
                    check_Orders["order"]["contact"]["name"],
                    check_Orders["order"]["contact"]["phone"],
                    "未付款",
                    order_number,
                    res["bank_transaction_id"])
                mycursor.execute(sql, val)
                mydb.commit()



            if res["status"]==0:
                mycursor.execute("UPDATE orders_data SET payment_status=(%s)  WHERE order_number =(%s)",("已付款",order_number,))
                mydb.commit()
                result={
                    "data": {
                        "number": order_number,
                        "payment": {
                            "status": "已付款",
                            "message": "付款成功"
                        }
                    }
                }
                mydb.close()
                return json.dumps(result),200
            else :
                result={
                    "data": {
                        "number": order_number,
                        "payment": {
                            "status": "未付款",
                            "message": "付款失敗"
                        }
                    }
                }
                mydb.close()
                return json.dumps(result),200
        except:
            return jsonify({"error":True,"message":"伺服器內部錯誤"}),500





@orders_api.route("/api/order/<orderNumber>")
def get_Order(orderNumber):
    #取得使用者狀態
    check_user_status =  session.get('email')
    if check_user_status == None:
        return json.dumps({"error":True,"message":"未登入系統，拒絕存取"}),403

    mydb = connection_pool.get_connection()
    mycursor = mydb.cursor(buffered=True)

    #查訂單資料
    mycursor.execute("SELECT * FROM orders_data WHERE order_number = %s",(orderNumber,))
    check_order_number = mycursor.fetchone()
    

    #查景點資料
    mycursor.execute("SELECT * FROM attractions_data  WHERE id = %s",(check_order_number[1],))
    check_attraction = mycursor.fetchone()
    


    if check_order_number != None:

        if check_order_number[8] == "已付款":
            status = 0
        else:
            status = 1    

        result={
            "data": {
                "number": check_order_number[9],
                "price": check_order_number[4],
                "trip": {
                "attraction": {
                    "id": check_order_number[1],
                    "name": check_attraction[1],
                    "address": check_attraction[4],
                    "image": check_attraction[9].split(",")[0]
                },
                "date": check_order_number[2],
                "time": check_order_number[3]
                },
                "contact": {
                "name": check_order_number[6],
                "email": check_order_number[5],
                "phone": check_order_number[7]
                },
                "status": status
            }
        }
        #print(result)
        # #郵寄
        # send_mail()

        mydb.close()
        return json.dumps(result),200
    
    else:
        result={
            "data":None
        }
        mydb.close()
        return json.dumps(result),200

    
    

    
