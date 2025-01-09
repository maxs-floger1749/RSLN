import logging
import feedparser

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RssReader:
    def read_rss(self, url):
        try:
            feed = feedparser.parse(url)
            if feed.get('bozo') == 1:
                 logging.error(f"Ошибка при парсинге RSS: {feed.bozo_exception}")
                 return f"Ошибка при парсинге RSS: {feed.bozo_exception}"

            if not feed.entries:
               return "Нет новостей для отображения."
            result = ""
            for entry in feed.entries:
                result += f"Название: {entry.title}\n"
                result += f"Ссылка: {entry.link}\n"
                result += "---\n"
            return result
        except Exception as e:
           logging.error(f"Ошибка при чтении RSS: {e}")
           return f"Ошибка при чтении RSS: {e}"