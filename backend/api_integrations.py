import requests
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

def get_city_data(city_name):
    """Get all city data with proper error handling"""
    with ThreadPoolExecutor() as executor:
        futures = {
            'maps': executor.submit(get_google_maps_data, city_name),
            'news': executor.submit(get_news_data, city_name),
            'weather': executor.submit(get_weather_data, city_name)
        }
        
        results = {}
        for key, future in futures.items():
            try:
                results[key] = future.result()
            except Exception as e:
                results[key] = {
                    'error': str(e),
                    'source': key
                }
        
        return results
    
def get_google_maps_data(city):
    params = {
        'address': city,
        'key': os.getenv('MAPS_API_KEY'),
        'fields': 'geometry,address_components'
    }
    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=params)
    return response.json()

def get_news_data(city):
    params = {
        'q': city,
        'apiKey': os.getenv('NEWS_API_KEY'),
        'pageSize': 3
    }
    response = requests.get('https://newsapi.org/v2/everything', params=params)
    return response.json()

def get_weather_data(city_name):
    """Fetch current weather and forecast using WeatherAPI"""
    try:
        # First get coordinates for the city (required by many weather APIs)
        geocode_url = "http://api.openweathermap.org/geo/1.0/direct"
        geocode_params = {
            'q': city_name,
            'limit': 1,
            'appid': os.getenv('WEATHER_API_KEY')
        }
        
        geo_response = requests.get(geocode_url, params=geocode_params)
        geo_response.raise_for_status()
        location = geo_response.json()[0]
        
        # Now get weather data
        weather_url = "https://api.openweathermap.org/data/2.5/weather"
        weather_params = {
            'lat': location['lat'],
            'lon': location['lon'],
            'appid': os.getenv('WEATHER_API_KEY'),
            'units': 'metric'  # or 'imperial'
        }
        
        weather_response = requests.get(weather_url, params=weather_params)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        
        # Format the relevant data
        return {
            'temperature': weather_data['main']['temp'],
            'conditions': weather_data['weather'][0]['description'],
            'humidity': weather_data['main']['humidity'],
            'wind_speed': weather_data['wind']['speed'],
            'icon': weather_data['weather'][0]['icon']
        }
        
    except Exception as e:
        print(f"Weather API error: {str(e)}")
        return {
            'error': f"Could not fetch weather data: {str(e)}",
            'source': 'OpenWeatherMap'
        }
def get_weather(city_name):
    """Fetch weather using OpenWeatherMap API"""
    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                'q': city_name,
                'appid': os.getenv('WEATHER_API_KEY'),
                'units': 'metric'
            }
        )
        data = response.json()
        return {
            'temp': data['main']['temp'],
            'conditions': data['weather'][0]['description'],
            'humidity': data['main']['humidity']
        }
    except Exception as e:
        return {'error': str(e)}
