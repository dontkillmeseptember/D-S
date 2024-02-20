from misc.libraries import os, json

"""Создание JSON-файла с данными об товарах"""
user_path = os.path.join("app", "database", "rsb_data.json")

def create_rsb_file(file_name) -> None:
	"""Создание JSON-файла с данными об товарах"""
	directory = os.path.join("app", "database")

	if not os.path.exists(directory):
		os.makedirs(directory)

	file_path = os.path.join(directory, file_name)

	if not os.path.exists(file_path):
		with open(file_path, "w") as file:
			json.dump({}, file)

def is_rsb_in_data(user_id, user_data) -> bool:
	"""Функция для проверки наличия пользователя в JSON-файле"""
	return str(user_id) in user_data

def load_rsb_data() -> dict:
	"""Функция для загрузки данных об товарах из JSON-файла"""
	try:
		if os.path.exists(user_path):
			with open(user_path, "r", encoding="utf-8") as file:
				return json.load(file)
			
	except FileNotFoundError:	
		return {}

def check_rsb_data(user_id) -> dict:
	"""Функция для проверки наличия пользователя в JSON-файле"""
	try:
		with open(user_path, "r", encoding="utf-8") as file:
			user_data = json.load(file)
			return user_data.get(str(user_id), {})
	
	except FileNotFoundError:
		return {}

def save_rsb_data(data) -> None:
	"""Функция для сохранения данных об товарах в JSON-файл"""
	with open(user_path, "w", encoding="utf-8") as file:
		json.dump(data, file, ensure_ascii=False, indent=4)