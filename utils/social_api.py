import logging
import requests
import json
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SocialAPI:
    def get_vk_feed(self):
       try:
           access_token = 'YOUR_VK_ACCESS_TOKEN' # Замените на свой access_token
           user_id = 'YOUR_VK_USER_ID' # Замените на свой user_id
           version = '5.131'
           url = 'https://api.vk.com/method/newsfeed.get'
           params = {
               'access_token': access_token,
               'filters': 'post',
               'user_id': user_id,
               'v': version,
               'count': 5
             }
           response = requests.get(url, params=params)
           response.raise_for_status()
           data = response.json()
           if "response" not in data:
                 logging.error(f"Ошибка получения ленты VK: {data.get('error', 'Неизвестная ошибка')}")
                 return f"Ошибка получения ленты VK: {data.get('error', 'Неизвестная ошибка')}"
           items = data.get("response", {}).get('items', [])
           if not items:
               return "Нет новых записей в ленте."
           result = "Лента VK:\n"
           for item in items:
              text = item.get('text', 'Без текста')
              from_id = item.get('from_id', "Неизвестно")
              date = item.get('date', "Неизвестно")
              result += f"Отправитель: {from_id} \n"
              result += f"Текст: {text} \n"
              result += f"Дата: {date} \n"
              result += '-----\n'
           return result
       except requests.exceptions.RequestException as e:
           logging.error(f"Ошибка при обращении к API VK: {e}")
           return f"Ошибка при обращении к API VK: {e}"
       except Exception as e:
            logging.error(f"Непредвиденная ошибка при получении ленты VK: {e}")
            return f"Непредвиденная ошибка при получении ленты VK: {e}"