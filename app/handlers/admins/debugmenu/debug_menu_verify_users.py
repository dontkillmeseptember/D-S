from data.loader import dp, bot
from data.config import ConfigBot
from data.config_Keyboard import ConfigVerifyUsers, ConfigRoleUsers
from data.loader_keyboard import LoaderInlineKeyboardsAdmin, LoaderReplyKeyboards
from data.states_groups import DebugAdminState

from database.requests.user_db import load_user_data, is_user_in_data, save_user_data
from database.requests.admin_db import load_admin_data, is_admin_in_data

from misc.libraries import types,FSMContext

"""Создаем обработчик для верификации пользователей"""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "ADD_VERIFY")
@dp.callback_query_handler(lambda callback_data: callback_data.data == "BACK_VERIFY")
async def add_verify_handler(callback_query: types.CallbackQuery) -> str:
	"""Проверяем зарегистрирован пользователь в базе админов"""
	admin_data_db = load_admin_data()

	"""Загружаем базу данных о пользователе"""
	user_data_db = load_user_data()

	try:
		if is_user_in_data(ConfigBot.USERID(callback_query), user_data_db):
			if is_admin_in_data(ConfigBot.USERID(callback_query), admin_data_db):
				"""Выводим клавиатуры для обработчика меню панели управления"""
				keyboard_back = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK

				await bot.edit_message_text("💬 Список пользователей, которые просят верификацию своих аккаунтов:\n\n"
										   f"{ConfigBot.GETCONSIDERATIONVERIFY(user_data_db)}\n\n"
										   "Пожалуйста, проведите верификацию и примите соответствующие меры.", 
											callback_query.from_user.id, 
											callback_query.message.message_id,
											reply_markup=keyboard_back)
			else:
				raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: ADD_VERIFY_HANDLER, TESTING: IS_ADMIN_IN_DATA")
		else:
			raise ValueError("ERROR: 161, TEXT: ВЕРИФИЦИРОВАННЫЙ ПОЛЬЗОВАТЕЛЬ ПОПЫТАЛСЯ ЗАЙТИ В МЕНЮ ДЛЯ ВЕРИФИКАЦИИ ПОЛЬЗОВАТЕЛЕЙ")
	except:
		raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: ADD_VERIFY_HANDLER")

"""Создаем обработчик для подтверждения верификации пользователей"""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "VERIFY")
async def verify_handler(callback_query: types.CallbackQuery) -> DebugAdminState:
	"""Проверяем зарегистрирован пользователь в базе админов"""
	admin_data_db = load_admin_data()

	"""Загружаем базу данных о пользователе"""
	user_data_db = load_user_data()

	try:
		if is_user_in_data(ConfigBot.USERID(callback_query), user_data_db):
			if is_admin_in_data(ConfigBot.USERID(callback_query), admin_data_db):
				await bot.send_message(callback_query.from_user.id,
						   			   "💬 Выполните верификацию следующих пользователей по их <b>USER_ID</b>, которые представлены выше в предыдущем сообщении.\n\n"
						   			   "❕ Для верификации пользователей достаточно ввести соответствующий <b>USER_ID</b>")

				"""Переходим в фазу, где вводят USER_ID для верификации пользователя"""
				await DebugAdminState.VerifyUsersForAdminState.set()

			else:
				raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: VERIFY_HANDLER, TESTING: IS_ADMIN_IN_DATA")
		else:
			raise ValueError("ERROR: 161, TEXT: ВЕРИФИЦИРОВАННЫЙ ПОЛЬЗОВАТЕЛЬ ПОПЫТАЛСЯ ЗАЙТИ В МЕНЮ ДЛЯ ВЕРИФИКАЦИИ ПОЛЬЗОВАТЕЛЕЙ")
	except:
		raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: VERIFY_HANDLER")

"""Создаем обработчик фазы, где администратор вводит USER_ID и подтверждает верификацию"""
@dp.message_handler(state=DebugAdminState.VerifyUsersForAdminState)
async def input_user_id_handler(message: types.Message, state: FSMContext) -> DebugAdminState:
	"""Загружаем базу данных о пользователе"""
	user_data_db = load_user_data()

	try:
		if is_user_in_data(ConfigBot.USERMESSAGE(message), user_data_db):
			"""Выводим клавиатуры для обработчика главного меню"""
			keyboard_menu = LoaderReplyKeyboards(message).KEYBOARDS_MENU

			"""Выводим клавиатуры для обработчика меню панели управления"""
			keyboard_back_verify = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_VERIFY

			"""Меняем пользователю статус верификации и т.д."""
			user_data_db[str(ConfigBot.USERMESSAGE(message))]["VERIFY_DATA"]["STATUS_VERIFY_USER"] = ConfigVerifyUsers().YES_VERIFY_USER
			user_data_db[str(ConfigBot.USERMESSAGE(message))]["VERIFY_DATA"]["VERIFY_USER"] = True
			user_data_db[str(ConfigBot.USERMESSAGE(message))]["VERIFY_DATA"]["CONSIDERATION_VERIFY_USER"] = False
			user_data_db[str(ConfigBot.USERMESSAGE(message))]["USER_ROLE"] = ConfigRoleUsers().USER
			user_data_db[str(ConfigBot.USERMESSAGE(message))]["NAME_USER_ROLE"] = ConfigRoleUsers().USER_NAME

			save_user_data(user_data_db)

			await message.answer(f"💬 Поздравляем! Верификация завершена успешно.\n\n"
								f" • Имя пользователя на текущий момент: <a href='{ConfigBot.USERNAMEBOT(ConfigBot.USERMESSAGE(message))}'>{ConfigBot.USERLASTNAMEBOT(ConfigBot.USERMESSAGE(message))}</a>\n"
								f" • <b>USER_ID</b> пользователя: <code>{ConfigBot.USERMESSAGE(message)}</code>\n\n"
								f"Если у вас есть дополнительные вопросы или потребуется дополнительная информация, не стесняйтесь обращаться к нашей <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрации</b></a>.\n\n",
								reply_markup = keyboard_back_verify)

			await bot.send_message(ConfigBot.USERMESSAGE(message),
						  		   f"💬 Поздравляем, <a href='{ConfigBot.USERNAMEBOT(ConfigBot.USERMESSAGE(message))}'>{ConfigBot.USERLASTNAMEBOT(ConfigBot.USERMESSAGE(message))}</a> ваш аккаунт успешно <b>верифицирован</b>.\n\n"
								   f"Если у вас есть дополнительные вопросы или нужна дополнительная помощь, не стесняйтесь обращаться к нашей <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрации</b></a>.", 
								   reply_markup = keyboard_menu)
			
			await state.finish()

		elif not is_user_in_data(ConfigBot.USERMESSAGE(message), user_data_db):
			await message.answer("💬 Извините, но похоже, что введен неверный <b>USER_ID</b>.\n\n"
								 "Пожалуйста, убедитесь, что вы вводите правильный <b>USER_ID</b> пользователя и повторите попытку.")
		else:
			raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: INPUT_USER_ID_HANDLER, TESTING: IS_USER_IN_DATA")
	except:
		raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: INPUT_USER_ID_HANDLER")