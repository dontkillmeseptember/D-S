from data.loader import dp
from data.config import ConfigBot
from data.config_Keyboard import ConfigReplyKeyboard
from data.loader_keyboard import LoaderInlineKeyboardsMemoryDiary

from database.requests.user_db import load_user_data, is_user_in_data
from database.requests.version_db import get_bot_version

from misc.libraries import types, FSMContext
from misc.loggers import logger

@dp.message_handler(lambda message: message.text == f"{ConfigReplyKeyboard().MEMORYDIARY}")
async def Memory_Diary_Handler(Message: types.Message, state: FSMContext) -> None:
	USER_DATA_DB = load_user_data()
	VERSION_BOT = get_bot_version()

	try:
		USER_ID = ConfigBot.USERID(Message)
		USER_NAME = ConfigBot.USERNAME(Message)
		USER_LAST_NAME = ConfigBot.USERLASTNAME(Message)

		START_MESSAGE = f"<a href='https://t.me/{USER_NAME}'>{USER_LAST_NAME}</a>"

		if is_user_in_data(USER_ID, USER_DATA_DB):
			USER_VERSION_BOT = ConfigBot.USERVERSIONBOT(Message)

			if USER_VERSION_BOT == VERSION_BOT:
				USER_YEAR = ConfigBot.GET_USER_DAY_YEAR_MONTH('year')
				USER_MONTH = ConfigBot.GET_USER_DAY_YEAR_MONTH('month')

				memory_days_inline_keyboard = LoaderInlineKeyboardsMemoryDiary(year = USER_YEAR, month = USER_MONTH).INLINE_KEYBOARDS_MEMORY_DAYS

				await Message.answer(f"💬 {START_MESSAGE}, вся ваша история:", reply_markup = memory_days_inline_keyboard)

				await state.set_data({"year": USER_YEAR, "month": USER_MONTH})

			elif not USER_VERSION_BOT == VERSION_BOT:
				await Message.answer(f"💬 {START_MESSAGE}! Рады сообщить, что вышла <b>новая версия</b> нашего бота с улучшениями и новыми возможностями.\n\n" 
										"❕ Для получения всех новинок и обновлений, пожалуйста, воспользуйтесь командой <b><code>/update</code></b>.\n\n" 
										"Спасибо за ваше внимание и активное использование нашего бота! 🤍")
										
		elif not is_user_in_data(USER_ID, USER_DATA_DB):
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{USER_NAME}] попытался зайти в Дневник Памяти.")

		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных.")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

async def GENERATE_SELECTED_CALENDAR_MARKUP(year: int, month: int) -> None:
	try:
		memory_days_inline_keyboard = LoaderInlineKeyboardsMemoryDiary(year = year, month = month).INLINE_KEYBOARDS_MEMORY_DAYS

		return memory_days_inline_keyboard
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

@dp.callback_query_handler(lambda callback_data: callback_data.data.startswith("MONTH_"))
async def Memory_Diary_Month_Handler(CallbackQuery: types.CallbackQuery, state: FSMContext) -> None:
	USER_DATA_DB = load_user_data()

	try:
		USER_ID = ConfigBot.USERID(CallbackQuery)
		USER_NAME = ConfigBot.USERNAME(CallbackQuery)
		USER_LAST_NAME = ConfigBot.USERLASTNAME(CallbackQuery)

		START_MESSAGE = f"<a href='https://t.me/{USER_NAME}'>{USER_LAST_NAME}</a>"

		if is_user_in_data(USER_ID, USER_DATA_DB):
			STATE_GET_DATA = await state.get_data()

			CURRENT_YEAR = STATE_GET_DATA.get("year", 2024)
			CURRENT_MONTH = STATE_GET_DATA.get("month", 1)
			
			CALLBACK_DATA = CallbackQuery.data.split("_")[1]

			if CALLBACK_DATA == "NEXT":
				CURRENT_MONTH += 1

				if CURRENT_MONTH > 12:
					CURRENT_MONTH = 1
					CURRENT_YEAR += 1

			elif CALLBACK_DATA == "BACK":
				CURRENT_MONTH -= 1

				if CURRENT_MONTH < 1:
					CURRENT_MONTH = 12
					CURRENT_YEAR -= 1

			if CURRENT_YEAR > 2024:
				CURRENT_YEAR = 2024
			
			elif CURRENT_YEAR < 2022:
				CURRENT_YEAR = 2022

			memory_days_inline_keyboard = await GENERATE_SELECTED_CALENDAR_MARKUP(year = CURRENT_YEAR, month = CURRENT_MONTH)

			await CallbackQuery.message.edit_text(f"💬 {START_MESSAGE}, вся ваша история:", reply_markup = memory_days_inline_keyboard)

			await state.update_data(year = CURRENT_YEAR, month = CURRENT_MONTH)

		elif not is_user_in_data(USER_ID, USER_DATA_DB):
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{USER_NAME}] попытался зайти в Дневник Памяти.")

		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных.")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)