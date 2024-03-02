from data.config import ConfigBot
from data.config_Keyboard import ConfigReplyKeyboard, ConfigRoleUsers

from database.requests.user_db import load_user_data, is_user_in_data
from database.requests.version_db import get_bot_version
from database.requests.info_update_db import load_update_data

from misc.libraries import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from misc.loggers import logger

"""Создаем общую функцию для уменьшения дублирования кода"""
def create_reply_keyboard(buttons_data, row_width = 1) -> ReplyKeyboardMarkup:
	try:
		return ReplyKeyboardMarkup([[KeyboardButton(text) for text in row] for row in buttons_data], resize_keyboard = True, row_width = row_width)
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем функцию чтобы прятать клавиатуру в нужный момент"""
def hide_keyboard() -> ReplyKeyboardRemove:
	return ReplyKeyboardRemove()

"""Создаем клавиатуру для команды /start"""
def create_start_keyboard() -> create_reply_keyboard:
	start_reply_keyboard = [[ConfigReplyKeyboard().RUN_BOT]]

	return create_reply_keyboard(start_reply_keyboard)

"""Создаем клавиатуру для главного меню"""
def create_menu_keyboard(message) -> create_reply_keyboard:
	"""Объявляем переменную с выводом информации о верификации пользователя и его роли"""
	USER_VERIFICATION = ConfigBot.USERVERIFY(message)
	USER_SMILE_ROLE = ConfigBot.USERROLE(message) if ConfigBot.USERROLE(message) is not None else ""

	if USER_VERIFICATION is None or USER_VERIFICATION is False:
		main_menu_reply_keyboard = [
			[ConfigReplyKeyboard().UPDATE + get_bot_version(), USER_SMILE_ROLE + ConfigReplyKeyboard().PROFILE]
		]
	
	elif USER_VERIFICATION:
		main_menu_reply_keyboard = [
			[ConfigReplyKeyboard().WORLDDINARA, USER_SMILE_ROLE + ConfigReplyKeyboard().PROFILE],
			[ConfigReplyKeyboard().CHAT],
			[ConfigReplyKeyboard().UPDATE + get_bot_version(), ConfigReplyKeyboard().BATTLEPASS]
		]
	
	else:
		logger.warning("⚠️ USER_VERIFICATION не ровняется True или False")

	return create_reply_keyboard(main_menu_reply_keyboard)

"""Создаем клавиатуру для вкладки Мир Динары"""
def create_world_menu_keyboard(message) -> create_reply_keyboard:
	"""Объявляем переменные с выводом информации о пользователе и о его верификации"""
	USER_DATA_DB = load_user_data()
	USER_VERIFICATION = ConfigBot.USERVERIFY(message)

	"""Объявляем проверку верифицирован пользователь или нет"""
	if USER_VERIFICATION is None or USER_VERIFICATION is False:
		return None
	
	elif USER_VERIFICATION:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID"""
		USER_ID = ConfigBot.USERID(message)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			"""Объявляем переменную с выводом информации о пользователе: USER_ROLE"""
			USER_ROLE_KEYBOARD = USER_DATA_DB.get(str(USER_ID), {}).get("USER_ROLE", None)

			if USER_ROLE_KEYBOARD in [ConfigRoleUsers().USER, ConfigRoleUsers().ADMIN]:
				world_menu_reply_keyboard = [
					[ConfigReplyKeyboard().RATION, ConfigReplyKeyboard().SPORT],
					[ConfigReplyKeyboard().MEMORYDIARY],
					[ConfigReplyKeyboard().MAINMENU, ConfigReplyKeyboard().MARKET]
				]
				
				return create_reply_keyboard(world_menu_reply_keyboard)
			else:
				logger.warning("⚠️ USER_ROLE_KEYBOARD не ровняется USER или ADMIN")
		else:
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{ConfigBot.USERNAME(message)}] попытался войти во вкладку 'Мир Динары'.")
	else:
		logger.warning("⚠️ USER_VERIFICATION не ровняется True или False")

"""Создаем клавиатуру для вкладки "Обновления" для пользователей"""
def create_info_update_keyboard() -> create_reply_keyboard:
	"""Объявляем переменную о выводе информации об обновлениях."""
	UPDATE_DATA_DB = load_update_data()

	"""Выполняем цикл для вывода информации об обновлениях."""
	info_update_reply_keyboard = [f"{UPDATE_DATA_DB[update_id]['EMODJI_UPDATE']} • {UPDATE_DATA_DB[update_id]['NAME_UPDATE']}" for update_id in reversed(UPDATE_DATA_DB.keys())]
	info_update_reply_keyboard = [info_update_reply_keyboard[i:i + 3] for i in range(0, len(info_update_reply_keyboard), 3)]

	"""Добавляем кнопку возврата в главное меню."""
	info_update_reply_keyboard.append([ConfigReplyKeyboard().MAINMENU])

	return create_reply_keyboard(info_update_reply_keyboard, row_width = 3)

"""Создаем клавиатуру для команды /update для обновления бота"""
def create_update_keyboard() -> create_reply_keyboard:
	update_reply_keyboard = [[ConfigReplyKeyboard().DOWNLOAD_UPDATE + get_bot_version() + " •"]]

	return create_reply_keyboard(update_reply_keyboard)

"""Создаем клавиатуру для завершения обновления бота"""
def create_finish_update_keyboard() -> create_reply_keyboard:
	finish_update_reply_keyboard = [[ConfigReplyKeyboard().FINISH_DOWNLOAD]]

	return create_reply_keyboard(finish_update_reply_keyboard)