import logging
import webbrowser
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Browser:
    def __init__(self):
        self.sites = {
            "https://vk.com": ["vk", "вк"],
            "https://www.youtube.com/": ['youtube', 'ютуб'],
            "https://ru.wikipedia.org": ["вики", "wiki"],
            "https://ru.aliexpress.com": ['али', 'ali', 'aliexpress', 'алиэспресс'],
            "http://google.com": ['гугл', 'google'],
            "https://www.amazon.com": ['амазон', 'amazon'],
            "https://www.apple.com/ru": ['apple', 'эпл'],
             "https://telete.in/gurupython": ['пайтонгуру', 'pythonguru']
        }

    def open_url(self, command):
        if not command:
           logging.warning("Пустая команда")
           return "Пожалуйста, скажите название сайта или URL."

        url = command.split()[-1].lower()
        if self.is_valid_url(url):
           try:
              webbrowser.open_new_tab(url)
              return f"Открываю URL: {url}"
           except webbrowser.Error as e:
              logging.error(f"Ошибка открытия URL {url}: {e}")
              return f"Ошибка открытия URL {url}: {e}"
        else:
           for site_url, keywords in self.sites.items():
                if any(keyword in url for keyword in keywords):
                    try:
                        webbrowser.open_new_tab(site_url)
                        return f"Открываю сайт: {site_url}"
                    except webbrowser.Error as e:
                       logging.error(f"Ошибка открытия сайта {site_url}: {e}")
                       return f"Ошибка открытия сайта {site_url}: {e}"
        logging.warning(f"Сайт или URL не распознаны: {command}")
        return "Сайт или URL не распознаны."
    
    def is_valid_url(self, url):
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE
        )
        return bool(regex.match(url))
