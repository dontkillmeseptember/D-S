from data.loader import dp
from data.config import ConfigBot
from data.config_Keyboard import ConfigReplyKeyboard
from data.loader_keyboard import LoaderReplyKeyboards

from database.requests.version_db import get_bot_version

from misc.libraries import types
from misc.loggers import logger

@dp.message_handler(lambda message: message.text == f"{ConfigReplyKeyboard().WORLDDINARA}")
async def world_dinara_handler(message: types.Message) -> None:
	"""Объявляем переменные с выводом версии бота"""
	VERSION_BOT = get_bot_version()

	try:
		"""Объявляем переменную с выводом текущей версии пользователя"""
		USER_VERSION_BOT = ConfigBot.USERVERSIONBOT(message)

		if USER_VERSION_BOT == VERSION_BOT:
			"""Объявляем переменные о выводе клавиатуры для возвращения в главное меню вкладки Мир Динары"""
			world_menu_reply_keyboard = LoaderReplyKeyboards(message).KEYBOARDS_WORLD_MENU
			
			await message.answer(f"💬 Добро пожаловать в раздел <b>«{ConfigReplyKeyboard().WORLDDINARA[4:]}»</b>.\n\n", reply_markup=world_menu_reply_keyboard)

		elif USER_VERSION_BOT != VERSION_BOT:
			await message.answer(f"💬 <a href='https://t.me/{ConfigBot.USERNAME(message)}'>{ConfigBot.USERLASTNAME(message)}</a>! Рады сообщить, что вышла <b>новая версия</b> нашего бота с улучшениями и новыми возможностями.\n\n" 
								"❕ Для получения всех новинок и обновлений, пожалуйста, воспользуйтесь командой <b><code>/update</code></b>.\n\n" 
								"Спасибо за ваше внимание и активное использование нашего бота! 🤍")
		else:
			logger.warning("⚠️ USER_VERSION_BOT не ровняется к текущей версии бота.")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)