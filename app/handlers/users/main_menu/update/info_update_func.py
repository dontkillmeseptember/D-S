from data.loader import dp
from data.config import ConfigBot
from data.config_Keyboard import ConfigReplyKeyboard
from data.loader_keyboard import LoaderReplyKeyboards

from database.requests.version_db import get_bot_version
from database.requests.user_db import load_user_data, is_user_in_data
from database.requests.info_update_db import load_update_data

from misc.libraries import types
from misc.loggers import logger

"""Создаем обработчик для кнопки "Обновления"."""
@dp.message_handler(lambda message: message.text == ConfigReplyKeyboard().UPDATE + get_bot_version())
async def info_update_handler(message: types.Message) -> None:
	"""Объявляем переменные с выводом информации о пользователе и версии бота."""
	USER_DATA_DB = load_user_data()
	VERSION_BOT = get_bot_version()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID."""
		USER_ID = ConfigBot.USERID(message)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			"""Объявляем переменную с выводом текущей версии пользователя."""
			USER_VERSION_BOT = ConfigBot.USERVERSIONBOT(message)

			if USER_VERSION_BOT == VERSION_BOT:
				"""Объявляем переменную с выводом клавиатуру обновлений для пользователя."""
				info_update_reply_keyboard = LoaderReplyKeyboards().KEYBOARDS_INFO_UPDATE

				await message.answer(f"💬 Добро пожаловать в раздел <b>«{ConfigReplyKeyboard().UPDATE[5:] + VERSION_BOT}»</b>.\n\n"
						 			  "Выберите интересующее вас <b>обновление</b>, чтобы узнать подробности о <b>внесенных изменениях, новых функциях и улучшениях</b>.",
									  reply_markup = info_update_reply_keyboard)
			
			elif USER_VERSION_BOT != VERSION_BOT:
				await message.answer(f"💬 <a href='https://t.me/{ConfigBot.USERNAME(message)}'>{ConfigBot.USERLASTNAME(message)}</a>! Рады сообщить, что вышла <b>новая версия</b> нашего бота с улучшениями и новыми возможностями.\n\n" 
									  "❕ Для получения всех новинок и обновлений, пожалуйста, воспользуйтесь командой <b><code>/update</code></b>.\n\n" 
									  "Спасибо за ваше внимание и активное использование нашего бота! 🤍")
			
			else:
				logger.warning("⚠️ USER_VERSION_BOT не ровняется к текущей версии бота.")
		
		elif not is_user_in_data(USER_ID, USER_DATA_DB):
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{ConfigBot.USERNAME(message)}] попытался зайти во вкладку {ConfigReplyKeyboard().BATTLEPASS[4:]}.")
		
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует админ в базе данных.")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик для вкладок с обновлениями бота."""
async def update_tabs_handler(message: types.Message) -> None:
	"""Объявляем переменную с выводом информации об обновлениях бота, текущей версии бота и пользователя."""
	UPDATE_DATA_DB = load_update_data()
	USER_DATA_DB = load_user_data()
	VERSION_BOT = get_bot_version()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID."""
		USER_ID = ConfigBot.USERID(message)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			"""Объявляем переменную с выводом текущей версии пользователя."""
			USER_VERSION_BOT = ConfigBot.USERVERSIONBOT(message)

			if USER_VERSION_BOT == VERSION_BOT:
				for ID_UPDATE, UPDATE_DATA_ID in UPDATE_DATA_DB.items():
					TEXT = f"{UPDATE_DATA_ID['EMODJI_UPDATE']} • {UPDATE_DATA_ID['NAME_UPDATE']}"

					if message.text == TEXT:
						await message.answer(f"💬 {UPDATE_DATA_ID['MESSAGE_UPDATE']}\n\n"
											  " • Прочитать об обновлении можно здесь:\n"
											 f" ↳ {UPDATE_DATA_ID['URL_UPDATE']}\n\n"
											 f"Если у вас есть какие-либо вопросы или нужна помощь, не стесняйтесь обращаться к <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрации</b></a>.")
				
				return ID_UPDATE

			elif USER_VERSION_BOT != VERSION_BOT:
				await message.answer(f"💬 <a href='https://t.me/{ConfigBot.USERNAME(message)}'>{ConfigBot.USERLASTNAME(message)}</a>! Рады сообщить, что вышла <b>новая версия</b> нашего бота с улучшениями и новыми возможностями.\n\n" 
									  "❕ Для получения всех новинок и обновлений, пожалуйста, воспользуйтесь командой <b><code>/update</code></b>.\n\n" 
									  "Спасибо за ваше внимание и активное использование нашего бота! 🤍")
			
			else:
				logger.warning("⚠️ USER_VERSION_BOT не ровняется к текущей версии бота.")

		elif not is_user_in_data(USER_ID, USER_DATA_DB):
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{ConfigBot.USERNAME(message)}] попытался зайти во вкладку {ConfigReplyKeyboard().BATTLEPASS[4:]}.")
		
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует админ в базе данных.")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)