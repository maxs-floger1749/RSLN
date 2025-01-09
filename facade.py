import logging
from assistant_core import Assistant
from data_models import UserSettings

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
class AssistantFacade:
    def __init__(self, profile='default', knowledge_file="config/knowledge.json", theme=None, language = 'ru'):
      self.assistant = Assistant(profile=profile, knowledge_file=knowledge_file, theme=theme, language = language)
      self.theme = theme
      self.language = language

    async def handle_command(self, command):
        return await self.assistant.handle_command(command)
    async def add_knowledge(self, pattern, response):
        return await self.assistant.add_knowledge(pattern, response)
    async def set_reminder(self, reminder_text, reminder_time):
       return await self.assistant.set_reminder(reminder_text, reminder_time)
    async def get_reminders(self):
      return await self.assistant.get_reminders()
    async def set_alarm(self, alarm_time):
         return await self.assistant.set_alarm(alarm_time)
    async def create_note(self, title, text):
      return await self.assistant.create_note(title, text)
    async def get_notes(self):
      return await self.assistant.get_notes()
    async def delete_note(self, title):
      return await self.assistant.delete_note(title)
    async def create_calendar_event(self, name, time):
      return await self.assistant.create_calendar_event(name, time)
    async def get_calendar_events(self):
        return await self.assistant.get_calendar_events()
    def switch_profile(self, profile):
        self.assistant.switch_profile(profile)
    def switch_language(self, language):
        self.assistant.switch_language(language)
    async def record_audio_text(self):
        return await self.assistant.record_audio_text()