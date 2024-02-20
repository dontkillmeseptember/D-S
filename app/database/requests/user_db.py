from misc.libraries import os, json

"""Путь к JSON-файлу с данными о пользователях"""
user_path = os.path.join("app", "database", "users_data.json")

def create_user_file(file_name) -> None:
	"""Функция для создания JSON-файла"""
	directory = os.path.join("app", "database")

	if not os.path.exists(directory):
		os.makedirs(directory)

	file_path = os.path.join(directory, file_name)

	if not os.path.exists(file_path):
		with open(file_path, "w") as file:
			json.dump({}, file)

def is_user_in_data(user_id, user_data) -> bool:
	"""Проверка наличия пользователя в JSON-файле"""
	return str(user_id) in user_data

def load_user_data() -> dict:
	"""Загрузка данных о пользователях из JSON-файла"""
	try:
		with open(user_path, "r", encoding="utf-8") as file:
			return json.load(file)
		
	except FileNotFoundError:
		return {}

def save_user_data(data) -> None:
	"""Сохранение данных о пользователях в JSON-файл"""
	with open(user_path, "w", encoding="utf-8") as file:
		json.dump(data, file, ensure_ascii=False, indent=4)

def check_user_data(user_id) -> dict:
	"""Проверка наличия пользователя в JSON-файле"""
	if os.path.exists(user_path):
		with open(user_path, "r", encoding="utf-8") as file:
			user_data = json.load(file)

			return user_data.get(str(user_id), {})
		
	return {}