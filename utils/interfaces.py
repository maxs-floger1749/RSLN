import abc

class MathEngine(abc.ABC):
    @abc.abstractmethod
    def solve(self, expression):
       pass
    @abc.abstractmethod
    def simplify(self, expression):
        pass
    @abc.abstractmethod
    def calculate_derivative(self, expression, variable='x'):
      pass
    @abc.abstractmethod
    def calculate_integral(self, expression, variable='x'):
        pass
    @abc.abstractmethod
    def matrix_operations(self, matrix_str, operation):
       pass
    @abc.abstractmethod
    def evaluate_expression(self, expression, values=None):
        pass
