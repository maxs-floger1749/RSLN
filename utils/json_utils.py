import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class JsonUtils:
    def format_json(self, json_string):
        try:
            formatted_json = json.dumps(json.loads(json_string), indent=4, ensure_ascii=False)
            return f"Отформатированный JSON:\n{formatted_json}"
        except json.JSONDecodeError as e:
            logging.error(f"Ошибка декодирования JSON: {e}")
            return f"Ошибка декодирования JSON: {e}"
        except Exception as e:
            logging.error(f"Ошибка при форматировании JSON: {e}")
            return f"Ошибка при форматировании JSON: {e}"