from data.loader import dp, bot
from data.config import ConfigBot
from data.loader_keyboard import LoaderInlineKeyboards
from data.states_groups import ProfileState

from database.requests.user_db import load_user_data, is_user_in_data, save_user_data
from database.requests.admin_db import load_admin_data, is_admin_in_data, save_admin_data

from misc.loggers import logger
from misc.libraries import types, FSMContext

from keyboards.users.ReplyKeyboard.ReplyKeyboard_all import hide_keyboard

"""Создаем обработчик для удаления аккаунта пользователя"""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "DELETE_ACCOUNT")
async def delete_account_handler(callback_query: types.CallbackQuery) -> ProfileState:
	"""Объявляем переменные с выводом данных о пользователе"""
	USER_DATA_DB = load_user_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID"""
		USER_ID = ConfigBot.USERID(callback_query)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)

			""""Объявляем переменные о выводе клавиатуры для возвращения обратно в профиль"""
			back_profile_inline_keyboard = LoaderInlineKeyboards(callback_query).INLINE_KEYBOARDS_BACK_PROFILEMENU

			await bot.send_message(chat_id = callback_query.message.chat.id, 
						  		   text = f"💬 Для <b>удаления</b> вашего аккаунта, <a href='https://t.me/{ConfigBot.USERNAME(callback_query)}'>{ConfigBot.USERLASTNAME(callback_query)}</a>, пожалуйста, введите ваш <b>текущий пароль</b>.\n\nЭтот шаг необходим для подтверждения вашей личности и обеспечения безопасности процесса удаления аккаунта.\n\n"
						  		   		  f"Если у вас возникли вопросы или вам требуется дополнительная помощь, не стесняйтесь обращаться к нашей <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрации</b></a>",
								   reply_markup = back_profile_inline_keyboard)

			"""Переходим фазу, где пользователь вводит пароль от учетной записи"""
			await ProfileState.SendUserPasswordState.set()
		else:
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{ConfigBot.USERNAME(callback_query)}] попытался удалить аккаунт.")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчика фазы, где пользователь вводит пароль от учетной записи"""
@dp.message_handler(state = ProfileState.SendUserPasswordState)
async def send_user_password_handler(message: types.Message) -> ProfileState:
	try:
		"""Объявляем переменную c выводом информации о пользователя: USER_PASSWORD, USER_MESSAGE"""
		USER_PASSWORD = ConfigBot.USERPASSWORD(message)
		USER_MESSAGE = ConfigBot.USERMESSAGE(message)

		if USER_PASSWORD == USER_MESSAGE:
			await message.answer(f"💬 Отлично, <a href='https://t.me/{ConfigBot.USERNAME(message)}'>{ConfigBot.USERLASTNAME(message)}</a>! Пароль от вашей учетной записи успешно <b>подтвержден</b>.\n\n"
								 f"Для окончательного подтверждения удаления аккаунта, введите <b>\"ПОДТВЕРЖДАЮ\"</b> (без кавычек). Этот шаг необходим для предотвращения случайного удаления аккаунта.\n\n"
								 f"Если у вас возникли вопросы или вам требуется дополнительная помощь, не стесняйтесь обращаться к нашей <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрации</b></a>")
			
			"""Переходим в фазу, где вводят ПОДТВЕРЖДАЮ для удаления аккаунта"""
			await ProfileState.SendApprovedState.set()

		elif USER_PASSWORD != USER_MESSAGE:
			await message.answer(f"⚠️ Кажется, что пароль введен <b>неверно</b>. Пожалуйста, проверьте свои данные и попробуйте еще раз.\n\n"
								 f"Если у вас возникли проблемы с доступом, вы можете связаться с нашей <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрацией</b></a>.")
		else:
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{ConfigBot.USERNAME(message)}] попытался ввести пароль от аккаунта.")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчика фазы, где пользователь вводит ПОДТВЕРЖДАЮ для удаления учетной записи"""
@dp.message_handler(state = ProfileState.SendApprovedState)
async def send_user_password_handler(message: types.Message, state: FSMContext) -> FSMContext:
	"""Объявляем переменные с выводом данных о пользователе и администраторах"""
	USER_DATA_DB = load_user_data()
	ADMIN_DATA_DB = load_admin_data()

	try:
		"""Объявляем переменную c выводом информации о пользователя: USER_MESSAGE, USER_ID"""
		USER_MESSAGE = ConfigBot.USERMESSAGE(message)
		USER_ID = ConfigBot.USERID(message)

		if USER_MESSAGE == "ПОДТВЕРЖДАЮ":
			"""Удаляем полностью все данные пользователя в базе данных пользователей и администраторов"""
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				del ADMIN_DATA_DB[str(USER_ID)]

				save_admin_data(ADMIN_DATA_DB)

			del USER_DATA_DB[str(USER_ID)]

			save_user_data(USER_DATA_DB)

			await message.answer(f"💬 <a href='https://t.me/{ConfigBot.USERNAME(message)}'>{ConfigBot.USERLASTNAME(message)}</a>! Вы успешно ввели <b>подтверждение.</b> Ваша учетная запись удалена <b>навсегда</b>.\n\n"
								 "Вы можете прочитать наше <a href='#'><b>прощальное письмо</b></a> от команды, в котором мы выражаем благодарность и желаем всего наилучшего.",
								 reply_markup = hide_keyboard())

			await state.finish()

		elif USER_MESSAGE != "ПОДТВЕРЖДАЮ":
			await message.answer("⚠️ Извините, но кажется, что вы ввели <b>неверное</b> подтверждение.\n\n"
								 "Для безопасности удаления аккаунта, пожалуйста, убедитесь, что вы вводите слово <b>\"ПОДТВЕРЖДАЮ\"</b> (без кавычек) корректно.\n\n"
								f"Если у вас возникли вопросы или вам требуется дополнительная помощь, не стесняйтесь обращаться к нашей <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрации</b></a>")
		else:
			logger.warning("⚠️ USER_MESSAGE не ровняется слову ПОДТВЕРЖДАЮ")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)