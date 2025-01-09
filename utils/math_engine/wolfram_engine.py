import logging
import wolframalpha
from utils.interfaces import MathEngine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WolframEngine(MathEngine):
    def __init__(self, api_key):
        self.client = wolframalpha.Client(api_key)

    def solve(self, expression):
        try:
            res = self.client.query(expression)
            if res['pod']:
               result = next(res.results).text
            else:
                result = "Нет ответа"
            return f"Решение: {result}"
        except Exception as e:
           logging.error(f"Ошибка при решении уравнения WolframAlpha: {e}")
           return f"Ошибка при решении уравнения WolframAlpha: {e}"
    
    def simplify(self, expression):
        try:
            res = self.client.query(f"Simplify {expression}")
            if res['pod']:
               result = next(res.results).text
            else:
                result = "Нет ответа"
            return f"Упрощенное выражение: {result}"
        except Exception as e:
            logging.error(f"Ошибка при упрощении выражения WolframAlpha: {e}")
            return f"Ошибка при упрощении выражения WolframAlpha: {e}"

    def calculate_derivative(self, expression, variable='x'):
        try:
            res = self.client.query(f"derivative of {expression} with respect to {variable}")
            if res['pod']:
               result = next(res.results).text
            else:
                result = "Нет ответа"
            return f"Производная: {result}"
        except Exception as e:
             logging.error(f"Ошибка при вычислении производной WolframAlpha: {e}")
             return f"Ошибка при вычислении производной WolframAlpha: {e}"
        
    def calculate_integral(self, expression, variable='x'):
        try:
            res = self.client.query(f"integrate {expression} with respect to {variable}")
            if res['pod']:
               result = next(res.results).text
            else:
                result = "Нет ответа"
            return f"Интеграл: {result}"
        except Exception as e:
            logging.error(f"Ошибка при вычислении интеграла WolframAlpha: {e}")
            return f"Ошибка при вычислении интеграла WolframAlpha: {e}"

    def matrix_operations(self, matrix_str, operation):
        try:
             res = self.client.query(f"{operation} of {matrix_str}")
             if res['pod']:
               result = next(res.results).text
             else:
                result = "Нет ответа"
             return f"Результат: {result}"
        except Exception as e:
             logging.error(f"Ошибка при работе с матрицами WolframAlpha: {e}")
             return f"Ошибка при работе с матрицами WolframAlpha: {e}"
    def evaluate_expression(self, expression, values=None):
        try:
            if values:
                input_expr = f"{expression} with {values}"
            else:
              input_expr = expression
            res = self.client.query(input_expr)
            if res['pod']:
               result = next(res.results).text
            else:
                result = "Нет ответа"
            return f"Значение выражения: {result}"
        except Exception as e:
            logging.error(f"Ошибка при вычислении выражения WolframAlpha: {e}")
            return f"Ошибка при вычислении выражения WolframAlpha: {e}"