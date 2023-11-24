from misc.libraries import ReplyKeyboardMarkup, KeyboardButton

"""Создаем клавиатуры для команды /start"""
def create_start_keyboard() -> ReplyKeyboardMarkup:
	"""Создание переменной для вывода клавиатуры"""
	keyboard_start = ReplyKeyboardMarkup(resize_keyboard=True) 
	keyboard_start.add(KeyboardButton("Запустить бот"))

	return keyboard_start