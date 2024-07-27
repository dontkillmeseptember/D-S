from data.loader import dp, bot
from data.config import ConfigBot, ConfigBotAsync
from data.config_Keyboard import ConfigInlineKeyboard
from data.loader_keyboard import LoaderInlineKeyboardsAdmin
from data.states_groups import DebugAdminState

from handlers.users.main_menu.update.info_update_func import update_tabs_handler

from database.requests.user_db import load_user_data, is_user_in_data, save_user_data
from database.requests.admin_db import load_admin_data, is_admin_in_data
from database.requests.info_update_db import load_update_data, save_update_data, is_update_in_data

from misc.libraries import types, FSMContext
from misc.loggers import logger

"""Создаем обработчик для управления Обновлениями."""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "UPDATE")
@dp.callback_query_handler(lambda callback_data: callback_data.data == "BACK_UPDATE", state = [DebugAdminState.AddUpdateForAdminState, DebugAdminState.DeleteUpdateForAdminState, DebugAdminState.EditUpdateForAdminState])
async def update_admin_handler(callback_query: types.CallbackQuery, state: FSMContext) -> str:
	"""Объявляем переменные для вывода информации о пользователе и администрации."""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID."""
		USER_ID = ConfigBot.USERID(callback_query)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				CURRENT_STATE = await state.get_state()

				"""Объявляем переменную с выводом клавиатуры для главного меню управления обновлениями."""
				menu_update_admin_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_UPDATEMENU

				INFO_MENU_UPDATE_ADMIN_MESSAGE = f"💬 Добро пожаловать в <b>«{ConfigInlineKeyboard().UPDATE[2:]}»</b>.\n\n" \
												 f"Здесь вы можете легко управлять обновлениями, добавлять их и удалять.\n\n" \
												 f" • <b>{ConfigInlineKeyboard().ADD_UPDATE[2:]}:</b> Используйте эту кнопку для добавление <b>новых</b> обновлений.\n\n" \
												 f" • <b>{ConfigInlineKeyboard().DELETE_UPDATE[:-2]}:</b> При необходимости вы можете <b>удалить</b> выбранные обновления из базы данных.\n\n" \
												 f" • <b>{ConfigInlineKeyboard().EDIT_UPDATE[2:-2]}:</b> Нажмите эту кнопку, чтобы <b>редактировать</b> обновления, которые в данный момент находятся в базе данных.\n\n" \
												 f"Управляйте с легкостью. Ваш комфорт - наша главная задача!"

				if not CURRENT_STATE or CURRENT_STATE.startswith("DebugAdminState:"):
					await bot.edit_message_text(INFO_MENU_UPDATE_ADMIN_MESSAGE,
												callback_query.from_user.id, 
												callback_query.message.message_id,
												reply_markup = menu_update_admin_inline_keyboard)

					"""Сбрасываем текущую фазу у администратора."""
					USER_DATA_DB[str(USER_ID)]["STATES_USER"]["UPDATE_ID"] = None

					save_user_data(USER_DATA_DB)

					await state.finish()

			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик для редактирования обновления."""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "EDIT_UPDATE")
async def edit_update_admin_handler(callback_query: types.CallbackQuery):
	"""Объявляем переменные для вывода информации о пользователе, администрации и обновлениях."""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()
	UPDATE_DATA_DB = load_update_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID."""
		USER_ID = ConfigBot.USERID(callback_query)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				"""Объявляем переменную с выводом клавиатуры для главного меню управления обновлениями."""
				back_update_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_UPDATE_MENU

				await bot.edit_message_text("💬 Для <b>редактирования</b> обновления введите ID, который вы хотели бы отредактировать:\n\n"
											f"{(ConfigBot.GETIDUPDATE(UPDATE_DATA_DB))}\n\n"
											f"Благодарим за вашу активность в <b>«{ConfigInlineKeyboard().UPDATE[2:]}»</b>.",
											callback_query.from_user.id,
											callback_query.message.message_id,
									   		reply_markup = back_update_inline_keyboard)
				
				await DebugAdminState.EditUpdateForAdminState.set()

			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик фазы, где администратор вводит ID обновления для редактирования его из базы данных."""
@dp.message_handler(state = DebugAdminState.EditUpdateForAdminState)
@dp.callback_query_handler(lambda callback_data: callback_data.data == "BACK_EDIT_UPDATE", state = [DebugAdminState.EditDescriptionUpdateForAdminState, DebugAdminState.EditNameUpdateForAdminState, DebugAdminState.EditLinkUpdateForAdminState, DebugAdminState.EditEmojiUpdateForAdminState])
async def edit_update_admin_handler(message_or_callbackQuery: types.Message | types.CallbackQuery) -> DebugAdminState:
	"""Объявляем переменные для вывода информации о пользователе, администрации и обновлениях."""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()
	UPDATE_DATA_DB = load_update_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID."""
		USER_ID = ConfigBot.USERID(message_or_callbackQuery)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				"""Объявляем переменную с выводом клавиатуры для фазы, где вводится ID обновления."""
				edit_menu_update_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEABOARDS_EDIT_MENU_UPDATE

				if isinstance(message_or_callbackQuery, types.Message):
					"""Объявляем переменную с выводом информации о пользователе: USER_MESSAGE"""
					USER_MESSAGE = ConfigBot.USERMESSAGE(message_or_callbackQuery)

					"""Сохраняем ID обновления для редактирования."""
					USER_DATA_DB[str(USER_ID)]["STATES_USER"]["UPDATE_ID"] = USER_MESSAGE

					save_user_data(USER_DATA_DB)

					"""Объявляем переменную с выводом информации о пользователе: USERSTATUSUPDATEID"""
					UPDATE_ID = ConfigBot.USERSTATUSUPDATEID(message_or_callbackQuery)

					"""Объявляем переменную с выводом сообщение о информации обновления."""
					INFO_UPDATE_ADMIN_MESSAGE_ONE = "💬 Краткая информация об обновлении:\n\n" \
													f" • <b>Название обновления:</b> <a href='{ConfigBot.GETUPDATE(UPDATE_ID, 'URL_UPDATE')}'>{ConfigBot.GETUPDATE(UPDATE_ID, 'NAME_UPDATE')}</a>\n\n" \
													f" • <b>Описание обновления:</b> {ConfigBot.GETUPDATE(UPDATE_ID, 'MESSAGE_UPDATE')}\n\n" \
													f" • <b>Дата добавления:</b> {ConfigBot.GETUPDATE(UPDATE_ID, 'DATA_UPDATE')}\n\n" \
													"Для внесения изменений, пожалуйста, выберите нужную кнопку ниже."
					
					if is_update_in_data(USER_MESSAGE, UPDATE_DATA_DB):
						await message_or_callbackQuery.answer(INFO_UPDATE_ADMIN_MESSAGE_ONE, reply_markup = edit_menu_update_inline_keyboard)

						"""Переходим в фазу, где вводят ID обновления для редактирование его из базы данных."""
						await DebugAdminState.EditUpdateForAdminState.set()
					
					elif not is_update_in_data(USER_MESSAGE, UPDATE_DATA_DB):
						await message_or_callbackQuery.answer("⚠️ Извините, но похоже, что обновление с введенным <b>ID</b> отсутствует в базе данных.\n\n"
																"Пожалуйста, убедитесь, что вы ввели корректный <b>ID</b> или проверьте актуальность информации.")
				
				elif isinstance(message_or_callbackQuery, types.CallbackQuery):
					"""Объявляем переменную с выводом информации о пользователе: USERSTATUSUPDATEID"""
					UPDATE_ID = ConfigBot.USERSTATUSUPDATEID(message_or_callbackQuery)

					"""Объявляем переменную с выводом сообщение о информации обновления."""
					INFO_UPDATE_ADMIN_MESSAGE_TWO = "💬 Краткая информация об обновлении:\n\n" \
													f" • <b>Название обновления:</b> <a href='{ConfigBot.GETUPDATE(UPDATE_ID, 'URL_UPDATE')}'>{ConfigBot.GETUPDATE(UPDATE_ID, 'NAME_UPDATE')}</a>\n\n" \
													f" • <b>Описание обновления:</b> {ConfigBot.GETUPDATE(UPDATE_ID, 'MESSAGE_UPDATE')}\n\n" \
													f" • <b>Дата добавления:</b> {ConfigBot.GETUPDATE(UPDATE_ID, 'DATA_UPDATE')}\n\n" \
													"Для внесения изменений, пожалуйста, выберите нужную кнопку ниже."
					
					await bot.edit_message_text(INFO_UPDATE_ADMIN_MESSAGE_TWO,
												message_or_callbackQuery.from_user.id,
												message_or_callbackQuery.message.message_id,
												reply_markup = edit_menu_update_inline_keyboard)
					
					"""Переходим в фазу, где вводят ID обновления для редактирование его из базы данных."""
					await DebugAdminState.EditUpdateForAdminState.set()
				
				else:
					logger.error("⚠️ Произошла непредвиденная ошибка с проверкой isinstance: %s", isinstance)
			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик для редактирования описания, названия, ссылки и эмодзи для обновления в базе данных."""
@dp.callback_query_handler(lambda callback_data: callback_data.data and callback_data.data.startswith("EDIT_"), state = DebugAdminState.EditUpdateForAdminState)
async def edit_all_update_admin_handler(callback_query: types.CallbackQuery):
	"""Объявляем переменные для вывода информации о пользователе, администрации и обновлениях."""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID."""
		USER_ID = ConfigBot.USERID(callback_query)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				"""Объявляем переменную с выводом inline клавиатуры для возвращения в фазу редактирования."""
				back_edit_update_menu_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_EDIT_UPDATE_MENU

				"""Объявляем переменную с выводом куска сообщения для окончанья главного сообщения."""
				END_MESSAGE = f"Благодарим за вашу активность в <b>«{ConfigInlineKeyboard().UPDATE[2:]}»</b>."

				if callback_query.data == "EDIT_MESSAGE_UPDATE":
					"""Объявляем переменную с выводом сообщение о информации редактирования описания."""
					EDIT_UPDATE_ADMIN_MESSAGE = "💬 Введите, пожалуйста, нужное описание для изменения текущего описания обновления.\n\n" \
												f"{END_MESSAGE}"
					
					"""Объявляем переменную с фазой, где администратор вводит новое описание для обновления."""
					await DebugAdminState.EditDescriptionUpdateForAdminState.set()

				elif callback_query.data == "EDIT_NAME_UPDATE":
					"""Объявляем переменную с выводом сообщение о информации редактирования названия."""
					EDIT_UPDATE_ADMIN_MESSAGE = "💬 Введите, пожалуйста, новое название для изменения текущего названия обновления.\n\n" \
												f"{END_MESSAGE}"
					
					"""Объявляем переменную с фазой, где администратор вводит новое название для обновления."""
					await DebugAdminState.EditNameUpdateForAdminState.set()

				elif callback_query.data == "EDIT_LINK_UPDATE":
					"""Объявляем переменную с выводом сообщение о информации редактирования ссылки."""
					EDIT_UPDATE_ADMIN_MESSAGE = "💬 Введите, пожалуйста, новую ссылку для изменения текущей ссылки на описание обновления.\n\n" \
												f"{END_MESSAGE}"
					
					"""Объявляем переменную с фазой, где администратор вводит новую ссылку для обновления."""
					await DebugAdminState.EditLinkUpdateForAdminState.set()

				elif callback_query.data == "EDIT_EMOJI_UPDATE":
					"""Объявляем переменную с выводом сообщение о информации редактирования эмодзи."""
					EDIT_UPDATE_ADMIN_MESSAGE = "💬 Введите, пожалуйста, новую эмодзи для изменения текущей эмодзи обновления.\n\n" \
												f"{END_MESSAGE}"
					
					"""Объявляем переменную с фазой, где администратор вводит новую эмодзи для обновления."""
					await DebugAdminState.EditEmojiUpdateForAdminState.set()
				
				await bot.edit_message_text(EDIT_UPDATE_ADMIN_MESSAGE,
											callback_query.from_user.id,
											callback_query.message.message_id,
									   		reply_markup = back_edit_update_menu_inline_keyboard)

			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик всех фаз, где администратор редактирует обновления."""
@dp.message_handler(state = [DebugAdminState.EditDescriptionUpdateForAdminState, DebugAdminState.EditNameUpdateForAdminState, DebugAdminState.EditLinkUpdateForAdminState, DebugAdminState.EditEmojiUpdateForAdminState])
async def item_edit_all_update_admin_handler(message: types.Message, state: FSMContext):
	"""Объявляем переменные для вывода информации о пользователе, администрации и обновлениях."""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()
	UPDATE_DATA_DB = load_update_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID."""
		USER_ID = ConfigBot.USERID(message)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				"""Объявляем переменную с выводом inline клавиатуры для возвращения в фазу редактирования."""
				back_edit_update_menu_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_EDIT_UPDATE_MENU

				"""Объявляем переменную с выводом информации о пользователе: USERSTATUSUPDATEID, USER_MESSAGE"""
				UPDATE_ID = ConfigBot.USERSTATUSUPDATEID(message)
				USER_MESSAGE = ConfigBot.USERMESSAGE(message)

				"""Объявляем переменную с выводом куска сообщения для окончанья главного сообщения."""
				END_MESSAGE = f"Благодарим за вашу активность в <b>«{ConfigInlineKeyboard().UPDATE[2:]}»</b>."

				"""Объявляем переменную, где выводим текущую фазу пользователя."""
				CURRENT_STATE = await state.get_state()

				if CURRENT_STATE == "DebugAdminState:EditDescriptionUpdateForAdminState":
					"""Объявляем переменную с выводом сообщение о информации редактирования описания."""
					EDIT_END_ADMIN_MESSAGE = "💬 Описание для обновления успешно изменено.\n\n" \
											f" • <b>Новое описание для обновления:</b> {USER_MESSAGE}\n\n" \
											f"{END_MESSAGE}"

					"""Объявляем функцию для сохранения описания обновления."""
					UPDATE_DATA_DB[UPDATE_ID]["MESSAGE_UPDATE"] = USER_MESSAGE

				elif CURRENT_STATE == "DebugAdminState:EditNameUpdateForAdminState":
					"""Объявляем переменную с выводом сообщение о информации редактирования названия."""
					EDIT_END_ADMIN_MESSAGE = "💬 Название для обновления успешно изменено.\n\n" \
											f" • <b>Новое название для обновления:</b> {USER_MESSAGE}\n\n" \
											f"{END_MESSAGE}"

					"""Объявляем функцию для сохранения названия обновления."""
					UPDATE_DATA_DB[UPDATE_ID]["NAME_UPDATE"] = USER_MESSAGE

				elif CURRENT_STATE == "DebugAdminState:EditLinkUpdateForAdminState":
					"""Объявляем переменную с выводом сообщение о информации редактирования ссылки."""
					EDIT_END_ADMIN_MESSAGE = "💬 Ссылка на описание для обновления успешно изменено.\n\n" \
											f" • <b>Новая ссылка на описание:</b> <a href='{USER_MESSAGE}'>Ссылка на описание</a>\n\n" \
											f"{END_MESSAGE}"

					"""Объявляем функцию для сохранения ссылки обновления."""
					UPDATE_DATA_DB[UPDATE_ID]["URL_UPDATE"] = USER_MESSAGE

				elif CURRENT_STATE == "DebugAdminState:EditEmojiUpdateForAdminState":
					"""Объявляем переменную с выводом сообщение о информации редактирования эмодзи."""
					EDIT_END_ADMIN_MESSAGE = "💬 Эмодзи для обновления успешно изменено.\n\n" \
											f" • <b>Новое эмодзи для обновления:</b> {USER_MESSAGE}\n\n" \
											f"{END_MESSAGE}"
					
					"""Объявляем функцию для сохранения эмодзи обновления."""
					UPDATE_DATA_DB[UPDATE_ID]["EMODJI_UPDATE"] = USER_MESSAGE

				save_update_data(UPDATE_DATA_DB)

				"""Вызываем функцию для перезагрузки обработчиков."""
				await ConfigBotAsync.RELOAD_HANDLERS_FOR_UPDATE(database_update = UPDATE_DATA_DB, handler = update_tabs_handler)

				await message.answer(EDIT_END_ADMIN_MESSAGE,
									reply_markup = back_edit_update_menu_inline_keyboard)
			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик для удаления обновлений из бота."""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "DELETE_UPDATE")
async def delete_update_admin_handler(callback_query: types.CallbackQuery):
	"""Объявляем переменные для вывода информации о пользователе, администрации и обновлениях."""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()
	UPDATE_DATA_DB = load_update_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID."""
		USER_ID = ConfigBot.USERID(callback_query)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				"""Выводим клавиатуры для обработчика кнопки назад"""
				back_update_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_UPDATE_MENU

				await bot.edit_message_text("💬 Для <b>удаления</b> обновления введите ID, который вы хотели бы удалить:\n\n"
											f"{(ConfigBot.GETIDUPDATE(UPDATE_DATA_DB))}\n\n"
											f"Благодарим за вашу активность в <b>«{ConfigInlineKeyboard().UPDATE[2:]}»</b>.",
											callback_query.from_user.id,
											callback_query.message.message_id,
									   		reply_markup = back_update_inline_keyboard)
				
				"""Переходим в фазу, где вводят ID обновления, чтобы удалить его из базы данных."""
				await DebugAdminState.DeleteUpdateForAdminState.set()

			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик фазы, где вводят ID обновления, чтобы удалить его из базы данных."""
@dp.message_handler(state = DebugAdminState.DeleteUpdateForAdminState)
async def delete_update_admin_state(message: types.Message):
	"""Объявляем переменные для вывода информации о пользователе, администрации и обновлениях."""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()
	UPDATE_DATA_DB = load_update_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID, USER_MESSAGE."""
		USER_ID = ConfigBot.USERID(message)
		USER_MESSAGE = ConfigBot.USERMESSAGE(message)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				if is_update_in_data(USER_MESSAGE, UPDATE_DATA_DB):
					"""Удаляем обновление из базы данных."""
					del UPDATE_DATA_DB[str(USER_MESSAGE)]

					save_update_data(UPDATE_DATA_DB)

					"""Выводим клавиатуры для обработчика кнопки назад"""
					back_update_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_UPDATE_MENU

					"""Вызываем функцию для перезагрузки обработчиков."""
					await ConfigBotAsync.RELOAD_HANDLERS_FOR_UPDATE(database_update = UPDATE_DATA_DB, handler = update_tabs_handler)

					await message.answer(f"💬 Отлично, обновление с ID <code>{ConfigBot.USERMESSAGE(message)}</code> успешно удален из базы данных.\n\n"
						  				 f"Благодарим за вашу активность в <b>«{ConfigInlineKeyboard().UPDATE[2:]}»</b>.",
										 reply_markup = back_update_inline_keyboard)
				else:
					await message.answer("⚠️ Извините, но похоже, что <b>обновление</b> с указанным <b>ID</b> не существует в базе данных.\n\n"
						  				 "Убедитесь, что вы ввели правильный ID, и повторите попытку.")
			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик для добавления обновлений на бота."""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "ADD_UPDATE")
async def add_update_admin_handler(callback_query: types.CallbackQuery):
	"""Объявляем переменные для вывода информации о пользователе, администрации и обновлениях."""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID."""
		USER_ID = ConfigBot.USERID(callback_query)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				"""Выводим клавиатуры для обработчика кнопки назад"""
				back_update_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_UPDATE_MENU

				await bot.edit_message_text("💬 Для <b>добавления</b> нового обновления, введите следующую информацию:\n\n"
						   			   		" • <b>ID Обновления:</b> [Введите ID Обновления]\n"
											" • <b>URL Ссылка на сайт:</b> [Укажите URL ссылку на обновление]\n"
											" • <b>Эмодзи обновления:</b> [Введите эмодзи]\n"
											" • <b>Название обновления:</b> [Введите название обновления]\n"
											" • <b>Сообщение к обновлению:</b> [Добавьте свое сообщение]\n\n"
											f"Благодарим за вашу активность в <b>«{ConfigInlineKeyboard().UPDATE[2:]}»</b>.",
											callback_query.from_user.id,
											callback_query.message.message_id,
									   		reply_markup = back_update_inline_keyboard)

				"""Переходим в фазу, где вводят обновление для добавления."""
				await DebugAdminState.AddUpdateForAdminState.set()

			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик фазы, где администратор вводит ID обновления и остальную информацию."""
@dp.message_handler(state = DebugAdminState.AddUpdateForAdminState)
async def item_add_update_admin_handler(message: types.Message):
	"""Объявляем переменные для вывода информации о пользователе, администрации и обновлениях."""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()
	UPDATE_DATA_DB = load_update_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID."""
		USER_ID = ConfigBot.USERID(message)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				"""Разделяем сообщение на ID обновления и остальную информацию."""
				PARTS = ConfigBot.USERMESSAGE(message).split()

				if len(PARTS) > 5:
					"""Выводим из сообщения - Артикул"""
					ID_UPDATE = PARTS[0]

					if is_update_in_data(ID_UPDATE, UPDATE_DATA_DB):
						await message.answer("⚠️ Извините, но похоже, что обновление с таким <b>ID</b> уже существует в базе данных.\n\n"
						   					 "Пожалуйста, уточните данные и убедитесь, что вы вводите <b>уникальные</b> ID для каждого обновления.")

					elif not is_update_in_data(ID_UPDATE, UPDATE_DATA_DB):
						"""Объявляем переменные для разделения PARTS на аспекты."""
						URL_SITE, EMODJI_UPDATE, NAME_UPDATE, MESSAGE = PARTS[1], PARTS[2], " ".join(PARTS[3:6]), " ".join(PARTS[6:])

						"""Сохраняем данные о товаре в базе данных товарах"""
						UPDATE_DATA_DB[str(ID_UPDATE)] = {
							"URL_UPDATE": URL_SITE,
							"EMODJI_UPDATE": EMODJI_UPDATE,
							"NAME_UPDATE": NAME_UPDATE,
							"MESSAGE_UPDATE": MESSAGE,
							"DATA_UPDATE": ConfigBot.GETTIMENOW()
						}

						save_update_data(UPDATE_DATA_DB)

						"""Выводим клавиатуры для обработчика кнопки назад"""
						back_update_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_UPDATE_MENU

						"""Вызываем функцию для перезагрузки обработчиков."""
						await ConfigBotAsync.RELOAD_HANDLERS_FOR_UPDATE(database_update = UPDATE_DATA_DB, handler = update_tabs_handler)

						await message.answer(f"💬 Данные обновления добавлены в <b>«{ConfigInlineKeyboard().UPDATE[2:]}»</b>.\n\n"
						   			   		 f" • <b>ID Обновления:</b> <code>{ID_UPDATE}</code>\n"
											 f" • <b>URL Ссылка на сайт:</b> <a href='{URL_SITE}'><b>Ссылка на сайт</b></a>\n"
											 f" • <b>Эмодзи обновления:</b> {EMODJI_UPDATE}\n"
											 f" • <b>Название обновления:</b> {NAME_UPDATE}\n"
											 f" • <b>Сообщение к обновлению:</b> {MESSAGE}\n\n"
											 f"Благодарим за вашу активность в <b>«{ConfigInlineKeyboard().UPDATE[2:]}»</b>.",
											 reply_markup = back_update_inline_keyboard)

				elif len(PARTS) < 5:
					await message.answer("⚠️ Извините, но для добавления обновления необходимо предоставить <b>полную</b> информацию. Пожалуйста, убедитесь, что вы ввели следующие данные:\n\n"
						   			   	 " • <b>ID Обновления:</b> [Введите ID Обновления]\n"
										 " • <b>URL Ссылка на сайт:</b> [Укажите URL ссылку на обновление]\n"
										 " • <b>Эмодзи обновления:</b> [Введите эмодзи]\n"
										 " • <b>Название обновления:</b> [Введите название обновления]\n"
										 " • <b>Сообщение к обновлению:</b> [Добавьте свое сообщение]\n\n"
										 "Пожалуйста, убедитесь, что все поля <b>заполнены</b>, и повторите попытку.")
			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)