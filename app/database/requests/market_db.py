from misc.libraries import os, json

"""Создание JSON-файла с данными об товарах"""
market_path = os.path.join("app", "database", "market_data.json")

def create_market_file(file_name) -> None:
	"""
	Создание файла рынка в указанном каталоге с заданным именем файла.

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

def is_market_in_data(market_id, market_data) -> bool:
	"""
	Проверяет, присутствует ли user_id в user_data.
	
	:param user_id: Идентификатор пользователя для проверки.
	:param user_data: Данные, в которых производится поиск user_id.
	:return: True, если user_id присутствует в user_data, в противном случае - False.
	"""
	return str(market_id) in market_data

"""Загрузка данных об товаров из JSON-файла"""
def load_market_data() -> dict:
	"""Загружает рыночные данные из указанного пути к файлу и возвращает их в виде словаря."""
	try:
		with open(market_path, "r", encoding="utf-8") as file:
			return json.load(file)
		
	except FileNotFoundError:
		return {}

"""Функция для проверки данных товара в JSON-файле"""
def check_market_data(market_id) -> dict:
	"""
	Проверяет существование файла рыночных данных, и если он существует, загружает данные и возвращает данные указанного пользователя.
	:param user_id: Идентификатор пользователя, для которого требуется получить рыночные данные
	:return: Словарь, содержащий рыночные данные пользователя, или пустой словарь, если данные пользователя не найдены
	"""
	try:
		with open(market_path, "r", encoding="utf-8") as file:
			market_data = json.load(file)		
			return market_data.get(str(market_id), {})
		
	except FileNotFoundError:
		return {}

"""Сохранение данных об товар в JSON-файл"""
def save_market_data(data) -> None:
	"""
	Сохранение рыночных данных в файл.

	:param data: Рыночные данные, которые нужно сохранить
	:return: Ничего
	"""
	with open(market_path, "w", encoding="utf-8") as file:
		json.dump(data, file, ensure_ascii=False, indent=4)