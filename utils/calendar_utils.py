import logging
import json
import os
import datetime
from data_models import CalendarEventItem

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Calendar:
    def __init__(self, profile, calendar_file="config/calendar_data.json"):
        self.profile = profile
        self.calendar_file = f"config/profiles/{profile}/calendar_data.json" if profile != "default" else calendar_file
        self.events = self._load_events()
    def _load_events(self):
        try:
            if not os.path.isfile(self.calendar_file):
                logging.error(f"Файл календаря не найден: {self.calendar_file}")
                return []
            with open(self.calendar_file, 'r', encoding='utf-8') as f:
                calendar_data = json.load(f)
            return [CalendarEventItem(**item) for item in calendar_data]
        except (FileNotFoundError, json.JSONDecodeError) as e:
           logging.error(f"Ошибка загрузки событий календаря: {e}. Использую пустой список: {traceback.format_exc()}")
           return []
    def _save_events(self):
        try:
            with open(self.calendar_file, "w", encoding='utf-8') as f:
                json.dump([event.__dict__ for event in self.events], f, indent=4, ensure_ascii=False)
        except Exception as e:
             logging.error(f"Ошибка при сохранении событий календаря: {e}")
             raise
    async def create_calendar_event(self, name, time):
        event = CalendarEventItem(name=name, time=time)
        self.events.append(event)
        self._save_events()
        logging.info(f"Событие добавлено: '{name}' на {time}")
    async def get_calendar_events(self):
        return self.events
    async def delete_calendar_event(self, name):
         try:
             for event in self.events:
                if event.name == name:
                  self.events.remove(event)
                  self._save_events()
                  logging.info(f"Событие удалено: {name}")
                  return
             logging.warning(f"Событие не найдено: {name}")
         except Exception as e:
           logging.error(f"Ошибка при удалении события из календаря: {e}")
           raise