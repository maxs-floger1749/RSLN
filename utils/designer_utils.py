import logging
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DesignerUtils:
    def get_colors_by_theme(self, theme):
        try:
            url = f"http://colormind.io/api/"
            data = {'model': 'default'}
            response = requests.post(url, json=data)
            response.raise_for_status()
            colors = response.json()['result']
            return f"Цвета для темы '{theme}':\n {', '.join([f'rgb({int(c[0])}, {int(c[1])}, {int(c[2])})' for c in colors])}"
        except requests.exceptions.RequestException as e:
             logging.error(f"Ошибка при запросе цветовой схемы: {e}")
             return f"Ошибка при запросе цветовой схемы: {e}"
        except Exception as e:
           logging.error(f"Непредвиденная ошибка при получении цветовой схемы: {e}")
           return f"Непредвиденная ошибка при получении цветовой схемы: {e}"