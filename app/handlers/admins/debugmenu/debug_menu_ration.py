from data.loader import dp, bot
from data.config import ConfigBot, ConfigBotAsync
from data.config_Keyboard import ConfigInlineKeyboard
from data.loader_keyboard import LoaderInlineKeyboardsAdmin
from data.states_groups import DebugAdminState

from database.requests.user_db import load_user_data, is_user_in_data, save_user_data
from database.requests.admin_db import load_admin_data, is_admin_in_data
from database.requests.ration_db import load_ration_data, is_ration_in_data, save_ration_data, is_weekday_in_data

from misc.libraries import types, FSMContext
from misc.loggers import logger

"""Создаем обработчик для управления Рационом."""
@dp.callback_query_handler(lambda callback_data: callback_data.data in ["RATION", "BACK_RATION"], state = [None, DebugAdminState.AddRationForAdminState, DebugAdminState.DeleteRationForAdminState, DebugAdminState.EditRationForAdminState, DebugAdminState.SelectRationForAdminState])
async def ration_admin_handler(callback_query: types.CallbackQuery, state: FSMContext) -> str:
	"""Объявляем переменные для вывода информации о пользователе и администрации."""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID, USER_NAME, USER_LAST_NAME."""
		USER_ID = ConfigBot.USERID(callback_query)
		USER_NAME = ConfigBot.USERNAME(callback_query)
		USER_LAST_NAME = ConfigBot.USERLASTNAME(callback_query)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				"""Объявляем переменную с выводом клавиатуры для меню управления рационом."""
				menu_ration_admin_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_RATION_MENU

				INFO_MENU_RATION_ADMIN_MESSAGE = f"💬 <a href='https://t.me/{USER_NAME}'>{USER_LAST_NAME}</a>, добро пожаловать в <b>«{ConfigInlineKeyboard().RATION[2:-2]}»</b>.\n\n" \
												 f"Здесь вы можете легко управлять рационом, добавлять его и удалять.\n\n" \
												 f" • <b>{ConfigInlineKeyboard().ADD_RATION[2:]}:</b> Используйте эту кнопку для добавление <b>нового</b> рациона.\n\n" \
												 f" • <b>{ConfigInlineKeyboard().DELETE_RATION[:-2]}:</b> При необходимости вы можете <b>удалить</b> выбранный рацион из базы данных.\n\n" \
												 f" • <b>{ConfigInlineKeyboard().EDIT_RATION[2:-2]}:</b> Нажмите эту кнопку, чтобы <b>редактировать</b> рацион, которые в данный момент находятся в базе данных.\n\n" \
												 f" • <b>{ConfigInlineKeyboard().SELECT_RATION[2:-2]}:</b> Чтобы выбрать <b>основной</b> рацион для пользователей, используйте эту кнопку.\n\n" \
												 f"Управляйте с легкостью. Ваш комфорт - наша главная задача!"
				
				await bot.edit_message_text(INFO_MENU_RATION_ADMIN_MESSAGE,
											callback_query.from_user.id, 
											callback_query.message.message_id,
											reply_markup = menu_ration_admin_inline_keyboard)
				
				await state.finish()
			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик для добавления, удаления и редактирования рациона для администрации."""
@dp.callback_query_handler(lambda callback_data: callback_data.data in ["ADD_RATION", "DELETE_RATION", "EDIT_RATION", "EDIT_NAME_RATION", "EDIT_EMOJI_RATION", "EDIT_WEEKDAY_RATION", "EDIT_WEEKDAY_DESCRIPTION", "EDIT_WEEKDAY_DELETE_MEALS", "EDIT_WEEKDAY_MEALS", "SELECT_RATION"], state = [None, DebugAdminState.EditRationForAdminState, DebugAdminState.EditWeekdayRationForAdminState])
async def all_ration_admin_handler(callback_query: types.CallbackQuery) -> str:
	"""Объявляем переменные для вывода информации о пользователе и администрации."""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()
	RATION_DATA_DB = load_ration_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID, WEEKDAY_ID, RATION_ID, USER_NAME, USER_LAST_NAME."""
		USER_ID = ConfigBot.USERID(callback_query)
		WEEKDAY_ID = ConfigBot.STATUS_USER_WEEKDAY_ID(callback_query)
		RATION_ID = ConfigBot.STATUS_USER_RATION_ID(callback_query)
		USER_NAME = ConfigBot.USERNAME(callback_query)
		USER_LAST_NAME = ConfigBot.USERLASTNAME(callback_query)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				"""Объявляем переменную с выводом Inline клавиатуры для возвращения во вкладку управления рационом."""
				back_menu_ration_admin_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_RATION_MENU

				"""Объявляем переменную с выводом куска сообщения для окончанья и начало главного сообщения."""
				START_MESSAGE = f"<a href='https://t.me/{USER_NAME}'>{USER_LAST_NAME}</a>"
				END_MESSAGE = f"Благодарим за вашу активность в <i><b>«{ConfigInlineKeyboard().RATION[2:-2]}»</b></i>."

				match callback_query.data:
					case "ADD_RATION":
						"""Объявляем переменную с выводом сообщения о информации добавления рациона."""
						RATION_ADMIN_MESSAGE = f"💬 {START_MESSAGE}, для <b>добавления нового рациона</b>, введите следующую информацию:\n\n" \
												" • <b>ID Рациона:</b> [ <i>Введите ID Рациона</i> ]\n" \
												" • <b>Эмодзи Рациона:</b> [ <i>Введите Эмодзи Рациона</i> ]\n" \
												" • <b>Название Рациона:</b> [ <i>Введите Название Рациона</i> ]\n\n" \
												f"{END_MESSAGE}"
						
						"""Объявляем фазу, где администратор вводит нужные данные для добавления нового рациона."""
						await DebugAdminState.AddRationForAdminState.set()
					
					case "DELETE_RATION":
						"""Объявляем переменную с выводом сообщения о информации удаления рациона."""
						RATION_ADMIN_MESSAGE = f"💬 {START_MESSAGE}, для <b>удаления рациона</b> введите <b>ID</b>, который вы хотели бы удалить:\n\n" \
												f"{ConfigBot.GET_ID_RATION(RATION_DATA_DB)}\n\n" \
												f"{END_MESSAGE}"
						
						"""Объявляем фазу, где администратор вводит ID рациона для удаления его."""
						await DebugAdminState.DeleteRationForAdminState.set()

					case "SELECT_RATION":
						"""Объявляем переменную с выводом сообщения о информации выбора рациона."""
						RATION_ADMIN_MESSAGE = f"💬 {START_MESSAGE}, для <b>выбора рациона</b> введите <b>ID</b>, который вы хотели бы выбрать:\n\n" \
												f"{ConfigBot.GET_ID_RATION(RATION_DATA_DB)}\n\n" \
												f"{END_MESSAGE}"
						
						"""Объявляем фазу, где администратор вводит ID рациона для выбора его."""
						await DebugAdminState.SelectRationForAdminState.set()

					case "EDIT_RATION":
						"""Объявляем переменную с выводом сообщения о информации редактирования рациона."""
						RATION_ADMIN_MESSAGE = f"💬 {START_MESSAGE}, для <b>редактирования рациона</b> введите <b>ID</b>, который вы хотели бы отредактировать.\n\n" \
												f"{ConfigBot.GET_ID_RATION(RATION_DATA_DB)}\n\n" \
												f"{END_MESSAGE}"

						"""Сбрасываем статус редактирования рациона."""
						USER_DATA_DB[str(USER_ID)]["STATES_USER"]["RATION_ID"] = None

						"""Объявляем фазу, где администратор вводит ID рациона для его редактирования."""
						await DebugAdminState.EditRationForAdminState.set()
					
					case "EDIT_NAME_RATION":
						"""Объявляем переменную с выводом сообщения о информации редактирования названия рациона."""
						RATION_ADMIN_MESSAGE = f"💬 {START_MESSAGE}, введите, пожалуйста, <b>новое название рациона</b> для изменения текущего названия.\n\n" \
												f" • <b>Название Рациона:</b> [ <i>{ConfigBot.GET_RATION(RATION_ID, 'NAME_RATION')}</i> ]\n\n" \
												f"{END_MESSAGE}"
						
						"""Объявляем фазу, где администратор вводит новое название рациона."""
						await DebugAdminState.NewNameRationForAdminState.set()
					
					case "EDIT_EMOJI_RATION":
						"""Объявляем переменную с выводом сообщения о информации редактирования эмодзи рациона."""
						RATION_ADMIN_MESSAGE = f"💬 {START_MESSAGE}, введите, пожалуйста, <b>новый эмодзи рациона</b> для изменения текущего эмодзи.\n\n" \
												f" • <b>Эмодзи Рациона:</b> [ <i>{ConfigBot.GET_RATION(RATION_ID, 'EMOJI_RATION')}</i> ]\n\n" \
												f"{END_MESSAGE}"
						
						"""Объявляем фазу, где администратор вводит новый эмодзи рациона."""
						await DebugAdminState.NewEmojiRationForAdminState.set()
					
					case "EDIT_WEEKDAY_RATION":
						"""Объявляем переменную с выводом сообщения о информации редактирования дня недели."""
						RATION_ADMIN_MESSAGE = f"💬 {START_MESSAGE}, для <b>редактирования дня недели</b> введите <b>ID</b>, который вы хотели бы отредактировать.\n\n" \
												f"{ConfigBot.GET_ID_WEEKDAY(RATION_DATA_DB, callback_query)}\n\n" \
												f"{END_MESSAGE}"
						
						"""Объявляем фазу, где администратор вводит ID Дня недели для его редактирования."""
						await DebugAdminState.EditWeekdayRationForAdminState.set()
					
					case "EDIT_WEEKDAY_DESCRIPTION":
						"""Объявляем переменную с выводом сообщения о информации редактирования описания дня недели."""
						RATION_ADMIN_MESSAGE = f"💬 {START_MESSAGE}, введите, пожалуйста, <b>новое описание {ConfigBot.TRANSTALED_WEEKDAY(WEEKDAY_ID)}</b>.\n\n" \
											   f" • <b>Описание {ConfigBot.TRANSTALED_WEEKDAY(WEEKDAY_ID)}:</b> [ {ConfigBot.GET_WEEKDAY(RATION_ID, WEEKDAY_ID, f'DESCRIPTION_{WEEKDAY_ID}') if ConfigBot.GET_WEEKDAY(RATION_ID, WEEKDAY_ID, f'DESCRIPTION_{WEEKDAY_ID}') else 'Нету описания'} ]\n\n" \
											   f"{END_MESSAGE}"
						
						"""Объявляем фазу, где администратор вводит новое описание дня недели."""
						await DebugAdminState.NewDescriptionWeekdayRationForAdminState.set()
					
					case "EDIT_WEEKDAY_DELETE_MEALS":
						"""Объявляем переменную с выводом сообщения о информации удаления блюда в дни недели."""
						RATION_ADMIN_MESSAGE = f"💬 {START_MESSAGE}, для <b>удаления блюда</b> введите <b>ID</b>, который вы хотели бы удалить.\n\n" \
											   f"{ConfigBot.GET_MEALS_WEEKDAY(RATION_DATA_DB, RATION_ID, WEEKDAY_ID)}\n\n" \
											   f"{END_MESSAGE}"
						
						"""Объявляем фазу, где администратор вводит ID блюда для его удаления."""
						await DebugAdminState.DeleteMealsRationForAdminState.set()
					
					case "EDIT_WEEKDAY_MEALS":
						"""Объявляем переменную с выводом сообщения о информации добавления блюда в день недели."""
						RATION_ADMIN_MESSAGE = f"💬 {START_MESSAGE}, для <b>добавления нового блюда</b>, введите следующую информацию:\n\n" \
											    " • <b>Тип Блюда:</b> [ <i>Введите тип блюда: BREAKFAST, LUNCH, DINNER</i> ]\n" \
												" • <b>Ссылка на Рецепт:</b> [ <i>Введите ссылку на рецепт</i> ]\n" \
												" • <b>Название Блюда:</b> [ <i>Введите название блюда</i> ]\n\n" \
												"Пример <b>добавления</b> нужного блюда в день недели:\n\n" \
												" • <i><b>«BREAKFAST» | «Ссылка на рецепт» | «Название Блюда»</b></i>\n\n" \
											   f"{END_MESSAGE}"
						
						"""Объявляем фазу, где администратор вводит нужные данные для добавления нового блюда."""
						await DebugAdminState.NewMealsWeekdayRationForAdminState.set()

				"""Объявляем переменную с выводом сообщения о редактировании рациона, и для сохранения message_id."""
				SENT_MESSAGE = await bot.edit_message_text(RATION_ADMIN_MESSAGE,
															callback_query.from_user.id,
															callback_query.message.message_id,
															reply_markup = back_menu_ration_admin_inline_keyboard)
				
				USER_DATA_DB[str(USER_ID)]["STATES_USER"]["PREVIOUS_MESSAGE_ID"] = SENT_MESSAGE.message_id

				save_user_data(USER_DATA_DB)

			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик фазы, где администратор вводит ID рациона для редактирования его."""
@dp.message_handler(state = [DebugAdminState.EditRationForAdminState, DebugAdminState.EditWeekdayRationForAdminState])
@dp.callback_query_handler(lambda callback_data: callback_data.data == "BACK_RATION", state = [DebugAdminState.NewNameRationForAdminState, DebugAdminState.NewEmojiRationForAdminState, DebugAdminState.EditWeekdayRationForAdminState, DebugAdminState.NewDescriptionWeekdayRationForAdminState, DebugAdminState.NewMealsWeekdayRationForAdminState, DebugAdminState.DeleteMealsRationForAdminState])
async def edit_ration_for_admin_handler(message_or_callbackQuery: types.Message | types.CallbackQuery, state: FSMContext) -> str:
	"""Объявляем переменную с выводом информации о пользователе и администрации."""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()
	RATION_DATA_DB = load_ration_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_MESSAGE, USER_ID, RATION_ID, USER_NAME, USER_LAST_NAME, MESSAGE_ID."""
		USER_ID = ConfigBot.USERID(message_or_callbackQuery)
		USER_NAME = ConfigBot.USERNAME(message_or_callbackQuery)
		USER_LAST_NAME = ConfigBot.USERLASTNAME(message_or_callbackQuery)
		MESSAGE_ID = ConfigBot.GETMESSAGEID(message_or_callbackQuery)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				"""Объявляем переменную с выводом Inline клавиатуры для редактирования рациона."""
				edit_menu_ration_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_EDIT_RATION_MENU
				edit_menu_weekdays_ration_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_EDIT_WEEKDAYS_RATION_MENU

				"""Объявляем переменную с выводом куска сообщения для начала главного сообщения."""
				START_MESSAGE = f"<a href='https://t.me/{USER_NAME}'>{USER_LAST_NAME}</a>"

				"""Объявляем переменную, где выводим текущую фазу пользователя."""
				CURRENT_STATE = await state.get_state()

				match message_or_callbackQuery:
					case types.Message():
						"""Объявляем переменную с выводом информации о пользователе: USER_MESSAGE."""
						USER_MESSAGE = ConfigBot.USERMESSAGE(message_or_callbackQuery)

						"""Удаляем последнее сообщение с информацией о рационе."""
						await ConfigBotAsync.DELETE_MESSAGE_USERS_AND_ADMINS(types = message_or_callbackQuery, message_id = MESSAGE_ID)

						match CURRENT_STATE:
							case "DebugAdminState:EditRationForAdminState":
								"""Объявляем сохранение ID рациона для редактирования."""
								USER_DATA_DB[str(USER_ID)]["STATES_USER"]["RATION_ID"] = USER_MESSAGE
								USER_DATA_DB[str(USER_ID)]["STATES_USER"]["PREVIOUS_MESSAGE_ID"] = None

								save_user_data(USER_DATA_DB)

								"""Объявляем переменную с выводом сообщение о информации рациона."""
								INFO_RATION_ADMIN_MESSAGE_ONE = "💬 Краткая информация об Рационе:\n\n" \
																f" • <b>Название Рациона:</b> {ConfigBot.GET_RATION(USER_MESSAGE, 'NAME_RATION')} • {ConfigBot.GET_RATION(USER_MESSAGE, 'EMOJI_RATION')}\n\n" \
																f" • <b>Дата Добавления:</b> {ConfigBot.GET_RATION(USER_MESSAGE, 'CREATE_TIME_RATION')}\n\n" \
																"<i>Для внесения изменений, пожалуйста, выберите нужную кнопку ниже.</i>"
						
								if is_ration_in_data(USER_MESSAGE, RATION_DATA_DB):
									await message_or_callbackQuery.answer(INFO_RATION_ADMIN_MESSAGE_ONE, reply_markup = edit_menu_ration_inline_keyboard)

									"""Объявляем фазу, где администратор выбирает, что именно нужно отредактировать."""
									await DebugAdminState.EditRationForAdminState.set()
								
								elif not is_ration_in_data(USER_MESSAGE, RATION_DATA_DB):
									await message_or_callbackQuery.answer(f"⚠️ {START_MESSAGE} извините, но похоже, что рацион с введенным <b>ID</b> отсутствует в базе данных.\n\n"
																			f" • <b>ID Рациона:</b> [ <code>{USER_MESSAGE}</code> ]\n\n"
																			"❕Убедитесь, что вы ввели <b>правильный ID</b>, и повторите попытку.")
							
							case "DebugAdminState:EditWeekdayRationForAdminState":
								"""Объявляем переменную с выводом информации о пользователе: RATION_ID, WEEKDAY_ID."""
								RATION_ID = ConfigBot.STATUS_USER_RATION_ID(message_or_callbackQuery)
								WEEKDAY_ID = ConfigBot.STATUS_USER_WEEKDAY_ID(message_or_callbackQuery)

								"""Объявляем сохранение ID Дня недели для редактирования."""
								USER_DATA_DB[str(USER_ID)]["STATES_USER"]["WEEKDAY_ID"] = USER_MESSAGE
								USER_DATA_DB[str(USER_ID)]["STATES_USER"]["PREVIOUS_MESSAGE_ID"] = None

								save_user_data(USER_DATA_DB)

								"""Объявляем переменную с выводом сообщение о информации дня недели."""
								INFO_WEEKDAY_RATION_ADMIN_MESSAGE_ONE = f"💬 Краткая информация {ConfigBot.TRANSTALED_WEEKDAY(WEEKDAY_ID)}:\n\n" \
																	    f" • <b>Название Рациона:</b> {ConfigBot.GET_RATION(RATION_ID, 'NAME_RATION')} • {ConfigBot.GET_RATION(RATION_ID, 'EMOJI_RATION')}\n\n" \
																	    f" • <b>Описание {ConfigBot.TRANSTALED_WEEKDAY(WEEKDAY_ID)}:</b> {ConfigBot.GET_WEEKDAY(RATION_ID, WEEKDAY_ID, f'DESCRIPTION_{WEEKDAY_ID}') if ConfigBot.GET_WEEKDAY(RATION_ID, WEEKDAY_ID, f'DESCRIPTION_{WEEKDAY_ID}') else 'Нету описания'}\n\n" \
																	    f" • <b>Количество Блюд:</b> {ConfigBot.LENS_WEEKDAY(RATION_DATA_DB, WEEKDAY_ID, message_or_callbackQuery)}\n\n" \
																	    f" • <b>Дата Добавления:</b> {ConfigBot.GET_RATION(RATION_ID, 'CREATE_TIME_RATION')}\n\n" \
																	     "<i>Для внесения изменений, пожалуйста, выберите нужную кнопку ниже.</i>"

								if is_weekday_in_data(USER_MESSAGE, RATION_DATA_DB):
									await message_or_callbackQuery.answer(INFO_WEEKDAY_RATION_ADMIN_MESSAGE_ONE, reply_markup = edit_menu_weekdays_ration_inline_keyboard)

									"""Объявляем фазу, где администратор выбирает, что именно нужно отредактировать."""
									await DebugAdminState.EditWeekdayRationForAdminState.set()
								
								elif not is_weekday_in_data(USER_MESSAGE, RATION_DATA_DB):
									await message_or_callbackQuery.answer(f"⚠️ {START_MESSAGE} извините, но похоже, что день недели с введенным <b>ID</b> отсутствует в базе данных.\n\n"
																			f" • <b>ID Дня Недели:</b> [ <code>{USER_MESSAGE}</code> ]\n\n"
																			"❕Убедитесь, что вы ввели <b>правильный ID</b>, и повторите попытку.")
					
					case types.CallbackQuery():
						"""Объявляем переменную с выводом информации о пользователе: RATION_ID, WEEKDAY_ID."""
						RATION_ID = ConfigBot.STATUS_USER_RATION_ID(message_or_callbackQuery)
						WEEKDAY_ID = ConfigBot.STATUS_USER_WEEKDAY_ID(message_or_callbackQuery)

						if CURRENT_STATE in ["DebugAdminState:NewNameRationForAdminState", "DebugAdminState:NewEmojiRationForAdminState", "DebugAdminState:EditWeekdayRationForAdminState"]:
							"""Объявляем переменную с выводом сообщение о информации рациона."""
							INFO_RATION_ADMIN_MESSAGE_TWO = "💬 Краткая информация об Рационе:\n\n" \
															f" • <b>Название Рациона:</b> {ConfigBot.GET_RATION(RATION_ID, 'NAME_RATION')} • {ConfigBot.GET_RATION(RATION_ID, 'EMOJI_RATION')}\n\n" \
															f" • <b>Дата Добавления:</b> {ConfigBot.GET_RATION(RATION_ID, 'CREATE_TIME_RATION')}\n\n" \
															"<i>Для внесения изменений, пожалуйста, выберите нужную кнопку ниже.</i>"

							await bot.edit_message_text(INFO_RATION_ADMIN_MESSAGE_TWO,
														message_or_callbackQuery.from_user.id,
														message_or_callbackQuery.message.message_id,
														reply_markup = edit_menu_ration_inline_keyboard)

							"""Объявляем фазу, где администратор выбирает, что именно нужно отредактировать."""
							await DebugAdminState.EditRationForAdminState.set()
						
						elif CURRENT_STATE in ["DebugAdminState:NewDescriptionWeekdayRationForAdminState", "DebugAdminState:NewMealsWeekdayRationForAdminState", "DebugAdminState:DeleteMealsRationForAdminState"]:
							"""Объявляем переменную с выводом сообщение о информации дня недели."""
							INFO_WEEKDAY_RATION_ADMIN_MESSAGE_TWO = f"💬 Краткая информация {ConfigBot.TRANSTALED_WEEKDAY(WEEKDAY_ID)}:\n\n" \
																	f" • <b>Название Рациона:</b> {ConfigBot.GET_RATION(RATION_ID, 'NAME_RATION')} • {ConfigBot.GET_RATION(RATION_ID, 'EMOJI_RATION')}\n\n" \
																	f" • <b>Описание {ConfigBot.TRANSTALED_WEEKDAY(WEEKDAY_ID)}:</b> {ConfigBot.GET_WEEKDAY(RATION_ID, WEEKDAY_ID, f'DESCRIPTION_{WEEKDAY_ID}') if ConfigBot.GET_WEEKDAY(RATION_ID, WEEKDAY_ID, f'DESCRIPTION_{WEEKDAY_ID}') else 'Нету описания'}\n\n" \
																	f" • <b>Количество Блюд:</b> {ConfigBot.LENS_WEEKDAY(RATION_DATA_DB, WEEKDAY_ID, message_or_callbackQuery)}\n\n" \
																	f" • <b>Дата Добавления:</b> {ConfigBot.GET_RATION(RATION_ID, 'CREATE_TIME_RATION')}\n\n" \
																		"<i>Для внесения изменений, пожалуйста, выберите нужную кнопку ниже.</i>"

							await bot.edit_message_text(INFO_WEEKDAY_RATION_ADMIN_MESSAGE_TWO,
														message_or_callbackQuery.from_user.id,
														message_or_callbackQuery.message.message_id,
														reply_markup = edit_menu_weekdays_ration_inline_keyboard)
							
							"""Объявляем фазу, где администратор выбирает, что именно нужно отредактировать."""
							await DebugAdminState.EditWeekdayRationForAdminState.set()
					
					case _:
						logger.error("⚠️ Произошла непредвиденная ошибка с проверкой типа данных: %s", type(message_or_callbackQuery))
			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик фазы, где администратор вводит новое название рациона."""
@dp.message_handler(state = [DebugAdminState.NewNameRationForAdminState, DebugAdminState.NewEmojiRationForAdminState, DebugAdminState.NewDescriptionWeekdayRationForAdminState, DebugAdminState.DeleteMealsRationForAdminState, DebugAdminState.SelectRationForAdminState])
async def new_name_and_emoji_ration_for_admin_handler(message: types.Message, state: FSMContext) -> str:
	"""Объявляем переменную с выводом информации о пользователе и администрации."""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()
	RATION_DATA_DB = load_ration_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID, RATION_ID, WEEKDAY_ID, USER_NAME, USER_LAST_NAME, USER_MESSAGE, MESSAGE_ID."""
		USER_ID = ConfigBot.USERID(message)
		RATION_ID = ConfigBot.STATUS_USER_RATION_ID(message)
		WEEKDAY_ID = ConfigBot.STATUS_USER_WEEKDAY_ID(message)
		USER_NAME = ConfigBot.USERNAME(message)
		USER_LAST_NAME = ConfigBot.USERLASTNAME(message)
		USER_MESSAGE = ConfigBot.USERMESSAGE(message)
		MESSAGE_ID = ConfigBot.GETMESSAGEID(message)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				"""Удаляем последнее сообщение с информацией о рационе."""
				await ConfigBotAsync.DELETE_MESSAGE_USERS_AND_ADMINS(types = message, message_id = MESSAGE_ID)

				"""Объявляем переменную с выводом Inline клавиатуры для возвращения во вкладку управления рационом."""
				back_menu_ration_admin_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_RATION_MENU

				"""Объявляем переменную с выводом куска сообщения для окончанья и начало главного сообщения."""
				START_MESSAGE = f"<a href='https://t.me/{USER_NAME}'>{USER_LAST_NAME}</a>"
				END_MESSAGE = f"Благодарим за вашу активность в <i><b>«{ConfigInlineKeyboard().RATION[2:-2]}»</b></i>."

				"""Объявляем переменную, где выводим текущую фазу пользователя."""
				CURRENT_STATE = await state.get_state()

				match CURRENT_STATE:
					case "DebugAdminState:SelectRationForAdminState":
						"""Объявляем переменную с выводом сообщение о информации выбора рациона для пользователя."""
						EDIT_NAME_RATION_MESSAGE = f"💬 {START_MESSAGE}, рацион для пользователей <b>успешно выбран</b>.\n\n" \
												   f" • <b>ID Рациона:</b> [ <i>{USER_MESSAGE}</i> ]\n\n" \
												   f"{END_MESSAGE}"
						
						"""Объявляем функцию для сохранения ID Рациона."""
						RATION_DATA_DB["RATION_MAIN"]["RATION_SELECT"] = USER_MESSAGE

						save_ration_data(RATION_DATA_DB)

						await ConfigBotAsync.NOTIFY_SELECT_RATION(types = message, database_users = USER_DATA_DB, database_admins = ADMIN_DATA_DB, name_ration = ConfigBot.GET_RATION(USER_MESSAGE, 'NAME_RATION'))

					case "DebugAdminState:NewNameRationForAdminState":
						"""Объявляем переменную с выводом сообщение о информации редактирования названия Рациона."""
						EDIT_NAME_RATION_MESSAGE = f"💬 {START_MESSAGE}, название для рациона <b>успешно изменено</b>.\n\n" \
												   f" • <b>Название Рациона:</b> [ <i>{USER_MESSAGE}</i> ]\n\n" \
												   f"{END_MESSAGE}"

						"""Объявляем функцию для сохранения названия Рациона."""
						RATION_DATA_DB[RATION_ID]["NAME_RATION"] = USER_MESSAGE

						save_ration_data(RATION_DATA_DB)
				
					case "DebugAdminState:NewEmojiRationForAdminState":
						"""Объявляем переменную с выводом сообщение о информации редактирования эмодзи Рациона."""
						EDIT_NAME_RATION_MESSAGE = f"💬 {START_MESSAGE}, эмодзи для рациона <b>успешно изменено</b>.\n\n" \
												   f" • <b>Эмодзи Рациона:</b> [ {USER_MESSAGE} ]\n\n" \
												   f"{END_MESSAGE}"
						
						"""Объявляем функцию для сохранения эмодзи Рациона."""
						RATION_DATA_DB[RATION_ID]["EMOJI_RATION"] = USER_MESSAGE

						save_ration_data(RATION_DATA_DB)
					
					case "DebugAdminState:NewDescriptionWeekdayRationForAdminState":
						"""Объявляем переменную с выводом сообщение о информации редактирования описания Рациона."""
						EDIT_NAME_RATION_MESSAGE = f"💬 {START_MESSAGE}, описание для {ConfigBot.TRANSTALED_WEEKDAY(WEEKDAY_ID)[0].lower() + ConfigBot.TRANSTALED_WEEKDAY(WEEKDAY_ID)[1:]} <b>успешно изменено</b>.\n\n" \
												   f" • <b>Описание {ConfigBot.TRANSTALED_WEEKDAY(WEEKDAY_ID)}:</b> [ <i>{USER_MESSAGE}</i> ]\n\n" \
												   f"{END_MESSAGE}"

						"""Объявляем функцию для сохранения описания Рациона."""
						RATION_DATA_DB[RATION_ID]["WEEKDAY"][WEEKDAY_ID][f"DESCRIPTION_{WEEKDAY_ID}"] = USER_MESSAGE

						save_ration_data(RATION_DATA_DB)
					
					case "DebugAdminState:DeleteMealsRationForAdminState":
						"""Объявляем переменную с выводом сообщение о информации удаления блюда из Рациона."""
						EDIT_NAME_RATION_MESSAGE = f"💬 {START_MESSAGE}, блюдо <b>успешно удалено</b>.\n\n" \
												   f" • <b>Тип Блюда:</b> [ <i>{USER_MESSAGE}</i> ]\n\n" \
												   f"{END_MESSAGE}"
						
						"""Объявляем функцию для удаления блюда из Рациона."""
						RATION_DATA_DB[RATION_ID]["WEEKDAY"][WEEKDAY_ID][USER_MESSAGE] = None
						RATION_DATA_DB[RATION_ID]["WEEKDAY"][WEEKDAY_ID][f"{USER_MESSAGE}_LINK_RECIPE"] = None

						save_ration_data(RATION_DATA_DB)

				await message.answer(EDIT_NAME_RATION_MESSAGE,
									 reply_markup = back_menu_ration_admin_inline_keyboard)

			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик фазы, где администратор вводит ID рациона для удаления его."""
@dp.message_handler(state = DebugAdminState.DeleteRationForAdminState)
async def delete_ration_for_admin_handler(message: types.Message) -> str:
	"""Объявляем переменную с выводом информации о пользователе и администрации."""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()
	RATION_DATA_DB = load_ration_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_MESSAGE, USER_ID, USER_NAME, USER_LAST_NAME, MESSAGE_ID."""
		USER_MESSAGE = ConfigBot.USERMESSAGE(message)
		USER_ID = ConfigBot.USERID(message)
		USER_NAME = ConfigBot.USERNAME(message)
		USER_LAST_NAME = ConfigBot.USERLASTNAME(message)
		MESSAGE_ID = ConfigBot.GETMESSAGEID(message)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				"""Объявляем переменную с выводом куска сообщения для окончанья и начало главного сообщения."""
				START_MESSAGE = f"<a href='https://t.me/{USER_NAME}'>{USER_LAST_NAME}</a>"
				END_MESSAGE = f"Благодарим за вашу активность в <i><b>«{ConfigInlineKeyboard().RATION[2:-2]}»</b></i>."

				if is_ration_in_data(USER_MESSAGE, RATION_DATA_DB):
					"""Удаляем последнее сообщение с информацией о рационе."""
					await ConfigBotAsync.DELETE_MESSAGE_USERS_AND_ADMINS(types = message, message_id = MESSAGE_ID)

					"""Объявляем переменную с выводом Inline клавиатуры для возвращения во вкладку управления рационом."""
					back_menu_ration_admin_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_RATION_MENU

					"""Объявляем функцию для удаления рациона из базы данных."""
					del RATION_DATA_DB[str(USER_MESSAGE)]

					save_ration_data(RATION_DATA_DB)

					await message.answer(f"💬 {START_MESSAGE}, отлично, упражнение с указанным <b>ID</b> успешно удален из базы данных.\n\n"
										 f" • <b>ID Рациона: [ <code>{USER_MESSAGE}</code> ]</b>\n\n"
						  				 f"{END_MESSAGE}",
										 reply_markup = back_menu_ration_admin_inline_keyboard)
				else:
					await message.answer(f"⚠️ {START_MESSAGE} извините, но похоже, что рацион с указанным <b>ID</b> не существует в базе данных.\n\n"
										 f" • <b>ID Рациона: [ <code>{USER_MESSAGE}</code> ]</b>\n\n"
						  				 "❕Убедитесь, что вы ввели <b>правильный ID</b>, и повторите попытку.")
			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик фазы, где администратор вводит нужные данные для добавления нового блюда."""
@dp.message_handler(state = DebugAdminState.NewMealsWeekdayRationForAdminState)
async def new_meals_weekday_ration_for_admin_handler(message: types.Message) -> str:
	"""Объявляем переменные для вывода информации о пользователе и администрации."""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()
	RATION_DATA_DB = load_ration_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID, RATION_ID, WEEKDAY_ID, USER_NAME, USER_LAST_NAME, MESSAGE_ID."""
		USER_ID = ConfigBot.USERID(message)
		RATION_ID = ConfigBot.STATUS_USER_RATION_ID(message)
		WEEKDAY_ID = ConfigBot.STATUS_USER_WEEKDAY_ID(message)
		USER_NAME = ConfigBot.USERNAME(message)
		USER_LAST_NAME = ConfigBot.USERLASTNAME(message)
		MESSAGE_ID = ConfigBot.GETMESSAGEID(message)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				"""Разделяем сообщение на ID рациона и остальную информацию."""
				PARTS = ConfigBot.USERMESSAGE(message).split()

				"""Объявляем переменную с выводом куска сообщения для окончанья и начало главного сообщения."""
				START_MESSAGE = f"<a href='https://t.me/{USER_NAME}'>{USER_LAST_NAME}</a>"
				END_MESSAGE = f"Благодарим за вашу активность в <i><b>«{ConfigInlineKeyboard().RATION[2:-2]}»</b></i>."

				if len(PARTS) > 3:
					"""Выводим из первого сообщения - Тип Блюда."""
					WEEKDAY_MEAL = PARTS[0]

					if WEEKDAY_MEAL in ["BREAKFAST", "LUNCH", "DINNER"]:
						"""Удаляем последнее сообщение с информацией о рационе."""
						await ConfigBotAsync.DELETE_MESSAGE_USERS_AND_ADMINS(types = message, message_id = MESSAGE_ID)
					
						"""Объявляем переменную с выводом Inline клавиатуры для возвращения во вкладку управления рационом."""
						back_menu_ration_admin_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_RATION_MENU

						"""Объявляем переменные для разделения PARTS на аспекты."""
						LINK_RECIPE_WEEKDAY, NAME_MEAL_WEEKDAY = PARTS[1], " ".join(PARTS[2:])

						"""Сохраняем данные о блюде в базу данных."""
						RATION_DATA_DB[str(RATION_ID)]["WEEKDAY"][WEEKDAY_ID][f"{WEEKDAY_MEAL}_LINK_RECIPE"] = LINK_RECIPE_WEEKDAY
						RATION_DATA_DB[str(RATION_ID)]["WEEKDAY"][WEEKDAY_ID][f"{WEEKDAY_MEAL}"] = NAME_MEAL_WEEKDAY

						save_ration_data(RATION_DATA_DB)

						await message.answer(f"💬 {START_MESSAGE}, новое <b>блюдо добавлено</b> в базу данных.\n\n"
											 f" • <b>Ссылка на Блюдо:</b> [ <a href='{LINK_RECIPE_WEEKDAY}'>ССЫЛКА</a> ]\n"
											 f" • <b>Название Блюда:</b> [ <i>{NAME_MEAL_WEEKDAY}</i> ]\n\n"
											 f"{END_MESSAGE}",
											 reply_markup = back_menu_ration_admin_inline_keyboard)

					else:
						await message.answer(f"⚠️ {START_MESSAGE}, извините, но для добавления блюда необходимо указать первый пункт.\n\n"
						   					 f" • <b>Тип Блюда:</b> [ <i>{WEEKDAY_MEAL}</i> ]\n\n"
											  "Пример <b>добавления</b> нужного блюда в день недели:\n\n"
											  " • <i><b>«BREAKFAST» | «Ссылка на рецепт» | «Название Блюда»</b></i>\n\n"
											  "❕ Пожалуйста, убедитесь, что поле [ <b>Тип Блюда/b> ] заполнено верно, и повторите попытку.")

				elif len(PARTS) < 3:
					await message.answer(f"⚠️ {START_MESSAGE}, извините, но для добавления блюда необходимо предоставить <b>полную информацию</b>. Пожалуйста, убедитесь, что вы ввели следующие данные:\n\n"
										  " • <b>Тип Блюда:</b> [ <i>Введите тип блюда: BREAKFAST, LUNCH, DINNER</i> ]\n" \
										  " • <b>Ссылка на Рецепт:</b> [ <i>Введите ссылку на рецепт</i> ]\n" \
										  " • <b>Название Блюда:</b> [ <i>Введите название блюда</i> ]\n\n" \
										  "❕ Пожалуйста, убедитесь, что все поля <b>заполнены</b>, и повторите попытку.")
			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик фазы, где администратор вводит нужные данные для добавления нового рациона."""
@dp.message_handler(state = DebugAdminState.AddRationForAdminState)
async def add_ration_for_admin_handler(message: types.Message) -> str:
	"""Объявляем переменные для вывода информации о пользователе и администрации."""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()
	RATION_DATA_DB = load_ration_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID, USER_NAME, USER_LAST_NAME, MESSAGE_ID."""
		USER_ID = ConfigBot.USERID(message)
		USER_NAME = ConfigBot.USERNAME(message)
		USER_LAST_NAME = ConfigBot.USERLASTNAME(message)
		MESSAGE_ID = ConfigBot.GETMESSAGEID(message)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				"""Разделяем сообщение на ID рациона и остальную информацию."""
				PARTS = ConfigBot.USERMESSAGE(message).split()

				"""Объявляем переменную с выводом куска сообщения для окончанья и начало главного сообщения."""
				START_MESSAGE = f"<a href='https://t.me/{USER_NAME}'>{USER_LAST_NAME}</a>"
				END_MESSAGE = f"Благодарим за вашу активность в <i><b>«{ConfigInlineKeyboard().RATION[2:-2]}»</b></i>."

				if len(PARTS) > 3:
					"""Выводим из первого сообщения - ID Рациона."""
					RATION_ID = PARTS[0]

					if is_ration_in_data(RATION_ID, RATION_DATA_DB):
						await message.answer(f"⚠️ {START_MESSAGE}, извините, но похоже, что рацион с таким <b>ID</b> уже существует в базе данных.\n\n"
						   					 f" • <b>ID Рациона: [ <code>{RATION_ID}</code> ]</b>\n\n"
						   					 "❕Пожалуйста, уточните данные и убедитесь, что вы вводите <b>уникальные  ID</b> для каждого рациона.")
					
					elif not is_ration_in_data(RATION_ID, RATION_DATA_DB):
						"""Удаляем последнее сообщение с информацией о рационе."""
						await ConfigBotAsync.DELETE_MESSAGE_USERS_AND_ADMINS(types = message, message_id = MESSAGE_ID)

						"""Объявляем переменную с выводом Inline клавиатуры для возвращения во вкладку управления рационом."""
						back_menu_ration_admin_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_RATION_MENU

						"""Объявляем переменные для разделения PARTS на аспекты."""
						EMOJI_RATION, NAME_RATION = PARTS[1], " ".join(PARTS[2:])

						"""Сохраняем данные о рационе в базу данных."""
						RATION_DATA_DB[str(RATION_ID)] = {
							"NAME_RATION": NAME_RATION,
							"EMOJI_RATION": EMOJI_RATION,
							"CREATE_TIME_RATION": ConfigBot.GETTIMENOW(),
							"WEEKDAY": {DAYS: {f"DESCRIPTION_{DAYS}": None, "BREAKFAST": None, "BREAKFAST_LINK_RECIPE": None, "LUNCH": None, "LUNCH_LINK_RECIPE": None, "DINNER": None, "DINNER_LINK_RECIPE": None} for DAYS in ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]}
						}
				
						save_ration_data(RATION_DATA_DB)

						await message.answer(f"💬 {START_MESSAGE}, новый <b>рацион добавлен</b> в базу данных.\n\n"
											 f" • <b>ID Рациона:</b> [ <code>{RATION_ID}</code> ]\n"
											 f" • <b>Эмодзи Рациона:</b> [ {EMOJI_RATION} ]\n"
											 f" • <b>Название Рациона:</b> [ <i>{NAME_RATION}</i> ]\n\n"
											 f"{END_MESSAGE}",
											 reply_markup = back_menu_ration_admin_inline_keyboard)

				elif len(PARTS) < 3:
					await message.answer(f"⚠️ {START_MESSAGE}, извините, но для добавления рациона необходимо предоставить <b>полную информацию</b>. Пожалуйста, убедитесь, что вы ввели следующие данные:\n\n"
										  " • <b>Тип Блюда:</b> [ <i>Введите тип блюда: BREAKFAST, LUNCH, DINNER</i> ]\n"
										  " • <b>Ссылка на Рецепт:</b> [ <i>Введите ссылку на рецепт</i> ]\n"
										  " • <b>Название Блюда:</b> [ <i>Введите название блюда</i> ]\n\n"
										  "❕ Пожалуйста, убедитесь, что все поля <b>заполнены</b>, и повторите попытку.")
			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)