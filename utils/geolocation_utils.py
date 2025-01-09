import logging
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GeolocationUtils:
    def search_nearby(self, query, location):
        try:
          lat, lon = location.split(',')
          lat = float(lat)
          lon = float(lon)
          url = f"https://nominatim.openstreetmap.org/search?q={query}&format=json&lat={lat}&lon={lon}&bounded=1&limit=3" # Для OpenStreetMap API
          response = requests.get(url)
          response.raise_for_status()
          data = response.json()

          if not data:
            return f"Ничего не найдено поблизости от ({lat}, {lon}) по запросу: {query}."
          result = f"Результаты поиска '{query}' рядом с ({lat}, {lon}):\n"
          for item in data:
            result += f"Название: {item['display_name']}\n"
            result += f"Широта: {item['lat']}, Долгота: {item['lon']}\n"
            result += "-----\n"
          return result
        except requests.exceptions.RequestException as e:
           logging.error(f"Ошибка при запросе к API геолокации: {e}")
           return f"Ошибка при запросе к API геолокации: {e}"
        except Exception as e:
           logging.error(f"Непредвиденная ошибка при запросе геолокации: {e}")
           return f"Непредвиденная ошибка при запросе геолокации: {e}"

    def get_location_by_ip(self, ip=None):
        try:
          url = f"http://ip-api.com/json/{ip if ip else ''}"
          response = requests.get(url)
          response.raise_for_status()
          data = response.json()
          if data.get('status') == 'success':
               return f"Страна: {data['country']}, Регион: {data['regionName']}, Город: {data['city']}, Координаты: {data['lat']}, {data['lon']}"
          else:
              logging.error(f"Не удалось получить данные по IP: {ip}. Причина: {data.get('message')}")
              return f"Не удалось получить данные по IP: {ip}. Причина: {data.get('message')}"
        except requests.exceptions.RequestException as e:
           logging.error(f"Ошибка при запросе IP-геолокации: {e}")
           return f"Ошибка при запросе IP-геолокации: {e}"
        except Exception as e:
           logging.error(f"Непредвиденная ошибка при запросе IP-геолокации: {e}")
           return f"Непредвиденная ошибка при запросе IP-геолокации: {e}"