import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CodeEditor:
   def create_code(self, filename, code):
        try:
            if not filename.endswith(".py"):
                filename += ".py"
            filepath = os.path.join(os.getcwd(), filename)
            with open(filepath, "w", encoding='utf-8') as file:
                file.write(code)
            logging.info(f"Файл кода '{filename}' успешно создан.")
            return f"Файл кода '{filename}' успешно создан."
        except Exception as e:
            logging.error(f"Ошибка при создании файла кода: {e}")
            return f"Ошибка при создании файла кода: {e}"