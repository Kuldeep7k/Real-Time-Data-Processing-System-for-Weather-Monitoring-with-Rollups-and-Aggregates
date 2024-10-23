import requests
import config
from datetime import datetime

def fetch_weather_data(city):
    """
    Fetches weather data for a given city from the OpenWeatherMap API.

    Parameters:
        city (str): The city name to fetch weather data for.

    Returns:
        dict or None: A dictionary with the following keys if the request is successful:
            - city (str): The city name.
            - temp (float): The current temperature in degrees Celsius.
            - feels_like (float): The current feels-like temperature in degrees Celsius.
            - humidity (int): The current humidity in percentage.
            - pressure (int): The current pressure in millibars.
            - weather_condition (str): The current weather condition.
            - wind_speed (float): The current wind speed in meters per second.
            - wind_direction (str): The current wind direction in degrees.
            - visibility (int): The current visibility in meters.
            - cloudiness (int): The current cloudiness in percentage.
            - timestamp (datetime): The timestamp of the API request in UTC.
        If the request fails, returns None.
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={config.API_KEY}&units=standard"  
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            'city': city,
            'temp': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'weather_condition': data['weather'][0]['description'],
            'wind_speed': data['wind']['speed'],
            'wind_direction': data['wind'].get('deg', 'N/A'), 
            'visibility': data.get('visibility', 'N/A'),  
            'cloudiness': data['clouds']['all'],  
            'timestamp': datetime.now()  
        }
    else:
        print(f"Error fetching weather data for {city}: {response.status_code}")
        return None
