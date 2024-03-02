from misc.libraries import os, json

"""Создание JSON-файла с данными об товарах"""
rsb_path = os.path.join("app", "database", "rsb_data.json")

def create_rsb_file(file_name) -> None:
	"""Создание JSON-файла с данными об товарах"""
	directory = os.path.join("app", "database")

	if not os.path.exists(directory):
		os.makedirs(directory)

	file_path = os.path.join(directory, file_name)

	if not os.path.exists(file_path):
		with open(file_path, "w") as file:
			json.dump({}, file)

def is_rsb_in_data(rsb_id, rsb_data) -> bool:
	"""Функция для проверки наличия пользователя в JSON-файле"""
	return str(rsb_id) in rsb_data

def load_rsb_data() -> dict:
	"""Функция для загрузки данных об товарах из JSON-файла"""
	try:
		if os.path.exists(rsb_path):
			with open(rsb_path, "r", encoding="utf-8") as file:
				return json.load(file)
			
	except FileNotFoundError:	
		return {}

def check_rsb_data(rsb_id) -> dict:
	"""Функция для проверки наличия пользователя в JSON-файле"""
	try:
		with open(rsb_path, "r", encoding="utf-8") as file:
			rsb_data = json.load(file)
			return rsb_data.get(str(rsb_id), {})
	
	except FileNotFoundError:
		return {}

def save_rsb_data(data) -> None:
	"""Функция для сохранения данных об товарах в JSON-файл"""
	with open(rsb_path, "w", encoding="utf-8") as file:
		json.dump(data, file, ensure_ascii=False, indent=4)