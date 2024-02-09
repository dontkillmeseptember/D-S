from data.config_Keyboard import ConfigInlineKeyboard

from data.user_db import load_user_data

from misc.libraries import InlineKeyboardButton, InlineKeyboardMarkup
from misc.loggers import logger

"""Создаем общую функцию для уменьшения дублирования кода"""
def create_admin_inline_keyboard(button_data, row_width = 1) -> InlineKeyboardMarkup:
	try:
		inline_keyboard = InlineKeyboardMarkup(row_width=row_width)

		for button_text, callback_data in button_data:
			inline_keyboard.add(InlineKeyboardButton(button_text, callback_data = callback_data))

		return inline_keyboard
	except Exception as e:
		logger.error("Произошла непредвиденная ошибка: %s", e)

"""Создаем inline клавиатуру для вкладки "Панель управления" для администрации"""
def test_create_debugmenu_inlinekeyboard() -> create_admin_inline_keyboard:
	debug_menu_inline_keyboard = [
		(ConfigInlineKeyboard().MARKET, "MARKET"),
		(ConfigInlineKeyboard().CHECK_USER, "CHECK_USER"),
		(ConfigInlineKeyboard().ADD_VERIFY, "ADD_VERIFY")
		["ㅤ", "#", ConfigInlineKeyboard().NEXT_EMODJI, "NEXT_DEBUG"]
	]

	return create_admin_inline_keyboard(debug_menu_inline_keyboard)

def create_debugmenu_inlinekeyboard() -> InlineKeyboardMarkup:
	"""Создание переменной для Inline клавиатуры"""
	debugmenu_inline_keyboard = InlineKeyboardMarkup(row_width=2)
	debugmenu_inline_keyboard.add(InlineKeyboardButton(ConfigInlineKeyboard().MARKET, callback_data="MARKET"))
	debugmenu_inline_keyboard.add(InlineKeyboardButton(ConfigInlineKeyboard().CHECK_USER, callback_data="CHECK_USER"))
	debugmenu_inline_keyboard.add(InlineKeyboardButton(ConfigInlineKeyboard().ADD_VERIFY, callback_data="ADD_VERIFY"))
	debugmenu_inline_keyboard.row(
		InlineKeyboardButton("ㅤ", callback_data="#"),
		InlineKeyboardButton(ConfigInlineKeyboard().NEXT_EMODJI, callback_data="NEXT_DEBUG")
	)

	return debugmenu_inline_keyboard

"""Создаем inline клавиатуру для вкладки ""Панель управления" для администрации, вторую страницу"""
def create_debugmenu_inlinekeyboard_next() -> InlineKeyboardMarkup:
	"""Создание переменной для Inline клавиатуры"""
	debugmenu_next_inline_keyboard = InlineKeyboardMarkup(row_width=2)
	debugmenu_next_inline_keyboard.add(InlineKeyboardButton(ConfigInlineKeyboard().RSB, callback_data="RSB"))
	debugmenu_next_inline_keyboard.row(
		InlineKeyboardButton(ConfigInlineKeyboard().BACK_EMODJI, callback_data="BACK_DEBUG"),
		InlineKeyboardButton("ㅤ", callback_data="#")
	)

	return debugmenu_next_inline_keyboard

"""Создаем inline клавиатуру назад для администрации"""
def create_back_inlinekeyboard() -> InlineKeyboardMarkup:
	"""Загружаем базу данных о пользователе"""
	user_data_db = load_user_data()

	try:
		"""Счетчик для нумерации пользователей"""
		user_info_list = []

		back_inline_keyboard = InlineKeyboardMarkup(row_width=2)

		for user_id, user_info in user_data_db.items():
			if "VERIFY_DATA" in user_info and user_info["VERIFY_DATA"]["CONSIDERATION_VERIFY_USER"]:
				"""Подготовка данных для сообщения"""
				last_name = user_info["USER_LAST_NAME"]
				user_name = user_info["USER_NAME"]
				link_profile = user_info["VERIFY_DATA"]["LINK_PROFILE_USER"]

				"""Добавление информации о пользователе в список"""
				user_info_list.append(f" • {len(user_info_list) + 1}: <a href=\"{user_name}\">{last_name}</a> — <a href=\"{link_profile}\">Ссылка на Профиль</a> — <code>{user_id}</code>")
			
		"""Если есть пользователи на рассмотрении, объединяем строки в одну строку"""
		if user_info_list:
			back_inline_keyboard.add(InlineKeyboardButton(ConfigInlineKeyboard().VERIFY, callback_data="VERIFY"))
			back_inline_keyboard.add(InlineKeyboardButton(ConfigInlineKeyboard().BACK, callback_data="BACK_DEBUG"))

			return back_inline_keyboard
		else:
			back_inline_keyboard.add(InlineKeyboardButton(ConfigInlineKeyboard().BACK, callback_data="BACK_DEBUG"))

			return back_inline_keyboard
	except:
		raise ValueError("ERROR: 404, FILE: INLINEKEYBOARDADMIN_ALL, FUNC: CREATE_BACK_INLINEKEYBOARD")

"""Создаем inline клавиатуру назад для администрации"""
def create_back_verify_inlinekeyboard() -> InlineKeyboardMarkup:
	"""Создание переменной для Inline клавиатуры"""
	back_verify_inline_keyboard = InlineKeyboardMarkup(row_width=2)
	back_verify_inline_keyboard.add(InlineKeyboardButton(ConfigInlineKeyboard().BACK, callback_data="BACK_VERIFY"))

	return back_verify_inline_keyboard

"""Создаем inline клавиатуру для управления корзиной товаров"""
def create_menu_market_admin_inlinekeyboard() -> InlineKeyboardMarkup:
	"""Создание переменной для Inline клавиатуры"""
	menu_market_admin_inline_keyboard = InlineKeyboardMarkup(row_width=2)
	menu_market_admin_inline_keyboard.row(
		InlineKeyboardButton(ConfigInlineKeyboard().ADD_MARKET, callback_data="ADD_MARKET"),
		InlineKeyboardButton(ConfigInlineKeyboard().DELETE_MARKET, callback_data="DELETE_MARKET")
	)
	menu_market_admin_inline_keyboard.add(InlineKeyboardButton(ConfigInlineKeyboard().CHECK_MARKET, callback_data="CHECK_MARKET"))
	menu_market_admin_inline_keyboard.add(InlineKeyboardButton(ConfigInlineKeyboard().BACK, callback_data="BACK_DEBUG"))

	return menu_market_admin_inline_keyboard

"""Создаем inline клавиатуру назад вовремя фазы добавления товаров в корзину"""
def create_back_market_inlinekeyboard() -> InlineKeyboardMarkup:
	"""Создание переменной для Inline клавиатуры"""
	back_market_inline_keyboard = InlineKeyboardMarkup(row_width=1)
	back_market_inline_keyboard.add(InlineKeyboardButton(ConfigInlineKeyboard().BACK, callback_data="BACK_MARKET"))

	return back_market_inline_keyboard

"""Создаем inline клавиатуру назад вовремя фазы просмотра товаров в корзину"""
def create_back_debug_market_inlinekeyboard() -> InlineKeyboardMarkup:
	"""Создание переменной для Inline клавиатуры"""
	back_debug_market_inline_keyboard = InlineKeyboardMarkup(row_width=1)
	back_debug_market_inline_keyboard.add(InlineKeyboardButton(ConfigInlineKeyboard().BACK, callback_data="BACK_DEBUG"))

	return back_debug_market_inline_keyboard

"""Создаем inline клавиатуру для управление RSB - Банком"""
def create_menu_rsb_admin_inlinekeyboard() -> InlineKeyboardMarkup:
	"""Создание переменной для Inline клавиатуры"""
	menu_rsb_admin_inline_keyboard = InlineKeyboardMarkup(row_width=2)
	menu_rsb_admin_inline_keyboard.row(
		InlineKeyboardButton(ConfigInlineKeyboard().ADD_RSB, callback_data="ADD_RSB"),
		InlineKeyboardButton(ConfigInlineKeyboard().DELETE_RSB, callback_data="DELETE_RSB")
	)
	menu_rsb_admin_inline_keyboard.add(InlineKeyboardButton(ConfigInlineKeyboard().REDIT_RSB, callback_data="REDIT_RSB"))
	menu_rsb_admin_inline_keyboard.add(InlineKeyboardButton(ConfigInlineKeyboard().BACK, callback_data="NEXT_DEBUG_TWO"))

	return menu_rsb_admin_inline_keyboard

"""Создаем inline клавиатуру назад вовремя фазы добавление номер кошелька в RSB"""
def create_back_rsb_inlinekeyboard() -> InlineKeyboardMarkup:
	"""Создание переменной для Inline клавиатуры"""
	back_rsb_inline_keyboard = InlineKeyboardMarkup(row_width=1)
	back_rsb_inline_keyboard.add(InlineKeyboardButton(ConfigInlineKeyboard().BACK, callback_data="BACK_RSB"))

	return back_rsb_inline_keyboard

"""Создаем inline клавиатуру меню редактирование кошельков в RSB - Банке"""
def create_menu_redit_rsb_admin_inlinekeyboard() -> InlineKeyboardMarkup:
	"""Создание переменной для Inline клавиатуры"""
	menu_redit_rsb_admin_inline_keyboard = InlineKeyboardMarkup(row_width=2)
	menu_redit_rsb_admin_inline_keyboard.row(
		InlineKeyboardButton(ConfigInlineKeyboard().RELOAD_WALLET, callback_data="RELOAD_WALLET"),
		InlineKeyboardButton(ConfigInlineKeyboard().ADD_BUDGET, callback_data="ADD_BUDGET")
	)
	menu_redit_rsb_admin_inline_keyboard.add(InlineKeyboardButton(ConfigInlineKeyboard().BACK, callback_data="BACK_RSB"))
	menu_redit_rsb_admin_inline_keyboard.row(
		InlineKeyboardButton(ConfigInlineKeyboard().ADD_ETH, callback_data="ADD_ETH"),
		InlineKeyboardButton(ConfigInlineKeyboard().ADD_INTEREST, callback_data="ADD_INTEREST")
	)

	return menu_redit_rsb_admin_inline_keyboard

"""Создаем Inline клавиатуру назад вовремя фаз редактирования кошелька"""
def create_back_redit_rsb_admin_inlinekeybard() -> InlineKeyboardMarkup:
	back_redit_rsb_admin_inlinke_keyboard = InlineKeyboardMarkup(row_width=2)
	back_redit_rsb_admin_inlinke_keyboard.add(InlineKeyboardButton(ConfigInlineKeyboard().BACK, callback_data="BACK_REDIT_RSB"))

	return back_redit_rsb_admin_inlinke_keyboard