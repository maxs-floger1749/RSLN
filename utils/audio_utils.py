import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AudioManager:
    def __init__(self):
       self.audio_dir = "audio"
       if not os.path.exists(self.audio_dir):
           os.makedirs(self.audio_dir)
    def play_audio(self, filepath):
        try:
            if os.name == 'nt':
               os.startfile(filepath) # Windows
            elif os.name == 'posix':
                os.system(f"aplay {filepath} &") # Linux
            else:
                raise NotImplementedError("Воспроизведение аудио не поддерживается в вашей ОС")
            logging.info(f"Воспроизвожу аудио: {filepath}")
            return f"Воспроизвожу аудио: {filepath}"
        except FileNotFoundError:
            logging.error(f"Аудио файл не найден: {filepath}")
            return f"Аудио файл не найден: {filepath}"
        except Exception as e:
           logging.error(f"Ошибка при воспроизведении аудио: {e}")
           return f"Ошибка при воспроизведении аудио: {e}"
    def record_audio(self, duration=5):
       pass