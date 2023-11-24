from aiogram import executor

from server.flask_app import keep_alive

from data.loader import dp, Create_JSON_file
from data.loader_handler import Loader_Handlers

from misc.libraries import logging

async def Start_bot():
	await Create_JSON_file()
	await Loader_Handlers()

if __name__ == '__main__':
	keep_alive()

	logging.basicConfig(level=logging.INFO)
	executor.start_polling(dp, skip_updates=True)