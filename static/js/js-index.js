fetch('http://127.0.0.1:3000/api/attractions?page=0')
  .then((response) => {
    // 操作 response 屬性、方法
    return response.json();
  })
  .then((data) => {
    // 實際存取到資料
    console.log(data);
    data1 = data.data;//把資料拿出來
    let el = document.getElementsByTagName('article')[0];
    for(let i=0;i<12;i++){
      console.log(data1[i].name,data1[i].mrt,data1[i].category);
      console.log(data1[i].images[0])
      let bigBox = document.createElement("div");
      bigBox.classList.add("attraction");

      let bigImg = document.createElement("img")//創造一個圖的盒子:可以把圖放進去
      bigBox.appendChild(bigImg);//大箱子裡面有圖的盒子
      let imgName = document.createElement("h5")//創造一個字的盒子:可以把字放進去
      imgName.classList.add("pics-name");//字的盒子裝字進去
      let text = document.createTextNode(data1[i].name);//字
      imgName.appendChild(text);//字的盒子裡面裝字
      bigBox.appendChild(imgName);
      bigImg.src="http://"+data1[i].images[0];

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

    }



  })
  .catch((error) => {
    // 錯誤回應
    console.log(error);
  });