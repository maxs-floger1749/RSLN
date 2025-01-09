import logging
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MovieInfo:
   def get_movie_description(self, title):
        try:
            api_key = "YOUR_OMDB_API_KEY" # Укажите свой API-ключ OMDb
            url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}&plot=full&r=json&lang=ru"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data.get('Response') == 'True':
                 plot = data.get('Plot', "Описание не найдено.")
                 return f"Описание фильма '{title}':\n{plot}"
            else:
                logging.error(f"Фильм '{title}' не найден: {data.get('Error')}")
                return f"Фильм '{title}' не найден: {data.get('Error')}"
        except requests.exceptions.RequestException as e:
            logging.error(f"Ошибка обращения к сервису OMDb: {e}")
            return f"Ошибка обращения к сервису OMDb: {e}"
        except KeyError:
            logging.error("Ошибка при разборе JSON ответа: не найден ключ 'Plot'.")
            return "Ошибка при разборе JSON ответа: не найден ключ 'Plot'."
        except Exception as e:
            logging.error(f"Непредвиденная ошибка при поиске фильма: {e}")
            return f"Произошла непредвиденная ошибка при поиске фильма: {e}"