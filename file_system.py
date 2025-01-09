import logging
import os
import shutil

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FileSystem:
    def create_file(self, filepath):
        try:
           os.makedirs(os.path.dirname(filepath), exist_ok=True)
           with open(filepath, 'w', encoding='utf-8') as f:
               pass
           logging.info(f"Файл '{filepath}' успешно создан.")
        except Exception as e:
           logging.error(f"Ошибка при создании файла: {e}")
           raise
    def read_file(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
               content = f.read()
            logging.info(f"Файл '{filepath}' успешно прочитан.")
            return content
        except FileNotFoundError:
            logging.error(f"Файл не найден: {filepath}")
            raise
        except Exception as e:
           logging.error(f"Ошибка при чтении файла: {e}")
           raise

    def delete_file(self, filepath):
        try:
            if os.path.isfile(filepath):
                os.remove(filepath)
            elif os.path.isdir(filepath):
                 shutil.rmtree(filepath)
            else:
                logging.error(f"Файл не найден: {filepath}")
                raise FileNotFoundError(f"Файл не найден: {filepath}")
            logging.info(f"Файл '{filepath}' успешно удален.")
        except FileNotFoundError:
             logging.error(f"Файл не найден: {filepath}")
             raise
        except Exception as e:
            logging.error(f"Ошибка при удалении файла: {e}")
            raise