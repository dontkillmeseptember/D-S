from misc.libraries import os, json

"""Путь к JSON-файлу с данными о обновлениях"""
update_path = os.path.join("app", "database", "update_data.json")

def create_update_file(file_name) -> None:
	"""Функция для создания JSON-файла"""
	directory = os.path.join("app", "database")

	if not os.path.exists(directory):
		os.makedirs(directory)

	file_path = os.path.join(directory, file_name)

	if not os.path.exists(file_path):
		with open(file_path, "w") as file:
			json.dump({}, file)

def is_update_in_data(update_id, update_data) -> bool:
	"""Проверка наличия обновлений в JSON-файле"""
	return str(update_id) in update_data

def load_update_data() -> dict:
	"""Загрузка данных о обновлениях из JSON-файла"""
	try:
		with open(update_path, "r", encoding="utf-8") as file:
			return json.load(file)
		
	except FileNotFoundError:
		return {}

def save_update_data(data) -> None:
	"""Сохранение данных о обновлениях в JSON-файл"""
	with open(update_path, "w", encoding="utf-8") as file:
		json.dump(data, file, ensure_ascii=False, indent=4)

def check_update_data(update_id) -> dict:
	"""Проверка наличия обновлений в JSON-файле"""
	if os.path.exists(update_path):
		with open(update_path, "r", encoding="utf-8") as file:
			update_data = json.load(file)

			return update_data.get(str(update_id), {})
		
	return {}