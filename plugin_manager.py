import logging
import importlib
import os
import inspect

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PluginManager:
    def __init__(self, plugin_dir='plugins'):
        self.plugin_dir = plugin_dir
        self.plugins = {}
        self._load_plugins()

    def _load_plugins(self):
        if not os.path.exists(self.plugin_dir):
            logging.warning(f"Директория плагинов не найдена: {self.plugin_dir}")
            return
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith('.py'):
                module_name = filename[:-3]
                try:
                    module_path = os.path.join(self.plugin_dir, filename)
                    spec = importlib.util.spec_from_file_location(module_name, module_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    for name, obj in inspect.getmembers(module):
                      if inspect.isclass(obj) and name.lower().endswith("plugin") and obj != "BasePlugin":
                         plugin_instance = obj()
                         self.plugins[module_name] = plugin_instance
                         logging.info(f"Плагин '{name}' загружен из '{filename}'")
                except Exception as e:
                    logging.error(f"Ошибка при загрузке плагина из '{filename}': {e}")
    def get_plugins(self):
       return self.plugins