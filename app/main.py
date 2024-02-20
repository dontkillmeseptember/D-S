from aiogram import executor

from server.fastapi_app import keep_alive

from data.loader import dp, bot, Create_JSON_file
from data.loader_handler import Loader_Handlers, Loader_Admin_Handlers
from data.config import ConfigBot

from database.requests.admin_db import load_admin_data
from database.requests.version_db import get_bot_version, load_version_data, save_version_bot_data
from database.requests.user_db import load_user_data

from misc.libraries import logging, asyncio
from misc.loggers import logger

async def Start_bot() -> None:
	"""
	Вызываем нужные функции для создания JSON файлов и загрузка хандлеров
	"""
	try:
		"""Вызываем нужные функции для создания JSON файлов и загрузка хандлеров"""
		await asyncio.gather(
			Create_JSON_file(),
			Loader_Handlers(),
			Loader_Admin_Handlers()
		)
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

async def On_StartUP() -> str:
	"""
	Объявляем переменную с выводом информации о администрации
	Получаем chat_id из данных JSON
	Получаем информации об админов: USER_LAST_NAME, USER_NAME
	"""
	try:
		"""Объявляем переменную с выводом информации о администрации, версии бота в JSON, версии бота в виртуальном окружении, о пользователях."""
		ADMIN_DATA_DB = load_admin_data()
		USER_DATA_DB = load_user_data()
		VERSION_DATA_DB = load_version_data()
		VERSION_BOT = get_bot_version()
		ENV_VERSION_BOT = ConfigBot().VERSION

		"""Отправляем администраторам сообщение в чат о запуске бота"""
		for chat_id, admin_data in ADMIN_DATA_DB.items():
			"""Получаем информации об админов: USER_LAST_NAME, USER_NAME"""
			USER_LAST_NAME = admin_data["USER_LAST_NAME"]
			USER_NAME = admin_data["USER_NAME"]

			await bot.send_message(chat_id = int(chat_id), text = f"🔔 • {ConfigBot.GETCURRENTHOUR()}, <a href='{USER_NAME}'>{USER_LAST_NAME}</a>, бот запущен в <b><i>{ConfigBot.GETTIMENOW()}</i></b>")

		"""Проверяем версию сохраненную в JSON и в виртуальном окружение"""
		if ENV_VERSION_BOT != VERSION_BOT:
			"""Сохраняем новую версию в JSON"""
			VERSION_DATA_DB["VERSION_BOT"]["VERSION"] = ENV_VERSION_BOT

			save_version_bot_data(VERSION_DATA_DB)

			"""Отправляем пользователям сообщение в чат о новой версии бота"""
			for user_id, user_data in USER_DATA_DB.items():
				"""Получаем информации об пользователе: USER_LAST_NAME, USER_NAME"""
				USER_LAST_NAME = user_data["USER_LAST_NAME"]
				USER_NAME = user_data["USER_NAME"]

				await bot.send_message(chat_id = int(user_id), text = f"💬 <a href='{USER_NAME}'>{USER_LAST_NAME}</a>! Рады сообщить, что вышла <b>новая версия - v{ENV_VERSION_BOT}</b> нашего бота с улучшениями и новыми возможностями.\n\n"
						   											  f"❕ Для получения всех новинок и обновлений, пожалуйста, воспользуйтесь командой <b><code>/update</code></b>.\n\n"
																	  f"Спасибо за ваше внимание и активное использование нашего бота! 🤍")

	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)
		
		return ADMIN_DATA_DB

if __name__ == '__main__':
	try:
		"""Регистрация обработчика на стартап"""
		loop = asyncio.get_event_loop()
		loop.create_task(On_StartUP())

		"""Запускаем FastAPI сервер"""
		keep_alive()

		"""Вызываем логгинг файлов для отображения информации"""
		logging.basicConfig(level=logging.INFO)

		"""Запускаем телеграмм бот"""
		executor.start_polling(dp, skip_updates=True)
	except Exception as e:
		logger.critical("⚠️ Произошла непредвиденная ошибка: %s", e)