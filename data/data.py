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

with open("taipei-attractions.json","r",encoding="utf-8") as file:
    data=json.load(file)

attractionsData=data['result']['results']

for i in range(len(attractionsData)):
    print(i)
    string = attractionsData[i]['file']#資料過濾，保留jpg、JPG、png、PNG
    list1 = string.split('http://')
    list2=[]
    for j in range(len(list1)):
        if '.jpg' in list1[j]:
            list2.append(list1[j])
        elif 'JPG' in list1[j]:
            list2.append(list1[j])
        elif 'PNG' in list1[j]:
            list2.append(list1[j])
        elif 'png' in list1[j]:
            list2.append(list1[j])
        else:
            continue
    separator=","#忘記看這裡https://zh-hant.hotbak.net/key/join%E5%87%BD%E6%95%B8.html
    attFile=separator.join(list2)        

    #放入資料庫
    sql = "INSERT INTO attractions_data (id,name,category,description,address,transport,mrt,latitude,longitude,images) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (attractionsData[i]['_id'],
        attractionsData[i]['stitle'],
        attractionsData[i]['CAT2'],
        attractionsData[i]['xbody'],
        attractionsData[i]['address'],
        attractionsData[i]['info'],
        attractionsData[i]['MRT'],
        attractionsData[i]['latitude'],
        attractionsData[i]['longitude'],
        attFile
        )
    mycursor.execute(sql, val)
    mydb.commit()   
    
        
    
            





