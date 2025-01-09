import logging
import torch
from transformers import pipeline, set_seed

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LargeLanguageModel:
    def __init__(self, model_name="gpt2", use_cuda=False, seed=42):
        self.model_name = model_name
        self.use_cuda = use_cuda
        self.seed = seed
        self.generator = None
        self._set_generator()
    def _set_generator(self):
      try:
         set_seed(self.seed)
         device = "cuda" if self.use_cuda and torch.cuda.is_available() else "cpu"
         self.generator = pipeline('text-generation', model=self.model_name, device=device)
         logging.info(f"Модель '{self.model_name}' загружена на устройство '{device}'.")
      except Exception as e:
           logging.error(f"Ошибка загрузки модели: {e}")
           raise
    def use_cuda(self):
        self.use_cuda = True
        self._set_generator()
    def use_cpu(self):
        self.use_cuda = False
        self._set_generator()
    def generate_text(self, prompt, max_length=100):
        try:
          if not self.generator:
            self._set_generator()
          output = self.generator(prompt, max_length=max_length, num_return_sequences=1)[0]['generated_text']
          return output
        except Exception as e:
            logging.error(f"Ошибка при генерации текста: {e}")
            return f"Ошибка при генерации текста: {e}"