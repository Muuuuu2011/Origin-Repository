import json
import mysql.connector
import os
from dotenv import load_dotenv

#讀取env
load_dotenv()
# 資料庫參數設定
mydb = mysql.connector.connect(
  host=os.getenv('db_host'),
  user=os.getenv('db_user'),
  password=os.getenv('db_password'),
  database=os.getenv('db_name')
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE user_data (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), password VARCHAR(255))")
