from misc.libraries import os, json

"""Создание JSON-файла с данными об упражнениях."""
sport_path = os.path.join("app", "database", "sport_data.json")

def create_sport_file(file_name) -> None:
	"""
	Создание файла упражнений в указанном каталоге с заданным именем файла.

	Параметры:
	- file_name: строка, представляющая имя файла, которое нужно создать

	Возвращает:
	- None
	"""
	directory = os.path.join("app", "database")

	if not os.path.exists(directory):
		os.makedirs(directory)

	file_path = os.path.join(directory, file_name)

	if not os.path.exists(file_path):
		with open(file_path, "w") as file:
			json.dump({}, file)

def is_sport_in_data(sport_id, sport_data) -> bool:
	"""
	Проверяет, присутствует ли sport_id в sport_data.
	
	:param sport_id: Идентификатор пользователя для проверки.
	:param sport_data: Данные, в которых производится поиск sport_id.
	:return: True, если sport_id присутствует в sport_data, в противном случае - False.
	"""
	return str(sport_id) in sport_data

"""Загрузка данных об упражнениях из JSON-файла"""
def load_sport_data() -> dict:
	"""Загружает упражнения из указанного пути к файлу и возвращает их в виде словаря."""
	try:
		with open(sport_path, "r", encoding="utf-8") as file:
			return json.load(file)
		
	except FileNotFoundError:
		return {}

"""Функция для проверки данных упражнений в JSON-файле"""
def check_sport_data(market_id) -> dict:
	"""
	Проверяет существование файла рыночных данных, и если он существует, загружает данные и возвращает данные указанного пользователя.

	:param market_id: Идентификатор пользователя, для которого требуется получить рыночные данные
	:return: Словарь, содержащий рыночные данные пользователя, или пустой словарь, если данные пользователя не найдены
	"""
	try:
		with open(sport_path, "r", encoding="utf-8") as file:
			market_data = json.load(file)		
			return market_data.get(str(market_id), {})
		
	except FileNotFoundError:
		return {}

"""Сохранение данных об упражнениях в JSON-файл"""
def save_sport_data(data) -> None:
	"""
	Сохранение упражнений в файл.

	:param data: Рыночные данные, которые нужно сохранить
	:return: Ничего
	"""
	with open(sport_path, "w", encoding = "utf-8") as file:
		json.dump(data, file, ensure_ascii = False, indent = 4)