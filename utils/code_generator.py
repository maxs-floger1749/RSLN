import logging
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CodeGenerator:
    def generate_class(self, class_name, attributes=None, methods=None):
        try:
           if not re.match("^[a-zA-Z_][a-zA-Z0-9_]*$", class_name):
               logging.error("Некорректное имя класса")
               return "Некорректное имя класса"
           class_code = f"class {class_name}:\n"
           if attributes:
                for attribute in attributes:
                    if not re.match("^[a-zA-Z_][a-zA-Z0-9_]*$", attribute):
                       logging.error(f"Некорректное имя атрибута: {attribute}")
                       return f"Некорректное имя атрибута: {attribute}"
                    class_code += f"    def __init__(self):\n        self.{attribute} = None\n"
           if methods:
               for method in methods:
                  if not re.match("^[a-zA-Z_][a-zA-Z0-9_]*$", method):
                      logging.error(f"Некорректное имя метода: {method}")
                      return f"Некорректное имя метода: {method}"
                  class_code += f"    def {method}(self):\n       pass\n"

           return f"Сгенерирован код класса:\n{class_code}"
        except Exception as e:
           logging.error(f"Ошибка при генерации кода класса: {e}")
           return f"Ошибка при генерации кода класса: {e}"