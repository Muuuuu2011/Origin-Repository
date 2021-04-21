import json
import mysql.connector

# 資料庫參數設定
mydb = mysql.connector.connect(
  host="localhost",
  user="admin",
  password="1234",
  database="website"
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
        str(list2)#轉字串才能放進資料庫
        )
    mycursor.execute(sql, val)
    mydb.commit()   
    
        
    
            





