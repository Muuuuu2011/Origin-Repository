from flask import *
import json
import mysql.connector

# 資料庫參數設定
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Chickenbot2011_",
  database="website"
)

mycursor = mydb.cursor()

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

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

@app.route("/api/attractions")
def attractions():
	try:

		page = int(request.args.get("page"))
		keyword = request.args.get("keyword")


		if keyword!=None:#有輸入關鍵字
			pageNum=page*12
			mycursor.execute("SELECT * FROM attractions_data WHERE name LIKE %s limit 12 offset %s ",("%"+keyword+"%",pageNum,))#忘記看這邊 https://stackoverflow.com/questions/24072084/like-in-mysql-connector-python
			check_count = mycursor.fetchall()

			mycursor.execute("SELECT * FROM attractions_data WHERE name LIKE %s ",("%"+keyword+"%",))#忘記看這邊 https://stackoverflow.com/questions/24072084/like-in-mysql-connector-python
			check_name = mycursor.fetchall()

		
			count=len(check_name)//12
			if page<count:
				next_Page=page+1
			else:
				next_Page=None


			if(len(check_name)!=0):#但找得到輸入的關鍵字的資料
				list1=[]	
				for i in check_count:
					data_dic={
						"id":str(i[0]),
						"name":i[1],
						"category":i[2],
						"description":i[3],
						"address":i[4],
						"transport":i[5],
						"mrt":i[6],
						"latitude":str(i[7]),
						"longitude":str(i[8]),
						"images":
							i[9].split(",")
					}
					data_dic=data_dic.copy()
					list1.append(data_dic)
				if(len(list1)==0):
					result={
						"error":True,
						"message":"查無資料"
					}
					return json.dumps(result),500
				return json.dumps({"nextPage":next_Page,"data":list1}),200
			else:
				result={
					"error":True,
					"message":"查無資料"
				}
				return json.dumps(result),500 
				
		else:
			#沒有輸入關鍵字
			pageNum=page*12
			mycursor.execute("SELECT * FROM attractions_data limit 12 offset %s",(pageNum,))#limit每次只選出12筆，offset從%s開始算起，因為要每12筆，所以當page輸入1則pageNum=page*12，就可以一直輪下去
			check_count = mycursor.fetchall()

			mycursor.execute("SELECT * FROM attractions_data")#limit每次只選出12筆，offset從%s開始算起，因為要每12筆，所以當page輸入1則pageNum=page*12，就可以一直輪下去
			check_name = mycursor.fetchall()


			list1=[]

			count=len(check_name)//12
			if page<count:
				next_Page=page+1
			else:
				next_Page=None

			for i in check_count:
				data_dic={
					"id":str(i[0]),
					"name":i[1],
					"category":i[2],
					"description":i[3],
					"address":i[4],
					"transport":i[5],
					"mrt":i[6],
					"latitude":str(i[7]),
					"longitude":str(i[8]),
					"images":
						i[9].split(",")
				}
				data_dic=data_dic.copy()
				list1.append(data_dic)
			if(len(list1)==0):
					result={
						"error":True,
						"message":"查無資料"
					}
					return json.dumps(result),500
			return json.dumps({"nextPage":next_Page,"data":list1}),200
	except:
		result={
			"error":True,
			"message":"伺服器內部錯誤"
			}
		return json.dumps(result),500
	


@app.route("/api/attraction/<attractionId>")
def attractionsId(attractionId):
	try:
		attractionId=int(attractionId)
		mycursor.execute("SELECT * FROM attractions_data WHERE id = %s",(attractionId,))#limit每次只選出12筆，offset從%s開始算起，因為要每12筆，所以當page輸入1則pageNum=page*12，就可以一直輪下去
		check_id = mycursor.fetchall()
		if len(check_id) != 0:
			list1=[]
			for i in check_id:
				data={
					"id":str(i[0]),
					"name":i[1],
					"category":i[2],
					"description":i[3],
					"address":i[4],
					"transport":i[5],
					"mrt":i[6],
					"latitude":str(i[7]),
					"longitude":str(i[8]),
					"images":
						i[9].split(",")
				}
			return json.dumps({"data":data}),200
		elif len(check_id) == 0:
			result={
				"error":True,
				"message":"景點編號不正確"
			}
			return json.dumps(result),400
	except:
		result={
			"error":True,
			"message":"伺服器內部錯誤"
		}
		return json.dumps(result),500


app.run(host="0.0.0.0",port=3000)