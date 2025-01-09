import logging
import re
import asyncio

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CommandStrategy:
   def __init__(self, assistant):
        self.assistant = assistant

   async def execute(self, command):
      pass

class WeatherStrategy(CommandStrategy):
    async def execute(self, command):
        match = re.search(r'какая погода ([\w\s]+)', command, re.IGNORECASE)
        if match:
            city = match.group(1).strip()
            response = self.assistant.weather.get_weather(city)
            self.assistant.speak(response)
            return response
        return None

class WikipediaStrategy(CommandStrategy):
    async def execute(self, command):
         match = re.search(r'найди в википедии ([\w\s]+)', command, re.IGNORECASE)
         if match:
             query = match.group(1).strip()
             response = self.assistant.wikipedia_search.search(query)
             self.assistant.speak(response)
             return response
         return None

class CalculatorStrategy(CommandStrategy):
    async def execute(self, command):
        match = re.search(r'вычислить ([\d\s\+\-\*\/\^]+)', command, re.IGNORECASE)
        if match:
           expression = match.group(1).strip()
           response = self.assistant.calculator.calculate(expression)
           self.assistant.speak(response)
           return response
        return None
class TranslateStrategy(CommandStrategy):
   async def execute(self, command):
        match = re.search(r'переведи ([\w\s\d.,!?]+) ([\w\-]+)', command, re.IGNORECASE)
        if match:
           text = match.group(1).strip()
           lang = match.group(2).strip()
           response = self.assistant.translator.translate(text, lang)
           self.assistant.speak(response)
           return response
        return None
class BrowserStrategy(CommandStrategy):
    async def execute(self, command):
        response = self.assistant.browser.open_url(command)
        self.assistant.speak(response)
        return response

class OpenUrlStrategy(CommandStrategy):
    async def execute(self, command):
       match = re.search(r'открой url ([\w\s:/\.\-]+)', command, re.IGNORECASE)
       if match:
            url = match.group(1).strip()
            response = self.assistant.browser.open_url(url)
            self.assistant.speak(response)
            return response
       return None

class GenerateTextStrategy(CommandStrategy):
   async def execute(self, command):
        match = re.search(r'сгенерировать текст ([\w\s\d.,!?]+)', command, re.IGNORECASE)
        if match:
           prompt = match.group(1).strip()
           response = self.assistant.llm.generate_text(prompt)
           self.assistant.speak(response)
           return response
        return None
class GenerateImageStrategy(CommandStrategy):
    async def execute(self, command):
        match = re.search(r'сгенерировать изображение ([\w\s\d.,!?]+)', command, re.IGNORECASE)
        if match:
           prompt = match.group(1).strip()
           response = await self.assistant.image_generator.generate_image(prompt)
           self.assistant.speak(response)
           return response
        return None
class ViewImageStrategy(CommandStrategy):
    async def execute(self, command):
        match = re.search(r'просмотри изображение ([\w\s\d.,!?/\\]+)', command, re.IGNORECASE)
        if match:
           filepath = match.group(1).strip()
           self.assistant.view_image(filepath)
           return f"Открываю изображение: {filepath}"
        return None
class UnitConvertStrategy(CommandStrategy):
   async def execute(self, command):
        match = re.search(r'конвертировать ([\w\s\d.,!?]+)', command, re.IGNORECASE)
        if match:
           expression = match.group(1).strip()
           response = self.assistant.unit_converter.convert_units(expression)
           self.assistant.speak(response)
           return response
        return None
class TextAnalysisStrategy(CommandStrategy):
    async def execute(self, command):
        match = re.search(r'подсчитать слова ([\w\s\d.,!?]+)', command, re.IGNORECASE)
        if match:
            text = match.group(1).strip()
            response = self.assistant.text_analyzer.count_words(text)
            self.assistant.speak(response)
            return response
        match = re.search(r'анализ текста ([\w\s\d.,!?]+)', command, re.IGNORECASE)
        if match:
             text = match.group(1).strip()
             response = self.assistant.text_analyzer.analyze_text(text)
             self.assistant.speak(response)
             return response
        return None
class JsonStrategy(CommandStrategy):
   async def execute(self, command):
        match = re.search(r'форматировать json ([\w\s\d.,{}:"!?]+)', command, re.IGNORECASE)
        if match:
            json_string = match.group(1).strip()
            response = self.assistant.json_utils.format_json(json_string)
            self.assistant.speak(response)
            return response
        return None
class CodeStrategy(CommandStrategy):
   async def execute(self, command):
        match = re.search(r'создать код ([\w\d\.]+) ([\w\s\d.,\n\'"=\(\)\+\-\*\/\^]+)', command, re.IGNORECASE)
        if match:
           filename = match.group(1).strip()
           code = match.group(2).strip()
           response = await self.assistant.code_editor.create_code(filename, code)
           self.assistant.speak(response)
           return response
        return None
class GeolocationStrategy(CommandStrategy):
   async def execute(self, command):
        match = re.search(r'поиск поблизости ([\w\s\d.,!?]+) ([\d\.]+[,][\d\.]+)', command, re.IGNORECASE)
        if match:
           query = match.group(1).strip()
           location = match.group(2).strip()
           response = self.assistant.api_handler.make_api_call(f"http://ip-api.com/json/{ip}")
           response = await self.assistant.api_handler.make_api_call(f"https://nominatim.openstreetmap.org/search?q={query}&format=json&lat={lat}&lon={lon}&bounded=1&limit=3")
           response = self.assistant.geolocation_utils.search_nearby(query, location)
           self.assistant.speak(response)
           return response
        return None
class SocialStrategy(CommandStrategy):
    async def execute(self, command):
       match = re.search(r'получить ленту вк', command, re.IGNORECASE)
       if match:
           response = self.assistant.social_api.get_vk_feed()
           self.assistant.speak(response)
           return response
       return None
class ProgrammerStrategy(CommandStrategy):
    async def execute(self, command):
        match = re.search(r'создать класс ([\w\d\.\_]+)', command, re.IGNORECASE)
        if match:
            class_name = match.group(1).strip()
            response = await self.assistant.programmer_utils.generate_code(class_name)
            self.assistant.speak(response)
            return response
        match = re.search(r'запустить код ([\w\d\.\_]+)', command, re.IGNORECASE)
        if match:
            filepath = match.group(1).strip()
            response = await self.assistant.programmer_utils.run_code(filepath)
            self.assistant.speak(response)
            return response
        return None
class WriterStrategy(CommandStrategy):
    async def execute(self, command):
        match = re.search(r'проверить плагиат ([\w\s\d.,!?]+)', command, re.IGNORECASE)
        if match:
          text = match.group(1).strip()
          response = "проверка плагиата не поддерживается."
          self.assistant.speak(response)
          return response
        match = re.search(r'проверить орфографию ([\w\s\d.,!?]+)', command, re.IGNORECASE)
        if match:
          text = match.group(1).strip()
          response = await self.assistant.writer_utils.check_spelling(text)
          self.assistant.speak(response)
          return response
        return None
class ManagerStrategy(CommandStrategy):
    async def execute(self, command):
        match = re.search(r'создать отчет по проекту ([\w\s\d.,!?]+)', command, re.IGNORECASE)
        if match:
            project_name = match.group(1).strip()
            response = await self.assistant.manager_utils.create_report(project_name)
            self.assistant.speak(response)
            return response
        return None
class DoctorStrategy(CommandStrategy):
    async def execute(self, command):
      match = re.search(r'анализ симптомов ([\w\s\d.,!?]+)', command, re.IGNORECASE)
      if match:
        symptoms = match.group(1).strip()
        response = self.assistant.doctor_utils.analyze_symptoms(symptoms)
        self.assistant.speak(response)
        return response
      return None
class TeacherStrategy(CommandStrategy):
   async def execute(self, command):
        match = re.search(r'сгенерировать тест по теме ([\w\s\d.,!?]+)', command, re.IGNORECASE)
        if match:
             topic = match.group(1).strip()
             response = self.assistant.teacher_utils.generate_test(topic)
             self.assistant.speak(response)
             return response
        return None
class DesignerStrategy(CommandStrategy):
    async def execute(self, command):
      match = re.search(r'цвета для сайта про ([\w\s\d.,!?]+)', command, re.IGNORECASE)
      if match:
        theme = match.group(1).strip()
        response = self.assistant.designer_utils.get_colors_by_theme(theme)
        self.assistant.speak(response)
        return response
      return None
class SportsmanStrategy(CommandStrategy):
    async def execute(self, command):
        match = re.search(r'анализ тренировки ([\w\s]+) ([\w\d\.]+)', command, re.IGNORECASE)
        if match:
            training_type = match.group(1).strip()
            distance = match.group(2).strip()
            response = self.assistant.sport_utils.analyze_training(training_type, distance)
            self.assistant.speak(response)
            return response
        return None
class PlannerStrategy(CommandStrategy):
    async def execute(self, command):
         match = re.search(r'создать план на ([\w]+)', command, re.IGNORECASE)
         if match:
           plan_type = match.group(1).strip()
           response = await self.assistant.planner.create_plan(plan_type)
           self.assistant.speak(response)
           return response
         return None
class SentimentStrategy(CommandStrategy):
    async def execute(self, command):
        match = re.search(r'анализ тональности ([\w\s\d.,!?]+)', command, re.IGNORECASE)
        if match:
          text = match.group(1).strip()
          response = self.assistant.sentiment_analyzer.analyze_sentiment(text)
          self.assistant.speak(response)
          return response
        return None
class RecommendationStrategy(CommandStrategy):
    async def execute(self, command):
        match = re.search(r'рекомендовать ([\w\s\d.,!?]+)', command, re.IGNORECASE)
        if match:
            topic = match.group(1).strip()
            response = self.assistant.recommender.get_recommendation(topic)
            self.assistant.speak(response)
            return response
        return None
class VisualizationStrategy(CommandStrategy):
    async def execute(self, command):
        match = re.search(r'построить график ([\w\s\d.,!?]+)', command, re.IGNORECASE)
        if match:
            description = match.group(1).strip()
            data = [1, 2, 3, 4]
            response = self.assistant.visualizer.create_plot(data, "line")
            self.assistant.speak(response)
            return response
        match = re.search(r'построить гистограмму ([\w\s\d.,!?]+)', command, re.IGNORECASE)
        if match:
            description = match.group(1).strip()
            data = [1, 2, 3, 4]
            response = self.assistant.visualizer.create_plot(data, "bar")
            self.assistant.speak(response)
            return response
        return None

class PlayMusicStrategy(CommandStrategy):
   async def execute(self, command):
        match = re.search(r'музыка ([\w\s\d.,!?/\\]+)', command, re.IGNORECASE)
        if match:
            filepath = match.group(1).strip()
            response = self.assistant.audio_manager.play_audio(filepath)
            self.assistant.speak(response)
            return response
        return None
class SearchImageStrategy(CommandStrategy):
    async def execute(self, command):
        match = re.search(r'найди картинку ([\w\s\d.,!?]+)', command, re.IGNORECASE)
        if match:
            query = match.group(1).strip()
            response = await self.assistant.image_downloader.download_image(query)
            self.assistant.speak(response)
            return response
        return None

class CreateFileStrategy(CommandStrategy):
    async def execute(self, command):
        match = re.search(r'создать файл ([\w\s\d.,!?/\\]+)', command, re.IGNORECASE)
        if match:
             filepath = match.group(1).strip()
             response = self.assistant.file_manager.create_file(filepath)
             self.assistant.speak(response)
             return response
        return None
class ReadFileStrategy(CommandStrategy):
    async def execute(self, command):
        match = re.search(r'прочитать файл ([\w\s\d.,!?/\\]+)', command, re.IGNORECASE)
        if match:
             filepath = match.group(1).strip()
             response = self.assistant.file_manager.read_file(filepath)
             self.assistant.speak(response)
             return response
        return None
class DeleteFileStrategy(CommandStrategy):
    async def execute(self, command):
        match = re.search(r'удалить файл ([\w\s\d.,!?/\\]+)', command, re.IGNORECASE)
        if match:
            filepath = match.group(1).strip()
            response = self.assistant.file_manager.delete_file(filepath)
            self.assistant.speak(response)
            return response
        return None
class RunProcessStrategy(CommandStrategy):
   async def execute(self, command):
      match = re.search(r'запустить процесс ([\w\s\d.,!?]+)', command, re.IGNORECASE)
      if match:
         process_name = match.group(1).strip()
         response
response = self.assistant.process_manager.run_process(process_name)
         self.assistant.speak(response)
         return response
      return None
class StopProcessStrategy(CommandStrategy):
   async def execute(self, command):
      match = re.search(r'завершить процесс ([\w\s\d.,!?]+)', command, re.IGNORECASE)
      if match:
         process_name = match.group(1).strip()
         response = self.assistant.process_manager.stop_process(process_name)
         self.assistant.speak(response)
         return response
      return None
class VolumeUpStrategy(CommandStrategy):
    async def execute(self, command):
          match = re.search(r'увеличить громкость', command, re.IGNORECASE)
          if match:
            response = self.assistant.volume_control.increase_volume()
            self.assistant.speak(response)
            return response
          return None
class VolumeDownStrategy(CommandStrategy):
    async def execute(self, command):
        match = re.search(r'уменьшить громкость', command, re.IGNORECASE)
        if match:
            response = self.assistant.volume_control.decrease_volume()
            self.assistant.speak(response)
            return response
        return None
class TimeStrategy(CommandStrategy):
    async def execute(self, command):
        match = re.search(r'время ([\w\/\s]+)', command, re.IGNORECASE)
        if match:
           timezone = match.group(1).strip()
           response = self.assistant.time_manager.get_current_time(timezone)
           self.assistant.speak(response)
           return response
        return None
class ReadRssStrategy(CommandStrategy):
   async def execute(self, command):
        match = re.search(r'читать rss ([\w\s\d.,:/\.\-]+)', command, re.IGNORECASE)
        if match:
            url = match.group(1).strip()
            response = self.assistant.rss_reader.read_rss(url)
            self.assistant.speak(response)
            return response
        return None
class MovieStrategy(CommandStrategy):
   async def execute(self, command):
        match = re.search(r'фильм ([\w\s\d.,!?]+)', command, re.IGNORECASE)
        if match:
           title = match.group(1).strip()
           response = self.assistant.movie.get_movie_description(title)
           self.assistant.speak(response)
           return response
        return None
class RecordAudioStrategy(CommandStrategy):
    async def execute(self, command):
        match = re.search(r'записать аудио ([\w\s\d.,!?]+)', command, re.IGNORECASE)
        if match:
            audio_duration = match.group(1).strip()
            response = await self.assistant.record_audio_text()
            self.assistant.speak(response)
            return response
        return None
class PlayAudioStrategy(CommandStrategy):
   async def execute(self, command):
        match = re.search(r'воспроизвести аудио ([\w\s\d.,!?/\\]+)', command, re.IGNORECASE)
        if match:
           filepath = match.group(1).strip()
           response = self.assistant.audio_manager.play_audio(filepath)
           self.assistant.speak(response)
           return response
        return None
class MathSolveStrategy(CommandStrategy):
   async def execute(self, command):
       match = re.search(r'решить ([\w\s\d.,!?=\+\-\*\/\^\(\)]+)', command, re.IGNORECASE)
       if match:
          expression = match.group(1).strip()
          response = await self.assistant.math_solver.solve_equation(expression)
          self.assistant.speak(response)
          return response
       return None

class MathSimplifyStrategy(CommandStrategy):
    async def execute(self, command):
        match = re.search(r'упростить ([\w\s\d.,!?\+\-\*\/\^\(\)]+)', command, re.IGNORECASE)
        if match:
            expression = match.group(1).strip()
            response = await self.assistant.math_solver.simplify_expression(expression)
            self.assistant.speak(response)
            return response
        return None
class MathDerivativeStrategy(CommandStrategy):
  async def execute(self, command):
       match = re.search(r'производная ([\w\s\d.,!?\+\-\*\/\^\(\)]+) (?:по ([\w]+))?', command, re.IGNORECASE)
       if match:
           expression = match.group(1).strip()
           variable = match.group(2).strip() if match.group(2) else 'x'
           response = await self.assistant.math_solver.calculate_derivative(expression, variable)
           self.assistant.speak(response)
           return response
       return None
class MathIntegralStrategy(CommandStrategy):
   async def execute(self, command):
       match = re.search(r'интеграл ([\w\s\d.,!?\+\-\*\/\^\(\)]+) (?:по ([\w]+))?', command, re.IGNORECASE)
       if match:
           expression = match.group(1).strip()
           variable = match.group(2).strip() if match.group(2) else 'x'
           response = await self.assistant.math_solver.calculate_integral(expression, variable)
           self.assistant.speak(response)
           return response
       return None
class MathMatrixStrategy(CommandStrategy):
    async def execute(self, command):
        match = re.search(r'матрица ([\w\s\d.,!?\[\]]+) ([\w]+)', command, re.IGNORECASE)
        if match:
            matrix_str = match.group(1).strip()
            operation = match.group(2).strip()
            response = await self.assistant.math_solver.matrix_operations(matrix_str, operation)
            self.assistant.speak(response)
            return response
        return None

class MathEvaluateStrategy(CommandStrategy):
   async def execute(self, command):
        match = re.search(r'вычислить выражение ([\w\s\d.,!?=\+\-\*\/\^\(\)]+) (?:с ([\w\s\d.,!?=\+\-\*\/\^\(\)]+))?', command, re.IGNORECASE)
        if match:
           expression = match.group(1).strip()
           values_str = match.group(2)
           values = None
           if values_str:
               try:
                  values = eval(values_str)
               except:
                    values = None
           response = await self.assistant.math_solver.evaluate_expression(expression, values)
           self.assistant.speak(response)
           return response
        return None
class CommandStrategyManager:
   def __init__(self, assistant):
       self.assistant = assistant
       self.strategies = {
          "какая погода": WeatherStrategy(assistant),
          "найди в википедии": WikipediaStrategy(assistant),
           "вычислить": CalculatorStrategy(assistant),
           "переведи": TranslateStrategy(assistant),
           "открой": BrowserStrategy(assistant),
            "открой url": OpenUrlStrategy(assistant),
           "сгенерировать текст": GenerateTextStrategy(assistant),
           "сгенерировать изображение": GenerateImageStrategy(assistant),
           "просмотри изображение": ViewImageStrategy(assistant),
           "конвертировать": UnitConvertStrategy(assistant),
           "подсчитать слова": TextAnalysisStrategy(assistant),
           "анализ текста": TextAnalysisStrategy(assistant),
           "форматировать json": JsonStrategy(assistant),
           "создать код": CodeStrategy(assistant),
           "поиск поблизости": GeolocationStrategy(assistant),
          "получить ленту вк": SocialStrategy(assistant),
          "создать класс": ProgrammerStrategy(assistant),
          "запустить код": ProgrammerStrategy(assistant),
            "проверить плагиат": WriterStrategy(assistant),
          "проверить орфографию": WriterStrategy(assistant),
          "создать отчет по проекту": ManagerStrategy(assistant),
          "анализ симптомов": DoctorStrategy(assistant),
          "сгенерировать тест по теме": TeacherStrategy(assistant),
          "цвета для сайта про": DesignerStrategy(assistant),
           "анализ тренировки": SportsmanStrategy(assistant),
            "создать план на": PlannerStrategy(assistant),
            "анализ тональности": SentimentStrategy(assistant),
          "рекомендовать": RecommendationStrategy(assistant),
            "построить график": VisualizationStrategy(assistant),
           "построить гистограмму": VisualizationStrategy(assistant),
           "музыка": PlayMusicStrategy(assistant),
          "найди картинку": SearchImageStrategy(assistant),
           "создать файл": CreateFileStrategy(assistant),
           "прочитать файл": ReadFileStrategy(assistant),
          "удалить файл": DeleteFileStrategy(assistant),
          "запустить процесс": RunProcessStrategy(assistant),
           "завершить процесс": StopProcessStrategy(assistant),
            "увеличить громкость": VolumeUpStrategy(assistant),
             "уменьшить громкость": VolumeDownStrategy(assistant),
             "время": TimeStrategy(assistant),
             "читать rss": ReadRssStrategy(assistant),
             "фильм": MovieStrategy(assistant),
           "записать аудио": RecordAudioStrategy(assistant),
           "воспроизвести аудио": PlayAudioStrategy(assistant),
           "решить": MathSolveStrategy(assistant),
            "упростить": MathSimplifyStrategy(assistant),
             "производная": MathDerivativeStrategy(assistant),
            "интеграл": MathIntegralStrategy(assistant),
           "матрица": MathMatrixStrategy(assistant),
           "вычислить выражение": MathEvaluateStrategy(assistant)
       }
   def get_strategy(self, command):
       for key in self.strategies:
           if key in command.lower():
               return self.strategies[key]
       return None
62. observer.py

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EventObserver:
    def __init__(self):
        self._subscribers = {}
    def subscribe(self, event_type, callback):
        if event_type not in self._subscribers:
           self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)
    def unsubscribe(self, event_type, callback):
        if event_type in self._subscribers:
           try:
             self._subscribers[event_type].remove(callback)
           except ValueError:
             logging.warning(f"Подписчик не найден: {callback}")
    async def notify(self, event_type, event_data):
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
               try:
                  await callback(event_data)
               except Exception as e:
                  logging.error(f"Ошибка при вызове подписчика: {e}")