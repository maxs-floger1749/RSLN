import logging
import subprocess

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CodeRunner:
    def run_code(self, filepath):
        try:
            if not filepath.endswith(".py"):
                logging.error("Указан неверный формат файла. Должен быть .py")
                return "Указан неверный формат файла. Должен быть .py"
            process = subprocess.Popen(['python', filepath], stdout=subprocess.
PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            if stderr:
                logging.error(f"Ошибка при выполнении кода:\n{stderr}")
                return f"Ошибка при выполнении кода:\n{stderr}"
            else:
                 logging.info(f"Код успешно выполнен:\n{stdout}")
                 return f"Код успешно выполнен:\n{stdout}"
        except FileNotFoundError:
            logging.error(f"Файл не найден: {filepath}")
            return f"Файл не найден: {filepath}"
        except Exception as e:
            logging.error(f"Ошибка при выполнении кода: {e}")
            return f"Ошибка при выполнении кода: {e}"