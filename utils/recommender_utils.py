import logging
import random
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Recommender:
    def __init__(self):
        self.recommendations = {
           "фильмы": ["Интерстеллар", "Начало", "Драйв", "Бегущий по лезвию 2049", "Бойцовский клуб"],
           "книги": ["1984", "Мастер и Маргарита", "Скотный двор", "Вино из одуванчиков", "451 градус по Фаренгейту"],
           "музыка": ["Pink Floyd", "Radiohead", "The Beatles", "Queen", "Nirvana"]
        }
    def get_recommendation(self, topic):
         try:
           if topic not in self.recommendations:
              return f"Рекомендации по теме '{topic}' не найдены."
           return f"Рекомендации по теме '{topic}':\n" + "\n".join(random.sample(self.recommendations[topic], min(5, len(self.recommendations[topic]))))
         except Exception as e:
            logging.error(f"Ошибка при получении рекомендации: {e}")
            return f"Ошибка при получении рекомендации: {e}"