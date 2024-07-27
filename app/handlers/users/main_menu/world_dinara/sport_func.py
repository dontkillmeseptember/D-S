from data.loader import dp, bot
from data.config import ConfigBot
from data.config_Keyboard import ConfigReplyKeyboard
from data.loader_keyboard import LoaderInlineKeyboards

from database.requests.sport_db import load_sport_data
from database.requests.user_db import load_user_data, is_user_in_data, save_user_data
from database.requests.version_db import get_bot_version

from misc.libraries import types, Union
from misc.loggers import logger

@dp.message_handler(lambda message: message.text == f"{ConfigReplyKeyboard().SPORT}")
async def sport_handler(message_or_callbackQuery: Union[types.Message, types.CallbackQuery]) -> None:
	"""Объявляем переменные с выводом данных о пользователе, данных спорта и версии бота."""
	USER_DATA_DB = load_user_data()
	SPORT_DATA_DB = load_sport_data()
	VERSION_BOT = get_bot_version()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID."""
		USER_ID = ConfigBot.USERID(message_or_callbackQuery)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			"""Объявляем переменную с выводом текущей версии пользователя."""
			USER_VERSION_BOT = ConfigBot.USERVERSIONBOT(message_or_callbackQuery)

			if USER_VERSION_BOT == VERSION_BOT:
				"""Объявляем переменные с выводом информации о пользователе: SELECTED_SPORT_USER, COUNT_SPORT."""
				USER_SPORT = ConfigBot.USERSELECTEDSPORT(message_or_callbackQuery)
				COUNT_SPORT = ConfigBot.GETLENUSERS(SPORT_DATA_DB)

				if not USER_SPORT:
					if COUNT_SPORT > 0:
						"""Выводим клавиатуру для отображения вкладок с упражнениями."""
						menu_sport_inline_keyboard = LoaderInlineKeyboards().INLINE_KEYBOARDS_MENU_SPORT

						await message_or_callbackQuery.answer(f"💬 Добро пожаловать во вкладку <b>«{ConfigReplyKeyboard().SPORT[5:]}»</b>.\n\n"
															  "Выберите те <b>упражнения</b>, которые вас интересуют и подходят вам.\n\n",
															   reply_markup = menu_sport_inline_keyboard)
					
					elif COUNT_SPORT == 0:
						await message_or_callbackQuery.answer(f"💬 Добро пожаловать во вкладку <b>«{ConfigReplyKeyboard().SPORT[5:]}»</b>.\n\n"
															   " • В данной вкладке нет доступных <b>упражнений</b>.\n\n")

				elif USER_SPORT:
					if COUNT_SPORT > 0:
						"""Создаем цикл который выводит нужную информацию о спорте который выбрал пользователь."""
						for ID_SPORT, SPORT_DATA_ID in SPORT_DATA_DB.items():
							TEXT = f"{SPORT_DATA_ID['CALLBACK_DATA_SPORT']}"

							if ConfigBot.USERSELECTEDSPORTNAME(message_or_callbackQuery) == TEXT:
								"""Объявляем переменную с выводом количества тренировок в упражнение."""
								COUNT_WORKOUT = ConfigBot.GETLENUSERS(SPORT_DATA_DB[ID_SPORT]['WORKOUTS'])

								await message_or_callbackQuery.answer(f"💬 <a href='https://t.me/{ConfigBot.USERNAME(message_or_callbackQuery)}'>{ConfigBot.USERLASTNAME(message_or_callbackQuery)}</a>, {SPORT_DATA_ID['MESSAGE_SPORT'][0].lower() + SPORT_DATA_ID['MESSAGE_SPORT'][1:]}\n\n"
																	  f" • {SPORT_DATA_ID['EMODJI_SPORT']} <b>{SPORT_DATA_ID['NAME_SPORT'][16:]}</b> — <b>{COUNT_WORKOUT}</b> Упражнений:\n"
																	  f"{ConfigBot.GETWORKOUT(SPORT_DATA_DB, message_or_callbackQuery)}")

						return ID_SPORT
					
					elif COUNT_SPORT == 0:
						await message_or_callbackQuery.answer(f"💬 Добро пожаловать во вкладку <b>«{ConfigReplyKeyboard().SPORT[5:]}»</b>.\n\n"
															   " • В данной вкладке нет доступных <b>упражнений</b>.\n\n")

			elif USER_VERSION_BOT != VERSION_BOT:
				await message_or_callbackQuery.answer(f"💬 <a href='https://t.me/{ConfigBot.USERNAME(message_or_callbackQuery)}'>{ConfigBot.USERLASTNAME(message_or_callbackQuery)}</a>! Рады сообщить, что вышла <b>новая версия</b> нашего бота с улучшениями и новыми возможностями.\n\n" 
									 "❕ Для получения всех новинок и обновлений, пожалуйста, воспользуйтесь командой <b><code>/update</code></b>.\n\n" 
									 "Спасибо за ваше внимание и активное использование нашего бота! 🤍")

			else:
				logger.warning("⚠️ USER_VERSION_BOT не ровняется к текущей версии бота.")

		elif not is_user_in_data(USER_ID, USER_DATA_DB):
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{ConfigBot.USERNAME(message_or_callbackQuery)}] попытался зайти в кодекс силы.")

		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных.")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

@dp.callback_query_handler(lambda callback_data: callback_data.data and callback_data.data.startswith("sport:"))
async def select_sport_callback(callback_query: types.CallbackQuery):
	"""Объявляем переменные с выводом данных о пользователе, данных спорта и версии бота."""
	USER_DATA_DB = load_user_data()
	SPORT_DATA_DB = load_sport_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID."""
		USER_ID = ConfigBot.USERID(callback_query)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			"""Сохраняем данные о выбранном спорте пользователя в JSON."""
			USER_DATA_DB[str(ConfigBot.USERID(callback_query))]["SELECTED_SPORT"]["SELECTED_SPORT_USER"] = True
			USER_DATA_DB[str(ConfigBot.USERID(callback_query))]["SELECTED_SPORT"]["SELECTED_SPORT_NAME"] = callback_query.data

			save_user_data(USER_DATA_DB)

			"""Создаем цикл который выводит нужную информацию о спорте который выбрал пользователь."""
			for ID_SPORT, SPORT_DATA_ID in SPORT_DATA_DB.items():
				TEXT = f"{SPORT_DATA_ID['CALLBACK_DATA_SPORT']}"

				if callback_query.data == TEXT:
					"""Объявляем переменную с выводом количества тренировок в упражнение."""
					COUNT_WORKOUT = ConfigBot.GETLENUSERS(SPORT_DATA_DB[ID_SPORT]['WORKOUTS'])

					await bot.edit_message_text(f"💬 <a href='https://t.me/{ConfigBot.USERNAME(callback_query)}'>{ConfigBot.USERLASTNAME(callback_query)}</a>, {SPORT_DATA_ID['MESSAGE_SPORT'][0].lower() + SPORT_DATA_ID['MESSAGE_SPORT'][1:]}\n\n"
											    f" • {SPORT_DATA_ID['EMODJI_SPORT']} <b>{SPORT_DATA_ID['NAME_SPORT'][16:]}</b> — <b>{COUNT_WORKOUT}</b> Упражнений:\n"
												f"{ConfigBot.GETWORKOUT(SPORT_DATA_DB, callback_query)}",
												callback_query.from_user.id, 
												callback_query.message.message_id)

			return ID_SPORT

		elif not is_user_in_data(USER_ID, USER_DATA_DB):
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{ConfigBot.USERNAME(callback_query)}] попытался зайти в кодекс силы.")

		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных.")

	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)