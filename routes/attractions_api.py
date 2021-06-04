from flask import *
from main import app
import json
import mysql.connector
from mysql.connector import pooling
from mysql.connector import Error
import os
from dotenv import load_dotenv

attractions_api = Blueprint('attractions_api',__name__)
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


@attractions_api.route("/api/attractions")
def attractions():
	try:
		mydb = connection_pool.get_connection()
		mycursor = mydb.cursor(buffered=True)
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
					mydb.close()
					return json.dumps(result),500
				mydb.close()	
				return json.dumps({"nextPage":next_Page,"data":list1}),200
			else:
				result={
					"error":True,
					"message":"查無資料"
				}
				mydb.close()
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
					mydb.close()
					return json.dumps(result),500
			mydb.close()		
			return json.dumps({"nextPage":next_Page,"data":list1}),200
	except:
		result={
			"error":True,
			"message":"伺服器內部錯誤"
			}
		return json.dumps(result),500
