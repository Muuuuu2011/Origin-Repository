var items;

window.onload = function getData(){
  //取得ID
  let getID = location.pathname.split('/')
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