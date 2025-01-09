import logging
import requests
import os
from PIL import Image
from io import BytesIO

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ImageDownloader:
    def __init__(self):
        self.download_dir = 'downloads'
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)


    async def download_image(self, query):
       try:
           search_url = f"https://api.unsplash.com/search/photos?query={query}&client_id=YOUR_UNSPLASH_API_KEY" # Укажите свой API-ключ Unsplash
           search_response = requests.get(search_url)
           search_response.raise_for_status()
           search_data = search_response.json()

           if not search_data['results']:
             return f"Изображение по запросу '{query}' не найдено."

           image_url = search_data['results'][0]['urls']['regular']
           image_response = requests.get(image_url)
           image_response.raise_for_status()
           image_data = image_response.content
           image = Image.open(BytesIO(image_data))
           image_name = f"{query.replace(' ', '_')}.{image.format.lower()}"
           filepath = os.path.join(self.download_dir, image_name)
           image.save(filepath)
           return f"Изображение по запросу '{query}' сохранено в: {filepath}"
       except requests.exceptions.RequestException as e:
           logging.error(f"Ошибка обращения к сервису поиска изображений: {e}")
           return f"Ошибка обращения к сервису поиска изображений: {str(e)}"
       except KeyError:
           logging.error("Ошибка при разборе JSON ответа: не найден ключ 'results'.")
           return "Ошибка при разборе JSON ответа: не найден ключ 'results'."
       except Exception as e:
           logging.error(f"Непредвиденная ошибка при поиске и загрузке изображения: {e}")
           return f"Произошла непредвиденная ошибка при поиске и загрузке изображения: {e}"
