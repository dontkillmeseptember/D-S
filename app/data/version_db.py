from data.config import ConfigBot

from misc.libraries import os, json

"""Создание функции для создания JSON-файла"""
def create_version_file(file_name):
	"""Переменная для вывода пути папки"""
	directory = os.path.join("app", "db")

	"""Проверка наличия папки, и создание её, если она не существует"""
	if not os.path.exists(directory):
		os.makedirs(directory)

	"""Формирование пути к файлу внутри указанной папки"""
	file_path = os.path.join(directory, file_name)

	"""Проверка наличия файла, и создание его, если он не существует"""
	if not os.path.exists(file_path):
		"""Открытие файла в режиме записи и запись в него пустого JSON-объекта"""
		data = {
			"version_bot": {
				"version": f"{ConfigBot().VERSION}"
			}
		}
		with open(file_path, "w") as file:
			json.dump(data, file, indent=4)

"""Функция для загрузки данных о версии из JSON-файла"""
def load_version_data():
	"""Формирование пути к файлу с данными о версии"""
	version_path = os.path.join("app", "db", "version_data.json")

	"""Проверка наличия файла с данными о версии"""
	if os.path.exists(version_path):
		"""# Если файл существует, открыть его для чтения"""
		with open(version_path, "r", encoding="utf-8") as file:
			return json.load(file)
		
	return {}

"""Функция для получения версии бота из данных о версии"""
def get_bot_version():
	"""Загрузка данных о версии с использованием предыдущей функции"""
	version_data = load_version_data()
	"""Извлечение версии бота из данных о версии"""
	version_bot = version_data.get("version_bot", {}).get("version", "")
	
	return version_bot