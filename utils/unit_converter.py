import logging
from unit_converter import UnitConverter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class UnitConverter:
  def __init__(self):
       self.unit_converter = UnitConverter()
       self.known_units = {
            'температура': ['celsius', 'fahrenheit', 'kelvin'],
            'длина': ['meters', 'kilometers', 'miles', 'yards', 'feet', 'inches'],
            'вес': ['kilograms', 'grams', 'pounds', 'ounces'],
            'время': ['seconds', 'minutes', 'hours', 'days']
        }
  def _parse_command(self, command):
       command = command.lower().strip()
       parts = command.split()
       if len(parts) < 4:
         return None, None, None, None
       try:
         value = float(parts[2])
       except ValueError:
         return None, None, None, None
       unit_from = parts[3]
       unit_to = parts[4]
       return parts[1], value, unit_from, unit_to

  def convert_units(self, command):
       try:
          unit_type, value, unit_from, unit_to = self._parse_command(command)
          if not unit_type or unit_from not in self.known_units.get(unit_type, []) or unit_to not in self.known_units.get(unit_type, []):
              logging.error(f"Неизвестная единица измерения в команде: {command}")
              return f"Неизвестная единица измерения в команде. Пожалуйста, проверьте ваш запрос: {command}"
          result = self.unit_converter.convert(value, unit_from, unit_to)
          return f"{value} {unit_from} = {result} {unit_to}"
       except Exception as e:
            logging.error(f"Ошибка при конвертации величин: {e}")
            return f"Ошибка при конвертации величин: {e}"