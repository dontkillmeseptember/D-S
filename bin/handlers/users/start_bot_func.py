from data.loader import dp
from data.config import LoaderKeyboards

from misc.libraries import types

"""Создаем обработчик команды /start"""
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message) -> None:
	"""Выводим клавиатуры для обработчика /start"""
	keyboard_start = LoaderKeyboards().KEYBOARDS_START
	
	await message.answer("Привет это бот", reply_markup=keyboard_start)