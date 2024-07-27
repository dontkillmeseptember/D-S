from data.loader import dp, bot
from data.config import ConfigBot
from data.config_Keyboard import ConfigReplyKeyboard, ConfigRoleUsers, ConfigVerifyUsers
from data.loader_keyboard import LoaderReplyKeyboards, LoaderInlineKeyboards
from data.states_groups import StartState

from database.requests.version_db import get_bot_version
from database.requests.user_db import load_user_data, is_user_in_data, save_user_data

from misc.libraries import types, FSMContext, Union
from misc.loggers import logger

from keyboards.users.ReplyKeyboard.ReplyKeyboard_all import hide_keyboard

"""Создаем обработчик команды /start"""
@dp.message_handler(commands=("start"))
async def start_command(message: types.Message) -> LoaderReplyKeyboards:
	"""Объявляем переменные с выводом данных о пользователе, версии бота и клавиатуры"""
	USER_DATA_DB = load_user_data()
	VERSION_BOT = get_bot_version()

	start_bot_reply_keyboard = LoaderReplyKeyboards(message).KEYBOARDS_START

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID"""
		USER_ID = ConfigBot.USERID(message)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			"""Объявляем переменную с выводом текущей версии пользователя"""
			USER_VERSION_BOT = ConfigBot.USERVERSIONBOT(message)

			if USER_VERSION_BOT == VERSION_BOT:
				await message.answer(f"{ConfigBot.GETCURRENTHOUR()} <a href='https://t.me/{ConfigBot.USERNAME(message)}'>{ConfigBot.USERLASTNAME(message)}</a> НАЖМИТЕ КНОПКУ ЗАПУСТИТЬ БОТА", reply_markup=start_bot_reply_keyboard)
			
			elif USER_VERSION_BOT != VERSION_BOT:
				await message.answer(f"💬 <a href='https://t.me/{ConfigBot.USERNAME(message)}'>{ConfigBot.USERLASTNAME(message)}</a>! Рады сообщить, что вышла <b>новая версия</b> нашего бота с улучшениями и новыми возможностями.\n\n" 
									"❕ Для получения всех новинок и обновлений, пожалуйста, воспользуйтесь командой <b><code>/update</code></b>.\n\n" 
									"Спасибо за ваше внимание и активное использование нашего бота! 🤍")
					
			else:
				logger.warning("⚠️ USER_VERSION_BOT не ровняется к текущей версии бота.")

		elif not is_user_in_data(USER_ID, USER_DATA_DB):
			await message.answer("Привет это бот", reply_markup=start_bot_reply_keyboard)
			
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных.")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем главный обработчик для команды /start"""
@dp.message_handler(lambda message: message.text == f"{ConfigReplyKeyboard().RUN_BOT}")
async def start_handler(message: types.Message) -> StartState:
	"""Объявляем переменную с выводом информации о пользователе"""
	USER_DATA_DB = load_user_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID"""
		USER_ID = ConfigBot.USERID(message)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			await message.answer(f"💬 Для использования бота, <a href='https://t.me/{ConfigBot.USERNAME(message)}'>{ConfigBot.USERLASTNAME(message)}</a>, пожалуйста, введите ваш <b>пароль</b>.", reply_markup=hide_keyboard())

			"""Переходим в фазу, где пользователь вводит придуманный пароль"""
			await StartState.RegistrationUserState.set()

		elif not is_user_in_data(USER_ID, USER_DATA_DB):
			"""Сохраняем USER_ID Пользователя и создаем дополнительные параметры, для следующих функций"""
			USER_DATA_DB[str(ConfigBot.USERID(message))] = {
				"USER_LAST_NAME": ConfigBot.USERLASTNAME(message),
				"USER_NAME": f"https://t.me/{ConfigBot.USERNAME(message)}",
				"VERSION_BOT": ConfigBot().VERSION
			}
			
			save_user_data(USER_DATA_DB)

			await message.answer(f"💬 <a href='https://t.me/{ConfigBot.USERNAME(message)}'>{ConfigBot.USERLASTNAME(message)}</a>, для начало регистрации в нашем боте, пожалуйста, придумайте ваш надежный <b>пароль</b>.\n\n"
								 "❕ Убедитесь, что он состоит из <b>12 символов</b>, включая хотя бы <b>одну цифру</b>.", reply_markup=hide_keyboard())
			
			"""Переходим в фазу, где пользователь вводит придуманный пароль"""
			await StartState.RegistrationUserState.set()
		
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных.")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчика фазы, где пользователь вводит придуманный пароль"""
@dp.message_handler(state=StartState.RegistrationUserState)
async def password_handler(message: types.Message, state: FSMContext) -> StartState:
	"""Объявляем переменную с выводом информации о пользователе"""
	USER_DATA_DB = load_user_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID"""
		USER_ID = ConfigBot.USERID(message)

		"""Проверяем есть ли пользователь в базе данных"""
		if is_user_in_data(USER_ID, USER_DATA_DB):
			"""Объявляем переменную с выводом информации о пользователе: USER_PASSWORD, USER_MESSAGE"""
			USER_PASSWORD = ConfigBot.USERPASSWORD(message)
			USER_MESSAGE = ConfigBot.USERMESSAGE(message)

			if USER_PASSWORD == None:
				"""Проверяем условия ввода пароль от пользователя"""
				if len(USER_MESSAGE) < 12 or not any(char.isalpha() for char in USER_MESSAGE) or not any(char.isdigit() for char in USER_MESSAGE):
					await message.answer("⚠️ Пароль должен состоять из <b>12 символов</b> и содержать хотя бы <b>одну цифру</b>.")

				else:
					"""Выводим Inline клавиатуру для обработчика пропуска фазы ввода нации для пользователя."""
					inline_keyboard_skip_phase_nation = LoaderInlineKeyboards(message).INLINE_KEYBOARDS_SKIP_PHASE_NATION

					"""Сохраняем пароль пользователя в базе данных"""
					USER_DATA_DB[str(USER_ID)]["USER_PASSWORD"] = USER_MESSAGE
					
					save_user_data(USER_DATA_DB)

					"""Объявляем переменную с выводом информации о пользователе: USER_NATION"""
					USER_NATION = ConfigBot.USERNATION(message)

					"""Проверяем есть ли уже страна у пользователя или нет"""
					if USER_NATION == None:
						await message.answer(f"💬 <a href='https://t.me/{ConfigBot.USERNAME(message)}'>{ConfigBot.USERLASTNAME(message)}</a>, отлично идем! Теперь уточним вашу <b>нацию</b> или <b>страну</b>.\n\n"
											"❕ Пожалуйста, укажите свою <b>национальность</b> или <b>страну проживания</b>.", reply_markup = inline_keyboard_skip_phase_nation)

						"""Переходим в фазу, где вводит свою нацию/страну"""
						await StartState.NationUserState.set()
						
					elif USER_NATION != None:
						"""Переходим в обработчик для входа в аккаунт"""
						await start_handler(message)
					
					else:
						logger.warning("⚠️ USER_NATION не ровняется None или не None.")

			elif USER_PASSWORD == USER_MESSAGE:
				"""Выводим клавиатуры для обработчика главного меню"""
				keyboard_menu = LoaderReplyKeyboards(message).KEYBOARDS_MENU

				await message.answer(f"💬 Прекрасно, <a href='https://t.me/{ConfigBot.USERNAME(message)}'>{ConfigBot.USERLASTNAME(message)}</a>! Ваш пароль успешно <b>подтвержден</b>. Добро пожаловать обратно!\n\n"
						 			 f"Если у вас есть какие-либо вопросы или нужна помощь, не стесняйтесь спрашивать нашу <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрацию</b></a>.", reply_markup=keyboard_menu)
				
				await state.finish()

			elif USER_PASSWORD != USER_MESSAGE:
				"""Выводим Inline клавиатуры для обработчика восстановления пароля"""
				inline_keyboard_recovery = LoaderInlineKeyboards(message).INLINE_KEYBOARDS_RECOVERY

				await message.answer("⚠️ Кажется, что пароль введен <b>неверно</b>. Пожалуйста, проверьте свои данные и попробуйте еще раз.\n\n"
						 			 f"❕ Если у вас возникли проблемы с доступом, вы можете воспользоваться функцией <b>восстановления пароля</b> или связаться с нашей <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрацией</b></a>.", reply_markup=inline_keyboard_recovery)
			
			else:
				logger.warning("⚠️ Произошла ошибка с USER_PASSWORD.")
		else:
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{ConfigBot.USERNAME(message)}] попытался вести пароль для входа в систему.")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчика фазы, где пользователь вводит нацию/страну"""
@dp.message_handler(state=StartState.NationUserState)
@dp.callback_query_handler(lambda callback_data: callback_data.data == "SKIP_PHASE_NATION", state = [StartState.NationUserState])
async def nation_handler(message_or_callbackQuery: Union[types.Message, types.CallbackQuery], state: FSMContext) -> FSMContext:
	"""Объявляем переменную с выводом информации о пользователе"""
	USER_DATA_DB = load_user_data()

	try:
		"""Выводим клавиатуры для обработчика главного меню."""
		keyboard_menu = LoaderReplyKeyboards(message_or_callbackQuery).KEYBOARDS_MENU
		
		"""Объявляем переменную с выводом информации о пользователе: USER_ID"""
		USER_ID = ConfigBot.USERID(message_or_callbackQuery)

		"""Проверяем есть ли пользователь в базе данных"""
		if is_user_in_data(USER_ID, USER_DATA_DB):
			"""Объявляем переменную с выводом сообщение о завершение регистрации учетной записи бота."""
			END_REGISTER_MESSAGE = f"💬 <a href='https://t.me/{ConfigBot.USERNAME(message_or_callbackQuery)}'>{ConfigBot.USERLASTNAME(message_or_callbackQuery)}</a>, поздравляем! <b>Регистрация завершена</b>. Теперь вы можете наслаждаться всеми возможностями нашего бота.\n\n" \
								   f"Если у вас возникнут вопросы или нужна помощь, не стесняйтесь обращаться нашей <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрации</b></a>."

			"""Сохраняем переменные которые пользователь ввел вовремя фазы регистрации учетной записи бота."""
			USER_DATA_DB[str(ConfigBot.USERID(message_or_callbackQuery))]["BOT_ID"] = ConfigBot.GETBOTID()
			USER_DATA_DB[str(ConfigBot.USERID(message_or_callbackQuery))]["USER_ROLE"] = ConfigRoleUsers().USER_NEW
			USER_DATA_DB[str(ConfigBot.USERID(message_or_callbackQuery))]["NAME_USER_ROLE"] = ConfigRoleUsers().USER_NAME_NEW

			"""Сохраняем выбранный спорт в базе данных."""
			USER_DATA_DB[str(ConfigBot.USERID(message_or_callbackQuery))]["SELECTED_SPORT"] = {
				"SELECTED_SPORT_USER": False,
				"SELECTED_SPORT_NAME": None
			}

			"""Сохраняем данные о верификации пользователя."""
			USER_DATA_DB[str(ConfigBot.USERID(message_or_callbackQuery))]["VERIFY_DATA"] = {
				"STATUS_VERIFY_USER": ConfigVerifyUsers().NOPE_VERIFY_USER,
				"VERIFY_USER": False,
				"CONSIDERATION_VERIFY_USER": False
			}

			"""Сохраняем текущие фазы вовремя изменения кошелька, редактирования упражнений и т.д."""
			USER_DATA_DB[str(ConfigBot.USERID(message_or_callbackQuery))]["STATES_USER"] = {
				"NUMBER_WALLET_ID": None,
				"SPORT_ID": None,
				"PREVIOUS_MESSAGE_ID": None
			}

			"""Сохраняем данные о уведомлениях."""
			USER_DATA_DB[str(ConfigBot.USERID(message_or_callbackQuery))]["NOTIFY_DATA"] = {
				"USER_NOTIFY": {
					"NOTIFY_RATION": True,
					"NOTIFY_SPORT": True,
					"NOTIFY_UPDATE": True
				}
			}

			if isinstance(message_or_callbackQuery, types.Message):
				"""Объявляем переменную с выводом информации о пользователе: USER_MESSAGE"""
				USER_MESSAGE = ConfigBot.USERMESSAGE(message_or_callbackQuery)

				"""Объявляем переменные с отправкой данных о введенной нации пользователем"""
				ENGLISH_NAME = ConfigBot.TRANSLATETOENGLISH(USER_MESSAGE)
				COUNTRY_INFO = ConfigBot.GETCOUNTRYINFO(ENGLISH_NAME)

				if COUNTRY_INFO:
					"""Сохраняем название страны который пользователь ввел."""
					USER_DATA_DB[str(ConfigBot.USERID(message_or_callbackQuery))]["NATION_USER"] = ConfigBot.USERMESSAGE(message_or_callbackQuery)

					save_user_data(USER_DATA_DB)

					await message_or_callbackQuery.answer(END_REGISTER_MESSAGE, reply_markup=keyboard_menu)
					
					await state.finish()

				elif not COUNTRY_INFO:
					await message_or_callbackQuery.answer("⚠️ Похоже, что вы ввели <b>несуществующую</b> страну. Пожалуйста, введите <b>настоящую</b> страну.")
				
				else:
					logger.warning("COUNTRY_INFO не ровняется никакой стране или нации.")
			
			elif isinstance(message_or_callbackQuery, types.CallbackQuery):
				"""Удаляем старое сообщение."""
				await bot.delete_message(message_or_callbackQuery.message.chat.id, message_or_callbackQuery.message.message_id)

				"""Сохраняем название страны который пользователь ввел."""
				USER_DATA_DB[str(ConfigBot.USERID(message_or_callbackQuery))]["NATION_USER"] = None

				save_user_data(USER_DATA_DB)

				await bot.send_message(chat_id = message_or_callbackQuery.message.chat.id, text = END_REGISTER_MESSAGE, reply_markup = keyboard_menu)
				
				await state.finish()

			else:
				logger.warning("⚠️ Произошел сбой с ISINSTANCE.")
		else:
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{ConfigBot.USERNAME(message_or_callbackQuery)}] попытался ввести нацию/страну.")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик для восстановления пароля от учетной запили пользователя"""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "RECOVERY_PASSWORD", state=StartState.RegistrationUserState)
async def recovery_password(callback_query: types.CallbackQuery):
	"""Загружаем базу данных о пользователе"""
	USER_DATA_DB = load_user_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID"""
		USER_ID = ConfigBot.USERID(callback_query)

		"""Проверяем есть ли пользователь в базе данных"""
		if is_user_in_data(USER_ID, USER_DATA_DB):
			await bot.edit_message_text(f"💬 <a href='https://t.me/{ConfigBot.USERNAME(callback_query)}'>{ConfigBot.USERLASTNAME(callback_query)}</a>, для восстановления пароля, введите ваш <b>BOT_ID</b>\n\n"
										f"❕ Если у вас возникнут вопросы или нужна помощь, не стесняйтесь обращаться нашей <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрации</b></a>.", callback_query.from_user.id, callback_query.message.message_id)

			"""Переходим в фазу, где вводят свой USER_ID"""
			await StartState.RecoveryPasswordState.set()

		else:
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{ConfigBot.USERNAME(callback_query)}] попытался восстановить пароль.")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик фазу, где пользователь вводит свой USER_ID"""
@dp.message_handler(state=StartState.RecoveryPasswordState)
async def recovery_password_handler(message: types.Message):
	"""Загружаем базу данных о пользователе"""
	USER_DATA_DB = load_user_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID"""
		USER_ID = ConfigBot.USERID(message)

		"""Проверяем есть ли пользователь в базе данных"""
		if is_user_in_data(USER_ID, USER_DATA_DB):
			"""Объявляем переменную с выводом информации о пользователе: USER_BOT_ID, USER_MESSAGE"""
			USER_BOT_ID = ConfigBot.USERBOTID(message)
			USER_MESSAGE = ConfigBot.USERMESSAGE(message)

			if USER_BOT_ID == USER_MESSAGE:
				"""Меняет текущий пароль пользователя на None"""
				USER_DATA_DB[str(USER_ID)]["USER_PASSWORD"] = None

				save_user_data(USER_DATA_DB)

				await message.answer(f"💬 Отлично, <a href='https://t.me/{ConfigBot.USERNAME(message)}'>{ConfigBot.USERLASTNAME(message)}</a>! <b>BOT_ID</b> успешно <b>подтвержден</b>.\n\n"
						 			 "Теперь вы можете безопасно ввести <b>новый пароль</b> для вашей учетной записи.\n\n"
						 			 "❕ Убедитесь, что он состоит из <b>12 символов</b>, включая хотя бы <b>одну цифру</b>.")

				"""Переходим в фазу, где вводят новый пароль"""
				await StartState.RegistrationUserState.set()

			elif USER_BOT_ID != USER_MESSAGE:
				await message.answer(f"⚠️ Извините, <a href='https://t.me/{ConfigBot.USERNAME(message)}'>{ConfigBot.USERLASTNAME(message)}</a>, но похоже, что введен неверный <b>BOT_ID</b>. Пожалуйста, убедитесь, что вы вводите правильные данные, и повторите попытку.\n\n"
						 			 f"❕ Если у вас возникли проблемы с доступом, не стесняйтесь обратиться за помощью к нашей <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрации</b></a>.")
			
			else:
				logger.warning("⚠️ USER_BOT_ID не ровняется введеному пользователем BOT_ID")
		else:
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{ConfigBot.USERNAME(message)}] попытался ввести свой BOT_ID.")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)