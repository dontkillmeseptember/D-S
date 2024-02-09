from data.config import ConfigBot
from data.config_Keyboard import ConfigInlineKeyboard

from misc.libraries import InlineKeyboardButton, InlineKeyboardMarkup
from misc.loggers import logger

"""Создаем общую функцию для уменьшения дублирования кода"""
def create_inline_keyboard(button_data, row_width = 1) -> InlineKeyboardMarkup:
	try:
		inline_keyboard = InlineKeyboardMarkup(row_width=row_width)

		for button_text, callback_data in button_data:
			inline_keyboard.add(InlineKeyboardButton(button_text, callback_data = callback_data))

		return inline_keyboard
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем inline клавиатуру для восстановления пароля от учетной записи пользователя"""
def create_recovery_inlinekeyboard() -> create_inline_keyboard:
	recovery_inline_keyboard = [(ConfigInlineKeyboard().RECOVERY_PASSWORD, "RECOVERY_PASSWORD")]

	return create_inline_keyboard(recovery_inline_keyboard)

"""Создаем inline клавиатуру для вкладки "Ваш профиль" для пользователей"""
def create_profilemenu_inlinekeyboard(message) -> create_inline_keyboard:
	"""Объявляем переменную с выводом информации о верификации пользователя"""
	USER_VERIFICATION = ConfigBot.USERVERIFY(message)

	if USER_VERIFICATION is None or USER_VERIFICATION is False:
		profile_menu_inline_keyboard = [
			(ConfigInlineKeyboard().VERIFY_ACCOUNT, "VERIFY_ACCOUNT"),
			(ConfigInlineKeyboard().DELETE_ACCOUNT, "DELETE_ACCOUNT")
		]
	
	elif USER_VERIFICATION:
		profile_menu_inline_keyboard = [
			(ConfigInlineKeyboard().RSB_BANK, "RSB_BANK"),
			(ConfigInlineKeyboard().DELETE_ACCOUNT, "DELETE_ACCOUNT")
		]
	
	else:
		logger.warning("⚠️ USER_VERIFICATION не ровняется True или False")
	
	return create_inline_keyboard(profile_menu_inline_keyboard, row_width = 2)
	
"""Создаем inline клавиатуру для вкладки когда пользователь ввел индивидуальный код"""
def create_back_profile_inlinekeyboard() -> create_inline_keyboard:
	back_profile_inline_keyboard = [(ConfigInlineKeyboard().BACK, "BACK_PROFILE")]

	return create_inline_keyboard(back_profile_inline_keyboard)

"""Создаем inline клавиатуру для вкладки "Корзина Товаров" для пользователей"""
def create_marketmenu_inlinekeyboard() -> create_inline_keyboard:
	market_menu_inline_keyboard = [(ConfigInlineKeyboard().CHECK_MARKET, "CHECK_MARKET")]

	return create_inline_keyboard(market_menu_inline_keyboard)

"""Создаем inline клавиатуру для вкладки "Корзина Товаров" для пользователей"""
def create_marketmenu_users_inlinekeyboard() -> create_inline_keyboard:
	market_menu_users_inline_keyboard = [(ConfigInlineKeyboard().CHECK_MARKET, "CHECK_MARKET_USERS")]

	return create_inline_keyboard(market_menu_users_inline_keyboard)

"""Создаем inline клавиатуру назад вовремя фазы добавления товаров в корзину"""
def create_back_market_users_inlinekeyboard() -> create_inline_keyboard:
	back_market_users_inline_keyboard = [(ConfigInlineKeyboard().BACK, "BACK_MARKET_USERS")]

	return create_inline_keyboard(back_market_users_inline_keyboard)

"""Создаем inline клавиатуру отменить поиск вовремя фазы поиска товаров в корзине"""
def create_back_market_check_users_inlinekeyboard() -> create_inline_keyboard:
	back_market_check_users_inline_keyboard = [(ConfigInlineKeyboard().NONE_SEARCH, "NONE_SEARCH")]

	return create_inline_keyboard(back_market_check_users_inline_keyboard)