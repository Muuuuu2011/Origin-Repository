//檢查是否登入
window.onload=function (){ 
    fetch("/api/user")
    .then((response) => {
        return response.json();
    }).then((check_result) => {
        //console.log(check_result.data)
        if(check_result.data==null){
            window.location.replace('/');
        }else{
            let greeting ="您好，"+check_result.data["name"]+"，您的訂單紀錄如下:";
            document.getElementById("history_Message").textContent=greeting;
            result = check_result.data
            get_history(result)
        }
    })
}

function get_history(result){

    // console.log(result["email"])


    fetch(`/api/history/${result["email"]}`)
    .then((response) => {

        return response.json();
    }).then((check_result) => {
        
        //載入資料
        getData(check_result);
    })
}    


function getData(check_result){
    // console.log(check_result.data[0])
    for (let i = 0; i < check_result.data.length; i++) {
        //圖箱子
        let img_box =document.createElement("div");
        img_box.classList.add("order_img_box");
        //圖  
        let img = document.createElement("img");
        img.src="http://"+check_result.data[i].image;
        img_box.appendChild(img);
        //景點資訊箱子
        let order_form_box = document.createElement("div");
        order_form_box.classList.add("order_form_box");
        //創造訂單編號
        let order_number = document.createElement("h2");
        order_number.classList.add("order_number");
        order_number.textContent="訂單編號："+check_result.data[i].order_number;
        order_form_box.appendChild(order_number);
        //訂單狀態
        date=check_result.data[i].date
        //判斷訂單時間函式
        date_status(date)
        let order_status = document.createElement("h2");
        order_status.classList.add("order_number");
        order_status.textContent="訂單狀態："+date_status_is;
        order_form_box.appendChild(order_status);
        //創造地點名稱
        let order_name = document.createElement("h2");
        order_name.classList.add("order_number")
        order_name.textContent=check_result.data[i].attraction_name;
        order_form_box.appendChild(order_name);
        //創造日期
        let order_date = document.createElement("div");
        order_date.classList.add("order_info");
        order_date.textContent="日期："+check_result.data[i].date;
        order_form_box.appendChild(order_date);
        //創造時間
        if (check_result.data[i].time=="morning"){
            time = "早上 9 點到下午 2 點";
        }else{
            time = "下午 2 點到晚上 9 點";
        }
        let order_time=document.createElement("div");
        order_time.classList.add("order_info");
        order_time.textContent="時間："+time;
        order_form_box.appendChild(order_time);
        //創造費用
        let order_price=document.createElement("div");
        order_price.classList.add("order_info");
        order_price.textContent="費用：新台幣 "+check_result.data[i].price+" 元";
        order_form_box.appendChild(order_price);
        //創造地點
        let order_address=document.createElement("div");
        order_address.classList.add("order_info");
        order_address.textContent="地點："+check_result.data[i].address;
        order_form_box.appendChild(order_address);
        //聯絡資訊箱子
        let contact_form_box = document.createElement("div");
        contact_form_box.classList.add("contact_form_box");
        //聯絡h3
        let h_3=document.createElement("h3");
        h_3.textContent="您的聯絡資訊：";
        contact_form_box.appendChild(h_3);
        //創造姓名
        let contact_name=document.createElement("p");
        contact_name.textContent="聯絡姓名："+check_result.data[i].name;
        contact_form_box.appendChild(contact_name);
        //創造信箱
        let contact_email=document.createElement("p");
        contact_email.textContent="聯絡信箱："+check_result.data[i].email;
        contact_form_box.appendChild(contact_email);
        //創造號碼
        let contact_phone=document.createElement("p");
        contact_phone.textContent="聯絡信箱："+check_result.data[i].phone;
        contact_form_box.appendChild(contact_phone);

        let hr = document.createElement("hr");
        let data_box=document.getElementById("data_box");
        data_box.appendChild(img_box);    
        data_box.appendChild(order_form_box);
        data_box.appendChild(contact_form_box);
        data_box.appendChild(hr);


    

    }
}


function date_status(date){
    ScheduleDate = date+" 00:00:00"; 
    Today=new Date();
    CurrentDate = Today.getFullYear()+"-"+(Today.getMonth()+1)+"-"+Today.getDate() +" 00:00:00";
    if ( (Date.parse(ScheduleDate)).valueOf() < (Date.parse(CurrentDate)).valueOf()){
        date_status_is="已結束"
        return date_status_is
    }else if((Date.parse(ScheduleDate)).valueOf() == (Date.parse(CurrentDate)).valueOf()){
        date_status_is="進行中"
        return date_status_is
    }else{
        date_status_is="準備中"
        return date_status_is
    }




}