var items;
load_data();
function load_data(){
  //取得ID
  let getID = location.pathname.split('/')
  console.log(getID)
  getID=parseInt(getID[2])
  
  if(getID<=319&&getID>0){
    src='/api/attraction/'+getID;
  }else{
    //如果輸入不存在ID數，引導回首頁
    window.location.replace('/');
  }
  //取得資料
  fetch(src)
  .then((response) => {
    return response.json();
  }).then((data) => {
    // 實際存取到資料
    createBox(data);
    start_Booking(getID)
  }).catch((error) => {
    // 錯誤
    
  });

}


//產生畫面
function createBox(data){
  //圖的盒子
  
  //for(i=0;i<data.data["images"].length;i++){
    let list = document.getElementById("img_List");
    let img = document.createElement("img");
    img.src="http://"+data.data["images"][0];
    for(i=0;i<data.data["images"].length;i++){
      let dot_box=document.getElementById("dot")
      let dot=document.createElement("li")
      dot_box.appendChild(dot)
    }
    list.appendChild(img);
  //}
  //name的盒子
  let el_box = document.getElementById("booking_box");
  let name = document.createElement("h3");
  name.classList.add("name");
  let attrcationName = document.createTextNode(data.data['name']);
  name.appendChild(attrcationName);
  el_box.appendChild(name);

  //category&mrt的盒子
  let booking_category_mrt = document.createElement("p");
  booking_category_mrt.classList.add("booking_category_mrt");
  let inbox = document.createTextNode(data.data['category']+" at "+data.data['mrt']);
  booking_category_mrt.appendChild(inbox);
  el_box.appendChild(booking_category_mrt);

  //各種雜七雜八的盒子
  let el_others_box = document.getElementById("description-box");
  let description_box = document.createElement("p");
  description_box.classList.add("description");
  let inbox_2 = document.createTextNode(data.data['description']);
  description_box.appendChild(inbox_2);
  el_others_box.appendChild(description_box);

  let el_address_box = document.getElementById("address-box"); 
  let address_box = document.createElement("p");
  address_box.classList.add("address");
  let inbox_3 = document.createTextNode(data.data['address']);
  address_box.appendChild(inbox_3);
  el_address_box.appendChild(address_box);

  let el_transport_box = document.getElementById("transport-box");
  let transport_box = document.createElement("p");
  transport_box.classList.add("transport");
  let inbox_4 = document.createTextNode(data.data['transport']);
  transport_box.appendChild(inbox_4);
  el_transport_box.appendChild(transport_box);

  imgControl(data,img);
  
}

//時段選擇按鈕事件
//上半天
let btn_radio1=document.getElementById("radio1");
let charge1 = document.getElementById("charge1_div");
let charge2 = document.getElementById("charge2_div");
let btn_radio2=document.getElementById("radio2");
btn_radio1.addEventListener("click",function(radioCheck){
    charge1.style.display='block';
    charge2.style.display='none';

})
//下半天
btn_radio2.addEventListener("click",function(radioCheck){
    charge2.style.display='block';
    charge1.style.display='none';

})

function imgControl(data,img){
  let count = 0
  let dots=document.getElementsByTagName("li")[0]
  dots.style.backgroundColor="black";
  //上下頁切換圖片作法:切網址
  let btn_Prev = document.getElementById("left_arrow");
  btn_Prev.addEventListener("click",function(){
    if(count==0){

      let dots=document.getElementsByTagName("li")[count]
      dots.style.backgroundColor="white";

      count=data.data["images"].length-1

    }else{
      let dots=document.getElementsByTagName("li")[count]
      dots.style.backgroundColor="white";
      count-=1;

    }
    img.src="http://"+data.data["images"][count];
    let dots=document.getElementsByTagName("li")[count]
    dots.style.backgroundColor="black";
  }) 

  let btn_Next = document.getElementById("right_arrow");
  btn_Next.addEventListener("click",function(){
    if(count===data.data["images"].length-1){
      let dots=document.getElementsByTagName("li")[count]
      dots.style.backgroundColor="white";
      count=0;
    }else{
      let dots=document.getElementsByTagName("li")[count]
      dots.style.backgroundColor="white";
      count+=1;
    }
    img.src="http://"+data.data["images"][count];
    let dots=document.getElementsByTagName("li")[count]
    dots.style.backgroundColor="black";
  }) 

}
//開始預定行程按鈕
function start_Booking(getID){
  let start_Booking_btn=document.getElementById("start_Booking_btn")
  
  
  
  start_Booking_btn.addEventListener("click",function(){
    
    //先檢查是否登入
    fetch("/api/user")
    .then((response) => {
      return response.json();
    }).then((check_result) => {
      //console.log(check_result.data)
      if(check_result.data==null){
        //取消隱藏的登入表單
        signIn.style.display = "block"
        //取消隱藏的背景黑幕
        back_ground.style.display = "block"
      }else{

        //取得預定資料
        let get_date=document.getElementById("choose_date").value
        if (get_date==""){
          alert("請選擇日期");
          return;
        }
        let get_time=document.getElementsByName("radio")
        if (get_time[0].checked==true){
          time = "morning"
          price = 2000
        }else if(get_time[1].checked==true){
          time = "afternoon"
          price = 2500
        }
        console.log(get_time[0].checked)
        console.log(getID)
        console.log(get_date)
        console.log(time)
        console.log(price)
        //呼叫建立預定行程api
        let data={
          "attractionId":getID,
          "date":get_date,
          "time":time,
          "price":price
          }
        let src ="/api/booking";
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
            window.location.replace('/booking');
          }
      })

      }
    }).catch((error) => {
      // 錯誤
      
    });


  })
    
}