import logging
from utils.math_adapter import MathAdapter
from utils.math_engine_factory import MathEngineFactory

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MathSolver:
    def __init__(self):
        self.math_adapter = None
        self.math_engine_factory = MathEngineFactory()

    def set_math_engine(self, engine_type):
        self.math_adapter = self.math_engine_factory.create_engine(engine_type)
        if not self.math_adapter:
            logging.error(f"Не удалось установить движок: {engine_type}")
            return "Не удалось установить движок."
        return f"Установлен движок: {engine_type}"

    async def solve_equation(self, expression):
        if not self.math_adapter:
            logging.warning("Движок вычислений не установлен. Использую sympy по умолчанию.")
            self.set_math_engine("sympy")
        return self.math_adapter.solve(expression)

    async def simplify_expression(self, expression):
        if not self.math_adapter:
            logging.warning("Движок вычислений не установлен. Использую sympy по умолчанию.")
            self.set_math_engine("sympy")
        return self.math_adapter.simplify(expression)
    async def calculate_derivative(self, expression, variable='x'):
         if not self.math_adapter:
            logging.warning("Движок вычислений не установлен. Использую sympy по умолчанию.")
            self.set_math_engine("sympy")
         return self.math_adapter.calculate_derivative(expression, variable)
    async def calculate_integral(self, expression, variable='x'):
        if not self.math_adapter:
           logging.warning("Движок вычислений не установлен. Использую sympy по умолчанию.")
           self.set_math_engine("sympy")
        return self.math_adapter.calculate_integral(expression, variable)
    async def matrix_operations(self, matrix_str, operation):
        if not self.math_adapter:
           logging.warning("Движок вычислений не установлен. Использую numpy по умолчанию.")
           self.set_math_engine("numpy")
        return self.math_adapter.matrix_operations(matrix_str, operation)

    async def evaluate_expression(self, expression, values=None):
        if not self.math_adapter:
           logging.warning("Движок вычислений не установлен. Использую sympy по умолчанию.")
           self.set_math_engine("sympy")
        return self.math_adapter.evaluate_expression(expression, values)