# modules
import streamlit as st
import requests
from datetime import datetime,timedelta
import pandas as pd


# API key - stored in the ,streamlit folder
api_key = st.secrets["api_key"]


# API call from open weather map web page
url = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}"

#function to fetch the lates weather data
def getWeather(city):
    result = requests.get(url.format(city, api_key))
    if result:
        json = result.json()
        # st.write(json)
        country = json['sys']['country']
        temp = json['main']['temp'] - 273.15
        humid = json['main']['humidity'] - 273.15
        icon = json['weather'][0]['icon']
        lon = json['coord']['lon']
        lat = json['coord']['lat']
        des = json['weather'][0]['description']
        res = [country, round(temp, 1), round(temp_feels, 1), humid, lon, lat, icon, des]
        return res, json
    else:
        print("Error in search !")


#function for fetching the historical data
def getHistData(lat, lon, start):
    res = requests.get(url_1,lat, lon, start, api_key)
    data - res.json()
    temp = []
    for hour in data["hourly"]:
        t = hour['temp']
        temp.append(t)
    return data, # TEMP:

# let's write the applicaiton
