from data.config import ConfigBot
from data.config_Keyboard import ConfigInlineKeyboard

from database.requests.admin_db import load_admin_data, is_admin_in_data
from database.requests.sport_db import load_sport_data

from misc.libraries import InlineKeyboardButton, InlineKeyboardMarkup, calendar
from misc.loggers import logger

"""Создаем общую функцию для уменьшения дублирования кода."""
def create_user_inline_keyboard(button_data, row_width = 1) -> InlineKeyboardMarkup:
	try:
		BUTTONS = []

		for row in button_data:
			BUTTON_ROW = []

			for BUTTON_TEXT, DATA in row:
				if isinstance(DATA, dict) and "url" in DATA:
					BUTTON_ROW.append(InlineKeyboardButton(BUTTON_TEXT, url = DATA["url"]))
				
				elif isinstance(DATA, str):
					BUTTON_ROW.append(InlineKeyboardButton(BUTTON_TEXT, callback_data = DATA))

				else:
					logger.error("⚠️ Произошла непредвиденная ошибка: %s", DATA)
			
			BUTTONS.append(BUTTON_ROW)
		
		return InlineKeyboardMarkup(row_width = row_width, inline_keyboard = BUTTONS)
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
		(False, False): [
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

def create_memory_diary_inlinekeyboard(year = None, month = None, day = 1) -> create_user_inline_keyboard:
	BACK_MONTH = month - 1 if month > 1 else 12
	BACK_YEAR = year - 1 if month == 1 else year
	NEXT_MONTH = month + 1 if month < 12 else 1
	NEXT_YEAR = year + 1 if month == 12 else year

	USER_DAY = ConfigBot.GET_USER_DAY_YEAR_MONTH('day')
	USER_YEAR = ConfigBot.GET_USER_DAY_YEAR_MONTH('year')
	USER_MONTH = ConfigBot.GET_USER_DAY_YEAR_MONTH('month')

	RUSSIAN_TRANSLATE_MONTHS = [
        'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
        'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
    ]

	memory_diary_inline_keyboard = [
		[
			(ConfigInlineKeyboard().BACK_EMODJI, f"MONTH_BACK_{BACK_YEAR}_{BACK_MONTH}"),
			(f"{year} • {RUSSIAN_TRANSLATE_MONTHS[month - 1]}", "#"),
			(ConfigInlineKeyboard().NEXT_EMODJI, f"MONTH_NEXT_{NEXT_YEAR}_{NEXT_MONTH}")
		]
	]

	DAYS_IN_MONTH = 31 if month in [1, 3, 5, 7, 8, 10, 12] else 30 if month != 2 else 29 if calendar.isleap(year) else 28

	while day <= DAYS_IN_MONTH:
		WEEK_BUTTONS = []

		for _ in range(7):
			if day > DAYS_IN_MONTH:
				break

			CALLBACK_DATA = f"{year}-{month:02d}-{day:02d}"
			MESSAGE_MEMORY_DIARY = ConfigBot.GET_MEMORY_DIARY(CALLBACK_DATA)

			if day == USER_DAY and month == USER_MONTH and year == USER_YEAR:
				if MESSAGE_MEMORY_DIARY:
					WEEK_BUTTONS.append((f"✉️", {"url": MESSAGE_MEMORY_DIARY}))
				else:
					WEEK_BUTTONS.append((f"• {str(day)} •", f"DATE_{CALLBACK_DATA}"))
			else:
				if MESSAGE_MEMORY_DIARY:
					WEEK_BUTTONS.append((f"✉️", {"url": MESSAGE_MEMORY_DIARY}))
				else:
					WEEK_BUTTONS.append((f"{str(day)}", f"DATE_{CALLBACK_DATA}"))

			day += 1
		
		memory_diary_inline_keyboard.append(WEEK_BUTTONS)

	return create_user_inline_keyboard(memory_diary_inline_keyboard, row_width = 7)

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