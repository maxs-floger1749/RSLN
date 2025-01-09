from dataclasses import dataclass

@dataclass
class ReminderItem:
    text: str
    time: str
@dataclass
class NoteItem:
    title: str
    text: str
@dataclass
class CalendarEventItem:
    name: str
    time: str

@dataclass
class UserSettings:
    last_profile: str = "default"
    theme: str = "light"
    language: str = "ru"