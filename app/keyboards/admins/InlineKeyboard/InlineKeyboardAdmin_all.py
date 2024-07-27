from data.config import ConfigBot
from data.config_Keyboard import ConfigInlineKeyboard

from database.requests.user_db import load_user_data

from misc.libraries import InlineKeyboardButton, InlineKeyboardMarkup
from misc.loggers import logger

"""Создаем общую функцию для уменьшения дублирования кода"""
def create_admin_inline_keyboard(button_data, row_width = 1) -> InlineKeyboardMarkup:
	try:
		buttons = [
			[InlineKeyboardButton(button_text, callback_data = callback_data) for button_text, callback_data in row]
			for row in button_data
		]
		return InlineKeyboardMarkup(row_width = row_width, inline_keyboard = buttons)
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем inline клавиатуру для вкладки "Панель управления" для администрации"""
def create_debugmenu_inlinekeyboard() -> create_admin_inline_keyboard:
	debug_menu_inline_keyboard = [
		[(ConfigInlineKeyboard().MARKET, "MARKET")],
		[(ConfigInlineKeyboard().CHECK_USER, "CHECK_USER")],
		[(ConfigInlineKeyboard().ADD_VERIFY, "ADD_VERIFY")],
		[
			("ㅤ", "#"),
			(ConfigInlineKeyboard().NEXT_EMODJI, "NEXT_DEBUG")
		]
	]

	return create_admin_inline_keyboard(debug_menu_inline_keyboard, row_width = 2)

"""Создаем inline клавиатуру для вкладки ""Панель управления" для администрации, вторую страницу"""
def create_debugmenu_inlinekeyboard_next() -> create_admin_inline_keyboard:
	debug_menu_next_inline_keyboard = [
		[(ConfigInlineKeyboard().RSB, "RSB")],
		[(ConfigInlineKeyboard().UPDATE, "UPDATE")],
		[(ConfigInlineKeyboard().SPORT, "SPORT")],
		[
			(ConfigInlineKeyboard().BACK_EMODJI, "BACK_DEBUG"),
			(ConfigInlineKeyboard().NEXT_EMODJI, "NEXT_DEBUG_THREE")
		]
	]

	return create_admin_inline_keyboard(debug_menu_next_inline_keyboard, row_width = 2)

"""Создаем Inline клавиатуру для вкладки "Панель управления" для администрации, третья страница."""
def create_debugmenu_inlinekeyboard_next_three() -> create_admin_inline_keyboard:
	debug_menu_next_three_inline_keyboard = [
		[(ConfigInlineKeyboard().RATION, "RATION")],
		[
			(ConfigInlineKeyboard().BACK_EMODJI, "BACK_DEBUG_TWO"),
			("ㅤ", "#")
		]
	]

	return create_admin_inline_keyboard(debug_menu_next_three_inline_keyboard, row_width = 2)

"""Создаем inline клавиатуру назад для администрации"""
def create_back_inlinekeyboard() -> create_admin_inline_keyboard:
	"""Объявляем переменную о выводе информации о пользователе"""
	USER_DATA_DB = load_user_data()

	back_inline_keyboard = [[(ConfigInlineKeyboard().BACK, "BACK_DEBUG")]]

	if ConfigBot.GETCONSIDERATIONVERIFY(USER_DATA_DB, keyboards = True):
		back_inline_keyboard.insert(0, [(ConfigInlineKeyboard().VERIFY, "VERIFY")])

	return create_admin_inline_keyboard(back_inline_keyboard)

"""Создаем inline клавиатуру назад для администрации"""
def create_back_verify_inlinekeyboard() -> create_admin_inline_keyboard:
	back_verify_inline_keyboard = [[(ConfigInlineKeyboard().BACK, "BACK_VERIFY")]]

	return create_admin_inline_keyboard(back_verify_inline_keyboard)

"""Создаем inline клавиатуру для управления корзиной товаров"""
def create_menu_market_admin_inlinekeyboard() -> create_admin_inline_keyboard:
	menu_market_admin_inline_keyboard = [
		[
			(ConfigInlineKeyboard().ADD_MARKET, "ADD_MARKET"),
			(ConfigInlineKeyboard().DELETE_MARKET, "DELETE_MARKET")
		],
		[(ConfigInlineKeyboard().CHECK_MARKET, "CHECK_MARKET")],
		[(ConfigInlineKeyboard().BACK, "BACK_DEBUG")]
	]

	return create_admin_inline_keyboard(menu_market_admin_inline_keyboard, row_width = 2)

"""Создаем inline клавиатуру назад вовремя фазы добавления товаров в корзину"""
def create_back_market_inlinekeyboard() -> create_admin_inline_keyboard:
	back_market_inline_keyboard = [[(ConfigInlineKeyboard().BACK, "BACK_MARKET")]]

	return create_admin_inline_keyboard(back_market_inline_keyboard)

"""Создаем inline клавиатуру назад вовремя фазы просмотра товаров в корзину"""
def create_back_debug_market_inlinekeyboard() -> create_admin_inline_keyboard:
	back_debug_market_inline_keyboard = [[(ConfigInlineKeyboard().BACK, "BACK_DEBUG")]]

	return create_admin_inline_keyboard(back_debug_market_inline_keyboard)

"""Создаем inline клавиатуру для управление RSB - Банком"""
def create_menu_rsb_admin_inlinekeyboard() -> create_admin_inline_keyboard:
	menu_rsb_admin_inline_keyboard = [
		[
			(ConfigInlineKeyboard().ADD_RSB, "ADD_RSB"),
			(ConfigInlineKeyboard().DELETE_RSB, "DELETE_RSB")
		],
		[(ConfigInlineKeyboard().REDIT_RSB, "REDIT_RSB")],
		[(ConfigInlineKeyboard().BACK, "BACK_DEBUG_INLINE_KEYBOARD_TWO")]
	]

	return create_admin_inline_keyboard(menu_rsb_admin_inline_keyboard, row_width = 2)

"""Создаем inline клавиатуру назад вовремя фазы добавление номер кошелька в RSB"""
def create_back_rsb_inlinekeyboard() -> create_admin_inline_keyboard:
	back_rsb_inline_keyboard = [[(ConfigInlineKeyboard().BACK, "BACK_RSB")]]

	return create_admin_inline_keyboard(back_rsb_inline_keyboard)

"""Создаем inline клавиатуру меню редактирование кошельков в RSB - Банке"""
def create_menu_redit_rsb_admin_inlinekeyboard() -> create_admin_inline_keyboard:
	menu_redit_rsb_admin_inline_keyboard = [
		[
			(ConfigInlineKeyboard().RELOAD_WALLET, "RELOAD_WALLET"),
			(ConfigInlineKeyboard().ADD_BUDGET, "ADD_BUDGET")
		],
		[(ConfigInlineKeyboard().BACK, "BACK_RSB")],
		[
			(ConfigInlineKeyboard().ADD_ETH, "ADD_ETH"),
			(ConfigInlineKeyboard().ADD_INTEREST, "ADD_INTEREST")
		]
	]

	return create_admin_inline_keyboard(menu_redit_rsb_admin_inline_keyboard, row_width = 2)

"""Создаем Inline клавиатуру назад вовремя фаз редактирования кошелька"""
def create_back_redit_rsb_admin_inlinekeybard() -> create_admin_inline_keyboard:
	back_redit_rsb_admin_inlinke_keyboard = [[(ConfigInlineKeyboard().BACK, "BACK_REDIT_RSB")]]

	return create_admin_inline_keyboard(back_redit_rsb_admin_inlinke_keyboard)

"""Создаем Inline клавиатуру для управления обновлениями."""
def create_menu_update_admin_inlinekeyboard() -> create_admin_inline_keyboard:
	menu_update_admin_inline_keyboard = [
		[
			(ConfigInlineKeyboard().ADD_UPDATE, "ADD_UPDATE"),
			(ConfigInlineKeyboard().DELETE_UPDATE, "DELETE_UPDATE")
		],
		[(ConfigInlineKeyboard().EDIT_UPDATE, "EDIT_UPDATE")],
		[(ConfigInlineKeyboard().BACK, "BACK_DEBUG_INLINE_KEYBOARD_TWO")]
	]

	return create_admin_inline_keyboard(menu_update_admin_inline_keyboard, row_width = 2)

"""Создаем Inline клавиатуру для редактирования обновления."""
def create_menu_edit_update_admin_inlinekeyboard() -> create_admin_inline_keyboard:
	menu_edit_update_admin_inline_keyboard = [
		[
			(ConfigInlineKeyboard().EDIT_MESSAGE_UPDATE, "EDIT_MESSAGE_UPDATE"),
			(ConfigInlineKeyboard().EDIT_NAME_UPDATE, "EDIT_NAME_UPDATE")
		],
		[(ConfigInlineKeyboard().BACK, "BACK_UPDATE")],
		[
			(ConfigInlineKeyboard().EDIT_LINK_UPDATE, "EDIT_LINK_UPDATE"),
			(ConfigInlineKeyboard().EDIT_EMOJI_UPDATE, "EDIT_EMOJI_UPDATE")
		]
	]

	return create_admin_inline_keyboard(menu_edit_update_admin_inline_keyboard, row_width = 2)

"""Создаем Inline клавиатуру для возвращения вовремя фазы редактирования обновления."""
def create_back_edit_update_inlinekeyboard() -> create_admin_inline_keyboard:
	back_edit_update_inline_keyboard = [[(ConfigInlineKeyboard().BACK, "BACK_EDIT_UPDATE")]]

	return create_admin_inline_keyboard(back_edit_update_inline_keyboard)

"""Создаем Inline клавиатуру назад вовремя фазы добавления обновления."""
def create_back_update_inlinekeyboard() -> create_admin_inline_keyboard:
	back_update_inline_keyboard = [[(ConfigInlineKeyboard().BACK, "BACK_UPDATE")]]

	return create_admin_inline_keyboard(back_update_inline_keyboard)

"""Создаем Inline клавиатуру для управлениями Упражнениями."""
def create_menu_sport_admin_inlinekeyboard() -> create_admin_inline_keyboard:
	menu_sport_admin_inline_keyboard = [
		[
			(ConfigInlineKeyboard().ADD_SPORT, "ADD_SPORT"),
			(ConfigInlineKeyboard().DELETE_SPORT, "DELETE_SPORT")
		],
		[(ConfigInlineKeyboard().EDIT_SPORT, "EDIT_SPORT")],
		[(ConfigInlineKeyboard().BACK, "BACK_DEBUG_INLINE_KEYBOARD_TWO")]
	]

	return create_admin_inline_keyboard(menu_sport_admin_inline_keyboard, row_width = 2)

"""Создаем Inline клавиатуру назад вовремя фаз добавления спорта."""
def create_back_sport_inlinekeyboard() -> create_admin_inline_keyboard:
	back_sport_inline_keyboard = [[(ConfigInlineKeyboard().BACK, "BACK_SPORT")]]

	return create_admin_inline_keyboard(back_sport_inline_keyboard)

"""Создаем Inline клавиатуру для редактирования упражнений."""
def create_menu_edit_sport_admin_inlinekeyboard() -> create_admin_inline_keyboard:
	menu_edit_sport_admin_inline_keyboard = [
		[(ConfigInlineKeyboard().DELETE_WORKOUT, "DELETE_WORKOUT")],
		[
			(ConfigInlineKeyboard().EDIT_SPORT_DESCRIPTION, "EDIT_SPORT_DESCRIPTION"),
			(ConfigInlineKeyboard().ADD_WORKOUT, "ADD_WORKOUT")
		],
		[(ConfigInlineKeyboard().BACK, "BACK_SPORT")]
	]

	return create_admin_inline_keyboard(menu_edit_sport_admin_inline_keyboard, row_width = 2)

"""Создаем Inline клавиатуру назад вовремя фаз редактирования упражнения."""
def create_back_edit_sport_admin_inlinekeybard() -> create_admin_inline_keyboard:
	back_edit_sport_admin_inlinke_keyboard = [[(ConfigInlineKeyboard().BACK, "BACK_EDIT_SPORT")]]

	return create_admin_inline_keyboard(back_edit_sport_admin_inlinke_keyboard)

"""Создаем Inline клавиатуры для управления Рационом."""
def create_menu_ration_admin_inlinekeyboard() -> create_admin_inline_keyboard:
	menu_ration_admin_inline_keyboard = [
		[
			(ConfigInlineKeyboard().ADD_RATION, "ADD_RATION"),
			(ConfigInlineKeyboard().DELETE_RATION, "DELETE_RATION")
		],
		[(ConfigInlineKeyboard().EDIT_RATION, "EDIT_RATION")],
		[(ConfigInlineKeyboard().BACK, "BACK_DEBUG_INLINE_KEYBOARD_THREE")]
	]

	return create_admin_inline_keyboard(menu_ration_admin_inline_keyboard, row_width = 2)