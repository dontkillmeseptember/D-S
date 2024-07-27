from data.loader import dp, bot
from data.config import ConfigBot
from data.config_Keyboard import ConfigInlineKeyboard, ConfigReplyKeyboard
from data.loader_keyboard import LoaderInlineKeyboardsAdmin
from data.states_groups import DebugAdminState

from database.requests.user_db import load_user_data, is_user_in_data
from database.requests.admin_db import load_admin_data, is_admin_in_data
from database.requests.market_db import load_market_data, save_market_data, is_market_in_data

from misc.libraries import types, FSMContext

"""Создаем обработчик для управление корзиной товаров"""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "MARKET")
@dp.callback_query_handler(lambda callback_data: callback_data.data == "BACK_DEBUG", state=DebugAdminState.ViewingMarketForAdminState)
@dp.callback_query_handler(lambda callback_data: callback_data.data == "BACK_MARKET", state=[DebugAdminState.AddMarketForAdminState, DebugAdminState.DeleteMarketForAdminState, DebugAdminState.CheckMarketForAdminState])
async def market_admin_handler(callback_query: types.CallbackQuery, state: FSMContext) -> str:
	"""Проверяем зарегистрирован пользователь в базе админов"""
	admin_data_db = load_admin_data()

	"""Загружаем базу данных о пользователе"""
	user_data_db = load_user_data()

	try:
		if is_user_in_data(ConfigBot.USERID(callback_query), user_data_db):
			if is_admin_in_data(ConfigBot.USERID(callback_query), admin_data_db):
				"""Получаем текущую фазу пользователя, для последующего определения участка кода"""
				current_state = await state.get_state()

				"""Выводим клавиатуры для обработчика меню панели управления"""
				inline_keyboard_menu_market_admin = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_MENUMARKET

				menu_market_admin_message = f"💬 Добро пожаловать в управление корзиной товаров.\n\n" \
											"Здесь вы можете легко управлять содержимым корзины. Вот описание к кнопкам:\n\n" \
											f" • <b>{ConfigInlineKeyboard().ADD_MARKET[2:]}</b>: Используйте эту кнопку для добавления <b>новых</b> товаров в корзину.\n\n" \
											f" • <b>{ConfigInlineKeyboard().DELETE_MARKET[:-2]}</b>: При необходимости вы можете <b>удалить</b> выбранные товары из корзины с помощью этой кнопки.\n\n" \
											f" • <b>{ConfigInlineKeyboard().CHECK_MARKET[2:-2]}</b>: Нажмите на эту кнопку, чтобы <b>просмотреть</b> полный список товаров, которые в данный момент находятся в корзине.\n\n" \
											"Спасибо за ваше внимание к деталям управления. Удачного управления."

				if current_state == "DebugAdminState:AddMarketForAdminState" or current_state == "DebugAdminState:DeleteMarketForAdminState" or current_state == "DebugAdminState:CheckMarketForAdminState" or current_state == None:
					await bot.edit_message_text(menu_market_admin_message,
												callback_query.from_user.id, 
												callback_query.message.message_id,
												reply_markup=inline_keyboard_menu_market_admin)
					
					await state.finish()
				
				elif current_state == "DebugAdminState:ViewingMarketForAdminState":
					"""Удаляем сообщение предыдущие сообщение"""
					await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)

					await bot.send_message(callback_query.message.chat.id,
										menu_market_admin_message,
										reply_markup=inline_keyboard_menu_market_admin)
					
					await state.finish()
				else:
					raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: ADD_VERIFY_HANDLER, TESTING: CURRENT_STATE")
			else:
				raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: ADD_VERIFY_HANDLER, TESTING: IS_ADMIN_IN_DATA")
		else:
			raise ValueError("ERROR: 161, TEXT: ВЕРИФИЦИРОВАННЫЙ ПОЛЬЗОВАТЕЛЬ ПОПЫТАЛСЯ ЗАЙТИ В МЕНЮ ДЛЯ ВЕРИФИКАЦИИ ПОЛЬЗОВАТЕЛЕЙ")
	except:
		raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: ADD_VERIFY_HANDLER")

"""Создаем обработчик для просмотра товаров в корзине"""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "CHECK_MARKET")
async def check_market_admin_handler(callback_query: types.CallbackQuery) -> DebugAdminState:
	"""Проверяем зарегистрирован пользователь в базе админов"""
	admin_data_db = load_admin_data()

	"""Загружаем базу данных о пользователе"""
	user_data_db = load_user_data()

	"""Загружаем данные о товарах из JSON файла"""
	market_data_db = load_market_data()

	try:
		if is_user_in_data(ConfigBot.USERID(callback_query), user_data_db):
			if is_admin_in_data(ConfigBot.USERID(callback_query), admin_data_db):
				"""Выводим клавиатуры для обработчика кнопки назад"""
				inline_keyboard_keyboard_back_market = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_MARKET

				await bot.edit_message_text("💬 Для <b>просмотра</b> подробной информации о товаре введите его артикул из списка:\n\n"
											f"{ConfigBot.GETARTICLEMARKET(market_data_db, ConfigBot.USERID(callback_query))}\n\n"
											"Благодарим за вашу активность в управлении корзиной товаров.",
											callback_query.from_user.id,
											callback_query.message.message_id,
									   		reply_markup=inline_keyboard_keyboard_back_market)

				"""Переходим в фазу, где вводят товар для добавления в корзину"""
				await DebugAdminState.ViewingMarketForAdminState.set()

			else:
				raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: DELETE_MARKET_ADMIN_HANDLER, TESTING: IS_ADMIN_IN_DATA")
		else:
			raise ValueError("ERROR: 161, TEXT: ВЕРИФИЦИРОВАННЫЙ ПОЛЬЗОВАТЕЛЬ ПОПЫТАЛСЯ ЗАЙТИ В МЕНЮ ДЛЯ ВЕРИФИКАЦИИ ПОЛЬЗОВАТЕЛЕЙ")
	except:
		raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: DELETE_MARKET_ADMIN_HANDLER")

"""Создаем обработчик фазы, где администратор вводит артикул товара и удаляет его из корзины"""
@dp.message_handler(state=DebugAdminState.ViewingMarketForAdminState)
async def check_item_market_admin_handler(message: types.Message) -> str:
	"""Проверяем зарегистрирован пользователь в боте"""
	user_data_db = load_user_data()

	"""Загружаем данные о товарах из JSON файла"""
	market_data_db = load_market_data()

	try:
		if is_user_in_data(ConfigBot.USERID(message), user_data_db):
			"""Проверяем зарегистрирован пользователь в базе админов"""
			admin_data_db = load_admin_data()

			if is_admin_in_data(ConfigBot.USERID(message), admin_data_db):
				if is_market_in_data(ConfigBot.USERMESSAGE(message), market_data_db):
					"""Выводим клавиатуры для обработчика кнопки назад"""
					inline_keyboards_back_market_debug_market = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_DEBUG_MARKET

					"""Создаем переменную с текстом для маркета"""
					message_market = f"💬 Информация о товаре:\n\n" \
									 f"<a href='{ConfigBot.GETMARKET(ConfigBot.USERMESSAGE(message), 'URL_SITE')}'>{ConfigBot.GETMARKET(ConfigBot.USERMESSAGE(message), 'NAME_MARKET')}</a> • <code>{ConfigBot.USERMESSAGE(message)}</code>\n\n" \
									 f" • <b>Комментарий:</b> {ConfigBot.GETMARKET(ConfigBot.USERMESSAGE(message), 'MESSAGE')}\n\n" \
									 f" • <b>Цена:</b> {ConfigBot.GETPRICE(ConfigBot.USERMESSAGE(message))} ₽\n\n" \
									 "Если вам нужно найти еще один товар, вы можете ввести новый артикул и продолжить поиск."

					await bot.send_photo(message.chat.id, photo=f"{ConfigBot.GETMARKET(ConfigBot.USERMESSAGE(message), 'URL_PHOTO')}", caption=message_market, reply_markup=inline_keyboards_back_market_debug_market)
				else:
					await message.answer("💬 Извините, но похоже, что товар с указанным <b>артикулом</b> не существует в корзине.\n\n"
						  				 "Убедитесь, что вы ввели правильный артикул, и повторите попытку.")
			else:
				raise ValueError("ERROR: 161, TEXT: НЕЗАРЕГИСТРИРОВАННЫЙ ПОЛЬЗОВАТЕЛЬ ПОПЫТАЛСЯ ВВЕСТИ ДОБАВИТЬ ТОВАР В КОРЗИНУ")
		else:
			raise ValueError("ERROR: 161, TEXT: НЕЗАРЕГИСТРИРОВАННЫЙ ПОЛЬЗОВАТЕЛЬ ПОПЫТАЛСЯ ВВЕСТИ ДОБАВИТЬ ТОВАР В КОРЗИНУ")
	except:
		raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: ADD_ITEM_MARKET_ADMIN_HANDLER")

"""Создаем обработчик для удаления товаров из корзины"""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "DELETE_MARKET")
async def delete_market_admin_handler(callback_query: types.CallbackQuery) -> DebugAdminState:
	"""Проверяем зарегистрирован пользователь в базе админов"""
	admin_data_db = load_admin_data()

	"""Загружаем базу данных о пользователе"""
	user_data_db = load_user_data()

	"""Загружаем данные о товарах из JSON файла"""
	market_data_db = load_market_data()

	try:
		if is_user_in_data(ConfigBot.USERID(callback_query), user_data_db):
			if is_admin_in_data(ConfigBot.USERID(callback_query), admin_data_db):
				"""Выводим клавиатуры для обработчика кнопки назад"""
				inline_keyboard_keyboard_back_market = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_MARKET

				await bot.edit_message_text("💬 Для <b>удаления</b> товара из корзины введите артикул товара, который вы хотели бы удалить:\n\n"
											f"{ConfigBot.GETARTICLEMARKET(market_data_db, ConfigBot.USERID(callback_query))}\n\n"
											"Благодарим за вашу активность в управлении корзиной товаров.",
											callback_query.from_user.id,
											callback_query.message.message_id,
									   		reply_markup=inline_keyboard_keyboard_back_market)

				"""Переходим в фазу, где вводят товар для добавления в корзину"""
				await DebugAdminState.DeleteMarketForAdminState.set()

			else:
				raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: DELETE_MARKET_ADMIN_HANDLER, TESTING: IS_ADMIN_IN_DATA")
		else:
			raise ValueError("ERROR: 161, TEXT: ВЕРИФИЦИРОВАННЫЙ ПОЛЬЗОВАТЕЛЬ ПОПЫТАЛСЯ ЗАЙТИ В МЕНЮ ДЛЯ ВЕРИФИКАЦИИ ПОЛЬЗОВАТЕЛЕЙ")
	except:
		raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: DELETE_MARKET_ADMIN_HANDLER")

"""Создаем обработчик фазы, где администратор вводит артикул товара и удаляет его из корзины"""
@dp.message_handler(state=DebugAdminState.DeleteMarketForAdminState)
async def delete_item_market_admin_handler(message: types.Message) -> str:
	"""Проверяем зарегистрирован пользователь в боте"""
	user_data_db = load_user_data()

	"""Загружаем данные о товарах из JSON файла"""
	market_data_db = load_market_data()

	try:
		if is_user_in_data(ConfigBot.USERID(message), user_data_db):
			"""Проверяем зарегистрирован пользователь в базе админов"""
			admin_data_db = load_admin_data()

			if is_admin_in_data(ConfigBot.USERID(message), admin_data_db):
				if is_market_in_data(ConfigBot.USERMESSAGE(message), market_data_db):
					"""Удаляем товар из корзины"""
					del market_data_db[str(ConfigBot.USERMESSAGE(message))]

					save_market_data(market_data_db)

					"""Выводим клавиатуры для обработчика кнопки назад"""
					inline_keyboard_keyboard_back_market = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_MARKET

					await message.answer(f"💬 Отлично, товар с артикулом <code>{ConfigBot.USERMESSAGE(message)}</code> успешно удален из корзины.\n\n"
						  				 f"Если у вас есть дополнительные вопросы или потребуется дополнительная информация, не стесняйтесь обращаться к нашей <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрации</b></a>.", 
										 reply_markup=inline_keyboard_keyboard_back_market)
				else:
					await message.answer("💬 Извините, но похоже, что товар с указанным <b>артикулом</b> не существует в корзине.\n\n"
						  				 "Убедитесь, что вы ввели правильный артикул, и повторите попытку.")
			else:
				raise ValueError("ERROR: 161, TEXT: НЕЗАРЕГИСТРИРОВАННЫЙ ПОЛЬЗОВАТЕЛЬ ПОПЫТАЛСЯ ВВЕСТИ ДОБАВИТЬ ТОВАР В КОРЗИНУ")
		else:
			raise ValueError("ERROR: 161, TEXT: НЕЗАРЕГИСТРИРОВАННЫЙ ПОЛЬЗОВАТЕЛЬ ПОПЫТАЛСЯ ВВЕСТИ ДОБАВИТЬ ТОВАР В КОРЗИНУ")
	except:
		raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: ADD_ITEM_MARKET_ADMIN_HANDLER")


"""Создаем обработчик для добавления товаров в корзину"""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "ADD_MARKET")
async def add_market_admin_handler(callback_query: types.CallbackQuery) -> DebugAdminState:
	"""Проверяем зарегистрирован пользователь в базе админов"""
	admin_data_db = load_admin_data()

	"""Загружаем базу данных о пользователе"""
	user_data_db = load_user_data()

	try:
		if is_user_in_data(ConfigBot.USERID(callback_query), user_data_db):
			if is_admin_in_data(ConfigBot.USERID(callback_query), admin_data_db):
				"""Выводим клавиатуры для обработчика кнопки назад"""
				inline_keyboard_keyboard_back_market = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_MARKET

				await bot.edit_message_text("💬 Для <b>добавления</b> нового товара в корзину, введите следующую информацию:\n\n"
						   			   		" • <b>Артикул:</b> [Введите артикул товара]\n"
											" • <b>URL Фотографии:</b> [Укажите URL ссылку на фотографию]\n"
											" • <b>URL Ссылка на Сайт Товара:</b> [Укажите URL ссылку на сайт]\n"
											" • <b>Название Товара:</b> [Введите название товара]\n"
											" • <b>Комментарий:</b> [Добавьте свой комментарий к товару]\n\n"
											"Благодарим за вашу активность в управлении корзиной товаров.",
											callback_query.from_user.id,
											callback_query.message.message_id,
									   		reply_markup=inline_keyboard_keyboard_back_market)

				"""Переходим в фазу, где вводят товар для добавления в корзину"""
				await DebugAdminState.AddMarketForAdminState.set()

			else:
				raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: ADD_MARKET_ADMIN_HANDLER, TESTING: IS_ADMIN_IN_DATA")
		else:
			raise ValueError("ERROR: 161, TEXT: ВЕРИФИЦИРОВАННЫЙ ПОЛЬЗОВАТЕЛЬ ПОПЫТАЛСЯ ЗАЙТИ В МЕНЮ ДЛЯ ВЕРИФИКАЦИИ ПОЛЬЗОВАТЕЛЕЙ")
	except:
		raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: ADD_MARKET_ADMIN_HANDLER")

"""Создаем обработчик фазы, где администратор вводит товар и добавляет его в корзину"""
@dp.message_handler(state=DebugAdminState.AddMarketForAdminState)
async def add_item_market_admin_handler(message: types.Message) -> str:
	"""Проверяем зарегистрирован пользователь в боте"""
	user_data_db = load_user_data()

	"""Загружаем данные о товарах из JSON файла"""
	market_data_db = load_market_data()

	try:
		if is_user_in_data(ConfigBot.USERID(message), user_data_db):
			"""Проверяем зарегистрирован пользователь в базе админов"""
			admin_data_db = load_admin_data()

			if is_admin_in_data(ConfigBot.USERID(message), admin_data_db):
				"""Разделяем сообщение на артикул, URL Фотографии, URL Сайта, Цена товара, Название товара и Сообщение к товару"""
				parts = ConfigBot.USERMESSAGE(message).split()

				if len(parts) > 5:
					"""Выводим из сообщения - Артикул"""
					ARTICLE_HUMBER = parts[0]

					if is_market_in_data(ARTICLE_HUMBER, market_data_db):
						await message.answer("💬 Извините, но похоже, что товар с таким <b>артикулом</b> уже существует в корзине товаров.\n\n"
						   					 "Пожалуйста, уточните данные и убедитесь, что вы вводите <b>уникальные</b> артикулы для каждого товара.")

					elif not is_market_in_data(ARTICLE_HUMBER, market_data_db):
						"""Выводим из сообщения - URL ссылку на фотографию"""
						URL_PHOTO = parts[1]
						"""Выводим из сообщения - URL ссылку на сайт товара"""
						URL_SITE = parts[2]
						"""Выводим из сообщения - Название товара"""
						NAME_MARKET = parts[3]
						"""Выводим из сообщения - Комментарий к товару"""
						MESSAGE = " ".join(parts[4:])

						"""Сохраняем данные о товаре в базе данных товарах"""
						market_data_db[str(ARTICLE_HUMBER)] = {
							"URL_PHOTO": URL_PHOTO,
							"URL_SITE": URL_SITE,
							"NAME_MARKET": NAME_MARKET,
							"MESSAGE": MESSAGE
						}

						save_market_data(market_data_db)

						"""Выводим клавиатуры для обработчика кнопки назад"""
						inline_keyboard_keyboard_back_market = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_BACK_MARKET

						await message.answer(f"💬 Данные товара для добавления в {ConfigReplyKeyboard().MARKET}.\n\n"
											f" • <b>Артикул:</b> <b><code>{ARTICLE_HUMBER}</code></b>\n"
											f" • <b>URL Фотографии:</b> <a href='{URL_PHOTO}'><b>Ссылка на фотографию</b></a>\n"
											f" • <b>URL Ссылка на Сайт Товара:</b> <a href='{URL_SITE}'><b>Ссылка на сайт товара</b></a>\n"
											f" • <b>Цена:</b> {ConfigBot.GETPRICE(ARTICLE_HUMBER)} ₽\n"
											f" • <b>Название Товара:</b> {NAME_MARKET}\n"
											f" • <b>Комментарий:</b> {MESSAGE}\n\n"
											"Благодарим за вашу активность в управлении корзиной товаров.",
											reply_markup=inline_keyboard_keyboard_back_market)
 
						"""Отправляем уведомление всем пользователем, что новый товар добавлен в корзину"""
						for users_data_id in user_data_db:
							if users_data_id != ConfigBot(message).USERID and users_data_id not in admin_data_db:
								await bot.send_message(int(users_data_id),
										f"💬 <a href='{ConfigBot.USERNAMEBOT(int(users_data_id))}'>{ConfigBot.USERLASTNAMEBOT(int(users_data_id))}</a>, мы рады сообщить вам, что в нашем магазине появился <b>новый</b> товар!\n\n"
										f" • <b>Название Товара:</b> {NAME_MARKET}\n\n"
										f"Для просмотра подробностей и возможного оформления заказа, просто зайдите во вкладку <b>{ConfigReplyKeyboard().MARKET}</b>.")

				elif len(parts) < 5:
					await message.answer("💬 Извините, но для добавления товара в корзину необходимо предоставить <b>полную</b> информацию. Пожалуйста, убедитесь, что вы ввели следующие данные:\n\n"
						                 " • <b>Артикул:</b> [Введите артикул товара]\n"
										 " • <b>URL Фотографии:</b> [Укажите URL ссылку на фотографию]\n"
										 " • <b>URL Ссылка на Сайт Товара:</b> [Укажите URL ссылку на сайт]\n"
										 " • <b>Цена:</b> [Укажите цену товара]\n"
										 " • <b>Название Товара:</b> [Введите название товара]\n"
										 " • <b>Комментарий:</b> [Добавьте свой комментарий к товару]\n\n"
										 "Пожалуйста, убедитесь, что все поля <b>заполнены</b>, и повторите попытку.")
			else:
				raise ValueError("ERROR: 161, TEXT: НЕЗАРЕГИСТРИРОВАННЫЙ ПОЛЬЗОВАТЕЛЬ ПОПЫТАЛСЯ ВВЕСТИ ДОБАВИТЬ ТОВАР В КОРЗИНУ")
		else:
			raise ValueError("ERROR: 161, TEXT: НЕЗАРЕГИСТРИРОВАННЫЙ ПОЛЬЗОВАТЕЛЬ ПОПЫТАЛСЯ ВВЕСТИ ДОБАВИТЬ ТОВАР В КОРЗИНУ")
	except:
		raise ValueError("ERROR: 404, FILE: DEBUG_ADMIN_FUNC, FUNC: ADD_ITEM_MARKET_ADMIN_HANDLER")