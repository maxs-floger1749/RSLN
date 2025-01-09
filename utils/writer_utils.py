import logging
import enchant
from utils.text_analyzer import TextAnalyzer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WriterUtils:
    def __init__(self):
       self.text_analyzer = TextAnalyzer()
       self.dictionary = enchant.Dict("ru_RU")

    async def count_words(self, text):
        return self.text_analyzer.count_words(text)
    async def analyze_text(self, text):
        return self.text_analyzer.analyze_text(text)
    async def check_spelling(self, text):
        try:
           words = text.split()
           misspelled = [word for word in words if not self.dictionary.check(word)]
           if misspelled:
               return f"Найдены ошибки в словах: {', '.join(misspelled)}"
           else:
               return "Ошибок не найдено."
        except Exception as e:
           logging.error(f"Ошибка при проверке орфографии: {e}")
           return f"Ошибка при проверке орфографии: {e}"