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
        document.getElementById("big_data_box").style.display="block";
        booking_content(booking_result);
    }
})


//放入行程
function booking_content(booking_result){
    //console.log(booking_result.data["price"])
    
    let name = "台北一日遊:"+booking_result.data.attraction["name"];
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

    attraction_data={
        "price": booking_result.data["price"],
        "trip": {
            "attraction": {
              "id": booking_result.data.attraction["id"],
              "name": booking_result.data.attraction["name"],
              "address": booking_result.data.attraction["address"],
              "image": "http://"+booking_result.data.attraction["image"][0]
            },
            "date": booking_result.data["date"],
            "time": booking_result.data["time"]
        }
    }
    // console.log(attraction_data.price,attraction_data.trip)
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



//金流設定TapPay

TPDirect.setupSDK(
    20457,
    'app_TA147ZtZM0RpecXyxKBnLCv2W86pH0rC501KtphMxeAxaZvodnfSgwECeTfG',
    'sandbox'
);

TPDirect.card.setup({
   fields: {
      number: {
         element: '#card-number',
         placeholder: '**** **** **** ****'
      },
      expirationDate: {
         element: '#card-expiration-date',
         placeholder: 'MM / YY'
      },
      ccv: {
         element: '#card-ccv',
         placeholder: 'CVV'
      }
   },
   styles: {
        // Style all elements
        input: {
            color: "gray",
        },
        // Styling ccv field
        "input.cvc": {
           // 'font-size': '16px'
        },
        // Styling expiration-date field
        "input.expiration-date": {
            //'font-size': '16px'
        },
        // Styling card-number field
        "input.card-number": {
           // 'font-size': '16px'
        },
        // style focus state
        ":focus": {
            'color': 'black'
        },
        // style valid state
        ".valid": {
            color: "green",
        },
        // style invalid state
        ".invalid": {
            color: "red",
        },
        // Media queries
        // Note that these apply to the iframe, not the root window.
        "@media screen and (max-width: 400px)": {
            input: {
                color: "orange",
            },
        },
    },
});



    
let pay_btn=document.getElementById("payment_button")
pay_btn.addEventListener("click",function(){
        const tappayStatus = TPDirect.card.getTappayFieldsStatus();

        if (document.getElementById("contact_name").value == '' || document.getElementById("contact_email").value =='' || document.getElementById("contact_phoneNumber").value==''){
            alert('請填入聯絡資訊');
            return;
        }

        // 確認是否可以 getPrime
        if (tappayStatus.canGetPrime === false) {
            alert('資料有誤，請輸入正確資料 ')
            console.log('can not get prime');
            return;
        }


        // Get prime
        TPDirect.card.getPrime((result) => {
            if (result.status !== 0) {
                alert('請確認資訊是否正確 ' + result.msg)
                // console.log(result.msg)
                return
            }
            console.log('get prime 成功')

            let data = {
                "prime":  result.card.prime,
                "order": {
                    "price": attraction_data.price,
                    "trip": attraction_data.trip,
                    "contact": {
                        "name": document.getElementById("contact_name").value,
                        "email": document.getElementById("contact_email").value,
                        "phone": document.getElementById("contact_phoneNumber").value,
                    },
                },
            };
    
            fetch("/api/orders", {
                body: JSON.stringify(data),
                headers: {
                    "content-type": "application/json",
                },
                method: "POST",
            })
                .then((res) => {
                    return res.json();
                })
                .then((data) => {
                    if (data["data"]["payment"]["status"]=="付款失敗"){
                        alert("付款失敗，請確認資料或其他原因")
                        return
                    }
                    // console.log(data["data"]["number"])
                    window.location.replace('/thankyou?number='+data["data"]["number"]);

                });
        });
        
});

