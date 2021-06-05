
//呼叫中央氣象局api
fetch("/api/weather")
    .then((response) => {
        return response.json();
    }).then((check_result) => {
        console.log(check_result)
        
        weather_data(check_result);

    })

    function weather_data(check_result){

        data=check_result["locations"]["0"]["location"]["0"]["weatherElement"]["0"]["time"];
        // console.log(data.length)
        //console.log(data[0]["startTime"])
        // a=data[0]["startTime"];
        // b=a.split(/-|:| /);

        for(let i=0;i<data.length;i++){
            
            if (i%2==0){
                continue;
            };
            
            if(data[i]["elementValue"]["1"]["value"]=="01"){

                let weather_img=document.createElement("img");
                weather_img.src="https://img.icons8.com/plasticine/64/000000/sun.png"
                let weather_box=document.getElementById("weather_box");
                date=data[i]["startTime"].split(/-|:| /);
                let word=document.createElement("p");
                word.textContent=date[1]+"/"+date[2];
                let div_box = document.createElement("div");
                div_box.classList.add("weather");
                div_box.appendChild(word);
                div_box.appendChild(weather_img);
                weather_box.appendChild(div_box);

            }else if(data[i]["elementValue"]["1"]["value"]=="02" | data[i]["elementValue"]["1"]["value"]=="03"){
                let weather_img=document.createElement("img");
                weather_img.src="https://img.icons8.com/plasticine/100/000000/partly-cloudy-day--v2.png"
                let weather_box=document.getElementById("weather_box");
                date=data[i]["startTime"].split(/-|:| /);
                let word=document.createElement("p");
                word.textContent=date[1]+"/"+date[2];
                let div_box = document.createElement("div");
                div_box.classList.add("weather");
                div_box.appendChild(word);
                div_box.appendChild(weather_img);
                weather_box.appendChild(div_box);
               

            }else if(data[i]["elementValue"]["1"]["value"]=="04" | data[i]["elementValue"]["1"]["value"]=="05" | data[i]["elementValue"]["1"]["value"]== "06" | data[i]["elementValue"]["1"]["value"]=="07"){
                
                let weather_img=document.createElement("img");
                weather_img.src="https://img.icons8.com/plasticine/100/000000/foggy-night-1.png"
                let weather_box=document.getElementById("weather_box");
                date=data[i]["startTime"].split(/-|:| /);
                let word=document.createElement("p");
                word.textContent=date[1]+"/"+date[2];
                let div_box = document.createElement("div");
                div_box.classList.add("weather");
                div_box.appendChild(word);
                div_box.appendChild(weather_img);
                weather_box.appendChild(div_box);

            }else{
                let weather_img=document.createElement("img");
                weather_img.src="https://img.icons8.com/plasticine/100/000000/rain.png"
                let weather_box=document.getElementById("weather_box");
                date=data[i]["startTime"].split(/-|:| /);
                let word=document.createElement("p");
                word.textContent=date[1]+"/"+date[2];
                let div_box = document.createElement("div");
                div_box.classList.add("weather");
                div_box.appendChild(word);
                div_box.appendChild(weather_img);
                weather_box.appendChild(div_box);
            }


        }

    }
