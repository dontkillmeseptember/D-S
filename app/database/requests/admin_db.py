from misc.libraries import os, json

"""Путь к JSON-файлу с данными о администраторах."""
admin_path = os.path.join("app", "database", "admins_data.json")

def create_admin_file(file_name) -> None:
	"""
	Создает административный файл в указанном каталоге с заданным именем файла. 
	:param file_name: Имя файла, который нужно создать.
	:return: None
	"""
	directory = os.path.join("app", "database")

	if not os.path.exists(directory):
		os.makedirs(directory)

	file_path = os.path.join(directory, file_name)

	if not os.path.exists(file_path):
		with open(file_path, "w") as file:
			json.dump({}, file)

def is_admin_in_data(admin_id, admin_data) -> bool:
	"""
	Проверяет, присутствует ли идентификатор пользователя в администраторских данных.

	:param user_id: Идентификатор пользователя для проверки.
	:param admin_data: Администраторские данные для поиска.
	:return: True, если идентификатор пользователя присутствует в администраторских данных, в противном случае - False.
	"""
	return str(admin_id) in admin_data

def load_admin_data() -> dict:
	"""
	Загрузить данные администратора из файла и вернуть их в виде словаря.

	Возвращает:
		dict: Данные администратора, загруженные из файла, или пустой словарь, если файл не существует.
	"""
	try:
		with open(admin_path, "r", encoding="utf-8") as file:
			return json.load(file)
		
	except FileNotFoundError:
		return {}

def save_admin_data(data) -> None:
	"""
	Сохранение данных администратора в файл.

	:param data: Данные, которые нужно сохранить.
	:return: None
	"""
	with open(admin_path, "w", encoding="utf-8") as file:
		json.dump(data, file, ensure_ascii=False, indent=4)