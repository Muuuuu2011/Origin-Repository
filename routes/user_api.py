from flask import *
import json
import mysql.connector
from mysql.connector import pooling
import time
from mysql.connector import Error

user_api = Blueprint('user_api',__name__)

# 資料庫參數設定
connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name = 'MySQLPool',
        pool_size = 5,
        pool_reset_session=True,
        host = "localhost",
        user = "admin",
        password = "1234",
        database = "website"
)




@user_api.route("/api/user",methods=["GET", "POST", "DELETE", "PATCH"])
def user():
    try:
        mydb = connection_pool.get_connection()
        mycursor = mydb.cursor(buffered=True)
        #sign up 註冊使用者
        if request.method=="POST":
            check_User=request.get_json()#調整格式

            if check_User["name"]==""or check_User["email"]=="" or check_User["password"]=="":
                return json.dumps({"error":True,"message":"註冊失敗，請輸入資料"}),400
            
            else:
                mycursor.execute("SELECT * FROM user_data WHERE email =(%s)",(check_User["email"],))
                check_email = mycursor.fetchone()
                if check_email == None:
                    sql = "INSERT INTO user_data (name,email,password) VALUES (%s, %s, %s)"
                    val=(check_User["name"],check_User["email"],check_User["password"])
                    mycursor.execute(sql, val)
                    mydb.commit()
                    mydb.close()
                    return json.dumps({"ok":True,}),200

                else:
                    return json.dumps({"error":True,"message":"註冊失敗，重複的 Email 或其他原因"}),400
        

        #sign in 使用者登入:
        elif request.method=="PATCH":
            check_User=request.get_json()
            
            if check_User["email"] == "" or check_User["password"] == "":
                return json.dumps({"error":True,"message":"登入失敗，請輸入帳號密碼"}),400
            
            else:
                #要知道是帳號或是密碼錯誤，所以分開來搜尋資料庫:
                mycursor.execute("SELECT * FROM user_data WHERE email =(%s)",(check_User["email"],))
                check_email = mycursor.fetchone()
                mycursor.execute("SELECT * FROM user_data WHERE password =(%s)",(check_User["password"],))
                check_password = mycursor.fetchone()
                #帳號錯誤
                if check_email == None:
                    mydb.close()
                    return json.dumps({"error":True,"message":"登入失敗，帳號錯誤"}),400
                #密碼錯誤
                elif check_password ==None:
                    mydb.close()
                    return json.dumps({"error":True,"message":"登入失敗，密碼錯誤"}),400
                #正確無誤，成功登入 設定cookies https://www.maxlist.xyz/2019/05/11/flask-cookie/
                else:
                    session["email"]=check_User["email"]
                    mydb.close()
                    return json.dumps({"ok":True}),200

        #sign out 使用者登出 刪除cookies https://www.maxlist.xyz/2019/05/11/flask-cookie/
        elif request.method=="DELETE":
            session.clear()
            return json.dumps({"ok":True}),200

        #check user status 檢查登入狀態 取得cookies https://www.maxlist.xyz/2019/05/11/flask-cookie/
        elif request.method=="GET":
            check_user_status =  session.get('email')
            if check_user_status !=None:
                mycursor.execute("SELECT * FROM user_data WHERE email = %s",(check_user_status,))
                check_status = mycursor.fetchone()
                check_result={
                    "data":{
                        "id":check_status[0],
                        "name":check_status[1],
                        "email":check_status[2]
                    }
                }
                mydb.close()
                return json.dumps(check_result),200

            else:
                check_result={
                    "data":None
                }
                mydb.close()
                return json.dumps(check_result),200
    
    except:
        return json.dumps({"error":True,"message":"伺服器內部錯誤"}),500

