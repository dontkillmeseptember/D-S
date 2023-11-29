from misc.libraries import InlineKeyboardButton, InlineKeyboardMarkup

from data.config_Keyboard import ConfigInlineKeyboard

"""Создаем inline клавиатуру для восстановления пароля от учетной записи пользователя"""
def create_recovery_inlinekeyboard() -> InlineKeyboardMarkup:
	"""Создание переменной для Inline клавиатуры"""
	recovery_inline_keyboard = InlineKeyboardMarkup(row_width=1)
	recovery_inline_keyboard.add(InlineKeyboardButton(ConfigInlineKeyboard().RECOVERY_PASSWORD, callback_data="RECOVERY_PASSWORD"))

	return recovery_inline_keyboard