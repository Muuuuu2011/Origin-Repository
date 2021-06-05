from flask import *
from main import app
from routes.attractions_api import attractions_api 
from routes.attractionId_api import attractionId_api
from routes.user_api import user_api
from routes.booking_api import booking_api
from routes.history_api import history_api
from routes.orders_api import orders_api
from routes.weather_api import weather_api



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
@app.route("/history")
def history():
	return render_template("history.html")


#APIs
#Attractions_api 顯示每12筆景點一頁的api:
app.register_blueprint(attractions_api)
#AttractionId_api 查詢指定ID的景點的api:
app.register_blueprint(attractionId_api)
#user_api 使用者相關API:註冊、檢查狀態、登入、登出
app.register_blueprint(user_api)
#booking_api預定行程API:取得未確認訂單、新預定、刪除目前預定
app.register_blueprint(booking_api)
#orders_api付款流程
app.register_blueprint(orders_api)
#history訂單記錄頁面
app.register_blueprint(history_api)
#天氣預報
app.register_blueprint(weather_api)






app.run(host="0.0.0.0",port=3000)