import logging
import wikipedia

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WikipediaSearch:
    def __init__(self, language='ru'):
        self.language = language
        wikipedia.set_lang(self.language)

    def search(self, query):
        try:
            result = wikipedia.summary(query, sentences=2)
            return result
        except wikipedia.exceptions.PageError:
            logging.error(f"Страница не найдена: {query}")
            return f"Страница не найдена: {query}"
        except wikipedia.exceptions.DisambiguationError as e:
            logging.error(f"Неоднозначный запрос: {query}. Возможные варианты: {e.options}")
            return f"Неоднозначный запрос: {query}. Попробуйте уточнить запрос."
        except Exception as e:
           logging.error(f"Ошибка поиска в Википедии: {e}")
           return f"Ошибка поиска в Википедии: {e}"
