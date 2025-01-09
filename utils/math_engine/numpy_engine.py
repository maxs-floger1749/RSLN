import logging
import numpy as np
from utils.interfaces import MathEngine
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NumpyEngine(MathEngine):
    def solve(self, expression):
        try:
           logging.warning(f"Решение уравнений с numpy не поддерживается")
           return "Решение уравнений с numpy не поддерживается"
        except Exception as e:
          logging.error(f"Ошибка при решении уравнения: {e}")
          return f"Ошибка при решении уравнения: {e}"

    def simplify(self, expression):
        try:
            logging.warning(f"Упрощение выражений с numpy не поддерживается")
            return "Упрощение выражений с numpy не поддерживается"
        except Exception as e:
            logging.error(f"Ошибка при упрощении выражения: {e}")
            return f"Ошибка при упрощении выражения: {e}"
        
    def calculate_derivative(self, expression, variable='x'):
        try:
           logging.warning(f"Вычисление производной с numpy не поддерживается")
           return "Вычисление производной с numpy не поддерживается"
        except Exception as e:
            logging.error(f"Ошибка при вычислении производной: {e}")
            return f"Ошибка при вычислении производной: {e}"

    def calculate_integral(self, expression, variable='x'):
        try:
           logging.warning(f"Вычисление интеграла с numpy не поддерживается")
           return "Вычисление интеграла с numpy не поддерживается"
        except Exception as e:
            logging.error(f"Ошибка при вычислении интеграла: {e}")
            return f"Ошибка при вычислении интеграла: {e}"
    
    def matrix_operations(self, matrix_str, operation):
        try:
            matrix = np.array(eval(matrix_str))
            if operation == "transpose":
                result = matrix.T
            elif operation == "determinant":
                result = np.linalg.det(matrix)
            elif operation == "inverse":
                result = np.linalg.inv(matrix)
            else:
                logging.error(f"Неизвестная операция: {operation}")
                return f"Неизвестная операция: {operation}"
            return f"Результат: {result}"
        except Exception as e:
           logging.error(f"Ошибка при работе с матрицами: {e}")
           return f"Ошибка при работе с матрицами: {e}"
    
    def evaluate_expression(self, expression, values=None):
        try:
          expr = eval(expression)
          if values:
             logging.warning(f"Подстановка значений в выражение с numpy не поддерживается")
             return f"Подстановка значений в выражение с numpy не поддерживается"
          else:
              return f"Значение выражения: {expr}"
        except Exception as e:
           logging.error(f"Ошибка при вычислении выражения: {e}")
           return f"Ошибка при вычислении выражения: {e}"