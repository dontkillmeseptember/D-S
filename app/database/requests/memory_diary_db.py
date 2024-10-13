from misc.libraries import os, json

"""Создание JSON-файла с данными об товарах"""
MEMORY_DIARY_PATH = os.path.join("app", "database", "memory_diary_data.json")

def Create_Memory_Diary_File(file_name) -> None:
	DIRECTORY = os.path.join("app", "database")

	if not os.path.exists(DIRECTORY):
		os.makedirs(DIRECTORY)

	FILE_PATH = os.path.join(DIRECTORY, file_name)

	if not os.path.exists(FILE_PATH):
		with open(FILE_PATH, "w") as file:
			json.dump({}, file)

def Check_Memory_Diary_Data(memory_diary_id) -> dict:
	try:
		with open(MEMORY_DIARY_PATH, "r", encoding="utf-8") as FILE:
			MEMORY_DIARY_DATA = json.load(FILE)

			return MEMORY_DIARY_DATA.get(str(memory_diary_id), {})
	
	except FileNotFoundError:
		return {}
