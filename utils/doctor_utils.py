import logging
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
class DoctorUtils:
    def analyze_symptoms(self, symptoms):
        try:
             symptoms = symptoms.lower()
             symptom_list = [s.strip() for s in symptoms.split(",")]
             diseases = {
                "ОРВИ": ["температура", "насморк", "кашель", "боль в горле"],
                "Грипп": ["высокая температура", "ломота в теле", "головная боль", "кашель"],
                "Аллергия": ["насморк", "чихание", "зуд", "красные глаза"]
             }
             possible_diseases = []
             for disease, disease_symptoms in diseases.items():
               if all(s in symptom_list for s in disease_symptoms):
                    possible_diseases.append(disease)

             if possible_diseases:
                return f"Возможные заболевания: {', '.join(possible_diseases)}"
             else:
                return "Заболевание не найдено."
        except Exception as e:
            logging.error(f"Ошибка при анализе симптомов: {e}")
            return f"Ошибка при анализе симптомов: {e}"