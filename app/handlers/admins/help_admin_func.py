from data.loader import dp
from data.config import ConfigBot

from data.admin_db import load_admin_data, is_admin_in_data

from misc.libraries import types
from misc.loggers import logger

"""Создаем обработчик команды !help"""
@dp.message_handler(lambda message: message.text == "!help")
async def help_admin_command(message: types.Message) -> str:
	"""Объявляем переменную с выводом данных о администрации"""
	ADMIN_DATA_DB = load_admin_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID"""
		USER_ID = ConfigBot.USERID(message)

		if is_admin_in_data(USER_ID , ADMIN_DATA_DB):
			await message.answer("Вот команды для использоваения")

		if not is_admin_in_data(USER_ID, ADMIN_DATA_DB):
			await message.answer("У вас нету прав использовать эту  команду")
		
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации.")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)