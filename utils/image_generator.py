import logging
import requests
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ImageGenerator:
    def __init__(self):
       self.image_dir = "generated_images"
       if not os.path.exists(self.image_dir):
           os.makedirs(self.image_dir)
    async def generate_image(self, prompt):
        try:
             api_key = "YOUR_STABLE_DIFFUSION_API_KEY"  # Замените на свой API-ключ Stable Diffusion API
             url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
             headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
             }
             data = {
                 "steps": 30,
                 "width": 1024,
                 "height": 1024,
                  "seed": 0,
                 "samples": 1,
                 "text_prompts": [
                      {
                       "text": prompt,
                        "weight": 1
                      }
                 ]
             }
             response = requests.post(url, headers=headers, json=data)
             response.raise_for_status()
             response_data = response.json()

             if not response_data['artifacts']:
                  logging.error(f"Изображение по запросу '{prompt}' не сгенерировано.")
                  return f"Изображение по запросу '{prompt}' не сгенерировано."
             image_data = response_data['artifacts'][0]['base64']
             image_name = f"generated_{prompt.replace(' ', '_')}.png"
             filepath = os.path.join(self.image_dir, image_name)
             with open(filepath, "wb") as file:
                file.write(bytes.fromhex(image_data))
             logging.info(f"Изображение по запросу '{prompt}' сохранено в: {filepath}")
             return f"Изображение по запросу '{prompt}' сохранено в: {filepath}"
        except requests.exceptions.RequestException as e:
             logging.error(f"Ошибка запроса к Stable Diffusion API: {e}")
             return f"Ошибка запроса к Stable Diffusion API: {e}"
        except KeyError:
             logging.error("Ошибка при разборе JSON: не найден ключ 'artifacts'.")
             return "Ошибка при разборе JSON: не найден ключ 'artifacts'."
        except Exception as e:
            logging.error(f"Непредвиденная ошибка при генерации изображения: {e}")
            return f"Непредвиденная ошибка при генерации изображения: {e}"