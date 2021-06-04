from flask import *
from main import app
import os
from dotenv import load_dotenv
import re
import requests
import json
weather_api = Blueprint('weather_api',__name__)

load_dotenv()

@weather_api.route("/api/weather")
def weather():

    response = requests.get("https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-091?Authorization=CWB-DD6B41F4-A301-465B-AB22-A9F285B320AA&locationName=%E8%87%BA%E5%8C%97%E5%B8%82")
    data=response.text
    r=json.loads(data)
    # print(r["records"])
    result={

    }
    return json.dumps(r["records"]),200