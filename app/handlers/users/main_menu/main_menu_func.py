from data.loader import dp
from data.config import ConfigBot, ConfigBotAsync
from data.config_Keyboard import ConfigReplyKeyboard
from data.loader_keyboard import LoaderReplyKeyboards

from database.requests.version_db import get_bot_version
from database.requests.info_update_db import load_update_data

from misc.libraries import types
from misc.loggers import logger

@dp.message_handler(lambda message: message.text in [ConfigReplyKeyboard().MAINMENU, ConfigReplyKeyboard().FINISH_DOWNLOAD])
async def main_menu_handler(message: types.Message) -> None:
	"""Объявляем переменные с выводом версии бота и информации об обновлениях."""
	VERSION_BOT = get_bot_version()
	UPDATE_DATA_DB = load_update_data()

	try:
		"""Объявляем переменную с выводом текущей версии пользователя."""
		# USER_ID = ConfigBot.USERID(message)
		USER_VERSION_BOT = ConfigBot.USERVERSIONBOT(message)
		# MESSAGE_ID = ConfigBot.GETMESSAGEID(message)

		if USER_VERSION_BOT == VERSION_BOT:
			"""Объявляем переменные о выводе клавиатуры для возвращения в главное меню."""
			main_menu_reply_keyboard = LoaderReplyKeyboards(message).KEYBOARDS_MENU

			if message.text == ConfigReplyKeyboard().MAINMENU:
				# await ConfigBotAsync.DELETE_MESSAGE_USERS_AND_ADMINS(types = message, message_id = MESSAGE_ID)

				await message.answer(f"💬 Добро пожаловать в раздел <b>«{ConfigReplyKeyboard().MAINMENU[4:]}»</b>.\n\n", reply_markup = main_menu_reply_keyboard)

				# await ConfigBotAsync.SAVE_MESSAGE_ID(user_id = USER_ID, send_message = SEND_MESSAGE)
			
			elif message.text == ConfigReplyKeyboard().FINISH_DOWNLOAD:
				for VERSION, UPDATE_DATA_ID in UPDATE_DATA_DB.items():
					if VERSION == ConfigBot().VERSION:
						await message.answer(f"{UPDATE_DATA_ID['MESSAGE_UPDATE']}", reply_markup = main_menu_reply_keyboard)
			
		elif USER_VERSION_BOT != VERSION_BOT:
			await message.answer(f"💬 <a href='https://t.me/{ConfigBot.USERNAME(message)}'>{ConfigBot.USERLASTNAME(message)}</a>! Рады сообщить, что вышла <b>новая версия</b> нашего бота с улучшениями и новыми возможностями.\n\n" 
								"❕ Для получения всех новинок и обновлений, пожалуйста, воспользуйтесь командой <b><code>/update</code></b>.\n\n" 
								"Спасибо за ваше внимание и активное использование нашего бота! 🤍")
		else:
			logger.warning("⚠️ USER_VERSION_BOT не ровняется к текущей версии бота.")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)