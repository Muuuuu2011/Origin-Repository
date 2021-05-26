from re import T
from routes.attractionId_api import attractionsId
from flask import *
import json
import mysql.connector
from mysql.connector import pooling
from routes.attractions_api import attractions_api 
from routes.attractionId_api import attractionId_api
from routes.user_api import user_api
from routes.booking_api import booking_api


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
mydb = connection_pool.get_connection()
mycursor = mydb.cursor(buffered=True)

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['SECRET_KEY'] = 'abc654_@123dda'
# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")


#APIs
#Attractions_api 顯示每12筆景點一頁的api:
app.register_blueprint(attractions_api)
#AttractionId_api 查詢指定ID的景點的api:
app.register_blueprint(attractionId_api)
#user_api 使用者相關API:註冊、檢查狀態、登入、登出
app.register_blueprint(user_api)
#booking_api預定行程API:取得未確認訂單、新預定、刪除目前預定
app.register_blueprint(booking_api)


app.run(port=3000)