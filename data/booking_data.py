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

mycursor.execute("CREATE TABLE booking_data (id INT AUTO_INCREMENT PRIMARY KEY,attractionId int not null,date VARCHAR(255) not null, time VARCHAR(255) not null, price int not null, user_mail VARCHAR(255) not null)")


mycursor.execute("CREATE TABLE orders_data (id INT AUTO_INCREMENT UNIQUE,attractionId INT not null,date VARCHAR(255) not null, time VARCHAR(255) not null, price INT not null, email VARCHAR(255) not null,name VARCHAR(255) not null,phone VARCHAR(255) not null,payment_status VARCHAR(255) not null,order_number  VARCHAR(255)  PRIMARY KEY  not null ,bank_transaction_id VARCHAR(255) not null,currentTime DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,image MEDIUMTEXT,attraction_name VARCHAR(255),address VARCHAR(255))")