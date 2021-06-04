
//呼叫中央氣象局api
fetch("https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-091?Authorization=CWB-DD6B41F4-A301-465B-AB22-A9F285B320AA&locationName=%E8%87%BA%E5%8C%97%E5%B8%82")
    .then((response) => {
        return response.json();
    }).then((check_result) => {
        //console.log(check_result.data)
        console.log(check_result)


    })