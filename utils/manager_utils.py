import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ManagerUtils:
  async def create_report(self, project_name):
     try:
         # Здесь должен быть код генерации отчета по проекту.
         logging.info(f"Создаю отчет по проекту: {project_name}")
         return f"Создан отчет по проекту '{project_name}'"
     except Exception as e:
         logging.error(f"Ошибка при создании отчета: {e}")
         return f"Ошибка при создании отчета: {e}"
