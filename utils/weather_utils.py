import logging
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Weather:
    def get_weather(self, city="Moscow"):
        try:
           url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=YOUR_OPENWEATHERMAP_API_KEY" # Укажите свой API-ключ OpenWeatherMap
           response = requests.get(url)
           response.raise_for_status()
           data = response.json()
           if data['cod'] == 200:
              weather_description = data['weather'][0]['description']
              temperature = data['main']['temp'] - 273.15
              return f"Погода в городе {city}: {weather_description}, температура {temperature:.2f} градусов Цельсия."
           else:
              logging.error(f"Ошибка получения погоды: {data['message']}")
              return f"Ошибка получения погоды: {data['message']}"
        except requests.exceptions.RequestException as e:
           logging.error(f"Ошибка обращения к сервису погоды: {str(e)}")
           return f"Ошибка обращения к сервису погоды: {str(e)}"
        except Exception as e:
           logging.error(f"Непредвиденная ошибка при получении погоды: {e}")
           return f"Произошла непредвиденная ошибка при получении погоды: {e}"
