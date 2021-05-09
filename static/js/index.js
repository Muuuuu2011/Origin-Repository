var page = 0;
let load_complete=false
let keyword;
let el = document.getElementsByTagName('article')[0];


Attractions()//先執行一次，登入時直接載入資料
//產生盒子
async function Attractions() {
  let src = '';
  
  if (page != null & keyword != null) {//會帶入之前存取的下一頁
    src = '/api/attractions?page='+page+"&keyword="+keyword;
  }else if(page != null){
    src = '/api/attractions?page='+page;
  } else {
    return ;
  }

  await fetch(src)
    .then((response) => {
      return response.json();
    }).then((data) => {
      // 實際存取到資料
      data1 = data.data;//把資料拿出來
      nextPage = data.nextPage;
      let cnt =0

      for (let i = 0; i < data.data.length; i++) {
        let bigBox = document.createElement("div");
        bigBox.classList.add("attraction");


        let a = document.createElement('a')
        a.href= "/attraction/"+data1[i].id;
        bigBox.appendChild(a);
        let bigImg = document.createElement("img")//創造一個圖的盒子:可以把圖放進去
        a.appendChild(bigImg);//大箱子裡面有圖的盒子
        let imgName = document.createElement("h5")//創造一個字的盒子:可以把字放進去
        imgName.classList.add("pics-name");//字的盒子裝字進去
        let text = document.createTextNode(data1[i].name);//字
        imgName.appendChild(text);//字的盒子裡面裝字
        bigBox.appendChild(imgName);
        bigImg.src = "http://" + data1[i].images[0];

        let smallBox = document.createElement("div");//創造裝"mrt-category"的箱子
        smallBox.classList.add("mrt-category");
        bigBox.appendChild(smallBox);
        let mrt = document.createElement("p");
        mrt.classList.add("mrt");
        let mrtName = document.createTextNode(data1[i].mrt);
        mrt.appendChild(mrtName);
        smallBox.appendChild(mrt);
        let category = document.createElement("p");
        let categoryName = document.createTextNode(data1[i].category);
        category.classList.add("category");
        category.appendChild(categoryName);
        smallBox.appendChild(category);
        el.appendChild(bigBox);
        cnt++
      }
      load_complete = cnt===data.data.length
      page = nextPage;//存取下一頁
    }).catch((error) => {
      // 錯誤
      el.innerHTML="查無此資料"
    });

};


window.addEventListener('scroll', function (e) {
  // var footer = document.getElementById("footer");
  // var rect = footer.getBoundingClientRect();
  if ((window.outerHeight + window.pageYOffset+10) >= document.body.offsetHeight && load_complete) {
    // getData()
    load_complete=false
    Attractions()
  }
})

btn = document.getElementById("search_button")
btn.addEventListener('click',function(e){
  keyword=document.getElementById("keyword").value;
  el.innerHTML=""
  page=0;
  load_complete=false
  Attractions(keyword,page)
})

