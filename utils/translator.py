import logging
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Translator:
    def __init__(self, yandex_api_key):
        self.yandex_api_key = yandex_api_key

    def translate(self, text, lang='en-ru'):
        url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
        if not self.yandex_api_key:
             logging.error("API-ключ Яндекс.Переводчика не найден.")
             return "API-ключ Яндекс.Переводчика не найден. Установите переменную окружения 'YANDEX_API_KEY' или передайте его через командную строку."
        if not text:
            logging.warning("Пожалуйста, скажите текст для перевода.")
            return "Пожалуйста, скажите текст для перевода."

        params = {
            'key': self.yandex_api_key,
            'text': text,
            'lang': lang
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            r = response.json()
            if "text" in r and r["text"]:
                return r["text"][0]
            else:
                logging.error("Ошибка в ответе API: не найден текст перевода.")
                return "Ошибка в получении перевода."
        except requests.exceptions.RequestException as e:
           logging.error(f"Ошибка обращения к сервису перевода: {str(e)}")
           return f"Ошибка обращения к сервису перевода: {str(e)}"
        except KeyError:
           logging.error("Ошибка при разборе JSON ответа: не найден ключ 'text'.")
           return "Ошибка в получении перевода."
        except Exception as e:
           logging.error(f"Непредвиденная ошибка: {str(e)}")
           return f"Произошла непредвиденная ошибка: {str(e)}"
