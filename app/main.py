from server.fastapi_app import keep_alive

from data.loader import dp, Create_JSON_file
from data.loader_handler import Loader_Handlers, Loader_Admin_Handlers, Loader_Register_Handlers, Loader_DebugMenu_Handlers
from data.config import ConfigBot, ConfigBotAsync

from database.requests.version_db import get_bot_version, load_version_data, save_version_bot_data
from database.requests.user_db import load_user_data

from misc.libraries import logging, asyncio
from misc.loggers import logger

async def start_bot() -> None:
	"""
	Вызываем нужные функции для создания JSON файлов и загрузка хандлеров.
	"""
	try:
		"""Вызываем нужные функции для создания JSON файлов и загрузка хандлеров."""
		await asyncio.gather(
			Create_JSON_file(),
			Loader_Handlers(),
			Loader_Admin_Handlers(),
			Loader_DebugMenu_Handlers()
		)
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

async def on_startup() -> str:
	"""
	Функция для обработки задач запуска.
	"""
	try:
		"""Объявляем переменную с выводом информации о версии бота в JSON, версии бота в виртуальном окружении, о пользователях."""
		USER_DATA_DB = load_user_data()
		VERSION_DATA_DB = load_version_data()
		VERSION_BOT = get_bot_version()
		ENV_VERSION_BOT = ConfigBot().VERSION

		"""Вызываем нужные функции для отправки уведомлений и загрузка хандлеров."""
		await asyncio.gather(
			ConfigBotAsync.NOTIFY_ADMINS(database_users = USER_DATA_DB),
			Loader_Register_Handlers()
		)

		if ENV_VERSION_BOT != VERSION_BOT:
			"""Сохраняем новую версию в JSON"""
			VERSION_DATA_DB["VERSION_BOT"]["VERSION"] = ENV_VERSION_BOT

			save_version_bot_data(VERSION_DATA_DB)

			await ConfigBotAsync.NOTIFY_UPDATE_USERS(database_users = USER_DATA_DB, env_version = ENV_VERSION_BOT)
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

if __name__ == '__main__':
	try:
		from aiogram import executor
		
		"""Запускаем асинхронную функцию."""
		loop = asyncio.get_event_loop()
		loop.create_task(on_startup())

		"""Запускаем FastAPI сервер."""
		keep_alive()

		"""Настройка логирования."""
		logging.basicConfig(level = logging.INFO)

		"""Запуск бота."""
		executor.start_polling(dp, skip_updates = True)
	except Exception as e:
		logger.critical("⚠️ Произошла непредвиденная ошибка: %s", e)