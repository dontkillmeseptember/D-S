from data.config import ConfigBot
from data.config_Keyboard import ConfigInlineKeyboard

from database.requests.admin_db import load_admin_data, is_admin_in_data
from database.requests.sport_db import load_sport_data

from misc.libraries import InlineKeyboardButton, InlineKeyboardMarkup
from misc.loggers import logger

"""Создаем общую функцию для уменьшения дублирования кода."""
def create_user_inline_keyboard(button_data, row_width = 1) -> InlineKeyboardMarkup:
	try:
		buttons = [
			[InlineKeyboardButton(button_text, callback_data = callback_data) for button_text, callback_data in row]
			for row in button_data
		]
		return InlineKeyboardMarkup(row_width = row_width, inline_keyboard = buttons)
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем inline клавиатуру для восстановления пароля от учетной записи пользователя."""
def create_recovery_inlinekeyboard() -> create_user_inline_keyboard:
	recovery_inline_keyboard = [[(ConfigInlineKeyboard().RECOVERY_PASSWORD, "RECOVERY_PASSWORD")]]

	return create_user_inline_keyboard(recovery_inline_keyboard)

"""Создаем Inline клавиатуру для пропуска фазы с вводом нации пользователя."""
def skip_phase_nation_inlinekeyboard() -> create_user_inline_keyboard:
	skip_phase_nation_inline_keyboard = [[(ConfigInlineKeyboard().SKIP_PHASE_NATION, "SKIP_PHASE_NATION")]]

	return create_user_inline_keyboard(skip_phase_nation_inline_keyboard)

"""Создаем inline клавиатуру для вкладки "Ваш профиль" для пользователей."""
def create_profilemenu_inlinekeyboard(message) -> create_user_inline_keyboard:
	"""Объявляем переменную с выводом информации о верификации пользователя и выбрал ли пользователей спорт или нет."""
	USER_VERIFICATION = ConfigBot.USERVERIFY(message)
	USER_SPORT = ConfigBot.USERSELECTEDSPORT(message)

	profile_menu_button_configs = {
		(None, False): [
			[(ConfigInlineKeyboard().VERIFY_ACCOUNT, "VERIFY_ACCOUNT")],
			[(ConfigInlineKeyboard().DELETE_ACCOUNT, "DELETE_ACCOUNT")]
		],
		(True, True): [
			[
				(ConfigInlineKeyboard().RSB_BANK, "RSB_BANK"),
				(ConfigInlineKeyboard().NOTIFY_USER, "NOTIFY")	
			],
			[
				(ConfigInlineKeyboard().CHANGE_SPORT_USERS, "CHANGE_SPORT_USERS")
			],
			[(ConfigInlineKeyboard().DELETE_ACCOUNT, "DELETE_ACCOUNT")]
		],
		(True, False): [
			[
				(ConfigInlineKeyboard().RSB_BANK, "RSB_BANK"),
				(ConfigInlineKeyboard().NOTIFY_USER, "NOTIFY")
			],
			[(ConfigInlineKeyboard().DELETE_ACCOUNT, "DELETE_ACCOUNT")]
		]
	}

	profile_menu_inline_keyboard = profile_menu_button_configs.get((USER_VERIFICATION, USER_SPORT), [])
	
	return create_user_inline_keyboard(profile_menu_inline_keyboard)

"""Создаем Inline клавиатуру для вкладки "Уведомления" для пользователей."""
def create_notify_inlinekeyboard(message) -> create_user_inline_keyboard:
	"""Объявляем переменную с выводом информации об администрации и о пользователе: USER_ID."""
	USER_ID = ConfigBot.USERID(message)
	ADMIN_DATA_DB = load_admin_data()

	if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
		notify_menu_inline_keyboard = [
			[
				(ConfigInlineKeyboard().NOTIFY_RUN_OFF if ConfigBot.GETNOTIFY('NOTIFY_RUN', True, message) else ConfigInlineKeyboard().NOTIFY_RUN_ON, "NOTIFY_RUNS"),
				(ConfigInlineKeyboard().NOTIFY_RATION_OFF if ConfigBot.GETNOTIFY('NOTIFY_RATION', True, message) else ConfigInlineKeyboard().NOTIFY_RATION_ON, "NOTIFY_RATIONS"),
			],
			[
				(ConfigInlineKeyboard().NOTIFY_SPORT_OFF if ConfigBot.GETNOTIFY('NOTIFY_SPORT', True, message) else ConfigInlineKeyboard().NOTIFY_SPORT_ON, "NOTIFY_SPORTS"),
				(ConfigInlineKeyboard().NOTIFY_UPDATE_OFF if ConfigBot.GETNOTIFY('NOTIFY_UPDATE', True, message) else ConfigInlineKeyboard().NOTIFY_UPDATE_ON, "NOTIFY_UPDATES"),
			],
			[(ConfigInlineKeyboard().BACK, "BACK_PROFILE")]
		]

	elif not is_admin_in_data(USER_ID, ADMIN_DATA_DB):
		notify_menu_inline_keyboard = [
			[(ConfigInlineKeyboard().NOTIFY_RATION_OFF_V2 if ConfigBot.GETNOTIFY('NOTIFY_RATION', True, message) else ConfigInlineKeyboard().NOTIFY_RATION_ON_V2, "NOTIFY_RATIONS"),],
			[
				(ConfigInlineKeyboard().NOTIFY_SPORT_OFF if ConfigBot.GETNOTIFY('NOTIFY_SPORT', True, message) else ConfigInlineKeyboard().NOTIFY_SPORT_ON, "NOTIFY_SPORTS"),
				(ConfigInlineKeyboard().NOTIFY_UPDATE_OFF if ConfigBot.GETNOTIFY('NOTIFY_UPDATE', True, message) else ConfigInlineKeyboard().NOTIFY_UPDATE_ON, "NOTIFY_UPDATES"),
			],
			[(ConfigInlineKeyboard().BACK, "BACK_PROFILE")]
		]

	else:
		logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))

	return create_user_inline_keyboard(notify_menu_inline_keyboard, row_width = 2)

"""Создаем Inline клавиатуру для вкладки "Изменить Упражнение" для пользователей."""
def create_change_sport_inlinekeyboard(message) -> create_user_inline_keyboard:
	"""Объявляем переменную с выводом информации об администрации и о пользователе: SPORT_DATA_DB."""
	SPORT_DATA_DB = load_sport_data()

	"""Выполняем цикл для вывода информации о кнопках, которые пользователь еще не выбрал."""
	change_sport_inline_keyboard = [[sport_data['NAME_SPORT'], sport_data['CALLBACK_DATA_SPORT']] for sport_data in SPORT_DATA_DB.values() if ConfigBot.USERSELECTEDSPORTNAME(message) != sport_data['CALLBACK_DATA_SPORT']]
	change_sport_inline_keyboard = [change_sport_inline_keyboard[i:i + 2] for i in range(0, len(change_sport_inline_keyboard), 2)] + [[(ConfigInlineKeyboard().BACK, "BACK_PROFILE")]]

	return create_user_inline_keyboard(change_sport_inline_keyboard)

"""Создаем Inline клавиатуру для вкладки "Кодекс Силы" для пользователей"""
def create_sport_menu_inlinekeyboard() -> create_user_inline_keyboard:
	"""Объявляем переменную о выводе информации об упражнениях."""
	SPORT_DATA_DB = load_sport_data()

	"""Выполняем цикл для вывода информации об упражнениях."""
	info_sport_inline_keyboard = [[sport_data['NAME_SPORT'], sport_data['CALLBACK_DATA_SPORT']] for sport_data in SPORT_DATA_DB.values()]
	info_sport_inline_keyboard = [info_sport_inline_keyboard[i:i + 2] for i in range(0, len(info_sport_inline_keyboard), 2)]

	return create_user_inline_keyboard(info_sport_inline_keyboard)

"""Создаем inline клавиатуру для вкладки когда пользователь ввел индивидуальный код."""
def create_back_profile_inlinekeyboard() -> create_user_inline_keyboard:
	back_profile_inline_keyboard = [[(ConfigInlineKeyboard().BACK, "BACK_PROFILE")]]

	return create_user_inline_keyboard(back_profile_inline_keyboard)

"""Создаем inline клавиатуру для вкладки "Корзина Товаров" для пользователей."""
def create_marketmenu_inlinekeyboard() -> create_user_inline_keyboard:
	market_menu_inline_keyboard = [[(ConfigInlineKeyboard().CHECK_MARKET, "CHECK_MARKET")]]

	return create_user_inline_keyboard(market_menu_inline_keyboard)

"""Создаем inline клавиатуру для вкладки "Корзина Товаров" для пользователей."""
def create_marketmenu_users_inlinekeyboard() -> create_user_inline_keyboard:
	market_menu_users_inline_keyboard = [[(ConfigInlineKeyboard().CHECK_MARKET, "CHECK_MARKET_USERS")]]

	return create_user_inline_keyboard(market_menu_users_inline_keyboard)

"""Создаем inline клавиатуру назад вовремя фазы добавления товаров в корзину."""
def create_back_market_users_inlinekeyboard() -> create_user_inline_keyboard:
	back_market_users_inline_keyboard = [[(ConfigInlineKeyboard().BACK, "BACK_MARKET_USERS")]]

	return create_user_inline_keyboard(back_market_users_inline_keyboard)

"""Создаем inline клавиатуру отменить поиск вовремя фазы поиска товаров в корзине."""
def create_back_market_check_users_inlinekeyboard() -> create_user_inline_keyboard:
	back_market_check_users_inline_keyboard = [[(ConfigInlineKeyboard().NONE_SEARCH, "NONE_SEARCH")]]

	return create_user_inline_keyboard(back_market_check_users_inline_keyboard)