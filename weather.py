# modules
import streamlit as st
import requests
from datetime import datetime,timedelta
import pandas as pd


# API key - stored in the ,streamlit folder
api_key = st.secrets["api_key"]
hist = st.secrets["records"]


# API call from open weather map web page
url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
url_1 = "http://history.openweathermap.org/data/2.5/onecall/timemachine?lat{}&lon={}$dl={}$appid={}"
#function to fetch the lates weather data
def getWeather(city):
    result = requests.get(url.format(city, api_key))
    if result:
        json = result.json()
        # st.write(json)
        country = json['sys']['country']
        temp = json['main']['temp'] - 273.15
        humid = json['main']['humidity'] - 273.15
        temp_feels = json['main']['feels_like'] - 273.15
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
    res = requests.get(url_1.format(lat, lon, start, hist))
    data = res.json()
    temp = []
    # for hour in data["hourly"]:
    #     t = hour['temp']
        # temp.append(t)
    st.write(data)
    return data, temp

# let's write the applicaiton
st.title("Weather Report Application")

im1, im2 = st.columns(2)

with im2:
    image0 = 'landscape.jfif'
    st.image(image0, use_column_width=True, caption = 'Somewhere in Netherlands.')
with im1:
    image1 = 'gloabe.jfif'
    st.image(image1, caption="The Open Weather API is used as the Data Resource for the application to funciton", use_column_width=True)
col1, col2 = st.columns(2)

with col1:
    st.header("GET TO KNOW THE WEATHER OF YOUR CURRENT CITY")
    city_name = st.text_input("Please Enter you city name")
with col2:
    if city_name:
        res, json = getWeather(city_name)
        # st.write(res)
        st.success('Current: ' + str(round(res[1], 2)))
        st.info('Feels Like: ' + str(round(res[2], 2)))
        st.subheader('Status: '+ res[7])
        web_str = "![Alt Text]" + "(http://openweathermap.org/img/wn/" + str(res[6]) + "@2x.png)"
        st.markdown(web_str)

        # show LAST % DAYS Data

if city_name:
    show_hist = st.beta_expander(label = 'Last 5 Days History')
    with show_hist:
        start_date_string = st.date_input('Current Date')
        date_df = []
        max_temp_df = []
        for i in range (5):
            date_str = start_date_string - timedelta(i)
            start_date = datetime.strptime(str(date_str), "%Y-%m-%d")
            timestamp_1 = datetime.timestamp(start_date)

            his, temp = getHistData(res[5], res[4], int(timestamp_1))
            date_df.append(date_str)
            max_temp_df.append(max(temp) - 273.15)

        df = pd.DataFrame()
        df['Date'] = date_df
        df['Max_temp'] = max_temp_df
        st.table(df)
