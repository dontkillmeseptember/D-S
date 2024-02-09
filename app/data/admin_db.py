from misc.libraries import os, json

"""Создание файла для хранения данных об администраторах"""
def create_admin_file(file_name):
	"""Формирование пути к папке для данных"""
	directory = os.path.join("app", "db")

	"""Проверка наличия папки, и создание её, если она не существует"""
	if not os.path.exists(directory):
		os.makedirs(directory)

	"""Формирование пути к файлу внутри указанной папки"""
	file_path = os.path.join(directory, file_name)

	"""Проверка наличия файла, и создание его, если он не существует"""
	if not os.path.exists(file_path):
		"""Открытие файла в режиме записи и запись в него пустого JSON-объекта"""
		with open(file_path, "w") as file:
			file.write("{}")

"""Проверка наличия администратора в данных"""
def is_admin_in_data(user_id, admin_data):
	"""Проверка, присутствует ли строковое представление user_id в admin_data"""
	return str(user_id) in admin_data

"""Загрузка данных об администраторах из JSON-файла"""
def load_admin_data():
	"""Формирование пути к файлу с данными об администраторах"""
	file_path = os.path.join("app", "db", "admins_data.json")

	"""Проверка наличия файла с данными об администраторах"""
	if os.path.exists(file_path):
		"""Если файл существует, открыть его для чтения"""
		with open(file_path, "r", encoding="utf-8") as file:
			return json.load(file)
		
	return {}

"""Сохранение данных об администраторах в JSON-файл"""
def save_admin_data(data):
	"""Формирование пути к файлу для сохранения данных об администраторах"""
	file_path = os.path.join("app", "db", "admins_data.json")

	"""Открытие файла для записи"""
	with open(file_path, "w", encoding="utf-8") as file:
		"""
		Запись данных в файл в формате JSON
		ensure_ascii=False гарантирует, что не-ASCII символы будут записаны как есть, а не в виде escape-последовательностей
		indent=4 добавляет отступы для улучшения читаемости JSON-файла
		"""
		json.dump(data, file, ensure_ascii=False, indent=4)