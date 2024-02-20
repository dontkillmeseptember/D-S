from data.loader import dp, bot
from data.config import ConfigBot, ConfigBotAsync
from data.config_Keyboard import ConfigReplyKeyboard
from data.loader_keyboard import LoaderReplyKeyboards

from database.requests.version_db import get_bot_version
from database.requests.user_db import load_user_data, is_user_in_data, save_user_data
from database.requests.admin_db import load_admin_data, is_admin_in_data

from misc.libraries import types, RetryAfter
from misc.loggers import logger

@dp.message_handler(lambda message: message.text == ConfigReplyKeyboard().UPDATE + get_bot_version())
async def info_update_handler(message: types.Message) -> None:
	"""Объявляем переменные с выводом информации о пользователе, версии бота и администрации."""
	USER_DATA_DB = load_user_data()
	VERSION_BOT = get_bot_version()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID."""
		USER_ID = ConfigBot.USERID(message)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			"""Объявляем переменную с выводом текущей версии пользователя"""
			USER_VERSION_BOT = ConfigBot.USERVERSIONBOT(message)

			if USER_VERSION_BOT == VERSION_BOT:
				await message.answer(f"💬 Добро пожаловать в раздел <b>«{ConfigReplyKeyboard().UPDATE[5:] + VERSION_BOT}»</b>.\n\n"
						 			  "Выберите интересующее вас <b>обновление</b>, чтобы узнать подробности о <b>внесенных изменениях, новых функциях и улучшениях</b>.")
			
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