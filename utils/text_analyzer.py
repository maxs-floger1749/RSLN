import logging
import spacy
from collections import Counter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TextAnalyzer:
    def __init__(self, language = "ru_core_news_sm"):
      self.nlp = spacy.load(language)
    def count_words(self, text):
        try:
            doc = self.nlp(text)
            words = [token.text for token in doc if token.is_alpha]
            word_counts = Counter(words)
            return f"Количество слов: {len(words)} \nУникальных слов: {len(word_counts)} \n{word_counts}"
        except Exception as e:
           logging.error(f"Ошибка при подсчете слов: {e}")
           return f"Ошибка при подсчете слов: {e}"

    def analyze_text(self, text):
        try:
           doc = self.nlp(text)
           sentences = [sent.text for sent in doc.sents]
           tokens = [token.text for token in doc]
           lemmas = [token.lemma_ for token in doc]
           pos = [(token.text, token.pos_) for token in doc]
           return f"Анализ текста:\n предложения: {sentences} \n токены: {tokens} \n леммы: {lemmas} \n части речи: {pos}"
        except Exception as e:
            logging.error(f"Ошибка анализа текста: {e}")
            return f"Ошибка анализа текста: {e}"