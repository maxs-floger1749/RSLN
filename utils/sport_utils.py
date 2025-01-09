import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
class SportUtils:
    def analyze_training(self, training_type, distance):
        try:
           if not isinstance(distance, str) or not distance.isdigit():
               return "Неверно указана дистанция. Она должна быть цифрой"
           distance = int(distance)
           if training_type == "бег":
               calories = 100 * distance
               return f"При беге на {distance} км вы сожгли примерно {calories} калорий."
           elif training_type == "плавание":
               calories = 75 * distance
               return f"При плавании на {distance} км вы сожгли примерно {calories} калорий."
           elif training_type == "велосипед":
              calories = 50 * distance
              return f"При езде на велосипеде на {distance} км вы сожгли примерно {calories} калорий."
           else:
             return f"Тип тренировки '{training_type}' не поддерживается."
        except Exception as e:
           logging.error(f"Ошибка при анализе тренировки: {e}")
           return f"Ошибка при анализе тренировки: {e}"