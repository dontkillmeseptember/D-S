from data.loader import dp, bot
from data.config import LoaderReplyKeyboards, ConfigBot, LoaderInlineKeyboards
from data.config_Keyboard import ConfigReplyKeyboard, ConfigRoleUsers

from data.user_db import load_user_data, is_user_in_data, save_user_data, check_user_data
from data.states_groups import StartState

from misc.libraries import types, FSMContext, random

from keyboards.users.ReplyKeyboard.ReplyKeyboard_all import hide_keyboard

"""Создаем обработчик команды /start"""
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message) -> LoaderReplyKeyboards:
	"""Проверяем зарегистрирован пользователь в боте"""
	user_data_db = load_user_data()

	"""Выводим клавиатуры для обработчика /start"""
	keyboard_start = LoaderReplyKeyboards().KEYBOARDS_START

	if is_user_in_data(ConfigBot.USERID(message), user_data_db):
		await message.answer(f"{ConfigBot.GETCURRENTHOUR()} <a href='https://t.me/{ConfigBot.USERNAME(message)}'>{ConfigBot.USERLASTNAME(message)}</a> НАЖМИТЕ КНОПКУ ЗАПУСТИТЬ БОТА", reply_markup=keyboard_start)
	else:
		await message.answer("Привет это бот", reply_markup=keyboard_start)

"""Создаем главный обработчик для команды /start"""
@dp.message_handler(lambda message: message.text == f"{ConfigReplyKeyboard().RUN_BOT}")
async def start_handler(message: types.Message) -> StartState:
	"""Проверяем зарегистрирован пользователь в боте"""
	user_data_db = load_user_data()

	try:
		if is_user_in_data(ConfigBot.USERID(message), user_data_db):
			"""Если пользователь прошел проверку, то что он зарегистрирован, то его просят вести пароль"""
			await message.answer(f"💬 Для использования бота, <a href='https://t.me/{ConfigBot.USERNAME(message)}'>{ConfigBot.USERLASTNAME(message)}</a>, пожалуйста, введите ваш <b>пароль</b>.", reply_markup=hide_keyboard())

			"""Переходим в фазу, где пользователь вводит придуманный пароль"""
			await StartState.RegistrationUserState.set()
		else:
			"""Сохраняем USER_ID Пользователя и создаем дополнительные параметры, для следующих функций"""
			user_data_db[str(ConfigBot.USERID(message))] = {
				"USER_LAST_NAME": ConfigBot.USERLASTNAME(message),
				"USER_NAME": f"https://t.me/{ConfigBot.USERNAME(message)}",
				"VERSION_BOT": ConfigBot().VERSION
			}
			
			save_user_data(user_data_db)

			"""Если пользователь не прошел проверку, то что он зарегистрирован, то его просят зарегистрироваться в боте"""
			await message.answer(f"💬 <a href='https://t.me/{ConfigBot.USERNAME(message)}'>{ConfigBot.USERLASTNAME(message)}</a>, для начало регистрации в нашем боте, пожалуйста, придумайте ваш надежный <b>пароль</b>.\n\n"
								 "❕ Убедитесь, что он состоит из <b>12 символов</b>, включая хотя бы <b>одну цифру</b>.", reply_markup=hide_keyboard())
			
			"""Переходим в фазу, где пользователь вводит придуманный пароль"""
			await StartState.RegistrationUserState.set()
	except:
		raise ValueError("ERROR: 404, FILE: START_BOT_FUNC, FUNC: START_HANDLER")

"""Создаем обработчика фазы, где пользователь вводит придуманный пароль"""
@dp.message_handler(state=StartState.RegistrationUserState)
async def password_handler(message: types.Message, state: FSMContext) -> StartState and FSMContext:
	"""Загружаем базу данных о пользователе"""
	user_data_db = load_user_data()
	check_user_data_db = check_user_data(ConfigBot.USERID(message))

	"""Получаем пароль пользователя"""
	user_password = check_user_data_db.get("USER_PASSWORD")
	user_nation = check_user_data_db.get("NATION_USER")

	try:
		"""Проверяем есть ли пользователь в базе данных"""
		if is_user_in_data(ConfigBot.USERID(message), user_data_db):
			if user_password == None:
				"""Проверяем условия ввода пароль от пользователя"""
				if len(ConfigBot.USERMESSAGE(message)) < 12 or not any(char.isalpha() for char in ConfigBot.USERMESSAGE(message)) or not any(char.isdigit() for char in ConfigBot.USERMESSAGE(message)):
					await message.answer("❕ Пароль должен состоять из <b>12 символов</b> и содержать хотя бы <b>одну цифру</b>.")
				else:
					"""Сохраняем пароль пользователя в базе данных"""
					user_data_db[str(ConfigBot.USERID(message))]["USER_PASSWORD"] = ConfigBot.USERMESSAGE(message)
					
					save_user_data(user_data_db)

					"""Проверяем есть ли уже страна у пользователя или нет"""
					if user_nation == None:
						await message.answer(f"💬 <a href='https://t.me/{ConfigBot.USERNAME(message)}'>{ConfigBot.USERLASTNAME(message)}</a>, отлично идем! Теперь уточним вашу <b>нацию</b> или <b>страну</b>.\n\n"
											"❕ Пожалуйста, укажите свою <b>национальность</b> или <b>страну проживания</b>.")

						"""Переходим в фазу, где вводит свою нацию/страну"""
						await StartState.NationUserState.set()
					elif user_nation != None:
						"""Переходим в обработчик для входа в аккаунт"""
						await start_handler(message)

			elif user_password == ConfigBot.USERMESSAGE(message):
				"""Выводим клавиатуры для обработчика главного меню"""
				keyboard_menu = LoaderReplyKeyboards().KEYBOARDS_MENU

				await message.answer(f"💬 Прекрасно, <a href='https://t.me/{ConfigBot.USERNAME(message)}'>{ConfigBot.USERLASTNAME(message)}</a>! Ваш пароль успешно <b>подтвержден</b>. Добро пожаловать обратно!\n\n"
						 			 f"Если у вас есть какие-либо вопросы или нужна помощь, не стесняйтесь спрашивать нашу <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрацию</b></a>.", reply_markup=keyboard_menu)
				
				await state.finish()

			elif user_password != ConfigBot.USERMESSAGE(message):
				"""Выводим Inline клавиатуры для обработчика восстановления пароля"""
				inline_keyboard_recovery = LoaderInlineKeyboards().INLINE_KEYBOARDS_RECOVERY

				await message.answer("💬 Кажется, что пароль введен <b>неверно</b>. Пожалуйста, проверьте свои данные и попробуйте еще раз.\n\n"
						 			 f"❕ Если у вас возникли проблемы с доступом, вы можете воспользоваться функцией <b>восстановления пароля</b> или связаться с нашей <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрацией</b></a>.", reply_markup=inline_keyboard_recovery)
		
				await state.finish()
		else:
			raise ValueError("ERROR: 161, TEXT: НЕЗАРЕГИСТРИРОВАННЫЙ ПОЛЬЗОВАТЕЛЬ ПОПЫТАЛСЯ ВВЕСТИ ПАРОЛЬ")
	except:
		raise ValueError("ERROR: 404, FILE: START_BOT_FUNC, FUNC: PASSWORD_HANDLER")

"""Создаем обработчика фазы, где пользователь вводит нацию/страну"""
@dp.message_handler(state=StartState.NationUserState)
async def nation_handler(message: types.Message, state: FSMContext) -> FSMContext:
	"""Загружаем базу данных о пользователе"""
	user_data_db = load_user_data()

	try:
		"""Проверяем есть ли пользователь в базе данных"""
		if is_user_in_data(ConfigBot.USERID(message), user_data_db):
			"""Отправляем название страны пользователя на проверку"""
			english_name = ConfigBot.TRANSLATETOENGLISH(ConfigBot.USERMESSAGE(message))
			country_info = ConfigBot.GETCOUNTRYINFO(english_name)

			if country_info:
				"""Генерация случайного 9-значного ID"""
				BOT_ID = ''.join(str(random.randint(0, 9)) for _ in range(9))

				"""Выводим клавиатуры для обработчика главного меню"""
				keyboard_menu = LoaderReplyKeyboards().KEYBOARDS_MENU

				"""Сохраняем название страны который пользователь ввел"""
				user_data_db[str(ConfigBot.USERID(message))]["NATION_USER"] = ConfigBot.USERMESSAGE(message)
				user_data_db[str(ConfigBot.USERID(message))]["BOT_ID"] = BOT_ID
				user_data_db[str(ConfigBot.USERID(message))]["USER_ROLE"] = ConfigRoleUsers().USER
				user_data_db[str(ConfigBot.USERID(message))]["NAME_USER_ROLE"] = ConfigRoleUsers().USER_NAME

				save_user_data(user_data_db)

				await message.answer(f"💬 <a href='https://t.me/{ConfigBot.USERNAME(message)}'>{ConfigBot.USERLASTNAME(message)}</a>, поздравляем! <b>Регистрация завершена</b>. Теперь вы можете наслаждаться всеми возможностями нашего бота.\n\n"
						 			 f"Если у вас возникнут вопросы или нужна помощь, не стесняйтесь обращаться нашей <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрации</b></a>.", reply_markup=keyboard_menu)
				
				await state.finish()
			else:
				await message.answer("❕ Похоже, что вы ввели <b>несуществующую</b> страну. Пожалуйста, введите <b>настоящую</b> страну.")
		else:
			raise ValueError("ERROR: 161, TEXT: НЕЗАРЕГИСТРИРОВАННЫЙ ПОЛЬЗОВАТЕЛЬ ПОПЫТАЛСЯ ВВЕСТИ НАЦИЮ/СТРАНУ")
	except:
		raise ValueError("ERROR: 404, FILE: START_BOT_FUNC, FUNC: NATION_HANDLER")

"""Создаем обработчик для восстановления пароля от учетной запили пользователя"""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "RECOVERY_PASSWORD")
async def recovery_password(callback_query: types.CallbackQuery):
	"""Загружаем базу данных о пользователе"""
	user_data_db = load_user_data()

	try:
		"""Проверяем есть ли пользователь в базе данных"""
		if is_user_in_data(ConfigBot.USERID(callback_query), user_data_db):
			await bot.edit_message_text(f"💬 <a href='https://t.me/{ConfigBot.USERNAME(callback_query)}'>{ConfigBot.USERLASTNAME(callback_query)}</a>, для восстановления пароля, введите ваш <b>BOT_ID</b>\n\n"
										f"❕ Если у вас возникнут вопросы или нужна помощь, не стесняйтесь обращаться нашей <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрации</b></a>.", callback_query.from_user.id, callback_query.message.message_id)

			"""Переходим в фазу, где вводят свой USER_ID"""
			await StartState.RecoveryPasswordState.set()
		else:
			raise ValueError("ERROR: 161, TEXT: НЕЗАРЕГИСТРИРОВАННЫЙ ПОЛЬЗОВАТЕЛЬ ПОПЫТАЛСЯ ВВЕСТИ ВОССТАНОВИТЬ ПАРОЛЬ")
	except:
		raise ValueError("ERROR: 404, FILE: START_BOT_FUNC, FUNC: RECOVERY_PASSWORD")

"""Создаем обработчик фазу, где пользователь вводит свой USER_ID"""
@dp.message_handler(state=StartState.RecoveryPasswordState)
async def recovery_password_handler(message: types.Message):
	"""Загружаем базу данных о пользователе"""
	user_data_db = load_user_data()
	check_user_data_db = check_user_data(ConfigBot.USERID(message))

	try:
		"""Проверяем есть ли пользователь в базе данных"""
		if is_user_in_data(ConfigBot.USERID(message), user_data_db):
			"""Получаем BOT_ID пользователя"""
			user_bot_id = check_user_data_db.get("BOT_ID")

			if user_bot_id == ConfigBot.USERMESSAGE(message):
				"""Меняет текущий пароль пользователя на None"""
				user_data_db[str(ConfigBot.USERID(message))]["USER_PASSWORD"] = None

				save_user_data(user_data_db)

				await message.answer(f"💬 Отлично, <a href='https://t.me/{ConfigBot.USERNAME(message)}'>{ConfigBot.USERLASTNAME(message)}</a>! <b>BOT_ID</b> успешно <b>подтвержден</b>.\n\n"
						 			 "Теперь вы можете безопасно ввести <b>новый пароль</b> для вашей учетной записи.\n\n"
						 			 "❕ Убедитесь, что он состоит из <b>12 символов</b>, включая хотя бы <b>одну цифру</b>.")

				"""Переходим в фазу, где вводят новый пароль"""
				await StartState.RegistrationUserState.set()

			elif user_bot_id != ConfigBot.USERMESSAGE(message):
				await message.answer(f"💬 Извините, <a href='https://t.me/{ConfigBot.USERNAME(message)}'>{ConfigBot.USERLASTNAME(message)}</a>, но похоже, что введен неверный <b>BOT_ID</b>. Пожалуйста, убедитесь, что вы вводите правильные данные, и повторите попытку.\n\n"
						 			 f"❕ Если у вас возникли проблемы с доступом, не стесняйтесь обратиться за помощью к нашей <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрации</b></a>.")
		else:
			raise ValueError("ERROR: 161, TEXT: НЕЗАРЕГИСТРИРОВАННЫЙ ПОЛЬЗОВАТЕЛЬ ПОПЫТАЛСЯ ВВЕСТИ СВОЙ BOT_ID")
	except:
		raise ValueError("ERROR: 404, FILE: START_BOT_FUNC, FUNC: RECOVERY_PASSWORD_HANDLER")