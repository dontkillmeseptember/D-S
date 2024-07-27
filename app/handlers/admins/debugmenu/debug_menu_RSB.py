from data.loader import dp, bot
from data.config import ConfigBot
from data.config_Keyboard import ConfigInlineKeyboard
from data.loader_keyboard import LoaderInlineKeyboardsAdmin
from data.states_groups import DebugAdminState

from database.requests.user_db import load_user_data, is_user_in_data
from database.requests.admin_db import load_admin_data, is_admin_in_data
from database.requests.rsb_db import load_rsb_data, save_rsb_data, is_rsb_in_data, check_rsb_data

from misc.libraries import types, Union, FSMContext
from misc.loggers import logger

"""Сохраняем number_wallet_id для редактирования кошельков"""
NUMBER_WALLET_ID = None

"""Создаем обработчик для управление RSB - Банком."""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "RSB")
@dp.callback_query_handler(lambda callback_data: callback_data.data == "BACK_RSB", state = [DebugAdminState.AddRSBForAdminState, DebugAdminState.DeleteRSBForAdminState, DebugAdminState.ReditRSBForAdminState])
async def rsb_admin_handler(callback_query: types.CallbackQuery, state: FSMContext) -> str:
	global NUMBER_WALLET_ID

	"""Объявляем переменные для вывода информации о пользователе и администрации."""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID."""
		USER_ID = ConfigBot.USERID(callback_query)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				CURRENT_STATE = await state.get_state()

				"""Объявляем переменную с выводом клавиатуры с меню для управления банком."""
				menu_rsb_admin_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_MENURSB

				INFO_MENU_RSB_ADMIN_MESSAGE = f"💬 Добро пожаловать в управление <b>RSB - Банком</b>.\n\n" \
										 	  f"Здесь вы можете легко управлять кошельками и добавлять их. Вот описание к кнопкам:\n\n" \
										 	  f" • <b>{ConfigInlineKeyboard().ADD_RSB[2:]}:</b> Используйте эту кнопку для добавление <b>новых</b> кошельков в <b>RSB</b>.\n\n" \
										 	  f" • <b>{ConfigInlineKeyboard().DELETE_RSB[:-2]}:</b> При необходимости вы можете <b>удалить</b> выбранные кошельки из <b>RSB</b> с помощью этой кнопки.\n\n" \
										 	  f" • <b>{ConfigInlineKeyboard().REDIT_RSB[2:-2]}:</b> Нажмите эту кнопку, чтобы <b>редактировать</b> кошельки, которые в данный момент находятся в <b>RSB</b>.\n\n" \
										 	  f"Спасибо за ваше внимание к деталям управления. Удачного управления."

				if not CURRENT_STATE or CURRENT_STATE.startswith("DebugAdminState:"):
					await bot.edit_message_text(INFO_MENU_RSB_ADMIN_MESSAGE,
												callback_query.from_user.id, 
												callback_query.message.message_id,
												reply_markup = menu_rsb_admin_inline_keyboard)
					
					NUMBER_WALLET_ID = None

					await state.finish()
			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик для редактирование кошельков в RSB"""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "REDIT_RSB")
async def redit_rsb_admin_handler(callback_query: types.CallbackQuery) -> DebugAdminState:
	"""Объявляем переменные с выводом информации о пользователе, администрации и банке"""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()
	RSB_DATA_DB = load_rsb_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID"""
		USER_ID = ConfigBot.USERID(callback_query)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				"""Объявляем переменную с выводом клавиатуры для возвращение в меню управления банком"""
				back_rsb_admin_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACKRSB

				await bot.edit_message_text("💬 Для <b>редактирования</b> кошелька из базы <b>RSB</b>, введите, пожалуйста, ID кошелька из списка.\n\n"
										   f"{ConfigBot.GETNUMBERWALLETRSB(RSB_DATA_DB, ConfigBot.USERID(callback_query))}\n\n"
										   	"Благодарим за вашу активность в управлении <b>RSB - Банком</b>.",
											callback_query.from_user.id,
											callback_query.message.message_id,
											reply_markup = back_rsb_admin_inline_keyboard)
				
				"""Переходим в фазу, где вводят ID кошелька для редактирование его из RSB"""
				await DebugAdminState.ReditRSBForAdminState.set()

			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик фазы, где администратор вводит ID кошелька и начинает редактировать его из RSB"""
@dp.message_handler(state = DebugAdminState.ReditRSBForAdminState)
@dp.callback_query_handler(lambda callback_data: callback_data.data == "BACK_REDIT_RSB", state = [DebugAdminState.AddEthReditRSBForAdminState, DebugAdminState.AddBudgetReditRSBForAdminState, DebugAdminState.AddInterestRSBForAdminState])
async def redit_numberWallet_rsb_admin_handler(message_or_callbackQuery: Union[types.Message, types.CallbackQuery]) -> DebugAdminState:
	global NUMBER_WALLET_ID

	"""Объявляем переменные с выводом информации о пользователе, администрации и банке"""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()
	RSB_DATA_DB = load_rsb_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID"""
		USER_ID = ConfigBot.USERID(message_or_callbackQuery)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
					"""Объявляем переменную с выводом клавиатуры для управление банком"""
					redit_menu_rsb_admin_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_REDITMENU

					if isinstance(message_or_callbackQuery, types.Message):
						"""Объявляем переменную с выводом информации о пользователе: USER_MESSAGE"""
						USER_MESSAGE = ConfigBot.USERMESSAGE(message_or_callbackQuery)

						"""Сохраняем ID кошелька в переменную NUMBER_WALLET_ID"""
						NUMBER_WALLET_ID = USER_MESSAGE

						"""Объявляем переменную с выводом сообщения о информации кошелька"""
						INFO_RSB_ADMIN_MESSAGE_TWO = f"💬 Текущая информация о кошельке.\n\n" \
												f" • ID кошелька: <b>{NUMBER_WALLET_ID}</b>\n\n" \
												f" • Баланс кошелька: <code>{ConfigBot.GETRSB(NUMBER_WALLET_ID, 'ETH', True, None)}</code> <b>ETH</b> - <code>{ConfigBot.GETRSB(NUMBER_WALLET_ID, 'USD', True, None)}</code> <b>USD</b> ~ <code>{ConfigBot.GETRSB(NUMBER_WALLET_ID, 'RUB', True, None)}</code> <b>RUB</b>\n\n" \
												f" • Текущий курс ETH: <b>1 ETH</b> ~ <code>{ConfigBot.GETRSB(NUMBER_WALLET_ID, 'CURRENT_ETH', True, None)}</code> <b>RUB</b>\n" \
												f" • Текущий курс USD: <b>1 USD</b> ~ <code>{ConfigBot.GETRSB(NUMBER_WALLET_ID, 'CURRENT_USD', True, None)}</code> <b>RUB</b>\n" \
												f" • Текущий курс RUB: <b>1 RUB</b> ~ <code>{ConfigBot.GETRSB(NUMBER_WALLET_ID, 'CURRENT_RUB', True, None)}</code> <b>USD</b>\n\n" \
												f" • Общий вклад в кошелек: 🧑🏻 <b>{ConfigBot.GETRSB(NUMBER_WALLET_ID, 'INTEREST_USER_ONE', True, None)}%</b> ~ <b>{ConfigBot.GETRSB(NUMBER_WALLET_ID, 'INTEREST_USER_TWO', True, None)}%</b> 👩🏻‍🦰\n\n" \
												f" • Общий бюджет: <code>{ConfigBot.GETRSB(NUMBER_WALLET_ID, 'ALL_SUM_ETH', True, None)}</code> <b>ETH</b> - <code>{ConfigBot.GETRSB(NUMBER_WALLET_ID, 'ALL_SUM_USD', True, None)}</code> <b>USD</b> ~ <code>{ConfigBot.GETRSB(NUMBER_WALLET_ID, 'ALL_SUM_RUB', True, None)}</code> <b>RUB</b>"

						if is_rsb_in_data(USER_MESSAGE, RSB_DATA_DB):
							await message_or_callbackQuery.answer(INFO_RSB_ADMIN_MESSAGE_TWO, reply_markup = redit_menu_rsb_admin_inline_keyboard)

							"""Переходим в фазу, где вводят ID кошелька для редактирование его из RSB"""
							await DebugAdminState.ReditRSBForAdminState.set()

						elif not is_rsb_in_data(USER_MESSAGE, RSB_DATA_DB):
							await message_or_callbackQuery.answer("⚠️ Извините, но похоже, что кошелек с введенным <b>ID</b> отсутствует в базе данных.\n\n"
																  "Пожалуйста, убедитесь, что вы ввели корректный <b>ID</b> или проверьте актуальность информации.")
						
						else:
							logger.error("⚠️ Произошла непредвиденная ошибка с проверкой ID кошелька: %s", is_rsb_in_data(USER_MESSAGE, RSB_DATA_DB))

					elif isinstance(message_or_callbackQuery, types.CallbackQuery):
						"""Объявляем переменную с выводом сообщения о информации кошелька"""
						INFO_RSB_ADMIN_MESSAGE_ONE = f"💬 Текущая информация о кошельке.\n\n" \
												f" • ID кошелька: <b>{NUMBER_WALLET_ID}</b>\n\n" \
												f" • Баланс кошелька: <code>{ConfigBot.GETRSB(NUMBER_WALLET_ID, 'ETH', True, None)}</code> <b>ETH</b> - <code>{ConfigBot.GETRSB(NUMBER_WALLET_ID, 'USD', True, None)}</code> <b>USB</b> ~ <code>{ConfigBot.GETRSB(NUMBER_WALLET_ID, 'RUB', True, None)}</code> <b>RUB</b>\n\n" \
												f" • Текущий курс ETH: <b>1 ETH</b> ~ <code>{ConfigBot.GETRSB(NUMBER_WALLET_ID, 'CURRENT_ETH', True, None)}</code> <b>RUB</b>\n" \
												f" • Текущий курс USD: <b>1 USD</b> ~ <code>{ConfigBot.GETRSB(NUMBER_WALLET_ID, 'CURRENT_USD', True, None)}</code> <b>RUB</b>\n" \
												f" • Текущий курс RUB: <b>1 RUB</b> ~ <code>{ConfigBot.GETRSB(NUMBER_WALLET_ID, 'CURRENT_RUB', True, None)}</code> <b>USD</b>\n\n" \
												f" • Общий вклад в кошелек: 🧑🏻 <b>{ConfigBot.GETRSB(NUMBER_WALLET_ID, 'INTEREST_USER_ONE', True, None)}%</b> ~ <b>{ConfigBot.GETRSB(NUMBER_WALLET_ID, 'INTEREST_USER_TWO', True, None)}%</b> 👩🏻‍🦰\n\n" \
												f" • Общий бюджет: <code>{ConfigBot.GETRSB(NUMBER_WALLET_ID, 'ALL_SUM_ETH', True, None)}</code> <b>ETH</b> - <code>{ConfigBot.GETRSB(NUMBER_WALLET_ID, 'ALL_SUM_USD', True, None)}</code> <b>USD</b> ~ <code>{ConfigBot.GETRSB(NUMBER_WALLET_ID, 'ALL_SUM_RUB', True, None)}</code> <b>RUB</b>"

						await bot.edit_message_text(INFO_RSB_ADMIN_MESSAGE_ONE,
													message_or_callbackQuery.from_user.id,
													message_or_callbackQuery.message.message_id,
													reply_markup = redit_menu_rsb_admin_inline_keyboard)

						"""Переходим в фазу, где вводят ID кошелька для редактирование его из RSB"""
						await DebugAdminState.ReditRSBForAdminState.set()
					
					else:
						logger.error("⚠️ Произошла непредвиденная ошибка с проверкой isinstance: %s", isinstance)
			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик для обновление кошелька RSB"""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "RELOAD_WALLET", state = DebugAdminState.ReditRSBForAdminState)
async def reload_wallet_rsb_admin_handler(callback_query: types.CallbackQuery) -> DebugAdminState:
	global NUMBER_WALLET_ID

	"""Объявляем переменные с выводом информации о пользователе, администрации и банке"""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()
	RSB_DATA_DB = load_rsb_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID"""
		USER_ID = ConfigBot.USERID(callback_query)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, USER_DATA_DB):
				"""Объявляем переменную с выводом данных из кошелька по ID кошелька"""
				check_rsb_data_db = check_rsb_data(NUMBER_WALLET_ID)
				wallet_data = check_rsb_data_db.get("ALL_SUM_WALLET", {})

				ETH, ALL_USD_START, ALL_RUB_START = (
					check_rsb_data_db.get("ETH"),
					wallet_data.get("ALL_SUM_USD_START"),
					wallet_data.get("ALL_SUM_RUB_START")
				)

				if ETH > 0:
					if ConfigBot.GETETHTOUSD() > 0:
						"""Обновляем данные связанные с USD в кошельке RSB"""
						USD_AMOUNT = float(ETH) * ConfigBot.GETETHTOUSD()
						USD_END_AMOUNT = float(USD_AMOUNT) + ALL_USD_START

						USD_FORMATTED = "{:.1f}".format(USD_AMOUNT)
						USD_END_FORMATTED = "{:.1f}".format(USD_END_AMOUNT)

						RSB_DATA_DB[str(NUMBER_WALLET_ID)]["USD"] = float(USD_FORMATTED)
						RSB_DATA_DB[str(NUMBER_WALLET_ID)]["ALL_SUM_WALLET"]["ALL_SUM_USD_END"] = float(USD_END_FORMATTED)
					
						if ConfigBot.GETETHTORUB() > 0:
							"""Обновляем данные связанные с RUB в кошельке RSB"""
							RUB_AMOUNT = float(ETH) * ConfigBot.GETETHTORUB()
							RUB_END_AMOUNT = int(RUB_AMOUNT) + ALL_RUB_START

							RSB_DATA_DB[str(NUMBER_WALLET_ID)]["RUB"] = int(RUB_AMOUNT)
							RSB_DATA_DB[str(NUMBER_WALLET_ID)]["ALL_SUM_WALLET"]["ALL_SUM_RUB_END"] = int(RUB_END_AMOUNT)
							RSB_DATA_DB[str(NUMBER_WALLET_ID)]["CURRENT"]["CURRENT_ETH"] = int(ConfigBot.GETETHTORUB())

							"""Обновляем текущий курс RUB к USD"""
							RSB_DATA_DB[str(NUMBER_WALLET_ID)]["CURRENT"]["CURRENT_RUB"] = round(ConfigBot.GETRUBTOUSD(), 3)

							"""Обновляем текущий курс USD к RUB"""
							RSB_DATA_DB[str(NUMBER_WALLET_ID)]["CURRENT"]["CURRENT_USD"] = int(ConfigBot.GETUSDTORUB())

						else:
							logger.critical("⚠️ Произошла непредвиденная ошибка с проверкой ETH: %s", ConfigBot.GETETHTORUB())
					else:
						logger.critical("⚠️ Произошла непредвиденная ошибка с проверкой ETH: %s", ConfigBot.GETETHTOUSD())
				else:
					logger.error("⚠️ Произошла непредвиденная ошибка с проверкой ETH: %s", ETH)

				save_rsb_data(RSB_DATA_DB)

				await redit_numberWallet_rsb_admin_handler(callback_query)
			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик для изменения вклада в кошелек RSB"""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "ADD_INTEREST", state = DebugAdminState.ReditRSBForAdminState)
async def change_interest_rsb_admin_handler(callback_query: types.CallbackQuery) -> DebugAdminState:
	global NUMBER_WALLET_ID

	"""Объявляем переменные с выводом информации о пользователе и администрации"""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID"""
		USER_ID = ConfigBot.USERID(callback_query)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, USER_DATA_DB):
				"""Объявляем переменную с выводом клавиатуры для возвращения в меню управления банком"""
				back_redit_menu_rsb_admin_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_REDIT_MENU

				await bot.edit_message_text("💬 Для <b>добавления</b> нужного количества <b>общего вклада</b> в кошелек, введите, пожалуйста, необходимые проценты.\n\n"
											"Пример <b>добавления</b> нужного количества общего вклада:\n\n"
											" • <b><i>«Первый Пользователь» «Второй Пользователь»</i></b>\n\n"
											"После ввода процентов, они будут <b>добавлены</b> в указанный кошелек:\n\n"
											f" • <b><i>«{NUMBER_WALLET_ID}»</i></b>\n\n",
											callback_query.from_user.id,
											callback_query.message.message_id,
											reply_markup = back_redit_menu_rsb_admin_inline_keyboard)
				
				"""Переходим в фазу, где администратор вводит нужное количество вкладка в кошелек"""
				await DebugAdminState.AddInterestRSBForAdminState.set()

			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик фазы, где администратор вводит проценты общего вклада в кошелек RSB"""
@dp.message_handler(state = DebugAdminState.AddInterestRSBForAdminState)
async def item_change_interest_rsb_admin_handler(message: types.Message) -> DebugAdminState:
	global NUMBER_WALLET_ID

	"""Объявляем переменные с выводом информации о пользователе, администрации и банке"""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()
	RSB_DATA_DB = load_rsb_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID"""
		USER_ID = ConfigBot.USERID(message)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				"""Объявляем переменную о выводе информации пользователя и для разделения сообщений от пользователя"""
				USER_MESSAGE = ConfigBot.USERMESSAGE(message)
				PARTS = USER_MESSAGE.split()

				if len(PARTS) == 2:
					"""Объявляем переменные для разделения PARTS на аспекты"""
					USER_ONE, USER_TWO = PARTS

					if int(USER_ONE) + int(USER_TWO) == 100:
						RSB_DATA_DB[str(NUMBER_WALLET_ID)]["INTEREST"]["INTEREST_USER_ONE"] = int(USER_ONE)
						RSB_DATA_DB[str(NUMBER_WALLET_ID)]["INTEREST"]["INTEREST_USER_TWO"] = int(USER_TWO)
						
						save_rsb_data(RSB_DATA_DB)

						"""Объявляем переменную с выводом клавиатуры для возвращения в меню управления банком"""
						redit_menu_rsb_admin_inline_keyboard_back = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_REDIT_MENU

						await message.answer("💬 Отлично, общий вклад в кошелек успешно <b>обновлен</b>.\n\n"
						   					 "Общий вклад был <b>добавлен</b> в указанный кошелек:\n\n"
											f" • <b>{NUMBER_WALLET_ID}</b>\n\n"
											f"Теперь <b>общий вклад</b> кошелька составляет: 🧑🏻 <b>{USER_ONE}%</b> ~ <b>{USER_TWO}%</b> 👩🏻‍🦰\n\n",
						   					 reply_markup = redit_menu_rsb_admin_inline_keyboard_back)

					elif int(USER_ONE) + int(USER_TWO) > 100:
						await message.answer("⚠️ Извините, похоже, что <b>введенный</b> общий вклад в сумме больше чем <b>100%</b>.")
					
					elif int(USER_ONE) + int(USER_TWO) < 100:
						await message.answer("⚠️ Извините, похоже, что <b>введенный</b> общий вклад в сумме меньше чем <b>100%</b>.")

					else:
						logger.warning("⚠️ USER_ONE, USER_TWO не ровняются в сумме 100: %s", USER_ONE, USER_TWO)

				elif len(PARTS) != 2:
					await message.answer("⚠️ Извините, похоже, что <b>введенный</b> общий вклад имеет неверный формат.\n\n"
						  				 "Например, <b>введите</b> проценты в формате:\n\n"
										 " • <b><i>«30» «70»</i></b>\n\n"
										 "После <b>ввода</b> процентов, она будут <b>добавлены</b> в указанный кошелек:\n\n"
										 f"• <b><i>«{NUMBER_WALLET_ID}»</i></b>")

				else:
					logger.warning("⚠️ PARTS Не ровняется к двум: %s", len(PARTS))
			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик для изменения общего бюджета в кошельке RSB"""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "ADD_BUDGET", state = DebugAdminState.ReditRSBForAdminState)
async def add_budget_rsb_admin_handler(callback_query: types.CallbackQuery) -> DebugAdminState:
	global NUMBER_WALLET_ID

	"""Объявляем переменные с выводом информации о пользователе и администрации"""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID"""
		USER_ID = ConfigBot.USERID(callback_query)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				"""Объявляем переменную с выводом клавиатуры для возвращения в меню управления банком"""
				back_redit_menu_rsb_admin_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_REDIT_MENU

				await bot.edit_message_text("💬 Для <b>добавления</b> нужного количества <b>бюджета</b> в кошелек, введите, пожалуйста, необходимую сумму.\n\n"
											"Пример <b>добавления</b> нужного количества бюджета:\n\n"
											" • <b><i>«Сумма ETH» «Сумма USD» «Сумма RUB»</i></b>\n\n"
										    "После ввода суммы, она будет <b>добавлена</b> в указанный кошелек:\n\n"
											f" • <b><i>«{NUMBER_WALLET_ID}»</i></b>\n\n",
											callback_query.from_user.id,
											callback_query.message.message_id,
											reply_markup = back_redit_menu_rsb_admin_inline_keyboard)
				
				"""Переходим в фазу где вводят нужное количество общего бюджета для добавления в кошелек"""
				await DebugAdminState.AddBudgetReditRSBForAdminState.set()

			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик фазы, где администратор вводит бюджет для кошелька в RSB"""
@dp.message_handler(state = DebugAdminState.AddBudgetReditRSBForAdminState)
async def item_add_budget_rsb_admin_handler(message: types.Message) -> DebugAdminState:
	global NUMBER_WALLET_ID
	
	"""Объявляем переменные с выводом информации о пользователе, администрации и банке"""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()
	RSB_DATA_DB = load_rsb_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID"""
		USER_ID = ConfigBot.USERID(message)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				"""Объявляем переменную о выводе информации пользователя и для разделения сообщений от пользователя"""
				USER_MESSAGE = ConfigBot.USERMESSAGE(message)
				PARTS = USER_MESSAGE.split()

				"""Объявляем переменную с выводом данных из кошелька по ID кошелька"""
				check_rsb_data_db = check_rsb_data(NUMBER_WALLET_ID)
				wallet_data = check_rsb_data_db.get("ALL_SUM_WALLET", {})

				ETH, USD, RUB, ALL_ETH_START, ALL_USD_START, ALL_RUB_START = (
					check_rsb_data_db.get("ETH"),
					check_rsb_data_db.get("USD"),
					check_rsb_data_db.get("RUB"),
					wallet_data.get("ALL_SUM_ETH_START"),
					wallet_data.get("ALL_SUM_USD_START"),
					wallet_data.get("ALL_SUM_RUB_START")
				)

				if len(PARTS) == 3:
					"""Объявляем переменные для разделения PARTS на аспекты"""
					ETH_ADMIN, USD_ADMIN, RUB_ADMIN = PARTS

					if float(ETH_ADMIN) > 0:
						ALL_ETH_ADMIN = ALL_ETH_START + float(ETH_ADMIN)
						ALL_ETH_ADMIN_END = float(ALL_ETH_ADMIN) + ETH

						ETH_START_FORMATTED = "{:.3f}".format(ALL_ETH_ADMIN)
						ETH_END_FORMATTED = "{:.3f}".format(ALL_ETH_ADMIN_END)

						RSB_DATA_DB[str(NUMBER_WALLET_ID)]["ALL_SUM_WALLET"]["ALL_SUM_ETH_START"] = float(ETH_START_FORMATTED)
						RSB_DATA_DB[str(NUMBER_WALLET_ID)]["ALL_SUM_WALLET"]["ALL_SUM_ETH_END"] = float(ETH_END_FORMATTED)
					
					elif float(ETH_ADMIN) < 0:
						return None

					if float(USD_ADMIN) > 0:
						ALL_USD_ADMIN = ALL_USD_START + float(USD_ADMIN)
						ALL_USD_ADMIN_END = float(ALL_USD_ADMIN) + USD

						USD_END_FORMATTED = "{:.1f}".format(ALL_USD_ADMIN_END)

						RSB_DATA_DB[str(NUMBER_WALLET_ID)]["ALL_SUM_WALLET"]["ALL_SUM_USD_START"] = float(ALL_USD_ADMIN)
						RSB_DATA_DB[str(NUMBER_WALLET_ID)]["ALL_SUM_WALLET"]["ALL_SUM_USD_END"] = float(USD_END_FORMATTED)

					elif float(USD_ADMIN) < 0:
						return None

					if int(RUB_ADMIN) > 0:
						ALL_RUB_ADMIN = ALL_RUB_START + int(RUB_ADMIN)
						ALL_RUB_ADMIN_END = int(ALL_RUB_ADMIN) + RUB

						RSB_DATA_DB[str(NUMBER_WALLET_ID)]["ALL_SUM_WALLET"]["ALL_SUM_RUB_START"] = int(ALL_RUB_ADMIN)
						RSB_DATA_DB[str(NUMBER_WALLET_ID)]["ALL_SUM_WALLET"]["ALL_SUM_RUB_END"] = int(ALL_RUB_ADMIN_END)
					
					elif int(RUB_ADMIN) < 0:
						return None

					save_rsb_data(RSB_DATA_DB)

					"""Объявляем переменную с выводом клавиатуры для возвращения в меню управления банком"""
					redit_menu_rsb_admin_inline_keyboard_back = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_REDIT_MENU

					await message.answer(f"💬 Отлично, бюджет кошелька успешно <b>обновлен</b>.\n\n"
										  "Общая сумма бюджета была <b>добавлена</b> в указанный кошелек:\n\n"
										 f" • <b>{NUMBER_WALLET_ID}</b>\n\n"
						  				  "К существующей сумме бюджета было <b>добавлено</b>:\n\n"
						  				 f" • <b><code>{ETH_ADMIN}</code> ETH <code>{USD_ADMIN}</code> USD <code>{RUB_ADMIN}</code> RUB</b>\n\n"
										  "Теперь <b>общая сумма</b> бюджета составляет:\n\n"
						  				 f" • <b><code>{ETH_END_FORMATTED}</code> ETH <code>{USD_END_FORMATTED}</code> USD <code>{ALL_RUB_ADMIN_END}</code> RUB</b>\n\n",
										 reply_markup = redit_menu_rsb_admin_inline_keyboard_back)

				elif len(PARTS) != 3:
					await message.answer("⚠️ Извините, похоже, что <b>введенный</b> бюджет имеет неверный формат.\n\n"
						  				 "Например, <b>введите</b> сумму в формате:\n\n"
										 " • <b><i>«3.20» ETH «100» USD «2500» RUB</i></b>\n\n"
										 "После <b>ввода</b> суммы, она будет <b>добавлена</b> в указанный кошелек:\n\n"
										 f"• <b><i>«{NUMBER_WALLET_ID}»</i></b>")

				else:
					logger.warning("⚠️ PARTS Не ровняется к трем: %s", len(PARTS))
			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик для добавление ETH в кошелек RSB"""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "ADD_ETH", state = DebugAdminState.ReditRSBForAdminState)
async def add_eth_rsb_admin_handler(callback_query: types.CallbackQuery) -> DebugAdminState:
	global NUMBER_WALLET_ID

	"""Проверяем зарегистрирован пользователь в базе админов"""
	admin_data_db = load_admin_data()

	"""Загружаем базу данных о пользователе"""
	user_data_db = load_user_data()

	try:
		if is_user_in_data(ConfigBot.USERID(callback_query), user_data_db):
			if is_admin_in_data(ConfigBot.USERID(callback_query), admin_data_db):
				"""Выводим клавиатуры для обработчика кнопки назад"""
				inline_keyboard_back_redit_menu_rsb_admin = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_REDIT_MENU

				await bot.edit_message_text("💬 Для <b>добавления</b> нужного количества <b>ETH</b> в кошелек, введите, пожалуйста, необходимую сумму.\n\n"
											"Пример <b>добавления</b> нужного количества <b>ETH</b> в кошелек:\n\n"
											" • <b><i>«Сумма ETH»</i></b>\n\n"
										    "После ввода суммы, она будет <b>добавлена</b> в указанный кошелек:\n\n"
											f" • <b><i>«{NUMBER_WALLET_ID}»</i></b>\n\n",
											callback_query.from_user.id,
											callback_query.message.message_id,
											reply_markup=inline_keyboard_back_redit_menu_rsb_admin)
				
				"""Переходим в фазу, где вводят количество ETH для добавления в кошелек"""
				await DebugAdminState.AddEthReditRSBForAdminState.set()
			else:
				raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: ADD_ETH_RSB_ADMIN_HANDLER, TESTING: IS_ADMIN_IN_DATA")
		else:
			raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: ADD_ETH_RSB_ADMIN_HANDLER, TESTING: IS_USER_IN_DATA")
	except:
		raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: ADD_ETH_RSB_ADMIN_HANDLER")

"""Создаем обработчик фазы, где администратор вводит количество ETH и добавляет его в кошелек"""
@dp.message_handler(state = DebugAdminState.AddEthReditRSBForAdminState)
async def item_add_eth_rsb_admin_handler(message: types.Message) -> DebugAdminState:
	global NUMBER_WALLET_ID

	"""Проверяем зарегистрирован пользователь в базе админов"""
	admin_data_db = load_admin_data()

	"""Загружаем базу данных о пользователе"""
	user_data_db = load_user_data()

	"""Загружаем базу данных о RSB"""
	rsb_data_db = load_rsb_data()

	try:
		if is_user_in_data(ConfigBot.USERID(message), user_data_db):
			if is_admin_in_data(ConfigBot.USERID(message), admin_data_db):
				"""Вводим из message номер кошелька и проверяем его"""
				check_rsb_data_db = check_rsb_data(NUMBER_WALLET_ID)

				"""Объявляем переменную с выводом данных из кошелька по ID кошелька"""
				check_rsb_data_db = check_rsb_data(NUMBER_WALLET_ID)
				wallet_data = check_rsb_data_db.get("ALL_SUM_WALLET", {})

				ETH, ALL_ETH_START, ALL_USD_START, ALL_RUB_START, ALL_ETH_END, ALL_USD_END, ALL_RUB_END = (
					check_rsb_data_db.get("ETH"),
					wallet_data.get("ALL_SUM_ETH_START"),
					wallet_data.get("ALL_SUM_USD_START"),
					wallet_data.get("ALL_SUM_RUB_START"),
					wallet_data.get("ALL_SUM_ETH_END"),
					wallet_data.get("ALL_SUM_USD_END"),
					wallet_data.get("ALL_SUM_RUB_END"),
				)

				"""Сохраняем введенное значение администратором в базу данных о кошельке RSB"""
				if float(ConfigBot.USERMESSAGE(message)) > 0:
					ETH_AMOUNT = ETH + float(ConfigBot.USERMESSAGE(message))
					ETH_FORMATTED = "{:.3f}".format(ETH_AMOUNT)

					rsb_data_db[str(NUMBER_WALLET_ID)]["ETH"] = float(ETH_FORMATTED)
					save_rsb_data(rsb_data_db)

					if ALL_ETH_END > 0:
						ETH_END_AMOUNT = ALL_ETH_END + float(ConfigBot.USERMESSAGE(message))
						ETH_END_FORMATTED = "{:.3f}".format(ETH_END_AMOUNT)

						rsb_data_db[str(NUMBER_WALLET_ID)]["ALL_SUM_WALLET"]["ALL_SUM_ETH_END"] = float(ETH_END_FORMATTED)
						save_rsb_data(rsb_data_db)

					elif ALL_ETH_END == 0:
						ETH_END_AMOUNT = ALL_ETH_START + float(ConfigBot.USERMESSAGE(message))
						ETH_END_FORMATTED = "{:.3f}".format(ETH_END_AMOUNT)

						rsb_data_db[str(NUMBER_WALLET_ID)]["ALL_SUM_WALLET"]["ALL_SUM_ETH_END"] = float(ETH_END_FORMATTED)
						save_rsb_data(rsb_data_db)

					"""Сохраняем переведенное значение ETH в USD"""
					if ConfigBot.GETETHTOUSD() > 0:
						USD_AMOUNT = float(ETH_AMOUNT) * ConfigBot.GETETHTOUSD()
						USD_FORMATTED = "{:.1f}".format(USD_AMOUNT)

						rsb_data_db[str(NUMBER_WALLET_ID)]["USD"] = float(USD_FORMATTED)
						save_rsb_data(rsb_data_db)

						if ALL_USD_END > 0:
							USD_END_AMOUNT = ALL_USD_END + float(USD_FORMATTED)
							USD_END_FORMATTED = "{:.1f}".format(USD_END_AMOUNT)

							rsb_data_db[str(NUMBER_WALLET_ID)]["ALL_SUM_WALLET"]["ALL_SUM_USD_END"] = float(USD_END_FORMATTED)
							save_rsb_data(rsb_data_db)

						elif ALL_USD_END == 0:
							USD_END_AMOUNT = ALL_USD_START + float(USD_FORMATTED)
							USD_END_FORMATTED = "{:.1f}".format(USD_END_AMOUNT)

							rsb_data_db[str(NUMBER_WALLET_ID)]["ALL_SUM_WALLET"]["ALL_SUM_USD_END"] = float(USD_END_FORMATTED)
							save_rsb_data(rsb_data_db)

					elif ConfigBot.GETETHTOUSD() < 0:
						return None

					"""Сохраняем переведенное значение ETH в RUB"""
					if ConfigBot.GETETHTORUB() > 0:
						RUB_AMOUNT = float(ETH_AMOUNT) * ConfigBot.GETETHTORUB()

						rsb_data_db[str(NUMBER_WALLET_ID)]["RUB"] = int(RUB_AMOUNT)
						save_rsb_data(rsb_data_db)

						if ALL_RUB_END > 0:
							RUB_END_AMOUNT = ALL_RUB_END + int(RUB_AMOUNT)

							rsb_data_db[str(NUMBER_WALLET_ID)]["ALL_SUM_WALLET"]["ALL_SUM_RUB_END"] = int(RUB_END_AMOUNT)
							save_rsb_data(rsb_data_db)

						elif ALL_RUB_END == 0:
							RUB_END_AMOUNT = ALL_RUB_START + int(RUB_AMOUNT)

							rsb_data_db[str(NUMBER_WALLET_ID)]["ALL_SUM_WALLET"]["ALL_SUM_RUB_END"] = int(RUB_END_AMOUNT)
							save_rsb_data(rsb_data_db)

						"""Выводим клавиатуры для обработчика кнопки назад"""
						inline_keyboard_back_redit_menu_rsb_admin = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_REDIT_MENU

						await message.answer("💬 Успешно добавлено <b>ETH</b> в кошелек:\n\n"
						   					f" • ID кошелька: <b>{NUMBER_WALLET_ID}</b>\n\n"
											f" • Добавлено в кошелек: <code>{float(ConfigBot.USERMESSAGE(message))}</code> <b>ETH</b> - <code>{0}</code> <b>$</b> ~ <code>{0}</code> ₽\n\n"
											f" • Баланс кошелька: <code>{ConfigBot.GETRSB(NUMBER_WALLET_ID, 'ETH', True, None)}</code> <b>ETH</b> - <code>{ConfigBot.GETRSB(NUMBER_WALLET_ID, 'USD', True, None)}</code> <b>$</b> ~ <code>{ConfigBot.GETRSB(NUMBER_WALLET_ID, 'RUB', True, None)}</code> ₽\n\n"
											f" • Общий бюджет: <code>{ConfigBot.GETRSB(NUMBER_WALLET_ID, 'ALL_SUM_ETH', True, None)}</code> <b>ETH</b> - <code>{ConfigBot.GETRSB(NUMBER_WALLET_ID, 'ALL_SUM_USD', True, None)}</code> <b>$</b> ~ <code>{ConfigBot.GETRSB(NUMBER_WALLET_ID, 'ALL_SUM_RUB', True, None)}</code> ₽",
											reply_markup=inline_keyboard_back_redit_menu_rsb_admin)
					
					elif ConfigBot.GETETHTORUB() < 0:
						return None

				else:
					await message.answer("⚠️ Похоже, что введенное количество <b>ETH</b> имеет <b>неверный</b> формат.\n\n"
					 "Пожалуйста, убедитесь, что вы <b>вводите</b> количество <b>ETH</b> в правильном формате.\n\n"
					 " • Например, введите сумму в формате: <b><i>«3.20»</i></b>")
			else:
				raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: ITEM_ADD_ETH_RSB_ADMIN_HANDLER, TESTING: IS_ADMIN_IN_DATA")
		else:
			raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: ITEM_ADD_ETH_RSB_ADMIN_HANDLER, TESTING: IS_USER_IN_DATA")
	except:
		raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: ITEM_ADD_ETH_RSB_ADMIN_HANDLER")

"""Создаем обработчик для удаления кошелька из RSB"""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "DELETE_RSB")
async def delete_rsb_admin_handler(callback_query: types.CallbackQuery) -> DebugAdminState:
	"""Проверяем зарегистрирован пользователь в базе админов"""
	admin_data_db = load_admin_data()

	"""Загружаем базу данных о пользователе"""
	user_data_db = load_user_data()

	"""Загружаем базу данных о RSB"""
	rsb_data_db = load_rsb_data()

	try:
		if is_user_in_data(ConfigBot.USERID(callback_query), user_data_db):
			if is_admin_in_data(ConfigBot.USERID(callback_query), admin_data_db):
				"""Выводим клавиатуры для обработчика кнопки назад"""
				inline_keyboard_back_rsb_admin = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACKRSB

				await bot.edit_message_text("💬 Для <b>удаления</b> кошелька из базы <b>RSB</b>, введите, пожалуйста, ID кошелька из списка.\n\n"
											f"{ConfigBot.GETNUMBERWALLETRSB(rsb_data_db, ConfigBot.USERID(callback_query))}\n\n"
											"Благодарим за вашу активность в управлении <b>RSB - Банком</b>.",
											callback_query.from_user.id,
											callback_query.message.message_id,
											reply_markup=inline_keyboard_back_rsb_admin)
				
				"""Переходим в фазу, где вводят ID кошелька для удаления его из RSB"""
				await DebugAdminState.DeleteRSBForAdminState.set()

			else:
				raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: DELETE_RSB_ADMIN_HANDLER, TESTING: IS_ADMIN_IN_DATA")
		else:
			raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: DELETE_RSB_ADMIN_HANDLER, TESTING: IS_USER_IN_DATA")
	except:
		raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: DELETE_RSB_ADMIN_HANDLER")

"""Создаем обработчик фазы, где администратор вводит ID кошелька и удаляет его из RSB"""
@dp.message_handler(state=DebugAdminState.DeleteRSBForAdminState)
async def delete_numberWallet_rsb_admin_handler(message: types.Message) -> DebugAdminState:
	"""Проверяем зарегистрирован пользователь в базе админов"""
	admin_data_db = load_admin_data()

	"""Загружаем базу данных о пользователе"""
	user_data_db = load_user_data()

	"""Загружаем базу данных о RSB"""
	rsb_data_db = load_rsb_data()

	try:
		if is_user_in_data(ConfigBot.USERID(message), user_data_db):
			if is_admin_in_data(ConfigBot.USERID(message), admin_data_db):
				if is_rsb_in_data(ConfigBot.USERMESSAGE(message), rsb_data_db):
					"""Удаляем введенный номер кошелька из базы данных RSB"""
					del rsb_data_db[str(ConfigBot.USERMESSAGE(message))]

					save_rsb_data(rsb_data_db)

					"""Выводим клавиатуры для обработчика кнопки назад"""
					inline_keyboard_back_rsb_admin = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACKRSB

					await message.answer("💬 <b>ID кошелька</b> успешно удален из базы данных.\n\n"
						  				f" • <b>{ConfigBot.USERMESSAGE(message)}</b>\n\n"
										 "Благодарим за вашу активность в управлении <b>RSB - Банком</b>.", reply_markup=inline_keyboard_back_rsb_admin)

				elif not is_rsb_in_data(ConfigBot.USERMESSAGE(message), rsb_data_db):
					await message.answer("💬 Извините, но похоже, что кошелек с введенным <b>ID</b> отсутствует в базе данных.\n\n"
						  				 "Пожалуйста, убедитесь, что вы ввели корректный <b>ID</b> или проверьте актуальность информации.")
				else:
					raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: DELETE_ITEM_RSB_ADMIN_HANDLER, TESTING: IS_RSB_IN_DATA")
			else:
				raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: DELETE_ITEM_RSB_ADMIN_HANDLER, TESTING: IS_USER_IN_DATA")
		else:
			raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: DELETE_ITEM_RSB_ADMIN_HANDLER, TESTING: IS_USER_IN_DATA")
	except:
		raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: DELETE_ITEM_RSB_ADMIN_HANDLER")

"""Создаем обработчик для добавления кошелька в RSB"""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "ADD_RSB")
async def add_rsb_admin_handler(callback_query: types.CallbackQuery) -> DebugAdminState:
	"""Проверяем зарегистрирован пользователь в базе админов"""
	admin_data_db = load_admin_data()

	"""Загружаем базу данных о пользователе"""
	user_data_db = load_user_data()

	try:
		if is_user_in_data(ConfigBot.USERID(callback_query), user_data_db):
			if is_admin_in_data(ConfigBot.USERID(callback_query), admin_data_db):
				"""Выводим клавиатуры для обработчика кнопки назад"""
				inline_keyboard_back_rsb_admin = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACKRSB

				await bot.edit_message_text("💬 Для <b>добавления</b> ID кошелька в базу <b>RSB</b>, введите, пожалуйста, ID кошелька.\n\n"
											"После ввода <b>ID кошелька</b>, он будет включен в нашу базу данных.\n\n"
											"Благодарим за вашу активность в управлении <b>RSB - Банком</b>.",
											callback_query.from_user.id,
											callback_query.message.message_id,
									   		reply_markup=inline_keyboard_back_rsb_admin)

				"""Переходим в фазу, где вводят ID кошелька для добавления его в RSB"""
				await DebugAdminState.AddRSBForAdminState.set()

			else:
				raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: ADD_RSB_ADMIN_HANDLER, TESTING: IS_ADMIN_IN_DATA")
		else:
			raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: ADD_RSB_ADMIN_HANDLER, TESTING: IS_USER_IN_DATA")
	except:
		raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: ADD_RSB_ADMIN_HANDLER")

"""Создаем обработчик фазы, где администратор вводит ID кошелька и добавляет его в RSB"""
@dp.message_handler(state=DebugAdminState.AddRSBForAdminState)
async def add_numberWallet_rsb_admin_handler(message: types.Message) -> DebugAdminState:
	"""Проверяем зарегистрирован пользователь в базе админов"""
	admin_data_db = load_admin_data()

	"""Загружаем базу данных о пользователе"""
	user_data_db = load_user_data()

	"""Загружаем базу данных о RSB"""
	rsb_data_db = load_rsb_data()

	try:
		if is_user_in_data(ConfigBot.USERID(message), user_data_db):
			if is_admin_in_data(ConfigBot.USERID(message), admin_data_db):
				if is_rsb_in_data(ConfigBot.USERMESSAGE(message), rsb_data_db):
					await message.answer("💬 Извините, но данный <b>ID кошелька</b> уже присутствует в базе данных.\n\n"
						  				 "Пожалуйста, уточните введенные данные или проверьте актуальность информации.")

				elif not is_rsb_in_data(ConfigBot.USERMESSAGE(message), rsb_data_db):
					"""Сохраняем данные о товаре в базе данных товарах"""
					rsb_data_db[str(ConfigBot.USERMESSAGE(message))] = {
						"ETH": 0,
						"USD": 0,
						"RUB": 0,
						"CURRENT": {
							"CURRENT_ETH": 0,
							"CURRENT_USD": 0,
							"CURRENT_RUB": 0
						},
						"INTEREST": {
							"INTEREST_USER_ONE": 0,
							"INTEREST_USER_TWO": 0
						},
						"ALL_SUM_WALLET": {
							"ALL_SUM_ETH": 0,
							"ALL_SUM_USD": 0,
							"ALL_SUM_RUB": 0,
							"ALL_SUM_ETH_END": 0,
							"ALL_SUM_USD_END": 0,
							"ALL_SUM_RUB_END": 0
						}
					}

					save_rsb_data(rsb_data_db)

					"""Выводим клавиатуры для обработчика кнопки назад"""
					inline_keyboard_back_rsb_admin = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACKRSB

					await message.answer(f"💬 Кошелек добавлен в {ConfigInlineKeyboard().RSB_BANK}\n\n"
										 f" • <b>Общая сумма кошелька:</b> <code>{ConfigBot.GETRSB(ConfigBot.USERMESSAGE(message), 'ETH', True, message)}</code> <b>ETH</b> - <code>{ConfigBot.GETRSB(ConfigBot.USERMESSAGE(message), 'USD', True, message)}</code> <b>$</b> - <code>{ConfigBot.GETRSB(ConfigBot.USERMESSAGE(message), 'RUB', True, message)}</code> ₽\n\n"
										 "Благодарим за вашу активность в управление RSB - Банком.", reply_markup=inline_keyboard_back_rsb_admin)
				else:
					raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: ADD_NUMBERWALLET_RSB_ADMIN_HANDLER, TESTING: IS_RSB_IN_DATA")
			else:
				raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: ADD_NUMBERWALLET_RSB_ADMIN_HANDLER, TESTING: IS_ADMIN_IN_DATA")
		else:
			raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: ADD_NUMBERWALLET_RSB_ADMIN_HANDLER, TESTING: IS_USER_IN_DATA")
	except:
		raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: ADD_NUMBERWALLET_RSB_ADMIN_HANDLER")