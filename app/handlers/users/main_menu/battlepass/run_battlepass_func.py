from data.loader import dp, bot
from data.config import ConfigBot, ConfigBotAsync
from data.config_Keyboard import ConfigReplyKeyboard
from data.loader_keyboard import LoaderReplyKeyboards

from database.requests.version_db import get_bot_version
from database.requests.user_db import load_user_data, is_user_in_data, save_user_data
from database.requests.admin_db import load_admin_data, is_admin_in_data

from misc.libraries import types, RetryAfter
from misc.loggers import logger

@dp.message_handler(lambda message: message.text == ConfigReplyKeyboard().BATTLEPASS)
async def battlepass_handler(message: types.Message) -> None:
	"""Объявляем переменные с выводом информации о пользователе, версии бота и администрации."""
	USER_DATA_DB = load_user_data()
	ADMIN_DATA_DB = load_admin_data()
	VERSION_BOT = get_bot_version()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID."""
		USER_ID = ConfigBot.USERID(message)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			"""Объявляем переменную с выводом текущей версии пользователя"""
			USER_VERSION_BOT = ConfigBot.USERVERSIONBOT(message)

			if USER_VERSION_BOT == VERSION_BOT:
				if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
					print("Works")

				elif not is_admin_in_data(USER_ID, ADMIN_DATA_DB):
					await message.answer(f"❕<b>«{ConfigReplyKeyboard().BATTLEPASS[4:]}»</b> находится в разработке. Мы работаем над созданием уникального и захватывающего опыта для вас. Скоро вас ждут новые приключения!\n\n"
						  				 " • Приблизительная дата выхода: <b><i>22/04/2024</i></b>\n\n"
						  				 f"Если у вас есть какие-либо вопросы или нужна помощь, не стесняйтесь обращаться к <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрации</b></a>.")

				else:
					logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует админ в базе данных.")
			
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