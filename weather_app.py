import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Weather Forecast App",page_icon="🌤️",layout="centered")


def get_weather_data(city,Weather_api_key):
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + Weather_api_key +"&q=" + city
    response = requests.get(complete_url)
    return response.json()

def get_weather_forecast(lat,lon,Weather_api_key):
    base_url = "https://api.openweathermap.org/data/2.5/"
    complete_url = f"{base_url}forecast?lat={lat}&lon={lon}&appid={Weather_api_key}"
    response = requests.get(complete_url)
    return response.json()

def display_weekly_forecast(data):
    try:
        st.write("======================================================================")
        st.title("Weekly forecast")
        displayed_dates = set()
        
        c1,c2,c3,c4 = st.columns(4)
        with c1:
            st.metric("", "Day")
        with c2:
            st.metric("", "Desc")
        with c3:
            st.metric("", "Min temp")
        with c4:
            st.metric("", "Max temp")
        
        for day in data['list']:
            date = datetime.fromtimestamp(day['dt']).strftime('%A, %B %d')
            if date not in displayed_dates:
                displayed_dates.add(date)
                min_temp = day['main']['temp_min'] - 273.15
                max_temp = day['main']['temp_max'] - 273.15  # Corrected typo
                main = day['weather'][0]['main']
                weather_emoji = get_weather_emoji(main)
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.write(f"{date}")
                with c2:
                    st.write(f"{main.capitalize()}{weather_emoji}")
                with c3:
                    st.write(f"{min_temp:.1f}°C")
                with c4:
                    st.write(f"{max_temp:.1f}°C")
    except Exception as e:
        st.error(f"Error: {e}")

def get_weather_emoji(weather_main):
    weather_emojis = {
        "Clear": "☀️",
        "Clouds": "☁️",
        "Rain": "🌧️",
        "Drizzle": "🌦️",
        "Thunderstorm": "⛈️",
        "Snow": "❄️",
        "Mist": "🌫️",
        "Smoke": "💨",
        "Haze": "🌫️",
        "Dust": "🌪️",
        "Fog": "🌫️",
        "Sand": "🏜️",
        "Ash": "🌋",
        "Squall": "🌬️",
        "Tornado": "🌪️",
    }
    return weather_emojis.get(weather_main, "❓")


def app():
    
    ## Side bar 
    st.sidebar.title("Weather Forecasting App")
    city = st.sidebar.text_input("Enter city Name", "Ahmedabad")

    ##APIs
    weather_api_key="YOUR API KEY"

    ## Submit button
    submit = st.sidebar.button("Get Weather")

    if submit:
        st.title("Weather of " + city + " is:")
        with st.spinner("Fetching Weather data..."):
            weather_data = get_weather_data(city , weather_api_key)
            print(weather_data)

            if weather_data.get("cod") != 404:
                try:
                    weather = weather_data["weather"][0]  # Access the first item in the "weather" list
                    main_data = weather_data["main"]
                    wind = weather_data["wind"]
                    weather_emoji = get_weather_emoji(weather["main"])
                    lat = weather_data["coord"]["lat"]
                    lon = weather_data["coord"]["lon"]
                    



                    col1, col2 = st.columns(2)
                    with col1:
                        with col1:
                            st.metric("Weather",f"{weather['main']}{weather_emoji}")
                            st.metric("Temperature 🌡️", f"{weather_data['main']['temp'] - 273.15:.2f} °C ")
                            st.metric("Min Temp 🥶", f"{weather_data['main']['temp_min'] - 273.15:.2f} °C ")
                            st.metric("Wind speed 🎐", f"{weather_data['wind']['speed']} Km/s ")
                        
                        with col2:
                            st.metric("Description",f"{weather['description']}")
                            st.metric("Humidity 💧", f"{weather_data['main']['humidity']}%")
                            st.metric("Max Temp 🥵", f"{weather_data['main']['temp_max'] - 273.15:.2f} °C ")
                            st.metric("Pressure ", f"{weather_data['main']['pressure']} hPa ")

                    # Get forecast data
                    forecast_data = get_weather_forecast(lat, lon, weather_api_key)
                    print(forecast_data)
                    if  forecast_data.get("cod") != "404":
                        display_weekly_forecast(forecast_data)

                  

                except KeyError as e:
                    st.error(f"Missing key in response data: {e}")
                except IndexError as e:
                    st.error(f"Error accessing list index: {e}")




if __name__ == "__main__":
    app()
