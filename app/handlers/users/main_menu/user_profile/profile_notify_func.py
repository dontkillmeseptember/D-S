from data.loader import dp, bot
from data.config import ConfigBot
from data.loader_keyboard import LoaderInlineKeyboards
from data.states_groups import ProfileState

from database.requests.user_db import load_user_data, is_user_in_data, save_user_data
from database.requests.admin_db import load_admin_data, is_admin_in_data

from misc.loggers import logger
from misc.libraries import types

"""Создаем обработчик для управления уведомлениями бота для пользователей."""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "NOTIFY")
async def notify_user_handler(callback_query: types.CallbackQuery):
	"""Объявляем переменные с выводом данных о пользователе и администрации."""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID."""
		USER_ID = ConfigBot.USERID(callback_query)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			"""Объявляем переменную с выводом информации о верификации пользователя."""
			USER_VERIFICATION = ConfigBot.USERVERIFY(callback_query)

			if USER_VERIFICATION is None or USER_VERIFICATION is False:
				logger.warning(f"⚠️ Неверифицированный пользователь [@{ConfigBot.USERNAME(callback_query)}] попытался зайти в уведомления.")
			
			elif USER_VERIFICATION:
				"""Выводим inline клавиатуру для меню уведомлений."""
				notify_menu_inline_keyboard = LoaderInlineKeyboards(callback_query).INLINE_KEYBOARDS_NOTIFYMENU

				if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
					"""Объявляем переменную с выводом сообщения об информации уведомлениях для администрации."""
					INFO_NOTIFY_MENU_MESSAGE = f"💬 Текущая информация об уведомлениях.\n\n" \
											   f" • Уведомления об <b>«Запуске бота»</b> - <code>{'Вкл' if ConfigBot.GETNOTIFY('NOTIFY_RUN', True, callback_query) else 'Выкл'}</code>\n\n" \
											   f" • Уведомления об <b>«Рационе»</b> - <code>{'Вкл' if ConfigBot.GETNOTIFY('NOTIFY_RATION', True, callback_query) else 'Выкл'}</code>\n\n" \
											   f" • Уведомления об <b>«Кодексе силы»</b> - <code>{'Вкл' if ConfigBot.GETNOTIFY('NOTIFY_SPORT', True, callback_query) else 'Выкл'}</code>\n\n" \
											   f" • Уведомления об <b>«Обновлениях»</b> - <code>{'Вкл' if ConfigBot.GETNOTIFY('NOTIFY_UPDATE', True, callback_query) else 'Выкл'}</code>\n"

				elif not is_admin_in_data(USER_ID, ADMIN_DATA_DB):
					"""Объявляем переменную с выводом сообщения об информации уведомлениях для пользователей."""
					INFO_NOTIFY_MENU_MESSAGE = f"💬 Текущая информация об уведомлениях.\n\n" \
											   f" • Уведомления об <b>«Рационе»</b> - <code>{'Вкл' if ConfigBot.GETNOTIFY('NOTIFY_RATION', False, callback_query) else 'Выкл'}</code>\n\n" \
											   f" • Уведомления об <b>«Кодексе силы»</b> - <code>{'Вкл' if ConfigBot.GETNOTIFY('NOTIFY_SPORT', False, callback_query) else 'Выкл'}</code>\n\n" \
											   f" • Уведомления об <b>«Обновлениях»</b> - <code>{'Вкл' if ConfigBot.GETNOTIFY('NOTIFY_UPDATE', False, callback_query) else 'Выкл'}</code>\n"

				else:
					logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
				
				await bot.edit_message_caption(caption = INFO_NOTIFY_MENU_MESSAGE, 
											   chat_id = callback_query.message.chat.id, 
											   message_id = callback_query.message.message_id, 
											   reply_markup = notify_menu_inline_keyboard)
				
		else:
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{ConfigBot.USERNAME(callback_query)}] попытался зайти в уведомления.")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик для обработки callback запросов об выключения/включение уведомлений."""
@dp.callback_query_handler(lambda callback_data: callback_data.data in ["NOTIFY_RUNS", "NOTIFY_RATIONS", "NOTIFY_SPORTS", "NOTIFY_UPDATES"])
async def notify_user_handler(callback_query: types.CallbackQuery) -> ProfileState:
	try:
		"""Объявляем переменные с выводом информации о пользователе и callback данными."""
		USER_DATA_DB = load_user_data()
		CALLBACK_DATA = callback_query.data

		"""Объявляем словарь с данными для уведомлений."""
		NOTIFY_MAP = {
			"NOTIFY_RUNS": ("NOTIFY_RUN", True, "ADMIN_NOTIFY", "Запуск бота"),
			"NOTIFY_RATIONS": ("NOTIFY_RATION", False, "USER_NOTIFY", "Рацион"),
			"NOTIFY_SPORTS": ("NOTIFY_SPORT", False, "USER_NOTIFY", "Кодекс силы"),
			"NOTIFY_UPDATES": ("NOTIFY_UPDATE", False, "USER_NOTIFY", "Обновления"),
		}

		if CALLBACK_DATA in NOTIFY_MAP:
			NOTIFY_TYPE, IS_ADMIN, NOTIFY_CATEGORY, TEXT_NOTIFY = NOTIFY_MAP[CALLBACK_DATA]

			if ConfigBot.GETNOTIFY(NOTIFY_TYPE, IS_ADMIN, callback_query):
				USER_DATA_DB[str(ConfigBot.USERID(callback_query))]["NOTIFY_DATA"][NOTIFY_CATEGORY][NOTIFY_TYPE] = False

				await bot.answer_callback_query(callback_query.id, text = f"Уведомления для «{TEXT_NOTIFY}» выключены.")

			elif not ConfigBot.GETNOTIFY(NOTIFY_TYPE, IS_ADMIN, callback_query):
				USER_DATA_DB[str(ConfigBot.USERID(callback_query))]["NOTIFY_DATA"][NOTIFY_CATEGORY][NOTIFY_TYPE] = True

				await bot.answer_callback_query(callback_query.id, text = f"Уведомления для «{TEXT_NOTIFY}» включены.")

			save_user_data(USER_DATA_DB)

			await notify_user_keyboard_handler(callback_query)
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик для изменения inline клавиатуры для раздела связанный с уведомлениями и избежания рекурсии."""
async def notify_user_keyboard_handler(callback_query: types.CallbackQuery):
	try:
		"""Объявляем переменные с выводом информации о администрации и вывод данных о пользователе: USER_ID."""
		ADMIN_DATA_DB = load_admin_data()
		USER_ID = ConfigBot.USERID(callback_query)

		"""Объявляем словарь с данными для уведомлений."""
		NOTIFY_TYPES = {
			'NOTIFY_RUN': 'Уведомления об <b>«Запуске бота»</b>',
			'NOTIFY_RATION': 'Уведомления об <b>«Рационе»</b>',
			'NOTIFY_SPORT': 'Уведомления об <b>«Кодексе силы»</b>',
			'NOTIFY_UPDATE': 'Уведомления об <b>«Обновлениях»</b>'
		}

		INFO_NOTIFY_MENU_MESSAGE = f"💬 Текущая информация об уведомлениях.\n\n"

		if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
			INFO_NOTIFY_MENU_MESSAGE += " • " + " • ".join([f"{value} - <code>{'Вкл' if ConfigBot.GETNOTIFY(key, True, callback_query) else 'Выкл'}</code>\n\n" for key, value in NOTIFY_TYPES.items()])
		
		elif not is_admin_in_data(USER_ID, ADMIN_DATA_DB):
			INFO_NOTIFY_MENU_MESSAGE += " • " + " • ".join([f"{value} - <code>{'Вкл' if ConfigBot.GETNOTIFY(key, False, callback_query) else 'Выкл'}</code>\n\n" for key, value in NOTIFY_TYPES.items() if key != 'NOTIFY_RUN'])

		else:
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{ConfigBot.USERNAME(callback_query)}] попытался зайти в уведомления.")

		"""Выводим inline клавиатуру для меню уведомлений."""
		notify_menu_inline_keyboard = LoaderInlineKeyboards(callback_query).INLINE_KEYBOARDS_NOTIFYMENU

		await bot.edit_message_caption(caption = INFO_NOTIFY_MENU_MESSAGE, 
									   chat_id = callback_query.message.chat.id, 
									   message_id = callback_query.message.message_id,
									   reply_markup = notify_menu_inline_keyboard)
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)