from data.loader import dp, bot
from data.config import ConfigBot
from data.config_Keyboard import ConfigReplyKeyboard, ConfigVerifyUsers, ConfigRoleUsers
from data.loader_keyboard import LoaderInlineKeyboards, LoaderReplyKeyboards
from data.states_groups import ProfileState

from database.requests.user_db import load_user_data, is_user_in_data, save_user_data
from database.requests.rsb_db import load_rsb_data, is_rsb_in_data
from database.requests.admin_db import load_admin_data, is_admin_in_data, save_admin_data
from database.requests.version_db import get_bot_version

from misc.loggers import logger
from misc.libraries import types, FSMContext, Union

from keyboards.users.ReplyKeyboard.ReplyKeyboard_all import hide_keyboard

"""Сохранение message_id для удаления сообщений от бота"""
PREVIOUS_MESSAGE_ID = None

@dp.message_handler(lambda message: message.text == ConfigRoleUsers().USER + ConfigReplyKeyboard().PROFILE or
                                    message.text == ConfigRoleUsers().ADMIN + ConfigReplyKeyboard().PROFILE or
                                    message.text == ConfigRoleUsers().USER_NEW + ConfigReplyKeyboard().PROFILE)
@dp.callback_query_handler(lambda callback_data: callback_data.data == "BACK_PROFILE", state = [ProfileState.SendCodeAndSocialState, ProfileState.SendUserPasswordState, ProfileState.SendNumberWalletState, ProfileState.SendNumberWalletAndBackProfileState, None])
async def profile_handler(message_or_callbackQuery: Union[types.Message, types.CallbackQuery], state: FSMContext) -> None:
	global PREVIOUS_MESSAGE_ID

	"""Объявляем переменные с выводом данных о пользователе и версии бота"""
	USER_DATA_DB = load_user_data()
	VERSION_BOT = get_bot_version()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID"""
		USER_ID = ConfigBot.USERID(message_or_callbackQuery)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			"""Объявляем переменную с выводом текущей версии пользователя"""
			USER_VERSION_BOT = ConfigBot.USERVERSIONBOT(message_or_callbackQuery)

			if USER_VERSION_BOT == VERSION_BOT:
				"""Объявляем переменные с выводом информации о фотографии пользователя, выводим первую фотографию пользователя и клавиатуру"""
				PHOTO = await bot.get_user_profile_photos(USER_ID)
				PHOTO_USER = PHOTO.photos[0][-1].file_id

				profile_menu_inline_keyboard = LoaderInlineKeyboards(message_or_callbackQuery).INLINE_KEYBOARDS_PROFILEMENU

				"""Объявляем переменную с выводом сообщение о информации пользователя"""
				INFO_PROFILE_MESSAGE = "💬 Ваша текущая информация о профиле.\n\n" \
									  f" • Ваше имя на текущий момент: <b>{ConfigBot.USERLASTNAME(message_or_callbackQuery)}</b>\n" \
									  f" • Ваше имя пользователя: <b>@{ConfigBot.USERNAME(message_or_callbackQuery)}</b>\n\n" \
									  f" • Ваша страна проживания: <b>{ConfigBot.USERNATION(message_or_callbackQuery)}</b>\n\n" \
									  f" • Ваш <b>USER ID</b>: <code>{USER_ID}</code>\n" \
									  f" • Ваш <b>BOT ID</b>: <code>{ConfigBot.USERBOTID(message_or_callbackQuery)}</code>\n\n" \
									  f" • Ваш статус верификации: <b>{ConfigBot.USERSTATUSVERIFY(message_or_callbackQuery)}</b>\n\n" \
									  f" • Ваша роль на данный момент: {ConfigBot.USERROLE(message_or_callbackQuery)} <b>{ConfigBot.USERROLENAME(message_or_callbackQuery)}</b>"

				if isinstance(message_or_callbackQuery, types.Message):
					"""Объявляем переменную с выводом информации об администрации"""
					ADMIN_DATA_DB = load_admin_data()

					"""Сохраняем имя пользователя и имя на текущий момент для администрации"""
					if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
						ADMIN_DATA_DB[str(USER_ID)]["USER_LAST_NAME"] = ConfigBot.USERLASTNAME(message_or_callbackQuery)
						ADMIN_DATA_DB[str(USER_ID)]["USER_NAME"] = f"https://t.me/{ConfigBot.USERNAME(message_or_callbackQuery)}"

						save_admin_data(ADMIN_DATA_DB)

					"""Сохраняем имя пользователя и имя на текущий момент"""
					USER_DATA_DB[str(USER_ID)]["USER_LAST_NAME"] = ConfigBot.USERLASTNAME(message_or_callbackQuery)
					USER_DATA_DB[str(USER_ID)]["USER_NAME"] = f"https://t.me/{ConfigBot.USERNAME(message_or_callbackQuery)}"

					save_user_data(USER_DATA_DB)

					if PHOTO.photos:
						SENT_MESSAGE = await message_or_callbackQuery.answer_photo(photo = PHOTO_USER, caption = INFO_PROFILE_MESSAGE, reply_markup = profile_menu_inline_keyboard)

						PREVIOUS_MESSAGE_ID = SENT_MESSAGE.message_id

					elif not PHOTO.photos:
						SENT_MESSAGE = await message_or_callbackQuery.answer(INFO_PROFILE_MESSAGE, reply_markup = profile_menu_inline_keyboard)

						PREVIOUS_MESSAGE_ID = SENT_MESSAGE.message_id
					
					else:
						await message_or_callbackQuery.answer("⚠️ В данный момент профиль не работает.")

				elif isinstance(message_or_callbackQuery, types.CallbackQuery):
					"""Объявляем переменную, где выводим текущую фазу пользователя"""
					CURRENT_STATE = await state.get_state()

					if CURRENT_STATE == "ProfileState:SendUserPasswordState" or CURRENT_STATE == "ProfileState:SendCodeAndSocialState" or CURRENT_STATE == "ProfileState:SendNumberWalletAndBackProfileState":
						await bot.delete_message(message_or_callbackQuery.message.chat.id, message_or_callbackQuery.message.message_id)

						if PHOTO.photos:
							SENT_MESSAGE = await bot.send_photo(chat_id = message_or_callbackQuery.message.chat.id, photo = PHOTO_USER, caption = INFO_PROFILE_MESSAGE, reply_markup = profile_menu_inline_keyboard)

							PREVIOUS_MESSAGE_ID = SENT_MESSAGE.message_id

							await state.finish()

						elif not PHOTO.photos:
							SENT_MESSAGE = await bot.send_message(chat_id = message_or_callbackQuery.message.chat.id, text = INFO_PROFILE_MESSAGE, reply_markup = profile_menu_inline_keyboard)

							PREVIOUS_MESSAGE_ID = SENT_MESSAGE.message_id

							await state.finish()

						else:
							await message_or_callbackQuery.answer("⚠️ В данный момент профиль не работает.")

							await state.finish()
					
					elif CURRENT_STATE == "ProfileState:SendNumberWalletState" or CURRENT_STATE == None:
						if PHOTO.photos:
							await bot.edit_message_caption(caption = INFO_PROFILE_MESSAGE, chat_id = message_or_callbackQuery.message.chat.id, message_id = message_or_callbackQuery.message.message_id, reply_markup = profile_menu_inline_keyboard)

							await state.finish()

						elif not PHOTO.photos:
							await bot.edit_message_caption(caption = INFO_PROFILE_MESSAGE, chat_id = message_or_callbackQuery.message.chat.id, message_id = message_or_callbackQuery.message.message_id, reply_markup = profile_menu_inline_keyboard)

							await state.finish()

						else:
							await message_or_callbackQuery.answer("⚠️ В данный момент профиль не работает.")

							await state.finish()

				else:
					logger.warning("⚠️ Произошел сбой с ISINSTANCE.")

			elif USER_VERSION_BOT != VERSION_BOT:
				"""Объявляем переменную с выводом сообщения о новой версии бота"""
				INFO_NEW_VERSION_BOT_MESSAGE = f"💬 <a href='https://t.me/{ConfigBot.USERNAME(message_or_callbackQuery)}'>{ConfigBot.USERLASTNAME(message_or_callbackQuery)}</a>! Рады сообщить, что вышла <b>новая версия</b> нашего бота с улучшениями и новыми возможностями.\n\n" \
												"❕ Для получения всех новинок и обновлений, пожалуйста, воспользуйтесь командой <b><code>/update</code></b>.\n\n" \
												"Спасибо за ваше внимание и активное использование нашего бота! 🤍"

				if isinstance(message_or_callbackQuery, types.Message):
					await message_or_callbackQuery.answer(INFO_NEW_VERSION_BOT_MESSAGE)

				elif isinstance(message_or_callbackQuery, types.CallbackQuery):
					await bot.send_message(message_or_callbackQuery.chat.id, INFO_NEW_VERSION_BOT_MESSAGE)

				else:
					logger.error("⚠️ Произошла непредвиденная ошибка с проверкой isinstance: %s", isinstance)
			else:
				logger.warning("⚠️ Произошла непредвиденная ошибка с проверкой версии бота: %s", USER_VERSION_BOT)
		else:
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{ConfigBot.USERNAME(message_or_callbackQuery)}] попытался зайти в информацию о профиле.")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик входа в банк для пользователей"""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "RSB_BANK")
async def rsb_bank_user_handler(callback_query: types.CallbackQuery) -> ProfileState:
	"""Объявляем переменные с выводом данных о пользователе"""
	USER_DATA_DB = load_user_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID"""
		USER_ID = ConfigBot.USERID(callback_query)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			"""Объявляем переменную с выводом информации о верификации пользователя"""
			USER_VERIFICATION = ConfigBot.USERVERIFY(callback_query)

			if USER_VERIFICATION is None or USER_VERIFICATION is False:
				logger.warning(f"⚠️ Неверифицированный пользователь [@{ConfigBot.USERNAME(callback_query)}] попытался войти в меню банка.")
			
			elif USER_VERIFICATION:
				"""Объявляем переменные с выводом информации о существование кошелька у пользователя и клавиатуры для возвращения обратно в профиль"""
				USER_REGISTOR_WALLET = ConfigBot.USERREGISTORWALLET(callback_query)
				
				back_profile_inline_keyboard = LoaderInlineKeyboards(callback_query).INLINE_KEYBOARDS_BACK_PROFILEMENU

				if USER_REGISTOR_WALLET is None or USER_REGISTOR_WALLET is False:
					await bot.edit_message_caption(caption = f"💬 <a href='https://t.me/{ConfigBot.USERNAME(callback_query)}'>{ConfigBot.USERLASTNAME(callback_query)}</a>, для получения подробной информации о вашем <b>кошельке</b>, пожалуйста, укажите его <b>ID</b>.\n\nМы постараемся предоставить вам актуальные сведения.", 
												   chat_id = callback_query.message.chat.id,
												   message_id = callback_query.message.message_id,
												   reply_markup = back_profile_inline_keyboard)

					"""Переходим в фазу, где пользователь вводит ID кошелек для подключения"""
					await ProfileState.SendNumberWalletState.set()
				
				elif USER_REGISTOR_WALLET:
					"""Объявляем переменную с выводом сообщения о информации кошелька"""
					INFO_RSB_USER_MESSAGE = f"💬 Текущая информация о кошельке.\n\n" \
											f" • ID кошелька: <span class='tg-spoiler'><b>{ConfigBot.GETRSB(None, 'WALLET', False, callback_query)}</b></span>\n\n" \
											f" • Баланс кошелька: <code>{ConfigBot.GETRSB(None, 'ETH', False, callback_query)}</code> <b>ETH</b> - <code>{ConfigBot.GETRSB(None, 'USD', False, callback_query)}</code> <b>USD</b> ~ <code>{ConfigBot.GETRSB(None, 'RUB', False, callback_query)}</code> <b>RUB</b>\n\n" \
											f" • Текущий курс ETH: <b>1 ETH</b> ~ <code>{ConfigBot.GETRSB(None, 'CURRENT_ETH', False, callback_query)}</code> <b>RUB</b>\n" \
											f" • Текущий курс USD: <b>1 USD</b> ~ <code>{ConfigBot.GETRSB(None, 'CURRENT_USD', False, callback_query)}</code> <b>RUB</b>\n" \
											f" • Текущий курс RUB: <b>1 RUB</b> ~ <code>{ConfigBot.GETRSB(None, 'CURRENT_RUB', False, callback_query)}</code> <b>USD</b>\n\n" \
											f" • Общий вклад в кошелек: 🧑🏻 <b>{ConfigBot.GETRSB(None, 'INTEREST_USER_ONE', False, callback_query)}%</b> ~ <b>{ConfigBot.GETRSB(None, 'INTEREST_USER_TWO', False, callback_query)}%</b> 👩🏻‍🦰\n\n" \
											f" • Общий бюджет: <code>{ConfigBot.GETRSB(None, 'ALL_SUM_ETH', False, callback_query)}</code> <b>ETH</b> - <code>{ConfigBot.GETRSB(None, 'ALL_SUM_USD', False, callback_query)}</code> <b>USD</b> ~ <code>{ConfigBot.GETRSB(None, 'ALL_SUM_RUB', False, callback_query)}</code> <b>RUB</b>\n\n" \
											 "❕ Данные кошелька обновляются ровно в <b>00:00</b> по <b>МСК</b>."

					await bot.edit_message_caption(caption = INFO_RSB_USER_MESSAGE,
												   chat_id = callback_query.message.chat.id,
												   message_id = callback_query.message.message_id,
												   reply_markup = back_profile_inline_keyboard)
				
				else:
					logger.warning("⚠️ USER_REGISTOR_WALLET не ровняется True или False.")
			else:
				logger.warning("⚠️ USER_VERIFICATION не ровняется True или False.")
		else:
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{ConfigBot.USERNAME(callback_query)}] попытался зайти в меню банка.")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчика фазы, где пользователь вводит номер от кошелька"""
@dp.message_handler(state = [ProfileState.SendNumberWalletState, ProfileState.SendNumberWalletAndBackProfileState])
async def send_password_rsb_bank_user_handler(message: types.Message, state: FSMContext) -> ProfileState:
	global PREVIOUS_MESSAGE_ID

	"""Объявляем переменные с выводом данных о пользователе и данные о банке"""
	USER_DATA_DB = load_user_data()
	RSB_DATA_DB = load_rsb_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID"""
		USER_ID = ConfigBot.USERID(message)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			""""Объявляем переменные о выводе USER_MESSAGE и клавиатуры для возвращения обратно в профиль"""
			USER_MESSAGE = ConfigBot.USERMESSAGE(message)

			back_profile_inline_keyboard = LoaderInlineKeyboards(message).INLINE_KEYBOARDS_BACK_PROFILEMENU

			if isinstance(PREVIOUS_MESSAGE_ID, int):
				await bot.delete_message(message.chat.id, PREVIOUS_MESSAGE_ID)

				PREVIOUS_MESSAGE_ID = None

			elif PREVIOUS_MESSAGE_ID is None:
				return PREVIOUS_MESSAGE_ID
			
			if is_rsb_in_data(USER_MESSAGE, RSB_DATA_DB):
				"""Объявляем переменные с выводом информации о фотографии пользователя и выводим первую фотографию пользователя"""
				PHOTO = await bot.get_user_profile_photos(USER_ID)
				PHOTO_USER = PHOTO.photos[0][-1].file_id

				USER_DATA_DB[str(USER_ID)]["RSB_DATA"] = {
					"NUMBER_WALLET_USER": USER_MESSAGE,
					"REGISTOR_WALLET_USER": True,
					"WALLET_TIME_USER": ConfigBot.GETTIMENOW()
				}

				save_user_data(USER_DATA_DB)

				"""Объявляем переменную о выводе сообщения с информацией о кошельке"""
				INFO_RSB_USER_MESSAGE = f"💬 Текущая информация о кошельке.\n\n" \
										f" • ID кошелька: <span class='tg-spoiler'><b>{ConfigBot.GETRSB(None, 'WALLET', False, message)}</b></span>\n\n" \
										f" • Баланс кошелька: <code>{ConfigBot.GETRSB(None, 'ETH', False, message)}</code> <b>ETH</b> - <code>{ConfigBot.GETRSB(None, 'USD', False, message)}</code> <b>USD</b> ~ <code>{ConfigBot.GETRSB(None, 'RUB', False, message)}</code> <b>RUB</b>\n\n" \
										f" • Текущий курс ETH: <b>1 ETH</b> ~ <code>{ConfigBot.GETRSB(None, 'CURRENT_ETH', False, message)}</code> <b>RUB</b>\n" \
										f" • Текущий курс USD: <b>1 USD</b> ~ <code>{ConfigBot.GETRSB(None, 'CURRENT_USD', False, message)}</code> <b>RUB</b>\n" \
										f" • Текущий курс RUB: <b>1 RUB</b> ~ <code>{ConfigBot.GETRSB(None, 'CURRENT_RUB', False, message)}</code> <b>USD</b>\n\n" \
										f" • Общий вклад в кошелек: 🧑🏻 <b>{ConfigBot.GETRSB(None, 'INTEREST_USER_ONE', False, message)}%</b> ~ <b>{ConfigBot.GETRSB(None, 'INTEREST_USER_TWO', False, message)}%</b> 👩🏻‍🦰\n\n" \
										f" • Общий бюджет: <code>{ConfigBot.GETRSB(None, 'ALL_SUM_ETH', False, message)}</code> <b>ETH</b> - <code>{ConfigBot.GETRSB(None, 'ALL_SUM_USD', False, message)}</code> <b>USD</b> ~ <code>{ConfigBot.GETRSB(None, 'ALL_SUM_RUB', False, message)}</code> <b>RUB</b>\n\n" \
										"❕ Данные кошелька обновляются ровно в <b>00:00</b> по <b>МСК</b>."

				if PHOTO.photos:
					await message.answer_photo(photo = PHOTO_USER, caption = INFO_RSB_USER_MESSAGE, reply_markup = back_profile_inline_keyboard)

					await state.finish()

				elif not PHOTO.photos:
					await message.answer(INFO_RSB_USER_MESSAGE, reply_markup = back_profile_inline_keyboard)
					
					await state.finish()

				else:
					await message.answer("⚠️ В данный момент профиль не работает.")

					await state.finish()

			if not is_rsb_in_data(USER_MESSAGE, RSB_DATA_DB):
				await message.answer(f"⚠️ <a href='https://t.me/{ConfigBot.USERNAME(message)}'>{ConfigBot.USERLASTNAME(message)}</a>, Извините, но похоже, что <b>введенный</b> номер кошелька не существует в нашей системе. Убедитесь, что вы ввели корректный номер и повторите попытку.\n\n"
									 f"Если у вас возникли вопросы или вам требуется дополнительная помощь, не стесняйтесь обращаться к нашей <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрации</b></a>",
									 reply_markup = back_profile_inline_keyboard)

				"""Переходим в фазу, для перехода в профиль в нужную фазу"""
				await ProfileState.SendNumberWalletAndBackProfileState.set()
		else:
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{ConfigBot.USERNAME(message)}] попытался зайти в меню банка.")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

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
	"""Объявляем переменные с выводом данных о пользователе"""
	USER_DATA_DB = load_user_data()

	try:
		"""Объявляем переменную c выводом информации о пользователя: USER_MESSAGE, USER_ID"""
		USER_MESSAGE = ConfigBot.USERMESSAGE(message)
		USER_ID = ConfigBot.USERID(message)

		if USER_MESSAGE == "ПОДТВЕРЖДАЮ":
			"""Удаляем полностью все данные пользователя в базе данных пользователей"""
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

"""Создаем обработчик для верификации аккаунта пользователей"""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "VERIFY_ACCOUNT")
async def verify_handler(callback_query: types.CallbackQuery) -> ProfileState:
	"""Объявляем переменные с выводом данных о пользователе"""
	USER_DATA_DB = load_user_data()

	try:
		"""Объявляем переменную c выводом информации о пользователя: USER_ID"""
		USER_ID = ConfigBot.USERID(callback_query)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			"""Объявляем переменную c выводом информации о пользователя: USER_VERIFY"""
			USER_VERIFICATION = ConfigBot.USERVERIFY(callback_query)

			if USER_VERIFICATION is None or USER_VERIFICATION is False:
				"""Объявляем переменную c выводом информации о пользователя: USER_VERIFY"""
				USER_CONSIDERATION_VERIFICATION = ConfigBot.USERCONSIDERATIONVERIFY(callback_query)

				if USER_CONSIDERATION_VERIFICATION is None or USER_CONSIDERATION_VERIFICATION is False:
					await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
					
					VERIFICATION_CODE = ConfigBot.GETVERIFYCODE()

					"""Объявляем переменную с выводом сообщение о информации для верификации"""
					INFO_VERIFICATION_MESSAGE = f"💬 Для верификации вашего аккаунта, отправьте нам <b>четырехзначный код</b>, который мы выслали вам, а также предоставьте ссылку на <b>ваш профиль</b> в социальной сети ВКонтакте.\n\n" \
									f" • Ваш индивидуальный код: <b><code>{VERIFICATION_CODE}</code></b>\n\n" \
									f"Эти шаги необходимы для обеспечения безопасности вашей учетной записи."

					"""Сохраняем индивидуальный код пользователя в базу данных"""
					USER_DATA_DB[str(USER_ID)]["VERIFY_DATA"]["VERIFY_CODE_USER"] = VERIFICATION_CODE

					save_user_data(USER_DATA_DB)

					""""Объявляем переменные о выводе клавиатуры для возвращения обратно в профиль"""
					back_profile_inline_keyboard = LoaderInlineKeyboards(callback_query).INLINE_KEYBOARDS_BACK_PROFILEMENU

					await bot.send_message(chat_id = callback_query.message.chat.id, text = INFO_VERIFICATION_MESSAGE, reply_markup = back_profile_inline_keyboard)

					"""Переходим фазу, где пользователь вводит код и соц сеть"""
					await ProfileState.SendCodeAndSocialState.set()

				elif USER_CONSIDERATION_VERIFICATION:
					time_verify_message = f"💬 <a href='https://t.me/{ConfigBot.USERNAME(callback_query)}'>{ConfigBot.USERLASTNAME(callback_query)}</a>! Ваш аккаунт в настоящий момент проходит процесс <b>верификации</b>.\n\n" \
										   "Пожалуйста, ожидайте подтверждения от <b>администрации</b>. Этот процесс может занять некоторое время. Благодарим за терпение и понимание!\n\n" \
										  f"Если у вас возникли вопросы или вам требуется дополнительная помощь, не стесняйтесь обращаться к нашей <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрации</b></a>"

					await bot.send_message(chat_id = callback_query.message.chat.id, text = time_verify_message)

			elif USER_VERIFICATION:
				logger.warning(f"⚠️ Верифицированный пользователь [@{ConfigBot.USERNAME(callback_query)}] попытался верифицировать аккаунт.")
		else:
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{ConfigBot.USERNAME(callback_query)}] попытался верифицировать аккаунт.")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчика фазы, где пользователь вводит индивидуальный код"""
@dp.message_handler(state = ProfileState.SendCodeAndSocialState)
async def user_code_social_handler(message: types.Message, state: FSMContext) -> FSMContext:
	"""Объявляем переменные с выводом данных о пользователе"""
	USER_DATA_DB = load_user_data()

	try:
		"""Объявляем переменную о выводе информации пользователя и для разделения сообщений от пользователя"""
		USER_MESSAGE = ConfigBot.USERMESSAGE(message)
		PARTS = USER_MESSAGE.split()

		if len(PARTS) == 2:
			"""Объявляем переменные о выводе информации пользователя и выводе переменной с разделенной сообщения"""
			USER_VERIFICATION_CODE = ConfigBot.USERVERIFYCODE(message)
			INDIVIDUAL_CODE, VK_LINK = PARTS

			if USER_VERIFICATION_CODE == INDIVIDUAL_CODE and ConfigBot.CHECKVKPROFILELINK(VK_LINK):
				"""Объявляем переменные о выводе клавиатуры для возвращения в главное меню"""
				main_menu_reply_keyboard = LoaderReplyKeyboards(message).KEYBOARDS_MENU

				USER_DATA_DB[str(ConfigBot.USERID(message))]["VERIFY_DATA"]["STATUS_VERIFY_USER"] = ConfigVerifyUsers().CONSIDERATION_VERIFY_USER
				USER_DATA_DB[str(ConfigBot.USERID(message))]["VERIFY_DATA"]["CONSIDERATION_VERIFY_USER"] = True
				USER_DATA_DB[str(ConfigBot.USERID(message))]["VERIFY_DATA"]["LINK_PROFILE_USER"] = VK_LINK
				USER_DATA_DB[str(ConfigBot.USERID(message))]["VERIFY_DATA"]["VERIFY_TIME_USER"] = ConfigBot.GETTIMENOW()

				save_user_data(USER_DATA_DB)

				await message.answer(f"💬 Отлично, <a href='https://t.me/{ConfigBot.USERNAME(message)}'>{ConfigBot.USERLASTNAME(message)}</a>, ваш аккаунт в настоящее время находится на <b>рассмотрении</b> администрации.\n\n"
						 			  "Мы получили ваш <b>индивидуальный код</b> и ссылку на <b>ваш профиль</b> в ВКонтакте, и сейчас проводим необходимые проверки.\n\n"
									  "Пожалуйста, ожидайте окончательного решения. благодарим вас за предоставленную информацию и терпение.\n\n"
									 f"Если у вас возникли вопросы или вам требуется дополнительная помощь, не стесняйтесь обращаться к нашей <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрации</b></a>", reply_markup=main_menu_reply_keyboard)

				await state.finish()

			else:
				"""Проверка на неверный индивидуальный код, некорректную ссылку и в случае, если код и ссылка неверны"""
				if USER_VERIFICATION_CODE != INDIVIDUAL_CODE and ConfigBot.CHECKVKPROFILELINK(VK_LINK):
					await message.answer("⚠️ Неверный <b>индивидуальный код</b>. Пожалуйста, попробуйте снова.\n\n"
						  				f"Если у вас возникли вопросы или вам требуется дополнительная помощь, не стесняйтесь обращаться к нашей <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрации</b></a>")

				elif USER_VERIFICATION_CODE == INDIVIDUAL_CODE and not ConfigBot.CHECKVKPROFILELINK(VK_LINK):
					await message.answer("⚠️ Некорректная ссылка на <b>ваш профиль</b> ВКонтакте. Пожалуйста, попробуйте снова.\n\n"
						  				f"Если у вас возникли вопросы или вам требуется дополнительная помощь, не стесняйтесь обращаться к нашей <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрации</b></a>")

				elif USER_VERIFICATION_CODE != INDIVIDUAL_CODE and not ConfigBot.CHECKVKPROFILELINK(VK_LINK):
					await message.answer("⚠️ Неверный <b>индивидуальный код</b> и некорректная ссылка на <b>ваш профиль</b>. Пожалуйста, попробуйте снова.\n\n"
						  				f"Если у вас возникли вопросы или вам требуется дополнительная помощь, не стесняйтесь обращаться к нашей <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрации</b></a>")
				
				else:
					raise ValueError("ERROR: 404, FILE: PROFILE_FUNC, FUNC: USER_CODE_SOCIAL_HANDLER, TESTING: ConfigBot.USERVERIFYCODE(message)")
		elif len(PARTS) != 2:
			await message.answer("⚠️ Пожалуйста, введите <b>индивидуальный код</b> и ссылку на <b>ваш профиль</b> через пробел.\n\n"
								f"Если у вас возникли вопросы или вам требуется дополнительная помощь, не стесняйтесь обращаться к нашей <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрации</b></a>")
		else:
			logger.warning("⚠️ PARTS Не ровняется к двум: %s", len(PARTS))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)