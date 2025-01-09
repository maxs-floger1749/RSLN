import logging
import subprocess
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ProcessManager:
    async def start_process(self, process_name):
        try:
           if os.name == 'nt':
               subprocess.Popen(process_name) # Windows
           elif os.name == 'posix':
                subprocess.Popen(process_name.split()) # Linux
           return f"Процесс '{process_name}' запущен"
        except FileNotFoundError:
            logging.error(f"Программа не найдена: {process_name}")
            return f"Программа не найдена: {process_name}"
        except Exception as e:
            logging.error(f"Ошибка при запуске процесса: {e}")
            return f"Ошибка при запуске процесса: {e}"
    
    async def terminate_process(self, process_name):
        try:
            if os.name == 'nt':
                os.system(f"taskkill /im {process_name} /f") # Windows
            elif os.name == 'posix':
               os.system(f"pkill {process_name}")  # Linux
            return f"Процесс '{process_name}' завершен"
        except Exception as e:
           logging.error(f"Ошибка при завершении процесса: {e}")
           return f"Ошибка при завершении процесса: {e}"