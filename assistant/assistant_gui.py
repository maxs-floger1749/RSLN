import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog, filedialog, ttk, Text
import asyncio
import logging
import threading
from facade import AssistantFacade
import os
import time
import pyperclip
import subprocess
import json
from data_models import UserSettings
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='assistant.log')


class AssistantGUI:
    def __init__(self, master):
        self.master = master
        master.title("Голосовой ассистент")
        master.geometry("800x700")  # Увеличенный размер окна
        self.user_settings = self.load_settings()
        self.current_profile = self.user_settings.last_profile
        self.facade = AssistantFacade(profile=self.current_profile, theme=self.user_settings.theme, language = self.user_settings.language)
        self.apply_theme()
        self.is_recording = False

        self.progress_bar = ttk.Progressbar(master, orient=tk.HORIZONTAL, length=200, mode='indeterminate')
        self.progress_bar.pack(pady=5)

        self.output_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, height=20, width=100)
        self.output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.output_text.config(state=tk.DISABLED)
        
        self.text_input_frame = tk.Frame(master)
        self.text_input_frame.pack(padx=10, pady=5, fill=tk.X)

        self.text_input_text = Text(self.text_input_frame, height=5, width=80)
        self.text_input_text.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
       
        self.send_button = tk.Button(self.text_input_frame, text="Отправить", command=self.on_send)
        self.send_button.pack(side=tk.RIGHT, padx=5)
        self.record_button = tk.Button(self.text_input_frame, text="Начать запись", command=self.on_record)
        self.record_button.pack(side=tk.RIGHT, padx=5)

        self.menu_frame = tk.Frame(master)
        self.menu_frame.pack(pady=5, fill=tk.X)

        self.create_menu_buttons()
    def load_settings(self):
        try:
           with open("config/settings.json", "r") as f:
               settings_data = json.load(f)
           return UserSettings(**settings_data)
        except (FileNotFoundError, json.JSONDecodeError):
           return UserSettings()
    def save_settings(self):
        with open("config/settings.json", "w") as f:
           json.dump(self.user_settings.__dict__, f, indent=4)

    def apply_theme(self):
        theme = self.user_settings.theme
        if theme == "dark":
            self.master.config(bg="#2e2e2e")
            self.output_text.config(bg="#3e3e3e", fg="white", insertbackground="white")
            self.text_input_frame.config(bg="#2e2e2e")
            self.text_input_text.config(bg="#3e3e3e", fg="white", insertbackground="white")
        elif theme == "light":
            self.master.config(bg="white")
            self.output_text.config(bg="white", fg="black", insertbackground="black")
            self.text_input_frame.config(bg="white")
            self.text_input_text.config(bg="white", fg="black", insertbackground="black")
    def create_menu_buttons(self):
        buttons = [
            ("Погода", self.on_weather),
            ("Википедия", self.on_wikipedia),
            ("Калькулятор", self.on_calculator),
            ("Перевод", self.on_translate),
            ("Открыть сайт", self.on_browser),
             ("Открыть URL", self.on_open_url),
             ("Сгенерировать текст", self.on_generate_text),
              ("Сгенерировать изображение", self.on_generate_image),
            ("Добавить знания", self.on_add_knowledge),
             ("Напоминания", self.on_reminders),
             ("Будильник", self.on_alarm),
            ("Таймер", self.on_timer),
            ("Музыка", self.on_play_music),
            ("Поиск картинки", self.on_search_image),
            ("Заметки", self.on_notes),
             ("Файлы", self.on_file_manager),
             ("Процессы", self.on_process_manager),
            ("Громкость", self.on_volume_control),
            ("Календарь", self.on_calendar),
            ("RSS", self.on_rss),
            ("Время", self.on_time),
              ("Фильмы", self.on_movie),
              ("Аудио", self.on_audio),
               ("Код", self.on_code),
              ("JSON", self.on_json),
               ("Анализ текста", self.on_text_analysis),
                ("Конвертация", self.on_unit_convert),
                ("Местоположение", self.on_geolocation),
                ("Соцсети", self.on_social),
                 ("Программист", self.on_programmer),
                 ("Писатель", self.on_writer),
                  ("Менеджер", self.on_manager),
                   ("Врач", self.on_doctor),
                  ("Учитель", self.on_teacher),
                 ("Дизайнер", self.on_designer),
                   ("Спортсмен", self.on_sportsman),
                    ("Планирование", self.on_planner),
                     ("Тональность", self.on_sentiment),
                      ("Рекомендации", self.on_recommendation),
                       ("Визуализация", self.on_visualization),
              ("Тема", self.on_theme),
               ("Язык", self.on_language),
             ("Профиль", self.on_profile)
        ]
        for text, command in buttons:
            button = tk.Button(self.menu_frame, text=text, command=command)
            button.pack(side=tk.LEFT, padx=5)

    def update_output(self, message):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.config(state=tk.DISABLED)
        self.output_text.see(tk.END)
    def show_message_popup(self, title, message):
        messagebox.showinfo(title, message)
    def on_send(self, event=None):
        command = self.text_input_text.get("1.0", tk.END).strip()
        if command:
          self.text_input_text.delete("1.0", tk.END)
          self.run_command(command)
    def on_record(self):
        if not self.is_recording:
            self.is_recording = True
            self.record_button.config(text="Остановить запись")
            self.text_input_text.config(state=tk.DISABLED)
            threading.Thread(target=self.record_audio).start()
        else:
            self.is_recording = False
            self.record_button.config(text="Начать запись")
            self.text_input_text.config(state=tk.NORMAL)

    def record_audio(self):
        try:
            filepath = asyncio.run(self.facade.record_audio_text())
            if filepath:
              self.run_command(f"воспроизвести аудио {filepath}")
        except Exception as e:
           logging.error(f"Ошибка при записи и распознавании аудио: {e}")
           self.update_output(f"Ошибка при записи и распознавании аудио: {e}")
    def on_weather(self):
        city = simpledialog.askstring("Ввод", "Введите город:")
        if city:
            self.run_command(f"какая погода {city}")

    def on_wikipedia(self):
        query = simpledialog.askstring("Ввод", "Введите запрос для Википедии:")
        if query:
            self.run_command(f"найди в википедии {query}")

    def on_calculator(self):
        expression = simpledialog.askstring("Ввод", "Введите математическое выражение:")
        if expression:
            self.run_command(f"вычислить {expression}")

    def on_translate(self):
        text = simpledialog.askstring("Ввод", "Введите текст для перевода:")
        if text:
            language_pair = simpledialog.askstring("Ввод", "Введите пару языков (например, 'en-ru'):", initialvalue='en-ru')
            if language_pair:
              self.run_command(f"переведи {text} {language_pair}")

    def on_browser(self):
       site = simpledialog.askstring("Ввод", "Введите название сайта (например, 'открой google'):")
       if site:
          self.run_command(site)

    def on_open_url(self):
        url = simpledialog.askstring("Ввод", "Введите URL:")
        if url:
           self.run_command(f"открой url {url}")
    def on_generate_text(self):
       prompt = simpledialog.askstring("Ввод", "Введите текст запроса для генерации:")
       if prompt:
          self.run_command(f"сгенерировать текст {prompt}")
    def on_generate_image(self):
        prompt = simpledialog.askstring("Ввод", "Введите текст запроса для генерации изображения:")
        if prompt:
            self.run_command(f"сгенерировать изображение {prompt}")

    def on_add_knowledge(self):
        pattern = simpledialog.askstring("Ввод", "Введите паттерн (например, 'привет'):")
        if pattern:
           response = simpledialog.askstring("Ввод", "Введите ответ (например, 'Привет!')")
           if response:
                asyncio.run(self.facade.add_knowledge(pattern, response))
                self.update_output("Знание добавлено.")

    def on_view_image(self):
        filepath = filedialog.askopenfilename(title="Выберите файл изображения")
        if filepath:
            self.run_command(f"просмотри изображение {filepath}")
    def on_unit_convert(self):
       command = simpledialog.askstring("Ввод", "Введите команду конвертации (например 'конвертировать температуру 25 celsius fahrenheit')")
       if command:
           self.run_command(command)
    def on_text_analysis(self):
       command = simpledialog.askstring("Ввод", "Введите команду анализа текста (например 'подсчитать слова текст для анализа')")
       if command:
           self.run_command(command)
    def on_json(self):
        command = simpledialog.askstring("Ввод", "Введите команду для работы с JSON (например, 'форматировать json {\"key\": \"value\"}')")
        if command:
            self.run_command(command)
    def on_code(self):
       command = simpledialog.askstring("Ввод", "Введите команду для работы с кодом (например 'создать код test.py print(\"hello\")')")
       if command:
          self.run_command(command)
    def on_geolocation(self):
        command = simpledialog.askstring("Ввод", "Введите команду для работы с геолокацией (например 'поиск поблизости аптеки 55.75,37.61')")
        if command:
            self.run_command(command)
    def on_social(self):
        command = simpledialog.askstring("Ввод", "Введите команду для работы с соцсетями (например, 'получить ленту вк')")
        if command:
           self.run_command(command)
    def on_programmer(self):
       command = simpledialog.askstring("Ввод", "Введите команду для программиста (например 'создать класс Person')")
       if command:
           self.run_command(command)
    def on_writer(self):
        command = simpledialog.askstring("Ввод", "Введите команду для писателя (например 'проверить плагиат текст')")
        if command:
           self.run_command(command)
    def on_manager(self):
        command = simpledialog.askstring("Ввод", "Введите команду для менеджера (например 'создать отчет по проекту Project1')")
        if command:
           self.run_command(command)
    def on_doctor(self):
        command = simpledialog.askstring("Ввод", "Введите команду для врача (например 'анализ симптомов температура, кашель, насморк')")
        if command:
            self.run_command(command)
    def on_teacher(self):
        command = simpledialog.askstring("Ввод", "Введите команду для учителя (например 'сгенерировать тест по теме Python')")
        if command:
            self.run_command(command)
    def on_designer(self):
       command = simpledialog.askstring("Ввод", "Введите команду для дизайнера (например, 'цвета для сайта про космос')")
       if command:
          self.run_command(command)
    def on_sportsman(self):
        command = simpledialog.askstring("Ввод", "Введите команду для спортсмена (например, 'анализ тренировки бег 10 км')")
        if command:
           self.run_command(command)
    def on_planner(self):
        command = simpledialog.askstring("Ввод", "Введите команду для планирования (например, 'создать план на день')")
        if command:
            self.run_command(command)
    def on_sentiment(self):
       command = simpledialog.askstring("Ввод", "Введите команду для анализа тональности (например, 'анализ тональности текст')")
       if command:
           self.run_command(command)
    def on_recommendation(self):
        command = simpledialog.askstring("Ввод", "Введите команду для получения рекомендаций (например, 'рекомендовать фильмы')")
        if command:
            self.run_command(command)
    def on_visualization(self):
        command = simpledialog.askstring("Ввод", "Введите команду для визуализации (например, 'построить график доходов по месяцам')")
        if command:
            self.run_command(command)

    def on_reminders(self):
        try:
           action = simpledialog.askstring("Ввод", "Вы хотите 'поставить' или 'просмотреть' напоминание?")
           if action == "поставить":
              reminder_text = simpledialog.askstring("Ввод", "Введите текст напоминания:")
              if reminder_text:
                  reminder_time = simpledialog.askstring("Ввод", "Введите время напоминания в формате HH:MM:")
                  if reminder_time:
                     asyncio.run(self.facade.set_reminder(reminder_text, reminder_time))
                     self.update_output(f"Напоминание установлено на {reminder_time}")
           elif action == "просмотреть":
             reminders = asyncio.run(self.facade.get_reminders())
             if reminders:
               self.update_output(f"Напоминания:\n" + "\n".join([f"{r.time}: {r.text}" for r in reminders]))
             else:
               self.update_output("Нет установленных напоминаний.")
        except Exception as e:
            logging.error(f"Ошибка при работе с напоминаниями: {e}")
            self.update_output(f"Ошибка при работе с напоминаниями: {e}")
    def on_alarm(self):
         alarm_time = simpledialog.askstring("Ввод", "Введите время будильника в формате HH:MM:")
         if alarm_time:
             asyncio.run(self.facade.set_alarm(alarm_time))
             self.update_output(f"Будильник установлен на {alarm_time}")

    def on_timer(self):
        try:
            duration_str = simpledialog.askstring("Ввод", "Введите время таймера в секундах:")
            if duration_str:
                duration = int(duration_str)
                self.update_output(f"Таймер на {duration} секунд установлен.")
                threading.Thread(target=self.run_timer, args=(duration,)).start()
        except ValueError:
           self.update_output("Неверный формат ввода.")
        except Exception as e:
            logging.error(f"Ошибка при работе с таймером: {e}")
            self.update_output(f"Ошибка при работе с таймером: {e}")

    def run_timer(self, duration):
        for i in range(duration, 0, -1):
            self.update_output(f"Осталось: {i} секунд")
            time.sleep(1)
        self.update_output("Время вышло!")
        threading.Thread(target=self.play_notification_sound).start()

    def play_notification_sound(self):
        try:
            if os.name == 'nt':
                import winsound
                winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
            elif os.name == 'posix':
                os.system("aplay /usr/share/sounds/freedesktop/stereo/complete.oga &")  # Linux
        except Exception as e:
            logging.error(f"Ошибка при воспроизведении звука: {e}")

    def on_play_music(self):
        filepath = filedialog.askopenfilename(title="Выберите музыкальный файл")
        if filepath:
          self.run_command(f"музыка {filepath}")
    def on_search_image(self):
        query = simpledialog.askstring("Ввод", "Введите запрос для поиска изображения:")
        if query:
            self.run_command(f"найди картинку {query}")
    def on_notes(self):
        try:
           action = simpledialog.askstring("Ввод", "Вы хотите 'создать', 'просмотреть' или 'удалить' заметку?")
           if action == "создать":
              note_title = simpledialog.askstring("Ввод", "Введите заголовок заметки:")
              if note_title:
                 note_text = simpledialog.askstring("Ввод", "Введите текст заметки:")
                 if note_text:
                    asyncio.run(self.facade.create_note(note_title, note_text))
                    self.update_output(f"Заметка '{note_title}' создана.")
           elif action == "просмотреть":
               notes = asyncio.run(self.facade.get_notes())
               if notes:
                   self.update_output("Заметки:\n" + "\n".join([f"{note.title}:\n {note.text}" for note in notes]))
               else:
                   self.update_output("Нет созданных заметок.")
           elif action == "удалить":
                note_title = simpledialog.askstring("Ввод", "Введите заголовок заметки, которую хотите удалить:")
                if note_title:
                   asyncio.run(self.facade.delete_note(note_title))
                   self.update_output(f"Заметка '{note_title}' удалена.")

        except Exception as e:
            logging.error(f"Ошибка при работе с заметками: {e}")
            self.update_output(f"Ошибка при работе с заметками: {e}")

    def on_file_manager(self):
        try:
            action = simpledialog.askstring("Ввод", "Выберите действие: 'создать', 'прочитать' или 'удалить' файл")
            if action == "создать":
                filepath = simpledialog.askstring("Ввод", "Введите путь к файлу для создания:")
                if filepath:
                    self.run_command(f"создать файл {filepath}")
            elif action == "прочитать":
                filepath = filedialog.askopenfilename(title="Выберите файл для чтения")
                if filepath:
                  self.run_command(f"прочитать файл {filepath}")

            elif action == "удалить":
                filepath = simpledialog.askstring("Ввод", "Введите путь к файлу для удаления:")
                if filepath:
                    self.run_command(f"удалить файл {filepath}")

        except Exception as e:
            logging.error(f"Ошибка при работе с файлами: {e}")
            self.update_output(f"Ошибка при работе с файлами: {e}")
    def on_process_manager(self):
         try:
             action = simpledialog.askstring("Ввод", "Выберите действие: 'запустить' или 'завершить' процесс")
             if action == "запустить":
                process_name = simpledialog.askstring("Ввод", "Введите имя процесса для запуска:")
                if process_name:
                    self.run_command(f"запустить процесс {process_name}")
             elif action == "завершить":
                process_name = simpledialog.askstring("Ввод", "Введите имя процесса для завершения:")
                if process_name:
                    self.run_command(f"завершить процесс {process_name}")
         except Exception as e:
            logging.error(f"Ошибка при работе с процессами: {e}")
            self.update_output(f"Ошибка при работе с процессами: {e}")

    def on_volume_control(self):
        try:
            action = simpledialog.askstring("Ввод", "Выберите действие: 'увеличить' или 'уменьшить' громкость")
            if action == "увеличить":
                self.run_command(f"увеличить громкость")
            elif action == "уменьшить":
               self.run_command(f"уменьшить громкость")
        except Exception as e:
           logging.error(f"Ошибка при управлении громкостью: {e}")
           self.update_output(f"Ошибка при управлении громкостью: {e}")
    def on_calendar(self):
        try:
           action = simpledialog.askstring("Ввод", "Выберите действие: 'создать' или 'просмотреть' событие")
           if action == "создать":
              event_name = simpledialog.askstring("Ввод", "Введите название события:")
              if event_name:
                   event_time = simpledialog.askstring("Ввод", "Введите время события в формате HH:MM:")
                   if event_time:
                       asyncio.run(self.facade.create_calendar_event(event_name, event_time))
                       self.update_output(f"Событие '{event_name}' создано на {event_time}.")
           elif action == "просмотреть":
               events = asyncio.run(self.facade.get_calendar_events())
               if events:
                   self.update_output(f"События:\n" + "\n".join([f"{event.time}: {event.name}" for event in events]))
               else:
                  self.update_output("Нет созданных событий.")

        except Exception as e:
            logging.error(f"Ошибка при работе с календарем: {e}")
            self.update_output(f"Ошибка при работе с календарем: {e}")
    def on_time(self):
        try:
            timezone = simpledialog.askstring("Ввод", "Введите часовой пояс (например, 'Europe/Moscow'):", initialvalue="Europe/Moscow")
            if timezone:
                self.run_command(f"время {timezone}")
        except Exception as e:
           logging.error(f"Ошибка при получении времени: {e}")
           self.update_output(f"Ошибка при получении времени: {e}")
    def on_theme(self):
        try:
          theme = simpledialog.askstring("Ввод", "Выберите тему ('light' или 'dark'):", initialvalue=self.user_settings.theme)
          if theme in ["light", "dark"]:
               self.user_settings.theme = theme
               self.save_settings()
               self.apply_theme()
               self.update_output(f"Тема изменена на: {theme}")
          else:
              self.update_output("Неверная тема. Выберите 'light' или 'dark'.")
        except Exception as e:
             logging.error(f"Ошибка при переключении темы: {e}")
             self.update_output(f"Ошибка при переключении темы: {e}")
    def on_language(self):
        try:
            language = simpledialog.askstring("Ввод", "Выберите язык ('ru' или 'en'):", initialvalue=self.user_settings.language)
            if language in ["ru", "en"]:
                self.user_settings.language = language
                self.save_settings()
                self.facade.switch_language(self.user_settings.language)
                self.update_output(f"Язык изменен на: {language}")
            else:
                self.update_output("Неверный язык. Выберите 'ru' или 'en'.")
        except Exception as e:
            logging.error(f"Ошибка при смене языка: {e}")
            self.update_output(f"Ошибка при смене языка: {e}")

    def on_rss(self):
         try:
            url = simpledialog.askstring("Ввод", "Введите URL RSS-канала:")
            if url:
                self.run_command(f"читать rss {url}")
         except Exception as e:
            logging.error(f"Ошибка при чтении RSS-канала: {e}")
            self.update_output(f"Ошибка при чтении RSS-канала: {e}")
    def on_movie(self):
       try:
          title = simpledialog.askstring("Ввод", "Введите название фильма")
          if title:
             self.run_command(f"фильм {title}")
       except Exception as e:
            logging.error(f"Ошибка при получении описания фильма: {e}")
            self.update_output(f"Ошибка при получении описания фильма: {e}")
    def on_audio(self):
        try:
            action = simpledialog.askstring("Ввод", "Выберите действие: 'записать' или 'воспроизвести' аудио")
            if action == "записать":
                audio_duration = simpledialog.askinteger("Ввод", "Введите длительность записи в секундах:")
                if audio_duration:
                  self.run_command(f"записать аудио {audio_duration}")
            elif action == "воспроизвести":
                filepath = filedialog.askopenfilename(title="Выберите аудиофайл для воспроизведения")
                if filepath:
                     self.run_command(f"воспроизвести аудио {filepath}")
        except Exception as e:
           logging.error(f"Ошибка при работе с аудио: {e}")
           self.update_output(f"Ошибка при работе с аудио: {e}")
    def on_profile(self):
        try:
           action = simpledialog.askstring("Ввод", "Выберите действие: 'создать', 'загрузить' или 'удалить' профиль")
           if action == "создать":
              profile_name = simpledialog.askstring("Ввод", "Введите название нового профиля:")
              if profile_name:
                  self.create_profile(profile_name)
           elif action == "загрузить":
                profile_name = simpledialog.askstring("Ввод", "Введите имя профиля для загрузки:")
                if profile_name:
                    self.load_profile(profile_name)
           elif action == "удалить":
                profile_name = simpledialog.askstring("Ввод", "Введите имя профиля для удаления:")
                if profile_name:
                    self.delete_profile(profile_name)
        except Exception as e:
            logging.error(f"Ошибка при работе с профилями: {e}")
            self.update_output(f"Ошибка при работе с профилями: {e}")

    def create_profile(self, profile_name):
        try:
            if not os.path.exists(f"config/profiles/{profile_name}"):
                os.makedirs(f"config/profiles/{profile_name}")
                self.update_output(f"Создан новый профиль: {profile_name}")
                self.create_default_profile_files(profile_name)
            else:
               self.update_output(f"Профиль с таким именем уже существует: {profile_name}")
        except Exception as e:
            logging.error(f"Ошибка при создании профиля: {e}")
            self.update_output(f"Ошибка при создании профиля: {e}")
    def create_default_profile_files(self, profile_name):
        try:
          base_profile = "default"
          if os.path.exists(f"config/profiles/{base_profile}/knowledge.json"):
             with open(f"config/profiles/{base_profile}/knowledge.json", "r") as f:
                 knowledge_data = json.load(f)
             with open(f"config/profiles/{profile_name}/knowledge.json", "w") as f:
                 json.dump(knowledge_data, f, indent=4, ensure_ascii=False)
          if os.path.exists(f"config/profiles/{base_profile}/reminder_data.json"):
            with open(f"config/profiles/{base_profile}/reminder_data.json", "r") as f:
                reminder_data = json.load(f)
            with open(f"config/profiles/{profile_name}/reminder_data.json", "w") as f:
                 json.dump(reminder_data, f, indent=4, ensure_ascii=False)
          if os.path.exists(f"config/profiles/{base_profile}/notes_data.json"):
            with open(f"config/profiles/{base_profile}/notes_data.json", "r") as f:
                notes_data = json.load(f)
            with open(f"config/profiles/{profile_name}/notes_data.json", "w") as f:
               json.dump(notes_data, f, indent=4, ensure_ascii=False)
          if os.path.exists(f"config/profiles/{base_profile}/calendar_data.json"):
            with open(f"config/profiles/{base_profile}/calendar_data.json", "r") as f:
                calendar_data = json.load(f)
            with open(f"config/profiles/{profile_name}/calendar_data.json", "w") as f:
              json.dump(calendar_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
           logging.error(f"Ошибка при создании файлов для профиля: {e}")
           self.update_output(f"Ошибка при создании файлов для профиля: {e}")

    def load_profile(self, profile_name):
       try:
           if os.path.exists(f"config/profiles/{profile_name}"):
              self.current_profile = profile_name
              self.facade.switch_profile(self.current_profile)
              self.user_settings.last_profile = self.current_profile
              self.save_settings()
              self.update_output(f"Загружен профиль: {profile_name}")
           else:
                self.update_output(f"Профиль не найден: {profile_name}")
       except Exception as e:
            logging.error(f"Ошибка при загрузке профиля: {e}")
            self.update_output(f"Ошибка при загрузке профиля: {e}")
    def delete_profile(self, profile_name):
        try:
            if os.path.exists(f"config/profiles/{profile_name}"):
               os.rmdir(f"config/profiles/{profile_name}")
               self.update_output(f"Удален профиль: {profile_name}")
            else:
                self.update_output(f"Профиль не найден: {profile_name}")
        except Exception as e:
            logging.error(f"Ошибка при удалении профиля: {e}")
            self.update_output(f"Ошибка при удалении профиля: {e}")
    def run_command(self, command):
        self.progress_bar.start()
        threading.Thread(target=self.process_command, args=(command,)).start()
    
    def process_command(self, command):
       try:
           response = asyncio.run(self.facade.handle_command(command))
           if response:
                self.update_output(response)
       except Exception as e:
            logging.error(f"Непредвиденная ошибка: {e}")
            self.update_output(f"Непредвиденная ошибка: {e}")
       finally:
            self.progress_bar.stop()
    def copy_text_to_clipboard(self):
        selected_text = self.output_text.selection_get()
        if selected_text:
            try:
                pyperclip.copy(selected_text)
                self.update_output("Текст скопирован в буфер обмена.")
            except pyperclip.PyperclipException as e:
               logging.error(f"Ошибка при копировании в буфер обмена: {e}")
               self.update_output(f"Ошибка при копировании в буфер обмена: {e}")


def main():
    root = tk.Tk()
    gui = AssistantGUI(root)
    # Создаём меню
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

   
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Файл", menu=file_menu)

file_menu.add_command(label="Копировать выделенный текст", command=gui.copy_text_to_clipboard)
file_menu.add_separator()
file_menu.add_command(label="Выход", command=root.quit)
root.mainloop()


if __name__ == "__main__":
    main()

