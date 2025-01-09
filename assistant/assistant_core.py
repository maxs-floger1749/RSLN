import logging
import random
import time
import re
import json
import datetime
import signal
import argparse
import os
import traceback
import locale
import asyncio
from collections import deque
from concurrent.futures import ThreadPoolExecutor
import sys
import requests
import speech_recognition as sr
import webbrowser
import wikipedia
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import subprocess
import os
from PIL import Image
from io import BytesIO
import vlc
from utils.translator import Translator
from utils.calculator import Calculator
from utils.browser_utils import Browser
from utils.wikipedia_utils import WikipediaSearch
from utils.weather_utils import Weather
from utils.image_utils import ImageDownloader
from utils.reminder_utils import Reminder
from utils.note_utils import NoteManager
from utils.file_manager import FileManager
from utils.process_manager import ProcessManager
from utils.volume_control import VolumeControl
from utils.calendar_utils import Calendar
from utils.rss_reader import RssReader
from utils.math_utils import MathSolver
from utils.finance_utils import FinancialAnalyst
from utils.time_utils import TimeZoneManager
from utils.audio_utils import AudioManager
from utils.movie_utils import MovieInfo
import keyboard
from utils.code_editor import CodeEditor
from utils.code_runner import CodeRunner
from utils.code_syntax_checker import SyntaxChecker
from utils.code_generator import CodeGenerator
from utils.database_manager import DatabaseManager
from utils.language_utils import LanguageUtils
from utils.llm_utils import LargeLanguageModel
from utils.image_generator import ImageGenerator
from utils.social_api import SocialAPI
from utils.planner_utils import Planner
from utils.sentiment_utils import SentimentAnalyzer
from utils.recommender_utils import Recommender
from utils.visualization_utils import DataVisualizer
from utils.api_handler import APIHandler
from utils.math_engine_factory import MathEngineFactory
from command_strategies import CommandStrategyManager
from file_system import FileSystem
from observer import EventObserver
import spacy
import torch
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Assistant:
    def __init__(self, profile, knowledge_file="config/knowledge.json", max_questions=10, max_workers=5, encoding=None,
                 yandex_api_key=None, speech_timeout=5, speech_phrase_limit=10, wikipedia_language='ru', theme = None, language = 'ru'):
        self.profile = profile
        self.knowledge_file = f"config/profiles/{profile}/knowledge.json" if profile != "default" else knowledge_file
        self.knowledge_base = self._load_knowledge(self.knowledge_file, encoding)
        self.jokes = [
            "Почему программисты любят пасхальные яйца? Потому что в них много битов!",
            "Приходит программист в аптеку и спрашивает: 'У вас есть что-нибудь от кашля?' На что аптекарь отвечает: 'Да, можем вам продать глушитель.'",
        ]
        self.greetings = ["Привет!", "Здравствуйте!", "Здравствуй!"]
        self.farewells = ["До свидания!", "Пока!", "Всего хорошего!"]
        self.default_response = "Извини, я не понимаю."
        self.response_history = deque(maxlen=5)
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.question_queue = deque(maxlen=max_questions)
        self._shutdown_flag = False
        self.encoding = encoding if encoding else locale.getpreferredencoding()
        self._event_loop = asyncio.get_event_loop()
        self._signal_handler_task = None
        self._lock = asyncio.Lock()
        self.yandex_api_key = yandex_api_key if yandex_api_key else os.getenv('YANDEX_API_KEY')
        self.wolfram_api_key = os.getenv('WOLFRAM_API_KEY')
        self.speech_timeout = speech_timeout
        self.speech_phrase_limit = speech_phrase_limit
        self.wikipedia_language = wikipedia_language
        self.translator = Translator(self.yandex_api_key)
        self.calculator = Calculator()
        self.browser = Browser()
        self.wikipedia_search = WikipediaSearch(self.wikipedia_language)
        self.weather = Weather()
        self.image_downloader = ImageDownloader()
        self.reminder = Reminder(profile=self.profile)
        self.note_manager = NoteManager(profile=self.profile)
        self.file_manager = FileManager(FileSystem())
        self.process_manager = ProcessManager()
        self.volume_control = VolumeControl()
        self.calendar = Calendar(profile = self.profile)
        self.rss_reader = RssReader()
        self.math_solver = MathSolver()
        self.financial_analyst = FinancialAnalyst()
        self.time_manager = TimeZoneManager()
        self.audio_manager = AudioManager()
        self.movie = MovieInfo()
        self.code_editor = CodeEditor()
        self.code_runner = CodeRunner()
        self.code_syntax_checker = SyntaxChecker()
        self.code_generator = CodeGenerator()
        self.database_manager = DatabaseManager(profile=self.profile)
        self.language_utils = LanguageUtils(language=language)
        self.llm = LargeLanguageModel()
        self.image_generator = ImageGenerator()
        self.social_api = SocialAPI()
        self.planner = Planner(database_manager=self.database_manager)
        self.sentiment_analyzer = SentimentAnalyzer()
        self.recommender = Recommender()
        self.visualizer = DataVisualizer()
        self.api_handler = APIHandler()
        self.math_engine_factory = MathEngineFactory(self.wolfram_api_key)
        self.command_strategy_manager = CommandStrategyManager(self)
        self.observer = EventObserver()
        self.nlp = spacy.load(self.language_utils.get_spacy_model())
        self.math_adapter = None
        if torch.cuda.is_available():
            logging.info("GPU is available, using cuda for LLM.")
            self.llm.use_cuda()
        else:
           logging.info("GPU is not available, using CPU for LLM")

    def _load_knowledge(self, knowledge_file, encoding=None):
        try:
            if not os.path.isfile(knowledge_file):
                logging.error(f"Файл базы знаний не найден: {knowledge_file}")
                return {}
            with open(knowledge_file, "r", encoding=encoding if encoding else locale.getpreferredencoding()) as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"Ошибка загрузки базы знаний: {e}. Использую пустую базу: {traceback.format_exc()}")
            return {}
    def _set_math_engine(self, engine_type = "sympy"):
        self.math_adapter = self.math_engine_factory.create_engine(engine_type)
        if not self.math_adapter:
            self.speak(f"Не могу установить движок {engine_type}")

    def speak(self, message: str, asynchronous=False) -> None:
        if not message:
            return
        def _speak():
            try:
                logging.info(f'Говорю: {message}')
                print(message)
                time.sleep(1)
                self.response_history.append(message)
            except Exception as e:
                logging.error(f'Ошибка при выводе сообщения: {e}: {traceback.format_exc()}')
        if asynchronous:
            self._event_loop.run_in_executor(self.executor, _speak)
        else:
            _speak()

    async def _listen_async(self) -> str:
       try:
           logging.info("Начинаю слушать")
           return await self._event_loop.run_in_executor(None, self._recognize_speech)
       except EOFError:
           logging.warning("Получен EOF. Инициирую завершение...")
           self._shutdown_flag = True
           return ""
       except KeyboardInterrupt:
            logging.warning("Получен KeyboardInterrupt. Инициирую завершение...")
            self._shutdown_flag = True
            return ""
       except Exception as e:
           logging.error(f"Ошибка прослушивания ввода: {e}: {traceback.format_exc()}")
           return ""

    def _recognize_speech(self, language: str = 'ru-RU') -> str:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            logging.info("Начинаю прослушивание...")
            try:
                audio = recognizer.listen(source, timeout=self.speech_timeout, phrase_time_limit=self.speech_phrase_limit)
            except sr.WaitTimeoutError:
                logging.warning("Время ожидания прослушивания истекло.")
                return ""
            except Exception as e:
                logging.error(f"Ошибка при прослушивании: {e}")
                return ""
        try:
            text = recognizer.recognize_google(audio, language=language)
            logging.info(f"Распознанный текст: {text}")
            return text
        except sr.UnknownValueError:
            logging.error("Не удалось распознать речь.")
            return ""
        except sr.RequestError as e:
            logging.error(f"Ошибка обращения к сервису распознавания: {e}")
            return ""
        except Exception as e:
            logging.error(f"Непредвиденная ошибка при распознавании: {e}")
            return ""

    async def handle_command(self, command: str) -> str:
       if not command or self._shutdown_flag:
            return None
       try:
            strategy = self.command_strategy_manager.get_strategy(command)
            if strategy:
                result = await strategy.execute(command)
                return result
            else:
              for pattern, response_function in self.knowledge_base.items():
                   match = pattern.match(command)
                   if match:
                      response = response_function(match)
                      self.speak(response)
                      return response
              self.speak(self.default_response)
              return self.default_response
       except Exception as e:
           logging.error(f"Ошибка обработки команды: {e}: {traceback.format_exc()}")
           error_message = "Извини, произошла ошибка при обработке команды."
           self.speak(error_message)
           return error_message

    async def add_knowledge(self, pattern, response):
        try:
            self.knowledge_base[re.compile(pattern, re.IGNORECASE)] = lambda match: response
            self._save_knowledge()
        except Exception as e:
            logging.error(f"Ошибка при добавлении знаний: {e}")
            raise
    
    def add_knowledge_from_question(self, question):
        try:
          pattern = question.strip()
          response = self.default_response
          self.knowledge_base[re.compile(pattern, re.IGNORECASE)] = lambda match: response
          self._save_knowledge()
        except Exception as e:
            logging.error(f"Ошибка при добавлении знаний: {e}")
            raise

    def _save_knowledge(self):
        try:
           with open(self.knowledge_file, "w", encoding=self.encoding) as f:
              json.dump(
                {p.pattern: r for p, r in self.knowledge_base.items()}, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Ошибка при сохранении базы знаний: {e}")

    def view_image(self, filepath):
        try:
            if os.name == 'nt':
                os.startfile(filepath)  # Windows
            elif os.name == 'posix':
               subprocess.Popen(['xdg-open', filepath]) # Linux
            else:
                raise NotImplementedError("Просмотр изображений не поддерживается в вашей ОС")
        except Exception as e:
            logging.error(f"Ошибка при открытии изображения: {e}")
            raise

    async def send_email(self, recipient, subject, message):
        try:
            with open("config/email_config.json", "r") as config_file:
                email_config = json.load(config_file)
            sender_email = email_config['sender_email']
            sender_password = email_config['sender_password']
            smtp_server = email_config['smtp_server']
            smtp_port = email_config['smtp_port']
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
                logging.info(f"Email отправлен на {recipient}")
        except Exception as e:
           logging.error(f"Ошибка при отправке Email: {e}")
           raise

    async def set_reminder(self, reminder_text, reminder_time):
        try:
            await self.database_manager.add_reminder(reminder_text, reminder_time)
        except Exception as e:
           logging.error(f"Ошибка при установке напоминания: {e}")
           raise

    async def get_reminders(self):
       try:
           return await self.database_manager.get_reminders()
       except Exception as e:
          logging.error(f"Ошибка при получении напоминаний: {e}")
          raise
    async def set_alarm(self, alarm_time):
        try:
            while True:
                current_time = datetime.datetime.now().strftime("%H:%M")
                if current_time == alarm_time:
                   logging.info("Время будильника пришло!")
                   self.speak("Время будильника пришло!")
                   self.play_notification_sound()
                   break
                await asyncio.sleep(60)
        except Exception as e:
            logging.error(f"Ошибка при установке будильника: {e}")
            raise
    def play_notification_sound(self):
        try:
            if os.name == 'nt':
                import winsound
                winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
            elif os.name == 'posix':
                os.system("aplay /usr/share/sounds/freedesktop/stereo/complete.oga &")  # Linux
        except Exception as e:
            logging.error(f"Ошибка при воспроизведении звука: {e}")

    def play_music(self, filepath):
        try:
            instance = vlc.Instance()
            media = instance.media_new(filepath)
            player = instance.media_player_new()
            player.set_media(media)
            player.play()
        except Exception as e:
            logging.error(f"Ошибка при воспроизведении музыки: {e}")
            raise

    async def create_note(self, title, text):
        try:
           await self.note_manager.create_note(title, text)
        except Exception as e:
           logging.error(f"Ошибка при создании заметки: {e}")
           raise

    async def get_notes(self):
        try:
           return await self.note_manager.get_notes()
        except Exception as e:
           logging.error(f"Ошибка при чтении заметок: {e}")
           raise

    async def delete_note(self, title):
        try:
           await self.note_manager.delete_note(title)
        except Exception as e:
           logging.error(f"Ошибка при удалении заметки: {e}")
           raise
    def change_layout(self):
       try:
           keyboard.send("shift+alt")
       except Exception as e:
          logging.error(f"Ошибка при переключении раскладки: {e}")
          raise
    def switch_profile(self, profile):
        self.profile = profile
        self.knowledge_file = f"config/profiles/{profile}/knowledge.json" if profile != "default" else "config/knowledge.json"
        self.knowledge_base = self._load_knowledge(self.knowledge_file, self.encoding)
        self.reminder.reminders_file = f"config/profiles/{profile}/reminder_data.json" if profile != "default" else "config/reminder_data.json"
        self.note_manager.notes_file = f"config/profiles/{profile}/notes_data.json" if profile != "default" else "config/notes_data.json"
        self.calendar.calendar_file = f"config/profiles/{profile}/calendar_data.json" if profile != "default" else "config/calendar_data.json"
        self.database_manager.switch_profile(profile)
    def switch_language(self, language):
      self.language_utils.set_language(language)
      self.nlp = spacy.load(self.language_utils.get_spacy_model())

    async def record_audio_text(self, language = None):
      if language is None:
        language = self.language_utils.get_language()
      recognizer = sr.Recognizer()
      try:
          with sr.Microphone() as source:
               logging.info("Начинаю запись...")
               audio = recognizer.listen(source, phrase_time_limit=10)
          logging.info("Запись завершена")
          filename = os.path.join(self.audio_manager.audio_dir, f"recorded_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.wav")
          with open(filename, 'wb') as f:
                f.write(audio.get_wav_data())
          try:
             text = recognizer.recognize_google(audio, language=language)
             logging.info(f"Распознанный текст: {text}")
             return filename
          except sr.UnknownValueError:
               logging.error("Не удалось распознать речь.")
               return None
          except sr.RequestError as e:
             logging.error(f"Ошибка обращения к сервису распознавания: {e}")
             return None
          except Exception as e:
               logging.error(f"Непредвиденная ошибка при распознавании: {e}")
               return None
      except Exception as e:
            logging.error(f"Ошибка при записи аудио: {e}")
            return None
