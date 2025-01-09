import logging
import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DateUtils:
   def get_current_date(self):
        try:
            now = datetime.datetime.now()
            formatted_date = now.strftime("%Y-%m-%d")
            return f"Текущая дата: {formatted_date}"
        except Exception as e:
            logging.error(f"Ошибка при получении текущей даты: {e}")
            return f"Ошибка при получении текущей даты: {e}"
   def get_formatted_date(self, date_str, input_format="%Y-%m-%d", output_format="%d-%m-%Y"):
         try:
             date_object = datetime.datetime.strptime(date_str, input_format)
             formatted_date = date_object.strftime(output_format)
             return f"Отформатированная дата: {formatted_date}"
         except ValueError as e:
             logging.error(f"Ошибка форматирования даты: {e}")
             return f"Ошибка форматирования даты: {e}. Пожалуйста, проверьте формат даты."
         except Exception as e:
            logging.error(f"Непредвиденная ошибка при форматировании даты: {e}")
            return f"Непредвиденная ошибка при форматировании даты: {e}"