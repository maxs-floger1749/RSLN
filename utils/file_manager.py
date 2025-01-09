import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FileManager:
    async def create_file(self, filepath):
        try:
           with open(filepath, 'w') as f:
               f.write("")
           return f"Файл создан: {filepath}"
        except Exception as e:
           logging.error(f"Ошибка при создании файла: {e}")
           return f"Ошибка при создании файла: {e}"
    
    async def read_file(self, filepath):
        try:
          with open(filepath, 'r') as f:
                content = f.read()
          return f"Содержание файла:\n {content}"
        except FileNotFoundError:
           logging.error(f"Файл не найден: {filepath}")
           return f"Файл не найден: {filepath}"
        except Exception as e:
            logging.error(f"Ошибка при чтении файла: {e}")
            return f"Ошибка при чтении файла: {e}"

    async def delete_file(self, filepath):
        try:
            os.remove(filepath)
            return f"Файл удален: {filepath}"
        except FileNotFoundError:
            logging.error(f"Файл не найден: {filepath}")
            return f"Файл не найден: {filepath}"
        except Exception as e:
            logging.error(f"Ошибка при удалении файла: {e}")
            return f"Ошибка при удалении файла: {e}"