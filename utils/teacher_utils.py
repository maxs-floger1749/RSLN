import logging
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TeacherUtils:
    def generate_test(self, topic, questions_number=5):
      try:
          questions = {
            "Python": [
               "Что такое переменная в Python?",
               "Как создать список в Python?",
               "Что такое цикл for?",
                "Что такое функция в Python?"
              ],
            "JavaScript": [
                "Что такое DOM?",
                "Как объявить переменную в JavaScript?",
                "Что такое замыкание?",
                "Как работать с циклами?"
            ]
         }
          if topic not in questions:
             return f"Тесты по теме '{topic}' не найдены"
          test_questions = random.sample(questions[topic], min(questions_number, len(questions[topic])))
          return f"Тест по теме '{topic}':\n" + "\n".join([f"{i+1}. {q}" for i, q in enumerate(test_questions)])
      except Exception as e:
           logging.error(f"Ошибка при генерации теста: {e}")
           return f"Ошибка при генерации теста: {e}"