import logging
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Calculator:
    def __init__(self):
        self.operations_map = {
           "слож": "+",
            "+": "+",
            "выче": "-",
            "-": "-",
            "множ": "*",
            "x": "*",
            "*": "*",
            "дел": "/",
            "/": "/",
            "степен": "**"
        }

    def _get_operation(self, opers):
        for op in opers:
           if op in self.operations_map:
                return self.operations_map[op]
        return None
    def _perform_operation(self, op, num1, num2):
        if op == "+":
            return num1 + num2
        elif op == "-":
           return num1 - num2
        elif op == "*":
            return num1 * num2
        elif op == "/":
            if num2 != 0:
                return num1 / num2
            else:
                raise ValueError("Деление на ноль невозможно.")
        elif op == "**":
           return num1 ** num2
        else:
            raise ValueError("Неизвестная операция.")

    def calculate(self, voice):
        try:
            list_of_nums = voice.split()
            if len(list_of_nums) < 3:
               logging.error("Недостаточно данных для выполнения операции.")
               return "Недостаточно данных для выполнения операции."
            try:
                num_1 = float(list_of_nums[-2].strip())
                num_2 = float(list_of_nums[-1].strip())
            except ValueError:
                logging.error(f"Неверный формат числа в: {list_of_nums[-2]} или {list_of_nums[-1]}")
                return "Неверный формат числа. Пожалуйста, используйте цифры."
            opers = [list_of_nums[0].strip(), list_of_nums[-3].strip()]
            oper = self._get_operation(opers)
            if oper is None:
               logging.error(f"Операция не найдена в: {opers}")
               return "Неизвестная операция. Попробуйте еще раз."
            ans = self._perform_operation(oper, num_1, num_2)
            return f"{num_1} {oper} {num_2} = {ans}"
        except ValueError as e:
           logging.error(f"Ошибка вычислений: {e}")
           return f"Ошибка вычислений: {e}"
        except Exception as e:
           logging.error(f"Непредвиденная ошибка: {e}")
           return "Непредвиденная ошибка. Пожалуйста, скажите в другом формате. Например: 'сколько будет 5 + 5?'"
