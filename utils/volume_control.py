import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class VolumeControl:
    async def increase_volume(self):
        try:
            if os.name == 'nt':
                import ctypes
                ctypes.windll.winmm.keybd_event(0xAF, 0, 1, 0) # увеличить
                ctypes.windll.winmm.keybd_event(0xAF, 0, 3, 0)
            elif os.name == 'posix':
                 os.system("amixer set Master 5%+") # Linux
            return "Громкость увеличена"
        except Exception as e:
           logging.error(f"Ошибка при увеличении громкости: {e}")
           return f"Ошибка при увеличении громкости: {e}"
    async def decrease_volume(self):
        try:
            if os.name == 'nt':
                import ctypes
                ctypes.windll.winmm.keybd_event(0xAE, 0, 1, 0) # уменьшить
                ctypes.windll.winmm.keybd_event(0xAE, 0, 3, 0)
            elif os.name == 'posix':
                os.system("amixer set Master 5%-")  # Linux
            return "Громкость уменьшена"
        except Exception as e:
            logging.error(f"Ошибка при уменьшении громкости: {e}")
            return f"Ошибка при уменьшении громкости: {e}"