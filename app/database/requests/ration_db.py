from misc.libraries import os, json

"""Создание JSON-файла с данными об упражнениях."""
ration_path = os.path.join("app", "database", "ration_data.json")

def create_ration_file(file_name) -> None:
	"""
	Создание файла рациона в указанном каталоге с заданным именем файла.

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

def is_ration_in_data(ration_id, ration_data) -> bool:
	"""
	Проверяет, присутствует ли ration_id в ration_data.
	
	:param ration_id: Идентификатор пользователя для проверки.
	:param ration_data: Данные, в которых производится поиск ration_id.
	:return: True, если ration_id присутствует в ration_data, в противном случае - False.
	"""
	return str(ration_id) in ration_data

"""Загрузка данных об рационе из JSON-файла"""
def load_ration_data() -> dict:
	"""Загружает рацион из указанного пути к файлу и возвращает их в виде словаря."""
	try:
		with open(ration_path, "r", encoding="utf-8") as file:
			return json.load(file)
		
	except FileNotFoundError:
		return {}

"""Функция для проверки данных рациона в JSON-файле"""
def check_ration_data(ration_id) -> dict:
	"""
	Проверяет существование файла рациона, и если он существует, загружает данные и возвращает данные указанного пользователя.

	:param ration_id: Идентификатор пользователя, для которого требуется получить рыночные данные
	:return: Словарь, содержащий рыночные данные пользователя, или пустой словарь, если данные пользователя не найдены
	"""
	try:
		with open(ration_path, "r", encoding="utf-8") as file:
			ration_data = json.load(file)		
			return ration_data.get(str(ration_id), {})
		
	except FileNotFoundError:
		return {}

"""Сохранение данных об рационе в JSON-файл"""
def save_ration_data(data) -> None:
	"""
	Сохранение рациона в файл.

	:param data: Рыночные данные, которые нужно сохранить
	:return: Ничего
	"""
	with open(ration_path, "w", encoding = "utf-8") as file:
		json.dump(data, file, ensure_ascii = False, indent = 4)