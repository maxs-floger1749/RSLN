import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
class ProgrammerUtils:
  def __init__(self, code_editor, code_runner, syntax_checker, code_generator):
    self.code_editor = code_editor
    self.code_runner = code_runner
    self.syntax_checker = syntax_checker
    self.code_generator = code_generator
  async def create_code(self, filename, code):
        return self.code_editor.create_code(filename, code)
  async def run_code(self, filepath):
        return self.code_runner.run_code(filepath)
  async def check_code_syntax(self, code):
        return self.syntax_checker.check_syntax(code)
  async def generate_code(self, class_name, attributes=None, methods=None):
       return self.code_generator.generate_class(class_name, attributes, methods)