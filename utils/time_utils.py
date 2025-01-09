import logging
import datetime
import pytz

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TimeZoneManager:
    def get_current_time(self, timezone_name="UTC"):
        try:
            tz = pytz.timezone(timezone_name)
            current_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %Z%z")
            return f"Текущее время в {timezone_name}: {current_time}"
        except pytz.exceptions.UnknownTimeZoneError:
            logging.error(f"Неверный часовой пояс: {timezone_name}")
            return f"Неверный часовой пояс: {timezone_name}. Пожалуйста, выберите часовой пояс из списка pytz.all_timezones"
        except Exception as e:
            logging.error(f"Ошибка при получении времени: {e}")
            return f"Ошибка при получении времени: {e}"