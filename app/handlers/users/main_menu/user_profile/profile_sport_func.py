from data.loader import dp, bot
from data.config import ConfigBot
from data.loader_keyboard import LoaderInlineKeyboards
from data.states_groups import ProfileState

from database.requests.user_db import load_user_data, is_user_in_data, save_user_data
from database.requests.sport_db import load_sport_data

from misc.loggers import logger
from misc.libraries import types

"""Создаем обработчик для выбора спорта пользователя."""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "CHANGE_SPORT_USERS", state = [ProfileState.SelectedNewSportState, None])
async def change_sport_users_handler(callback_query: types.CallbackQuery):
	"""Объявляем переменные с выводом данных о пользователе и администрации."""
	USER_DATA_DB = load_user_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID."""
		USER_ID = ConfigBot.USERID(callback_query)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			"""Объявляем переменную с выводом информации о верификации пользователя."""
			USER_VERIFICATION = ConfigBot.USERVERIFY(callback_query)

			if USER_VERIFICATION is None or USER_VERIFICATION is False:
				logger.warning(f"⚠️ Неверифицированный пользователь [@{ConfigBot.USERNAME(callback_query)}] попытался зайти в изменение упражнения.")

			elif USER_VERIFICATION:
				"""Объявляем переменную с выводом inline клавиатуры для выбора нового упражнения пользователя."""
				change_sport_inline_keyboard = LoaderInlineKeyboards(callback_query).INLINE_KEYBOARDS_CHANGESPORT

				await bot.edit_message_caption(caption = f"💬 <a href='https://t.me/{ConfigBot.USERNAME(callback_query)}'>{ConfigBot.USERLASTNAME(callback_query)}</a>, eсли вы хотите <b>изменить</b> текущее упражнение на другое, пожалуйста, выберите <b>нужное</b> из списка ниже.\n\n"
								   						 f"Если у вас возникли вопросы или вам требуется дополнительная помощь, не стесняйтесь обращаться к нашей <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрации</b></a>", 
								   			   chat_id = callback_query.message.chat.id, 
											   message_id = callback_query.message.message_id, 
											   reply_markup = change_sport_inline_keyboard)
				
				await ProfileState.SelectedNewSportState.set()

		else:
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{ConfigBot.USERNAME(callback_query)}] попытался зайти в изменение упражнения.")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик фазы, где пользователь нажимает на нужное ему упражнение и выбирает новое упражнение."""
@dp.callback_query_handler(lambda callback_data: callback_data.data and callback_data.data.startswith("sport:"), state = ProfileState.SelectedNewSportState)
async def change_sport_handler(callback_query: types.CallbackQuery):
	"""Объявляем переменные с выводом данных о пользователе и администрации."""
	USER_DATA_DB = load_user_data()
	SPORT_DATA_DB = load_sport_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID."""
		USER_ID = ConfigBot.USERID(callback_query)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			"""Изменяет текущие упражнение на новое, которое выбрал пользователь."""
			USER_DATA_DB[str(USER_ID)]["SELECTED_SPORT"]["SELECTED_SPORT_NAME"] = callback_query.data

			save_user_data(USER_DATA_DB)

			SPORT_DATA_ID = next((sport_data for sport_id, sport_data in SPORT_DATA_DB.items() if sport_data["CALLBACK_DATA_SPORT"] == callback_query.data), None)

			if SPORT_DATA_ID:
				await bot.answer_callback_query(callback_query.id, text = f"Вы успешно изменили «{SPORT_DATA_ID['NAME_SPORT'][2:]}».")
			
			await change_sport_users_handler(callback_query)
		else:
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{ConfigBot.USERNAME(callback_query)}] попытался зайти в изменение упражнения.")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)