from misc.libraries import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from data.config_Keyboard import ConfigReplyKeyboard

"""Создаем функцию чтобы прятать клавиатуру в нужный момент"""
def hide_keyboard() -> ReplyKeyboardRemove:
	"""Создание переменной для того чтобы спрятать клавиатуру"""
	remove_keyboard = ReplyKeyboardRemove()

	return remove_keyboard

"""Создаем клавиатуру для команды /start"""
def create_start_keyboard() -> ReplyKeyboardMarkup:
	"""Создание переменной для вывода клавиатуры"""
	keyboard_start = ReplyKeyboardMarkup(resize_keyboard=True) 
	keyboard_start.add(KeyboardButton(f"{ConfigReplyKeyboard().RUN_BOT}"))

	return keyboard_start

"""Создаем клавиатуру для главного меню"""
def create_menu_keyboard() -> ReplyKeyboardMarkup:
	"""Создание переменной для вывода клавиатуры"""
	keyboard_menu = ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard_menu.add(KeyboardButton(f"{ConfigReplyKeyboard().PROFILE}"))

	return keyboard_menu