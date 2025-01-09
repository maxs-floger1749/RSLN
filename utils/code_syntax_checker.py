import logging
import subprocess

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SyntaxChecker:
   def check_syntax(self, code):
        try:
            process = subprocess.Popen(['python', '-m', 'pyflakes', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate(input=code)
            if stderr:
               logging.error(f"Синтаксические ошибки:\n{stderr}")
               return f"Синтаксические ошибки:\n{stderr}"
            elif stdout:
                logging.warning(f"Предупреждения синтаксиса:\n{stdout}")
                return f"Предупреждения синтаксиса:\n{stdout}"
            else:
                logging.info("Синтаксических ошибок не найдено.")
                return "Синтаксических ошибок не найдено."
        except FileNotFoundError:
            logging.error("Утилита pyflakes не установлена. Установите её командой: pip install pyflakes")
            return "Утилита pyflakes не установлена. Установите её командой: pip install pyflakes"
        except Exception as e:
            logging.error(f"Ошибка при проверке синтаксиса: {e}")
            return f"Ошибка при проверке синтаксиса: {e}"