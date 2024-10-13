from data.loader import dp, bot
from data.config import ConfigBot
from data.loader_keyboard import LoaderInlineKeyboards
from data.states_groups import ProfileState

from database.requests.user_db import load_user_data, is_user_in_data, save_user_data
from database.requests.rsb_db import load_rsb_data, is_rsb_in_data

from misc.loggers import logger
from misc.libraries import types, FSMContext

"""Создаем обработчик для входа в банк для пользователей."""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "RSB_BANK")
async def rsb_bank_user_handler(callback_query: types.CallbackQuery) -> ProfileState:
	"""Объявляем переменные с выводом данных о пользователе."""
	USER_DATA_DB = load_user_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID."""
		USER_ID = ConfigBot.USERID(callback_query)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			"""Объявляем переменную с выводом информации о верификации пользователя."""
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

					"""Переходим в фазу, где пользователь вводит ID кошелек для подключения."""
					await ProfileState.SendNumberWalletState.set()
				
				elif USER_REGISTOR_WALLET:
					"""Объявляем переменную с выводом сообщения о информации кошелька."""
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
	"""Объявляем переменные с выводом данных о пользователе и данные о банке"""
	USER_DATA_DB = load_user_data()
	RSB_DATA_DB = load_rsb_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID, MESSAGE_ID"""
		USER_ID = ConfigBot.USERID(message)
		MESSAGE_ID = ConfigBot.GETMESSAGEID(message)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			""""Объявляем переменные о выводе USER_MESSAGE и клавиатуры для возвращения обратно в профиль"""
			USER_MESSAGE = ConfigBot.USERMESSAGE(message)

			back_profile_inline_keyboard = LoaderInlineKeyboards(message).INLINE_KEYBOARDS_BACK_PROFILEMENU

			if isinstance(MESSAGE_ID, int):
				await bot.delete_message(message.chat.id, MESSAGE_ID)

				USER_DATA_DB[str(USER_ID)]["STATES_USER"]["PREVIOUS_MESSAGE_ID"] = None

			elif MESSAGE_ID is None:
				return MESSAGE_ID
			
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