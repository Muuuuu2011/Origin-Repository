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
            let greeting ="您好，"+check_result.data["name"]+"，待預定的行程如下:";
            document.getElementById("booking_Message").textContent=greeting;

            //預設聯絡資訊姓名、信箱值為使用者資料
            let name = check_result.data["name"];
            document.getElementById("contact_name").value=name;

            let email = check_result.data["email"];
            document.getElementById("contact_email").value=email;

            document.getElementById("footer").height="100%";
        }
    })

}



//檢查登入頁面
fetch("/api/booking")
.then((response) => {
    return response.json();
}).then((booking_result) => {
    //console.log(booking_result)
    if(booking_result.data==null){

        nothing_action()
       

    }else{
        booking_content(booking_result);
    }
})


//放入行程
function booking_content(booking_result){
    //console.log(booking_result.data["price"])

    let name = "台北一日遊:"+booking_result.data.attraction["name"]
    document.getElementById("booking_name").textContent=name;

    let date = booking_result.data["date"];
    document.getElementById("booking_detail1").textContent=date;

    if(booking_result.data["time"]=="afternoon"){
        let time = "下午2點到晚上9點"
        document.getElementById("booking_detail2").textContent=time;
    }else if(booking_result.data["time"]=="morning"){
        let time = "早上9點到下午四點"
        document.getElementById("booking_detail2").textContent=time;
    };

    let price = "新台幣 "+booking_result.data["price"]+" 元" ;
    document.getElementById("booking_detail3").textContent=price;

    let address = booking_result.data.attraction["address"];
    document.getElementById("booking_detail4").textContent=address;

    let box = document.getElementById("booking_img_box");
    let img = document.createElement("img");
    img.src="http://"+booking_result.data.attraction["image"][0];
    box.appendChild(img);


    //總價
    let total_price="總價：新台幣 "+booking_result.data["price"]+" 元" ;
    document.getElementById("total_price").textContent=total_price;
}

let delete_btn = document.getElementById("delete_booking")
delete_btn.addEventListener("click",function(){

    let src ="/api/booking";
    fetch(src,{
        method:'DELETE',
        headers: new Headers({
            'Content-Type': 'application/json'
          })
      }).then(function(response){
            return response.json();
      }).then(function(myJson){
            if (myJson.ok == true){
                nothing_action();
            }
      })

})

function nothing_action(){
     //顯示隱藏的div
     document.getElementById("booking_Message_box2").style.display="block";
     //隱藏其他資訊
     document.getElementById("big_data_box").style.display="None";
     //訊息內容
     let message = "目前沒有任何待預訂的行程"
     document.getElementById("nothing_message").textContent=message;

     document.getElementById("footer").style.height="100%";
     
}