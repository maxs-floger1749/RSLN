import logging
from utils.math_engines.sympy_engine import SympyEngine
from utils.math_engines.numpy_engine import NumpyEngine
from utils.math_engines.wolfram_engine import WolframEngine
from utils.math_adapter import MathAdapter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MathEngineFactory:
    def __init__(self, wolfram_api_key=None):
        self.wolfram_api_key = wolfram_api_key
    def create_engine(self, engine_type = "sympy"):
        if engine_type == "sympy":
            return MathAdapter(SympyEngine())
        elif engine_type == "numpy":
            return MathAdapter(NumpyEngine())
        elif engine_type == "wolfram" and self.wolfram_api_key:
            return MathAdapter(WolframEngine(self.wolfram_api_key))
        else:
           logging.error(f"Неизвестный тип движка: {engine_type} или нет API ключа для wolfram")
           return None