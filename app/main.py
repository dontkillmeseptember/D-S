from aiogram import executor

from server.flask_app import keep_alive

from data.config import ConfigBot

from data.admin_db import load_admin_data

from data.loader import dp, bot, Create_JSON_file
from data.loader_handler import Loader_Handlers, Loader_Admin_Handlers

from misc.libraries import logging, asyncio
from misc.loggers import logger

"""Обработчик для запуска нужных функций для работы бота"""
async def Start_bot() -> None:
	try:
		"""Вызываем нужные функции для создания JSON файлов и загрузка хандлеров"""
		await {
			Create_JSON_file(),
			Loader_Handlers(),
			Loader_Admin_Handlers()
		}
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Обработчик для отправки сообщения администрации"""
async def On_StartUP() -> str:
	try:
		"""Объявляем переменную с выводом информации о администрации"""
		ADMIN_DATA_DB = load_admin_data()

		"""Получаем chat_id из данных JSON"""
		for chat_id, admin_data in ADMIN_DATA_DB.items():
			"""Получаем информации об админов: USER_LAST_NAME, USER_NAME"""
			USER_LAST_NAME = admin_data["USER_LAST_NAME"]
			USER_NAME = admin_data["USER_NAME"]

			await bot.send_message(chat_id = int(chat_id), text = f"🔔 • {ConfigBot.GETCURRENTHOUR()}, <a href='{USER_NAME}'>{USER_LAST_NAME}</a>, бот запущен в <b><i>{ConfigBot.GETTIMENOW()}</i></b>")

			return admin_data
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)
		
		return ADMIN_DATA_DB

if __name__ == '__main__':
	try:
		"""Регистрация обработчика на стартап"""
		loop = asyncio.get_event_loop()
		loop.create_task(On_StartUP())

		"""Запускаем Flask сервер"""
		keep_alive()

		"""Вызываем логгинг файлов для отображения информации"""
		logging.basicConfig(level=logging.INFO)

		"""Запускаем телеграмм бот"""
		executor.start_polling(dp, skip_updates=True)
	except Exception as e:
		logger.critical("⚠️ Произошла непредвиденная ошибка: %s", e)