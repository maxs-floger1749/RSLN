import logging
import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Planner:
   def __init__(self, database_manager):
      self.database_manager = database_manager
   async def create_plan(self, plan_type):
       try:
           if plan_type == "день":
               plan = await self._generate_daily_plan()
               return plan
           elif plan_type == "неделя":
               plan = await self._generate_weekly_plan()
               return plan
           else:
               return f"Тип плана '{plan_type}' не поддерживается."
       except Exception as e:
            logging.error(f"Ошибка при создании плана: {e}")
            return f"Ошибка при создании плана: {e}"
   async def _generate_daily_plan(self):
       try:
           current_time = datetime.datetime.now().strftime("%H:%M")
           reminders = await self.database_manager.get_reminders()
           events = await self.database_manager.get_calendar_events()
           plan = f"План на день ({datetime.datetime.now().strftime('%d.%m.%Y')}):\n"
           plan += f"Текущее время: {current_time}\n"
           if reminders:
               plan += "Напоминания:\n" + "\n".join([f"{r.time}: {r.text}" for r in reminders]) + "\n"
           else:
               plan += "Нет напоминаний на сегодня.\n"
           if events:
               plan += "События:\n" + "\n".join([f"{event.time}: {event.name}" for event in events])
           else:
                plan += "Нет событий на сегодня."
           return plan
       except Exception as e:
             logging.error(f"Ошибка при создании дневного плана: {e}")
             return f"Ошибка при создании дневного плана: {e}"
   async def _generate_weekly_plan(self):
       try:
          current_time = datetime.datetime.now().strftime("%H:%M")
          reminders = await self.database_manager.get_reminders()
          events = await self.database_manager.get_calendar_events()
          plan = f"План на неделю ({datetime.datetime.now().strftime('%d.%m.%Y')}):\n"
          plan += f"Текущее время: {current_time}\n"
          if reminders:
            plan += "Напоминания:\n" + "\n".join([f"{r.time}: {r.text}" for r in reminders]) + "\n"
          else:
            plan += "Нет напоминаний на этой неделе.\n"
          if events:
            plan += "События:\n" + "\n".join([f"{event.time}: {event.name}" for event in events])
          else:
              plan += "Нет событий на этой неделе."
          return plan
       except Exception as e:
          logging.error(f"Ошибка при создании недельного плана: {e}")
          return f"Ошибка при создании недельного плана: {e}"
