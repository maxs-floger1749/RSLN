import logging
import json
import os
from data_models import ReminderItem
from data_models import CalendarEventItem

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DatabaseManager:
    def __init__(self, profile, reminders_file = "config/reminder_data.json", calendar_file="config/calendar_data.json"):
       self.profile = profile
       self.reminders_file = f"config/profiles/{profile}/reminder_data.json" if profile != "default" else reminders_file
       self.calendar_file = f"config/profiles/{profile}/calendar_data.json" if profile != "default" else calendar_file
       self.reminders = self._load_reminders()
       self.calendar_events = self._load_calendar_events()

    def switch_profile(self, profile):
        self.profile = profile
        self.reminders_file = f"config/profiles/{profile}/reminder_data.json" if profile != "default" else "config/reminder_data.json"
        self.calendar_file = f"config/profiles/{profile}/calendar_data.json" if profile != "default" else "config/calendar_data.json"
        self.reminders = self._load_reminders()
        self.calendar_events = self._load_calendar_events()
    def _load_reminders(self):
        try:
           if not os.path.isfile(self.reminders_file):
               logging.error(f"Файл напоминаний не найден: {self.reminders_file}")
               return []
           with open(self.reminders_file, 'r', encoding='utf-8') as f:
                reminders_data = json.load(f)
           return [ReminderItem(**item) for item in reminders_data]
        except (FileNotFoundError, json.JSONDecodeError) as e:
             logging.error(f"Ошибка загрузки напоминаний: {e}. Использую пустой список: {traceback.format_exc()}")
             return []
    def _save_reminders(self):
        try:
           with open(self.reminders_file, "w", encoding='utf-8') as f:
              json.dump([reminder.__dict__ for reminder in self.reminders], f, indent=4, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Ошибка при сохранении напоминаний: {e}")
            raise

    async def add_reminder(self, text, time):
       reminder = ReminderItem(text=text, time=time)
       self.reminders.append(reminder)
       self._save_reminders()
       logging.info(f"Напоминание добавлено: {text} на {time}")
    async def get_reminders(self):
       return self.reminders
    async def delete_reminder(self, text):
        try:
            for reminder in self.reminders:
               if reminder.text == text:
                 self.reminders.remove(reminder)
                 self._save_reminders()
                 logging.info(f"Напоминание удалено: {text}")
                 return
            logging.warning(f"Напоминание не найдено: {text}")
        except Exception as e:
             logging.error(f"Ошибка при удалении напоминания: {e}")
             raise

    def _load_calendar_events(self):
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
    def _save_calendar_events(self):
        try:
            with open(self.calendar_file, "w", encoding='utf-8') as f:
                json.dump([event.__dict__ for event in self.calendar_events], f, indent=4, ensure_ascii=False)
        except Exception as e:
             logging.error(f"Ошибка при сохранении событий календаря: {e}")
             raise

    async def add_calendar_event(self, name, time):
        event = CalendarEventItem(name=name, time=time)
        self.calendar_events.append(event)
        self._save_calendar_events()
        logging.info(f"Событие добавлено: '{name}' на {time}")
    async def get_calendar_events(self):
        return self.calendar_events
    async def delete_calendar_event(self, name):
         try:
             for event in self.calendar_events:
                if event.name == name:
                  self.calendar_events.remove(event)
                  self._save_calendar_events()
                  logging.info(f"Событие удалено: {name}")
                  return
             logging.warning(f"Событие не найдено: {name}")
         except Exception as e:
           logging.error(f"Ошибка при удалении события из календаря: {e}")
           raise