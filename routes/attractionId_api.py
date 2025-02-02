from flask import *
import json
import mysql.connector
from mysql.connector import pooling
from mysql.connector import Error
import os
from dotenv import load_dotenv

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

attractionId_api = Blueprint('attractionId_api',__name__)

@attractionId_api.route("/api/attraction/<attractionId>")
def attractionsId(attractionId):
	try:
		mydb = connection_pool.get_connection()
		mycursor = mydb.cursor(buffered=True)
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
			mydb.close()	
			return json.dumps({"data":data}),200
		elif len(check_id) == 0:
			result={
				"error":True,
				"message":"景點編號不正確"
			}
			mydb.close()
			return json.dumps(result),400
	except:
		result={
			"error":True,
			"message":"伺服器內部錯誤"
		}
		return json.dumps(result),500

