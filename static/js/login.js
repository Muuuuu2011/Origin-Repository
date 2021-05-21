
fetch("/api/user")
  .then((response) => {
    return response.json();
  }).then((check_result) => {
    //console.log(check_result.data)
    if(check_result.data!=null){
        document.getElementById("signin_signup").style.display="none";//登入成功後消失，改成顯示登出
        document.getElementById("sign_out").style.display="block"
    }else{
        document.getElementById("signin_signup").style.display="block";
        document.getElementById("sign_out").style.display="none"
    }
  }).catch((error) => {
    // 錯誤
    
  });


let signIn = document.getElementById("signIn")
let back_ground = document.getElementById("black_background")
//點擊觸發登入表單
login_btn = document.getElementById("signin_signup")
login_btn.addEventListener('click', function () {
  //取消隱藏的登入表單
  signIn.style.display = "block"
  //取消隱藏的背景黑幕
  back_ground.style.display = "block"
})

//點擊X或背景黑幕讓登入表單&黑幕隱藏
let cancel_btn_1 = document.getElementById("cancel_btn1")
let cancel_btn_2 = document.getElementById("cancel_btn2")
back_ground.addEventListener('click',cancel,false)
cancel_btn2.addEventListener('click',cancel)
cancel_btn1.addEventListener('click',cancel)
function cancel(){
  signIn.style.display="none"
  back_ground.style.display="none"
  signUp.style.display="none";
  document.getElementById("signIn_Message").style.display="none";//登入訊息提示框隱藏
  document.getElementById("signUp_Message").style.display="none";//註冊訊息提示框隱藏
}


//點擊"點此註冊"顯示註冊表單
let signUp=document.getElementById("signUp")
let go_SignUp_btn=document.getElementById("go_Sign_Up")
go_SignUp_btn.addEventListener('click',function(){
  signUp.style.display="block";
  back_ground.style.display="block"
  signIn.style.display="none";
})

//點擊"點此登入"顯示登入表單
let go_SignIn_btn=document.getElementById("go_Sign_In")
go_SignIn_btn.addEventListener('click',function(){
  signIn.style.display="block";
  signUp.style.display="none";
  back_ground.style.display="block"
})

//點擊按鈕把"註冊"資料送出
let signUp_button=document.getElementById("signUp_button")
signUp_button.addEventListener('click',function(){
  let sign_Up_name = document.getElementById("sign_Up_name").value
  let sign_Up_email = document.getElementById("sign_Up_email").value
  let sign_Up_password = document.getElementById("sign_Up_password").value
  let data={"name":sign_Up_name,
            "email":sign_Up_email,
            "password":sign_Up_password
            }
  let src ="/api/user";
  fetch(src,{
    method:'POST',
    body:JSON.stringify(data),
    headers: new Headers({
      'Content-Type': 'application/json'
      })
  }).then(function(response){
    return response.json();
  }).then(function(myJson){
    if (myJson.ok == true){
      x ="您好，"+sign_Up_name+"，註冊成功";
      document.getElementById("signUp_Message").style.display="block";
      document.getElementById("signUp_Message").textContent=x;//提示註冊成功
      document.getElementById("sign_Up_name").value="";//清空輸入欄位，一定要抓輸入框ID並設定value=""才能清空，只清變數不會影響輸入框的值
      document.getElementById("sign_Up_email").value="";
      document.getElementById("sign_Up_password").value="";
    }else{
      x = myJson.message;
      document.getElementById("signUp_Message").style.display="block";
      document.getElementById("signUp_Message").textContent=x;
      document.getElementById("sign_Up_name").value="";//清空輸入欄位，一定要抓輸入框ID並設定value=""才能清空，只清變數不會影響輸入框的值
      document.getElementById("sign_Up_email").value="";
      document.getElementById("sign_Up_password").value="";
    };
  })
})


//點擊按鈕把"登入"資料送出
let signIn_button=document.getElementById("signIn_button")
signIn_button.addEventListener('click',function(){
  let sign_In_email = document.getElementById("sign_In_email").value
  let sign_In_password = document.getElementById("sign_In_password").value
  let data={
            "email":sign_In_email,
            "password":sign_In_password
            }
  let src ="/api/user";
  fetch(src,{
    method:'PATCH',
    body:JSON.stringify(data),
    headers: new Headers({
      'Content-Type': 'application/json'
      })
  }).then(function(response){
        return response.json();
  }).then(function(myJson){
    if (myJson.ok == true){
        // signIn.style.display="none";
        // back_ground.style.display="none";
        // document.getElementById("signIn_Message").style.display="none";//訊息提示框消失
        // document.getElementById("signin_signup").style.display="none";//登入成功後消失，改成顯示登出
        // document.getElementById("sign_out").style.display="block"
        window.location.reload();
        //登入成功後重新載入頁面，然後使用最上面的檢查登入狀態來調整登入畫面
    }else{     
        x = myJson.message;
        document.getElementById("signIn_Message").style.display="block";
        document.getElementById("signIn_Message").textContent=x;
        document.getElementById("sign_In_email").value="";//清空輸入欄位，一定要抓輸入框ID並設定value=""才能清空，只清變數不會影響輸入框的值
        document.getElementById("sign_In_password").value="";
    };
  })
})

//點擊"登出"按鈕
let logout_btn=document.getElementById("sign_out")
logout_btn.addEventListener("click",function(){
    let src ="/api/user";
    fetch(src,{
        method:'DELETE',
        headers: new Headers({
            'Content-Type': 'application/json'
          })
      }).then(function(response){
            return response.json();
      }).then(function(myJson){
            if (myJson.ok == true){
                document.getElementById("signin_signup").style.display="block";
                document.getElementById("sign_out").style.display="none"
                window.location.reload();
            }
      })
})


let schedule_btn=document.getElementById("booking_Schedule")
schedule_btn.addEventListener("click",function(){
  fetch("/api/user")
  .then((response) => {
    return response.json();
  }).then((check_result) => {
    console.log(check_result.data)
    if(check_result.data==null){

      //取消隱藏的登入表單
      signIn.style.display = "block"
      //取消隱藏的背景黑幕
      back_ground.style.display = "block"
    }else{
      window.location.replace('/booking');
    }
  }).catch((error) => {
    // 錯誤
    
  });
})

//返回首頁
let title_btn=document.getElementById("title")
title_btn.addEventListener("click",function(){

  window.location.replace('/');
})