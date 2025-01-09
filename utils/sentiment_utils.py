import logging
from transformers import pipeline

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SentimentAnalyzer:
   def __init__(self, model_name='nlptown/bert-base-multilingual-uncased-sentiment'):
       try:
           self.sentiment_pipeline = pipeline('sentiment-analysis', model=model_name)
           logging.info(f"Модель анализа тональности '{model_name}' успешно загружена.")
       except Exception as e:
            logging.error(f"Ошибка при загрузке модели анализа тональности: {e}")
            self.sentiment_pipeline = None

   def analyze_sentiment(self, text):
        try:
            if not self.sentiment_pipeline:
               logging.error("Модель анализа тональности не загружена.")
               return "Модель анализа тональности не загружена."
            result = self.sentiment_pipeline(text)[0]
            return f"Тональность текста: {result['label']} (Уверенность: {result['score']:.4f})"
        except Exception as e:
            logging.error(f"Ошибка при анализе тональности: {e}")
            return f"Ошибка при анализе тональности: {e}"