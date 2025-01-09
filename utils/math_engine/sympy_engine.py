import logging
from sympy import sympify, solve, diff, integrate, Matrix,  lambdify
from sympy.parsing.mathematica import parse_mathematica
from sympy.core.sympify import SympifyError
from utils.interfaces import MathEngine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SympyEngine(MathEngine):
    def solve(self, expression):
        try:
            expression = expression.replace("=", "-(") + ")"
            expr = parse_mathematica(expression)
            result = solve(expr)
            return f"Решение: {result}"
        except SympifyError:
           logging.error(f"Неверный формат математического выражения.")
           return "Неверный формат математического выражения."
        except Exception as e:
            logging.error(f"Ошибка при решении математического выражения: {e}")
            return f"Ошибка при решении математического выражения: {e}"

    def simplify(self, expression):
        try:
           expr = sympify(expression)
           simplified_expr = expr.simplify()
           return f"Упрощенное выражение: {simplified_expr}"
        except SympifyError:
           logging.error("Неверный формат выражения.")
           return "Неверный формат выражения."
        except Exception as e:
           logging.error(f"Ошибка при упрощении выражения: {e}")
           return f"Ошибка при упрощении выражения: {e}"
    
    def calculate_derivative(self, expression, variable='x'):
        try:
           expr = sympify(expression)
           variable = sympify(variable)
           derivative = diff(expr, variable)
           return f"Производная: {derivative}"
        except SympifyError:
           logging.error("Неверный формат выражения или переменной.")
           return "Неверный формат выражения или переменной."
        except Exception as e:
            logging.error(f"Ошибка при вычислении производной: {e}")
            return f"Ошибка при вычислении производной: {e}"
    
    def calculate_integral(self, expression, variable='x'):
       try:
           expr = sympify(expression)
           variable = sympify(variable)
           integral = integrate(expr, variable)
           return f"Интеграл: {integral}"
       except SympifyError:
            logging.error("Неверный формат выражения или переменной.")
            return "Неверный формат выражения или переменной."
       except Exception as e:
            logging.error(f"Ошибка при вычислении интеграла: {e}")
            return f"Ошибка при вычислении интеграла: {e}"
    
    def matrix_operations(self, matrix_str, operation):
        try:
            matrix = Matrix(eval(matrix_str))
            if operation == "transpose":
                result = matrix.T
            elif operation == "determinant":
                result = matrix.det()
            elif operation == "inverse":
                result = matrix.inv()
            else:
               logging.error(f"Неизвестная операция: {operation}")
               return f"Неизвестная операция: {operation}"
            return f"Результат: {result}"
        except Exception as e:
           logging.error(f"Ошибка при работе с матрицами: {e}")
           return f"Ошибка при работе с матрицами: {e}"

    def evaluate_expression(self, expression, values=None):
       try:
          expr = sympify(expression)
          if values:
             evaluated_expr = expr.subs(values)
          else:
              evaluated_expr = expr
          return f"Значение выражения: {evaluated_expr}"
       except Exception as e:
           logging.error(f"Ошибка при вычислении выражения: {e}")
           return f"Ошибка при вычислении выражения: {e}"