from data.loader import dp, bot
from data.config import ConfigBot
from data.config_Keyboard import ConfigInlineKeyboard
from data.loader_keyboard import LoaderInlineKeyboardsAdmin
from data.states_groups import DebugAdminState

from database.requests.user_db import load_user_data, is_user_in_data, save_user_data
from database.requests.admin_db import load_admin_data, is_admin_in_data
from database.requests.sport_db import load_sport_data, save_sport_data, is_sport_in_data

from misc.libraries import types, FSMContext
from misc.loggers import logger

"""Создаем обработчик для управления Кодексом Силы."""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "SPORT")
@dp.callback_query_handler(lambda callback_data: callback_data.data == "BACK_SPORT", state = [DebugAdminState.AddSportForAdminState, DebugAdminState.DeleteSportForAdminState, DebugAdminState.EditSportForAdminState])
async def sport_admin_handler(callback_query: types.CallbackQuery, state: FSMContext) -> str:
	"""Объявляем переменные для вывода информации о пользователе и администрации."""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID."""
		USER_ID = ConfigBot.USERID(callback_query)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				CURRENT_STATE = await state.get_state()

				"""Объявляем переменную с выводом клавиатуры для главного меню управления кодексом силы."""
				menu_sport_admin_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_SPORT_MENU

				INFO_MENU_SPORT_ADMIN_MESSAGE = f"💬 Добро пожаловать в <b>«{ConfigInlineKeyboard().SPORT[2:]}»</b>.\n\n" \
												f"Здесь вы можете легко управлять упражнениями, добавлять их и удалять.\n\n" \
												f" • <b>{ConfigInlineKeyboard().ADD_SPORT[2:]}:</b> Используйте эту кнопку для добавление <b>новых</b> упражнений.\n\n" \
												f" • <b>{ConfigInlineKeyboard().DELETE_SPORT[:-2]}:</b> При необходимости вы можете <b>удалить</b> выбранные упражнения из базы данных.\n\n" \
												f" • <b>{ConfigInlineKeyboard().EDIT_SPORT[2:-2]}:</b> Нажмите эту кнопку, чтобы <b>редактировать</b> упражнения, которые в данный момент находятся в базе данных.\n\n" \
												f"Управляйте с легкостью. Ваш комфорт - наша главная задача!"

				if not CURRENT_STATE or CURRENT_STATE.startswith("DebugAdminState:"):
					await bot.edit_message_text(INFO_MENU_SPORT_ADMIN_MESSAGE,
												callback_query.from_user.id, 
												callback_query.message.message_id,
												reply_markup = menu_sport_admin_inline_keyboard)
					
					"""Сбрасываем текущую фазу у администратора."""
					USER_DATA_DB[str(ConfigBot.USERID(callback_query))]["STATES_USER"]["SPORT_ID"] = None

					save_user_data(USER_DATA_DB)

					await state.finish()
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик для изменение упражнений."""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "EDIT_SPORT")
async def edit_sport_handler(callback_query: types.CallbackQuery) -> DebugAdminState:
	"""Объявляем переменные с выводом информации о пользователе, администрации и упражнениях."""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()
	SPORT_DATA_DB = load_sport_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID"""
		USER_ID = ConfigBot.USERID(callback_query)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				"""Выводим клавиатуры для обработчика кнопки назад"""
				back_sport_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_SPORT_MENU

				await bot.edit_message_text("💬 Для <b>редактирования</b> упражнения из базы данных, введите, пожалуйста, <b>ID</b> упражнения из списка.\n\n"
										   f"{(ConfigBot.GETIDSPORT(SPORT_DATA_DB))}\n\n"
										   f"Благодарим за вашу активность в <b>«{ConfigInlineKeyboard().SPORT[2:]}»</b>.",
											callback_query.from_user.id,
											callback_query.message.message_id,
											reply_markup = back_sport_inline_keyboard)
				
				"""Переходим в фазу, где вводят ID упражнения для редактирование его из базы данных."""
				await DebugAdminState.EditSportForAdminState.set()

			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик фазы, где администратор вводит ID упражнения для редактирования его из базы данных."""
@dp.message_handler(state = DebugAdminState.EditSportForAdminState)
@dp.callback_query_handler(lambda callback_data: callback_data.data == "BACK_EDIT_SPORT", state = [DebugAdminState.EditDescriptionSportForAdminState, DebugAdminState.AddWorkoutForAdminState, DebugAdminState.DeleteWorkoutForAdminState])
async def edit_sport_admin_handler(message_or_callbackQuery: types.Message | types.CallbackQuery) -> DebugAdminState:
	"""Объявляем переменные с выводом информации о пользователе, администрации и упражнениях."""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()
	SPORT_DATA_DB = load_sport_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID"""
		USER_ID = ConfigBot.USERID(message_or_callbackQuery)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				"""Объявляем переменную с выводом клавиатуры для фазы, где вводится ID упражнения."""
				edit_menu_sport_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_EDIT_MENU_SPORT

				if isinstance(message_or_callbackQuery, types.Message):
					"""Объявляем переменную с выводом информации о пользователе: USER_MESSAGE"""
					USER_MESSAGE = ConfigBot.USERMESSAGE(message_or_callbackQuery)

					"""Сохраняем ID упражнения для редактирования."""
					USER_DATA_DB[str(ConfigBot.USERID(message_or_callbackQuery))]["STATES_USER"]["SPORT_ID"] = USER_MESSAGE

					save_user_data(USER_DATA_DB)

					"""Объявляем переменную с выводом информации о пользователе: USER_STATUSSPORTID"""
					SPORT_ID = ConfigBot.USERSTATUSSPORTID(message_or_callbackQuery)

					COUNT_WORKOUT = ConfigBot.GETLENUSERS(SPORT_DATA_DB[SPORT_ID]["WORKOUTS"])

					"""Объявляем переменную с выводом сообщение о информации упражнения."""
					INFO_SPORT_ADMIN_MESSAGE_ONE = "💬 Краткая информация об упражнении:\n\n" \
											  f" • <b>Название упражнения:</b> {ConfigBot.GETSPORT(USER_MESSAGE, 'NAME_SPORT')[2:]}\n\n" \
											  f" • <b>Описание упражнения:</b> {ConfigBot.GETSPORT(USER_MESSAGE, 'MESSAGE_SPORT')[2:]}\n\n" \
											  f" • <b>Количество тренировок:</b> {COUNT_WORKOUT}\n\n" \
											  f" • <b>Дата добавления:</b> {ConfigBot.GETSPORT(USER_MESSAGE, 'DATA_SPORT')}\n\n" \
											  "Для внесения изменений, пожалуйста, выберите нужную кнопку ниже."

					if is_sport_in_data(USER_MESSAGE, SPORT_DATA_DB):
						await message_or_callbackQuery.answer(INFO_SPORT_ADMIN_MESSAGE_ONE, reply_markup = edit_menu_sport_inline_keyboard)

						"""Переходим в фазу, где вводят ID упражнения для редактирование его из базы данных."""
						await DebugAdminState.EditSportForAdminState.set()

					elif not is_sport_in_data(USER_MESSAGE, SPORT_DATA_DB):
						await message_or_callbackQuery.answer("⚠️ Извините, но похоже, что упражнение с введенным <b>ID</b> отсутствует в базе данных.\n\n"
																"Пожалуйста, убедитесь, что вы ввели корректный <b>ID</b> или проверьте актуальность информации.")
				
				elif isinstance(message_or_callbackQuery, types.CallbackQuery):
					"""Объявляем переменную с выводом информации о пользователе: USER_STATUSSPORTID"""
					SPORT_ID = ConfigBot.USERSTATUSSPORTID(message_or_callbackQuery)

					COUNT_WORKOUT = ConfigBot.GETLENUSERS(SPORT_DATA_DB[SPORT_ID]["WORKOUTS"])

					"""Объявляем переменную с выводом сообщение о информации упражнения."""
					INFO_SPORT_ADMIN_MESSAGE_TWO = "💬 Краткая информация об упражнении.\n\n" \
											  f" • <b>Название упражнения:</b> {ConfigBot.GETSPORT(SPORT_ID, 'NAME_SPORT')[2:]}\n\n" \
											  f" • <b>Описание упражнения:</b> {ConfigBot.GETSPORT(SPORT_ID, 'MESSAGE_SPORT')[2:]}\n\n" \
											  f" • <b>Количество тренировок:</b> {COUNT_WORKOUT}\n\n" \
											  f" • <b>Дата добавления:</b> {ConfigBot.GETSPORT(SPORT_ID, 'DATA_SPORT')}\n\n" \
											  "Для внесения изменений, пожалуйста, выберите нужную кнопку ниже."

					await bot.edit_message_text(INFO_SPORT_ADMIN_MESSAGE_TWO,
												message_or_callbackQuery.from_user.id,
												message_or_callbackQuery.message.message_id,
												reply_markup = edit_menu_sport_inline_keyboard)

					"""Переходим в фазу, где вводят ID упражнения для редактирование его из базы данных."""
					await DebugAdminState.EditSportForAdminState.set()
				
				else:
					logger.error("⚠️ Произошла непредвиденная ошибка с проверкой isinstance: %s", isinstance)
			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))

	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик для удаления тренировок из упражнения."""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "DELETE_WORKOUT", state = DebugAdminState.EditSportForAdminState)
async def delete_sport_workout_admin_handler(callback_query: types.CallbackQuery):
	"""Объявляем переменные для вывода информации о пользователе, администрации и обновлениях."""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()
	SPORT_DATA_DB = load_sport_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID"""
		USER_ID = ConfigBot.USERID(callback_query)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				"""Объявляем переменную с выводом inline клавиатуры для возвращения в фазу редактирования."""
				back_edit_sport_menu_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_EDIT_SPORT_MENU

				await bot.edit_message_text("💬 Введите, пожалуйста, нужное ID тренировки для удаления его из базы данных.\n\n"
											f"{ConfigBot.GETIDWORKOUTS(SPORT_DATA_DB)}\n\n"
											f"Благодарим за вашу активность в <b>«{ConfigInlineKeyboard().SPORT[2:]}»</b>.",
											callback_query.from_user.id,
											callback_query.message.message_id,
									   		reply_markup = back_edit_sport_menu_inline_keyboard)
				
				"""Переход в фазу, где администратор вводит ID тренировки и удаляет ее из базы данных."""
				await DebugAdminState.DeleteWorkoutForAdminState.set()

			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик фазы, гдее администратор вводит ID тренировки для удаления ее из базы данных."""
@dp.message_handler(state = DebugAdminState.DeleteWorkoutForAdminState)
async def item_delete_sport_workout_admin_state(message: types.Message):
	"""Объявляем переменные для вывода информации о пользователе, администрации и обновлениях."""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()
	SPORT_DATA_DB = load_sport_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID, USER_MESSAGE"""
		USER_ID = ConfigBot.USERID(message)
		USER_MESSAGE = ConfigBot.USERMESSAGE(message)
		SPORT_ID = ConfigBot.USERSTATUSSPORTID(message)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				if is_sport_in_data(USER_MESSAGE, SPORT_DATA_DB[SPORT_ID]['WORKOUTS']):
					"""Удаляем тренировку из базы данных."""
					del SPORT_DATA_DB[SPORT_ID]['WORKOUTS'][USER_MESSAGE]

					save_sport_data(SPORT_DATA_DB)

					"""Объявляем переменную с выводом inline клавиатуры для возвращения в фазу редактирования."""
					back_edit_sport_menu_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_EDIT_SPORT_MENU

					await message.answer(f"💬 Отлично, тренировка с ID [<code>{ConfigBot.USERMESSAGE(message)}</code>] успешно удалено из базы данных.\n\n"
						  				 f"Благодарим за вашу активность в <b>«{ConfigInlineKeyboard().SPORT[2:]}»</b>.",
										 reply_markup = back_edit_sport_menu_inline_keyboard)
				else:
					await message.answer("⚠️ Извините, но похоже, что <b>тренировка</b> с указанным <b>ID</b> не существует в базе данных.\n\n"
						  				 "Убедитесь, что вы ввели правильный ID, и повторите попытку.")
			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик для добавления новых тренировок в упражнение."""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "ADD_WORKOUT", state = DebugAdminState.EditSportForAdminState)
async def add_sport_workout_admin_handler(callback_query: types.CallbackQuery):
	"""Объявляем переменные для вывода информации о пользователе, администрации и обновлениях."""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID"""
		USER_ID = ConfigBot.USERID(callback_query)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				"""Объявляем переменную с выводом inline клавиатуры для возвращения в фазу редактирования."""
				back_edit_sport_menu_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_EDIT_SPORT_MENU

				await bot.edit_message_text("💬 Для <b>добавления</b> новой тренировки, введите следующую информацию:\n\n"
											" • <b>ID тренировки:</b> [Добавьте ID тренировки]\n"
											" • <b>Эмодзи тренировки:</b> [Добавьте соответствующий эмодзи]\n"
											" • <b>Название тренировки:</b> [Добавьте название тренировки]\n"
											" • <b>Условия тренировки:</b> [Опишите условия выполнения]\n\n"
											f"Благодарим за вашу активность в <b>«{ConfigInlineKeyboard().SPORT[2:]}»</b>.",
											callback_query.from_user.id,
											callback_query.message.message_id,
									   		reply_markup = back_edit_sport_menu_inline_keyboard)

				"""Переходим в фазу, где вводят новые тренировки в упражнение."""
				await DebugAdminState.AddWorkoutForAdminState.set()

			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик фазы, где администратор вводит данные о новой тренировки для добавления ее в упражнение."""
@dp.message_handler(state = DebugAdminState.AddWorkoutForAdminState)
async def item_add_sport_workout_admin_handler(message: types.Message):
	"""Объявляем переменные для вывода информации о пользователе, администрации и обновлениях."""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()
	SPORT_DATA_DB = load_sport_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID"""
		USER_ID = ConfigBot.USERID(message)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				"""Разделяем сообщение на ID обновления и остальную информацию."""
				PARTS = ConfigBot.USERMESSAGE(message).split()

				"""Объявляем переменную с выводом информации о пользователе: USER_STATUSSPORTID"""
				SPORT_ID = ConfigBot.USERSTATUSSPORTID(message)

				if len(PARTS) > 3:
					"""Объявляем переменные для разделения PARTS на аспекты."""
					WORKOUT_ID, EMODJI_WORKOUT, NAME_WORKOUT, TERN_WORKOUT = PARTS[0], PARTS[1], " ".join(PARTS[2:3]), " ".join(PARTS[3:])

					"""Сохраняем данные о тренировки в базе данных упражнениях."""
					SPORT_DATA_DB[SPORT_ID]["WORKOUTS"][f"WORKOUT_{WORKOUT_ID}"] = {
						"EMODJI_WORKOUT": EMODJI_WORKOUT,
						"NAME_WORKOUT": NAME_WORKOUT,
						"TERN_WORKOUT": TERN_WORKOUT
					}

					save_sport_data(SPORT_DATA_DB)

					"""Объявляем переменную с выводом inline клавиатуры для возвращения в фазу редактирования."""
					back_edit_sport_menu_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_EDIT_SPORT_MENU

					await message.answer(f"💬 Новая тренировка добавлена в <b>«{ConfigBot.GETSPORT(SPORT_ID, 'NAME_SPORT')[2:]}»</b>.\n\n"
										 f" • <b>ID тренировки:</b> {WORKOUT_ID}\n"
										 f" • <b>Эмодзи тренировки:</b> {EMODJI_WORKOUT}\n"
										 f" • <b>Название тренировки:</b> {NAME_WORKOUT}\n"
										 f" • <b>Условия тренировки:</b> {TERN_WORKOUT}\n\n"
										 f"Благодарим за вашу активность в <b>«{ConfigInlineKeyboard().SPORT[2:]}»</b>.",
										 reply_markup = back_edit_sport_menu_inline_keyboard)

				elif len(PARTS) < 3:
					await message.answer("⚠️ Извините, но для добавления тренировки необходимо предоставить <b>полную</b> информацию. Пожалуйста, убедитесь, что вы ввели следующие данные:\n\n"
										 " • <b>ID тренировки:</b> [Добавьте ID тренировки]\n"
										 " • <b>Эмодзи тренировки:</b> [Добавьте соответствующий эмодзи]\n"
										 " • <b>Название тренировки:</b> [Добавьте название тренировки]\n"
										 " • <b>Условия тренировки:</b> [Опишите условия выполнения]\n\n"
										 "Пожалуйста, убедитесь, что все поля <b>заполнены</b>, и повторите попытку.")
			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик для редактирования описание упражнения."""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "EDIT_SPORT_DESCRIPTION", state = DebugAdminState.EditSportForAdminState)
async def edit_sport_description_admin_handler(callback_query: types.CallbackQuery):
	"""Объявляем переменные для вывода информации о пользователе, администрации и обновлениях."""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID"""
		USER_ID = ConfigBot.USERID(callback_query)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				"""Объявляем переменную с выводом inline клавиатуры для возвращения в фазу редактирования."""
				back_edit_sport_menu_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_EDIT_SPORT_MENU

				await bot.edit_message_text("💬 Введите, пожалуйста, нужное описание для изменения текущего описания упражнения.\n\n"
										   f"Благодарим за вашу активность в <b>«{ConfigInlineKeyboard().SPORT[2:]}»</b>.",
											callback_query.from_user.id,
											callback_query.message.message_id,
											reply_markup = back_edit_sport_menu_inline_keyboard)
				
				"""Переходим в фазу, где вводят новое описание упражнения и сохраняем его в базе данных."""
				await DebugAdminState.EditDescriptionSportForAdminState.set()
			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик фазы, где администратор вводит новое описание упражнения."""
@dp.message_handler(state = DebugAdminState.EditDescriptionSportForAdminState)
async def item_edit_sport_description_admin_handler(message: types.Message) -> DebugAdminState:
	"""Объявляем переменные для вывода информации о пользователе, администрации и спорте."""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()
	SPORT_DATA_DB = load_sport_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID"""
		USER_ID = ConfigBot.USERID(message)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				"""Объявляем переменную с выводом inline клавиатуры для возвращения в фазу редактирования."""
				back_edit_sport_menu_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_EDIT_SPORT_MENU

				"""Объявляем переменную с выводом информации о пользователе: USER_STATUSSPORTID, USER_MESSAGE"""
				SPORT_ID = ConfigBot.USERSTATUSSPORTID(message)
				USER_MESSAGE = ConfigBot.USERMESSAGE(message)

				"""Сохраняем новое описание упражнения в базе данных."""
				SPORT_DATA_DB[SPORT_ID]["MESSAGE_SPORT"] = f"{USER_MESSAGE}"

				save_sport_data(SPORT_DATA_DB)

				await message.answer("💬 Описание для упражнения успешно изменено.\n\n"
						 			f" • <b>Новое описание для упражнения:</b> {USER_MESSAGE}\n\n"
						 			f"Благодарим за вашу активность в <b>«{ConfigInlineKeyboard().SPORT[2:]}»</b>.",
									reply_markup = back_edit_sport_menu_inline_keyboard)

			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик для добавление новых упражнений."""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "ADD_SPORT")
async def add_sport_admin_handler(callback_query: types.CallbackQuery):
	"""Объявляем переменные для вывода информации о пользователе, администрации и обновлениях."""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID."""
		USER_ID = ConfigBot.USERID(callback_query)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				"""Объявляем переменную с выводом inline клавиатуры для возвращения."""
				back_sport_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_SPORT_MENU

				await bot.edit_message_text("💬 Для <b>добавления</b> нового упражнения, введите следующую информацию:\n\n"
						   			   		" • <b>ID Упражнения:</b> [Введите ID Упражнения]\n"
											" • <b>Эмодзи упражнения:</b> [Введите эмодзи]\n"
											" • <b>Название callback_query:</b> [Введите название callback_query]\n"
											" • <b>Название упражнения:</b> [Введите название упражнения]\n"
											" • <b>Описание к упражнению:</b> [Добавьте описание]\n\n"
											f"Благодарим за вашу активность в <b>«{ConfigInlineKeyboard().SPORT[2:]}»</b>.",
											callback_query.from_user.id,
											callback_query.message.message_id,
									   		reply_markup = back_sport_inline_keyboard)

				"""Переходим в фазу, где администрация вводят информацию о новом упражнении."""
				await DebugAdminState.AddSportForAdminState.set()

			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик фазы, где администратор вводит ID упражнения и остальную информацию."""
@dp.message_handler(state = DebugAdminState.AddSportForAdminState)
async def item_add_sport_admin_handler(message: types.Message) -> str:
	"""Объявляем переменные для вывода информации о пользователе, администрации и упражнениях."""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()
	SPORT_DATA_DB = load_sport_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID."""
		USER_ID = ConfigBot.USERID(message)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				"""Разделяем сообщение на ID упражнения и остальную информацию."""
				PARTS = ConfigBot.USERMESSAGE(message).split()

				if len(PARTS) > 5:
					"""Выводим из сообщения - ID Упражнения."""
					ID_SPORT = PARTS[0]

					if is_sport_in_data(ID_SPORT, SPORT_DATA_DB):
						await message.answer("⚠️ Извините, но похоже, что упражнение с таким <b>ID</b> уже существует в базе данных.\n\n"
						   					 "Пожалуйста, уточните данные и убедитесь, что вы вводите <b>уникальные</b> ID для каждого упражнения.")

					elif not is_sport_in_data(ID_SPORT, SPORT_DATA_DB):
						"""Объявляем переменные для разделения PARTS на аспекты."""
						EMODJI_SPORT, CALLBACK_DATA_SPORT, NAME_SPORT, MESSAGE = PARTS[1], PARTS[2], " ".join(PARTS[3:6]), " ".join(PARTS[6:])

						"""Сохраняем данные о упражнение в базе данных."""
						SPORT_DATA_DB[str(ID_SPORT)] = {
							"EMODJI_SPORT": EMODJI_SPORT,
							"CALLBACK_DATA_SPORT": f"sport:{CALLBACK_DATA_SPORT}",
							"NAME_SPORT": NAME_SPORT,
							"MESSAGE_SPORT": f"{MESSAGE}",
							"DATA_SPORT": ConfigBot.GETTIMENOW(),
							"WORKOUTS": {

							}
						}

						save_sport_data(SPORT_DATA_DB)

						"""Объявляем переменную с выводом inline клавиатуры для возвращения."""
						back_sport_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_SPORT_MENU

						await message.answer(f"💬 Новое <b>упражнение</b> добавлено в <b>«{ConfigInlineKeyboard().SPORT[2:]}»</b>.\n\n"
						   			   		 f" • <b>ID Упражнения:</b> <b>{ID_SPORT}</b>\n"
											 f" • <b>Эмодзи упражнения:</b> {EMODJI_SPORT}\n"
											 f" • <b>Название callback_query:</b> {CALLBACK_DATA_SPORT}\n"
											 f" • <b>Название упражнения:</b> {NAME_SPORT}\n"
											 f" • <b>Описание к упражнению:</b> {MESSAGE}\n\n"
											 f"Благодарим за вашу активность в <b>«{ConfigInlineKeyboard().SPORT[2:]}»</b>.",
											 reply_markup = back_sport_inline_keyboard)

				elif len(PARTS) < 5:
					await message.answer("⚠️ Извините, но для добавления упражнения необходимо предоставить <b>полную</b> информацию. Пожалуйста, убедитесь, что вы ввели следующие данные:\n\n"
						   			   	 " • <b>ID Упражнения:</b> [Введите ID Упражения]\n"
										 " • <b>Эмодзи упражнения:</b> [Введите эмодзи]\n"
										 " • <b>Название callback_query:</b> [Введите название callback_query]\n"
										 " • <b>Название упражнения:</b> [Введите название упражнения]\n"
										 " • <b>Описание к упражнения:</b> [Добавьте свое описание]\n\n"
										 "Пожалуйста, убедитесь, что все поля <b>заполнены</b>, и повторите попытку.")
			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик для удаления упражнений."""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "DELETE_SPORT")
async def delete_sport_admin_handler(callback_query: types.CallbackQuery):
	"""Объявляем переменные для вывода информации о пользователе, администрации и упражнениях."""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()
	SPORT_DATA_DB = load_sport_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID."""
		USER_ID = ConfigBot.USERID(callback_query)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				"""Объявляем переменную с выводом inline клавиатуры для возвращения."""
				back_sport_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_SPORT_MENU

				await bot.edit_message_text("💬 Для <b>удаления</b> упражнения введите ID, который вы хотели бы удалить:\n\n"
											f"{(ConfigBot.GETIDSPORT(SPORT_DATA_DB))}\n\n"
											f"Благодарим за вашу активность в <b>«{ConfigInlineKeyboard().SPORT[2:]}»</b>.",
											callback_query.from_user.id,
											callback_query.message.message_id,
									   		reply_markup = back_sport_inline_keyboard)

				"""Переходим в фазу, где администратор вводит ID упражнения для удаления его из базы данных."""
				await DebugAdminState.DeleteSportForAdminState.set()

			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик фазы, где вводят ID упражнения, чтобы удалить его из базы данных."""
@dp.message_handler(state = DebugAdminState.DeleteSportForAdminState)
async def delete_sport_admin_state(message: types.Message):
	"""Объявляем переменные для вывода информации о пользователе, администрации и упражнениях."""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()
	SPORT_DATA_DB = load_sport_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID, USER_MESSAGE."""
		USER_ID = ConfigBot.USERID(message)
		USER_MESSAGE = ConfigBot.USERMESSAGE(message)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				if is_sport_in_data(USER_MESSAGE, SPORT_DATA_DB):
					"""Удаляем упражнение из базы данных."""
					del SPORT_DATA_DB[str(USER_MESSAGE)]

					save_sport_data(SPORT_DATA_DB)

					"""Объявляем переменную с выводом inline клавиатуры для возвращения."""
					back_sport_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_SPORT_MENU

					await message.answer(f"💬 Отлично, упражнение с ID [<code>{ConfigBot.USERMESSAGE(message)}</code>] успешно удален из базы данных.\n\n"
						  				 f"Благодарим за вашу активность в <b>«{ConfigInlineKeyboard().SPORT[2:]}»</b>.",
										 reply_markup = back_sport_inline_keyboard)
				else:
					await message.answer("⚠️ Извините, но похоже, что <b>упражнение</b> с указанным <b>ID</b> не существует в базе данных.\n\n"
						  				 "Убедитесь, что вы ввели правильный ID, и повторите попытку.")
			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)