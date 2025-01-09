import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PersonalityUtils:
   def get_personality_type(self, user_type):
         try:
            if user_type == "экстраверт":
               return "Экстраверты любят быть в центре внимания, общаться и действовать в команде."
            elif user_type == "интроверт":
               return "Интроверты предпочитают уединение и размышления, а также глубокую работу над узким кругом задач."
            else:
              return "Неизвестный тип личности"
         except Exception as e:
            logging.error(f"Ошибка при определении типа личности: {e}")
            return f"Ошибка при определении типа личности: {e}"