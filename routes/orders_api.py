# from typing import MutableMapping
from flask import *
from main import app,mail
import json
import mysql.connector
# from mysql.connector import pooling
# from mysql.connector import Error
import requests
import datetime
# from flask_mail import Mail
from flask_mail import Message
from threading import Thread
import os
from dotenv import load_dotenv
import re

orders_api = Blueprint('orders_api',__name__)

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

@app.route("/api/orders",methods=["POST"])
def orders():
        #取得使用者狀態
        check_user_status =  session.get('email')
        if check_user_status == None:
            return json.dumps({"error":True,"message":"未登入系統，拒絕存取"}),403
        # try:
        check_Orders=request.get_json()
        #檢查信箱格式用
        p = re.compile(r"[^@]+@[^@]+\.[^@]+")
        # print(len(check_Orders["order"]["contact"]["phone"]),re.match(r'09', check_Orders["order"]["contact"]["phone"])!=None)
        # print(check_Orders)
        #聯絡資料為空
        if check_Orders["order"]["contact"]["name"]=="" or check_Orders["order"]["contact"]["email"]=="" or check_Orders["order"]["contact"]["phone"]=="":
            return json.dumps({"error":True,"message":"請輸入聯絡資料"}),400
        
        elif not p.match(check_Orders["order"]["contact"]["email"]):
            return json.dumps({"error":True,"message":"信箱格式不正確"}),400

        elif len(check_Orders["order"]["contact"]["phone"])!= 10 or re.match(r'09', check_Orders["order"]["contact"]["phone"])==None:
            return json.dumps({"error":True,"message":"手機號碼不正確"}),400

        #發送請求給TayPay
        url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"

        data = {
            "prime": check_Orders["prime"],
            "partner_key": os.getenv('key'),
            "merchant_id": os.getenv('id'),
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
            'x-api-key': os.getenv('key')
        }
        response = requests.post(url,data=json.dumps(data),headers=headers)
        res = response.json()
        # print(res)

        #建立訂單
        mydb = connection_pool.get_connection()
        mycursor = mydb.cursor(buffered=True)

        #訂單編號生成
        time=str(datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'))
        order_number= "ODT"+time
        

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

        #查景點資料
        mycursor.execute("SELECT * FROM attractions_data  WHERE id = %s",(check_Orders["order"]["trip"]["attraction"]["id"],))
        check_attraction = mycursor.fetchone()

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
            

            if check_Orders["order"]["trip"]["time"] == "morning":
                tour_time="早上9點到下午4點"
            else:
                tour_time="下午2點到晚上9點"

            send_mail(
                check_Orders,
                check_attraction,
                orderNumber=order_number,
                att_name=check_attraction[1],
                date= check_Orders["order"]["trip"]["date"],
                time=tour_time,
                price=check_Orders["order"]["price"],
                address=check_attraction[4],
                name=check_Orders["order"]["contact"]["name"],
                mail=check_Orders["order"]["contact"]["email"],
                phone=check_Orders["order"]["contact"]["phone"],
                )
            #移除預定行程的訂單
            mycursor.execute("DELETE FROM booking_data WHERE user_mail =(%s)",(check_user_status,))
            mydb.commit()

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
        # except:
        #     return jsonify({"error":True,"message":"伺服器內部錯誤"}),500





@app.route("/api/order/<orderNumber>")
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
    
    mycursor.execute("UPDATE orders_data SET image=(%s),attraction_name=(%s),address=(%s)  WHERE order_number =(%s)",(check_attraction[9],check_attraction[1],check_attraction[4],orderNumber,))
    mydb.commit()

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

        mydb.close()
        return json.dumps(result),200
    
    else:
        result={
            "data":None
        }
        mydb.close()
        return json.dumps(result),200
    
#郵件函式
def send_mail(check_Orders,check_attraction,**kwargs):
	msg = Message("感謝您預定台北一日遊:"+check_attraction[1], recipients=[ check_Orders["order"]["contact"]["email"]])
	template="sendmailtest"

	msg.html=render_template(template + '.html',**kwargs)
	thr = Thread(target=send_async_email, args=[app, msg])
	thr.start()
	return "OK"

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

