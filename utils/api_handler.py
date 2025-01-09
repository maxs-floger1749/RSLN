import logging
import requests
import json
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class APIHandler:
    def make_api_call(self, url, method='GET', headers=None, data=None):
        try:
           if method.upper() == 'GET':
                response = requests.get(url, headers=headers)
           elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data)
           elif method.upper() == 'PUT':
                response = requests.put(url, headers=headers, json=data)
           elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=headers)
           else:
             logging.error(f"Неподдерживаемый HTTP метод: {method}")
             return f"Неподдерживаемый HTTP метод: {method}"
           response.raise_for_status()
           if 'application/json' in response.headers.get('Content-Type', ''):
              return response.json()
           return response.text
        except requests.exceptions.RequestException as e:
            logging.error(f"Ошибка при обращении к API: {e}")
            return f"Ошибка при обращении к API: {e}"
        except Exception as e:
            logging.error(f"Непредвиденная ошибка при выполнении запроса к API: {e}")
            return f"Непредвиденная ошибка при выполнении запроса к API: {e}"