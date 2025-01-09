import logging
from utils.interfaces import MathEngine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MathAdapter(MathEngine):
    def __init__(self, engine):
        self.engine = engine

    def solve(self, expression):
        return self.engine.solve(expression)
    def simplify(self, expression):
        return self.engine.simplify(expression)
    def calculate_derivative(self, expression, variable='x'):
        return self.engine.calculate_derivative(expression, variable)
    def calculate_integral(self, expression, variable='x'):
        return self.engine.calculate_integral(expression, variable)
    def matrix_operations(self, matrix_str, operation):
        return self.engine.matrix_operations(matrix_str, operation)
    def evaluate_expression(self, expression, values=None):
        return self.engine.evaluate_expression(expression, values)