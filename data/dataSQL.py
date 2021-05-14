import json
import mysql.connector

# 資料庫參數設定
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="chickenbot2011_",
  database="website"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE customers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), password VARCHAR(255))")
