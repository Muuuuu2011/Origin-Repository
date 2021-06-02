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
            let greeting ="您好，"+check_result.data["name"]+"，非常感謝您的預定，您的行程如下:";
            document.getElementById("thankyou_Message").textContent=greeting;

        }
    })

}
//取得訂單編號
//得到完整網址後，取後面的訂單編號
let orderNumber = location.href.split("=")[1];

fetch(`/api/order/${orderNumber}`)
.then((response) => {
    return response.json();
}).then((check_result) => {
    
    //載入資料
    getData(check_result);


})


function getData(check_result){
    //圖
    let order_img_box =document.getElementById("order_img_box");
    let order_img = document.createElement("img");
    order_img.src="http://"+check_result["data"]["trip"]["attraction"]["image"];
    order_img_box.appendChild(order_img);
    //訂單編號
    document.getElementById("order_number").textContent="訂單編號："+check_result["data"]["number"];
    //景點名稱
    document.getElementById("order_name").textContent="台北一日遊："+check_result["data"]["trip"]["attraction"]["name"];
    //日期
    document.getElementById("order_detail_date").textContent=check_result["data"]["trip"]["date"];
    //時間
    document.getElementById("order_detail_time").textContent=check_result["data"]["trip"]["time"];
    //費用
    document.getElementById("order_detail_price").textContent=check_result["data"]["price"];
    //地點
    document.getElementById("order_detail_address").textContent=check_result["data"]["trip"]["attraction"]["address"];
    //聯絡人姓名
    document.getElementById("contact_name").textContent=check_result["data"]["contact"]["name"];
    //聯絡人信箱
    document.getElementById("contact_email").textContent=check_result["data"]["contact"]["email"];
    //聯絡人手機
    document.getElementById("contact_phone").textContent=check_result["data"]["contact"]["phone"];



}
