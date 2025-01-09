import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LanguageUtils:
    def __init__(self, language='ru'):
        self.language = language
        self.spacy_model = self._get_spacy_model()

    def set_language(self, language):
        if language in ["ru", "en"]:
           self.language = language
           self.spacy_model = self._get_spacy_model()
        else:
          logging.error("Неподдерживаемый язык")

    def get_language(self):
        return self.language
    def get_spacy_model(self):
       return self.spacy_model
    def _get_spacy_model(self):
        if self.language == "ru":
            return "ru_core_news_sm"
        elif self.language == "en":
            return "en_core_web_sm"
        else:
            logging.error("Неподдерживаемый язык. Использую 'ru_core_news_sm'")
            return "ru_core_news_sm"