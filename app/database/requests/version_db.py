from data.config import ConfigBot

from misc.libraries import os, json

"""Путь к JSON-файлу с данными о версии"""
version_path = os.path.join("app", "database", "version_data.json")

def create_version_file(file_name) -> None:
	"""Функция для создания JSON-файла с данными о версии"""
	directory = os.path.join("app", "database")

	if not os.path.exists(directory):
		os.makedirs(directory)

	file_path = os.path.join(directory, file_name)

	if not os.path.exists(file_path):
		with open(file_path, "w") as file:
			 json.dump({"VERSION_BOT": {"VERSION": f"{ConfigBot().VERSION}"}} , file, indent=4)

def load_version_data() -> dict:
	"""Функция для загрузки данных о версии"""
	try:
		if os.path.exists(version_path):
			with open(version_path, "r", encoding="utf-8") as file:
				return json.load(file)
			
	except FileNotFoundError:	
		return {}

def get_bot_version() -> str:
	"""Функция для получения версии бота"""

	"""Загружаем данные о версии"""
	version_data = load_version_data()

	return version_data.get("VERSION_BOT", {}).get("VERSION", "")

def save_version_bot_data(data) -> None:
	"""
	Сохранение данных текущей версии бота в файл.

	:param data: Данные, которые нужно сохранить.
	:return: None
	"""
	with open(version_path, "w", encoding="utf-8") as file:
		json.dump(data, file, ensure_ascii=False, indent=4)