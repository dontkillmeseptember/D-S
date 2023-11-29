from misc.libraries import os, json

"""Создание функции для создания JSON-файла"""
def create_user_file(file_name) -> json:
	"""Переменная для вывода пути папки"""
	directory = os.path.join("bin", "db")

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

"""Функция для проверки наличия пользователя в данных"""
def is_user_in_data(user_id, user_data) -> json:
	"""Проверка, присутствует ли строковое представление user_id в user_data"""
	return str(user_id) in user_data

"""Функция для загрузки данных о пользователях из JSON-файла"""
def load_user_data() -> json:
	"""Формирование пути к файлу с данными о пользователях"""
	user_path = os.path.join("bin", "db", "users_data.json")

	"""Проверка наличия файла с данными о пользователях"""
	if os.path.exists(user_path):
		"""Если файл существует, открыть его для чтения"""
		with open(user_path, "r", encoding="utf-8") as file:
			"""Загрузка данных о пользователях из файла и возврат их"""
			return json.load(file)
		
	return {}

"""Сохранение данных о пользователях в JSON-файл"""
def save_user_data(data) -> json:
	"""Формирование пути к файлу для сохранения данных о пользователях"""
	user_path = os.path.join("bin", "db", "users_data.json")

	"""Открытие файла для записи"""
	with open(user_path, "w", encoding="utf-8") as file:
		"""
		Запись данных в файл в формате JSON

		ensure_ascii=False гарантирует, что не-ASCII символы будут записаны как есть, а не в виде escape-последовательностей
		indent=4 добавляет отступы для улучшения читаемости JSON-файла
		"""
		json.dump(data, file, ensure_ascii=False, indent=4)

"""Функция для проверки данных пользователя в JSON-файле"""
def check_user_data(user_id) -> json:
	"""Формирование пути к файлу с данными о пользователях"""
	user_path = os.path.join("bin", "db", "users_data.json")

	"""Проверка наличия файла с данными о пользователях"""
	if os.path.exists(user_path):
		"""Если файл существует, открыть его для чтения"""
		with open(user_path, "r", encoding="utf-8") as file:
			"""Загрузка данных о пользователях из файла"""
			user_data = json.load(file)
			"""Извлечение данных о пользователе с указанным user_id, если он существует"""
			return user_data.get(str(user_id), {})
		
	return {}