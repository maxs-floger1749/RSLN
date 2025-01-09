import logging
import json
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Reminder:
    def __init__(self, profile, reminders_file="config/reminder_data.json"):
        self.profile = profile
        self.reminders_file = f"config/profiles/{profile}/reminder_data.json" if profile != "default" else reminders_file

    async def set_reminder(self, reminder_text, reminder_time):
       try:
         with open(self.reminders_file, "r") as reminder_file:
           reminders = json.load(reminder_file)
       except (FileNotFoundError, json.JSONDecodeError):
           reminders = []
       reminders.append({"text": reminder_text, "time": reminder_time})
       try:
           with open(self.reminders_file, "w") as reminder_file:
               json.dump(reminders, reminder_file, indent=4)
       except Exception as e:
          logging.error(f"Ошибка при сохранении напоминания: {e}")
          raise

    async def get_reminders(self):
        try:
            with open(self.reminders_file, "r") as reminder_file:
                 reminders = json.load(reminder_file)
            return reminders
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        except Exception as e:
            logging.error(f"Ошибка при чтении напоминаний: {e}")
            raise