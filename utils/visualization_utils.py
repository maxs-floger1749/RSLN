import logging
import matplotlib.pyplot as plt
import os
from io import BytesIO
import base64

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataVisualizer:
   def __init__(self):
       self.image_dir = "visualizations"
       if not os.path.exists(self.image_dir):
           os.makedirs(self.image_dir)
   def create_plot(self, data, data_type, labels=None):
       try:
           if not data:
                return "Нет данных для построения графика."
           if data_type == "line":
               self.create_line_plot(data, labels)
           elif data_type == "bar":
               self.create_bar_plot(data, labels)
           else:
             return f"Тип графика '{data_type}' не поддерживается."
           return f"График '{data_type}' успешно создан. "
       except Exception as e:
            logging.error(f"Ошибка при построении графика: {e}")
            return f"Ошибка при построении графика: {e}"

   def create_line_plot(self, data, labels=None):
         try:
             plt.figure(figsize=(10, 6))
             if labels:
                plt.plot(labels, data)
             else:
               plt.plot(data)
             plt.xlabel("X")
             plt.ylabel("Y")
             plt.title("Line Plot")
             filepath = self._save_plot()
         except Exception as e:
            logging.error(f"Ошибка при построении линейного графика: {e}")
            raise
   def create_bar_plot(self, data, labels = None):
         try:
             plt.figure(figsize=(10, 6))
             if labels:
                plt.bar(labels, data)
else:
                plt.bar(range(len(data)), data)
             plt.xlabel("X")
             plt.ylabel("Y")
             plt.title("Bar Chart")
             filepath = self._save_plot()
         except Exception as e:
             logging.error(f"Ошибка при построении гистограммы: {e}")
             raise
   def _save_plot(self):
      try:
          buffer = BytesIO()
          plt.savefig(buffer, format='png')
          buffer.seek(0)
          plot_data = base64.b64encode(buffer.read()).decode()
          filepath = os.path.join(self.image_dir, f"plot_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.png")
          with open(filepath, "wb") as f:
                f.write(base64.b64decode(plot_data))
          plt.close()
          return filepath
      except Exception as e:
         logging.error(f"Ошибка сохранения графика: {e}")
         raise