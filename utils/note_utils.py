import logging
import json
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NoteManager:
    def __init__(self, profile, notes_file="config/notes_data.json"):
        self.profile = profile
        self.notes_file = f"config/profiles/{profile}/notes_data.json" if profile != "default" else notes_file

    async def create_note(self, title, text):
       try:
            with open(self.notes_file, "r") as notes_file:
              notes = json.load(notes_file)
       except (FileNotFoundError, json.JSONDecodeError):
            notes = []
       notes.append({"title": title, "text": text})
       try:
           with open(self.notes_file, "w") as notes_file:
              json.dump(notes, notes_file, indent=4)
       except Exception as e:
          logging.error(f"Ошибка при создании заметки: {e}")
          raise

    async def get_notes(self):
        try:
           with open(self.notes_file, "r") as notes_file:
              notes = json.load(notes_file)
           return notes
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        except Exception as e:
           logging.error(f"Ошибка при чтении заметок: {e}")
           raise

    async def delete_note(self, title):
       try:
          with open(self.notes_file, "r") as notes_file:
                notes = json.load(notes_file)
          notes = [note for note in notes if note['title'] != title]
          with open(self.notes_file, "w") as notes_file:
              json.dump(notes, notes_file, indent=4)
       except Exception as e:
            logging.error(f"Ошибка при удалении заметки: {e}")
            raise