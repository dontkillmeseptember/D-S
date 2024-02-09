from misc.libraries import os, json

"""Создание файла для хранения данных об товарах"""
def create_rsb_file(file_name):
	"""Проверяем наличие директории, если ее нет, то создаем"""
	directory = os.path.join("app", "db")

	"""Проверка наличия папки, и создание её, если она не существует"""
	if not os.path.exists(directory):
		os.makedirs(directory)

	"""Формируем путь к файлу"""
	file_path = os.path.join(directory, file_name)

	"""Если файл не существует, то создаем его и записываем пустой JSON объект"""
	if not os.path.exists(file_path):
		with open(file_path, "w") as file:
			file.write("{}")

"""Проверка наличия товаров в данных"""
def is_rsb_in_data(user_id, user_data):
	"""Проверка, присутствует ли строковое представление user_id в admin_data"""
	return str(user_id) in user_data

"""Загрузка данных об товаров из JSON-файла"""
def load_rsb_data():
	"""Формирование пути к файлу с данными об товарах"""
	user_path = os.path.join("app", "db", "rsb_data.json")

	"""Проверка наличия файла с данными об товарах"""
	if os.path.exists(user_path):
		"""Если файл существует, открыть его для чтения"""
		with open(user_path, "r", encoding="utf-8") as file:
			return json.load(file)
		
	return {}

"""Функция для проверки данных товара в JSON-файле"""
def check_rsb_data(user_id):
	"""Формирование пути к файлу с данными о товарах"""
	user_path = os.path.join("app", "db", "rsb_data.json")

	"""Проверка наличия файла с данными о товарах"""
	if os.path.exists(user_path):
		"""Если файл существует, открыть его для чтения"""
		with open(user_path, "r", encoding="utf-8") as file:
			"""Загрузка данных о товаре из файла"""
			user_data = json.load(file)
			"""Извлечение данных о товаре с указанным user_id, если он существует"""
			return user_data.get(str(user_id), {})
		
	return {}

"""Сохранение данных об товар в JSON-файл"""
def save_rsb_data(data):
	"""Формирование пути к файлу для сохранения данных об товарах"""
	user_path = os.path.join("app", "db", "rsb_data.json")

	"""Открытие файла для записи"""
	with open(user_path, "w", encoding="utf-8") as file:
		"""
		Запись данных в файл в формате JSON
		ensure_ascii=False гарантирует, что не-ASCII символы будут записаны как есть, а не в виде escape-последовательностей
		indent=4 добавляет отступы для улучшения читаемости JSON-файла
		"""
		json.dump(data, file, ensure_ascii=False, indent=4)