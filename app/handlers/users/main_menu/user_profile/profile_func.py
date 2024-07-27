from data.loader import dp, bot
from data.config import ConfigBot
from data.config_Keyboard import ConfigReplyKeyboard, ConfigRoleUsers
from data.loader_keyboard import LoaderInlineKeyboards
from data.states_groups import ProfileState

from database.requests.user_db import load_user_data, is_user_in_data, save_user_data
from database.requests.admin_db import load_admin_data, is_admin_in_data, save_admin_data
from database.requests.version_db import get_bot_version
from database.requests.sport_db import load_sport_data

from misc.loggers import logger
from misc.libraries import types, FSMContext, Union

@dp.message_handler(lambda message: message.text == ConfigRoleUsers().USER + ConfigReplyKeyboard().PROFILE or
									message.text == ConfigRoleUsers().ADMIN + ConfigReplyKeyboard().PROFILE or
									message.text == ConfigRoleUsers().USER_NEW + ConfigReplyKeyboard().PROFILE)
@dp.callback_query_handler(lambda callback_data: callback_data.data == "BACK_PROFILE", state = [ProfileState.SendCodeAndSocialState, ProfileState.SendUserPasswordState, ProfileState.SendNumberWalletState, ProfileState.SendNumberWalletAndBackProfileState, ProfileState.SelectedNewSportState, None])
async def profile_handler(message_or_callbackQuery: Union[types.Message, types.CallbackQuery], state: FSMContext) -> None:
	"""Объявляем переменные с выводом данных о пользователе, выбранном упражнение, версии бота."""
	USER_DATA_DB = load_user_data()
	VERSION_BOT = get_bot_version()
	SPORT_DATA_DB = load_sport_data()

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
				INFO_PROFILE_MESSAGE = f"💬 Ваша текущая информация о профиле.\n\n" \
									   f" • Ваше имя на текущий момент: <b>{ConfigBot.USERLASTNAME(message_or_callbackQuery)}</b>\n" \
									   f" • Ваше имя пользователя: <b>@{ConfigBot.USERNAME(message_or_callbackQuery)}</b>\n\n" \
									   f" • Ваша страна проживания: <b>{ConfigBot.USERNATION(message_or_callbackQuery)}</b>\n\n" \
									   f" • Ваш <b>USER ID</b>: <code>{USER_ID}</code>\n" \
									   f" • Ваш <b>BOT ID</b>: <code>{ConfigBot.USERBOTID(message_or_callbackQuery)}</code>\n\n" \
									   f"{ConfigBot.GETSELECTEDSPORT(type = message_or_callbackQuery, sport_data = SPORT_DATA_DB)}" \
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

						USER_DATA_DB[str(USER_ID)]["STATES_USER"]["PREVIOUS_MESSAGE_ID"] = SENT_MESSAGE.message_id

					elif not PHOTO.photos:
						SENT_MESSAGE = await message_or_callbackQuery.answer(INFO_PROFILE_MESSAGE, reply_markup = profile_menu_inline_keyboard)

						USER_DATA_DB[str(USER_ID)]["STATES_USER"]["PREVIOUS_MESSAGE_ID"] = SENT_MESSAGE.message_id
					
					else:
						await message_or_callbackQuery.answer("⚠️ В данный момент профиль не работает.")

				elif isinstance(message_or_callbackQuery, types.CallbackQuery):
					"""Объявляем переменную, где выводим текущую фазу пользователя"""
					CURRENT_STATE = await state.get_state()

					if CURRENT_STATE == "ProfileState:SendUserPasswordState" or CURRENT_STATE == "ProfileState:SendCodeAndSocialState" or CURRENT_STATE == "ProfileState:SendNumberWalletAndBackProfileState":
						await bot.delete_message(message_or_callbackQuery.message.chat.id, message_or_callbackQuery.message.message_id)

						if PHOTO.photos:
							SENT_MESSAGE = await bot.send_photo(chat_id = message_or_callbackQuery.message.chat.id, photo = PHOTO_USER, caption = INFO_PROFILE_MESSAGE, reply_markup = profile_menu_inline_keyboard)

							USER_DATA_DB[str(USER_ID)]["STATES_USER"]["PREVIOUS_MESSAGE_ID"] = SENT_MESSAGE.message_id

							await state.finish()

						elif not PHOTO.photos:
							SENT_MESSAGE = await bot.send_message(chat_id = message_or_callbackQuery.message.chat.id, text = INFO_PROFILE_MESSAGE, reply_markup = profile_menu_inline_keyboard)

							USER_DATA_DB[str(USER_ID)]["STATES_USER"]["PREVIOUS_MESSAGE_ID"] = SENT_MESSAGE.message_id

							await state.finish()

						else:
							await message_or_callbackQuery.answer("⚠️ В данный момент профиль не работает.")

							await state.finish()
					
					elif CURRENT_STATE == "ProfileState:SendNumberWalletState" or CURRENT_STATE == "ProfileState:SelectedNewSportState" or CURRENT_STATE == None:
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