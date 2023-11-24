from misc.libraries import os, json, types

"""Создание функции для создания JSON-файла"""
def create_user_file(file_name):
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