from data.loader import dp, bot
from data.config import ConfigBot
from data.config_Keyboard import ConfigReplyKeyboard, ConfigInlineKeyboard
from data.loader_keyboard import LoaderInlineKeyboards
from data.states_groups import MarketState

from database.requests.market_db import load_market_data, is_market_in_data
from database.requests.user_db import load_user_data, is_user_in_data
from database.requests.version_db import get_bot_version

from misc.libraries import types, FSMContext, Union
from misc.loggers import logger

@dp.message_handler(lambda message: message.text == f"{ConfigReplyKeyboard().MARKET}")
@dp.callback_query_handler(lambda callback_data: callback_data.data == "BACK_MARKET_USERS", state = [MarketState.CheckMarketState])
async def market_handler(message_or_callbackQuery: Union[types.Message, types.CallbackQuery], state: FSMContext) -> None:
	"""Объявляем переменные с выводом данных о пользователе, данных маркета и версии бота"""
	MARKET_DATA_DB = load_market_data()
	VERSION_BOT = get_bot_version()
	USER_DATA_DB = load_user_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID"""
		USER_ID = ConfigBot.USERID(message_or_callbackQuery)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			"""Объявляем переменную с выводом текущей версии пользователя"""
			USER_VERSION_BOT = ConfigBot.USERVERSIONBOT(message_or_callbackQuery)

			if USER_VERSION_BOT == VERSION_BOT:
				""""Объявляем переменные о выводе клавиатуры меню маркета для пользователей"""
				market_menu_users_inline_keyboard = LoaderInlineKeyboards(message_or_callbackQuery).INLINE_KEYBOARDS_MARKETMENU_USERS

				if isinstance(message_or_callbackQuery, types.Message):
					await message_or_callbackQuery.answer(f"💬 Добро пожаловать во вкладку <b>«{ConfigReplyKeyboard().MARKET[4:]}»</b>.\n\n"
															f" • На данный момент у вас <b>{ConfigBot.GETLENUSERS(MARKET_DATA_DB)}</b> товаров в корзине.\n\n"
															f"❕ Для просмотра полного <b>списка товаров</b> и <b>дополнительных деталей</b>, пожалуйста, нажмите на кнопку <b>«{ConfigInlineKeyboard().CHECK_MARKET[2:-2]}»</b>.", 
															reply_markup = market_menu_users_inline_keyboard)
					
					await state.finish()

				elif isinstance(message_or_callbackQuery, types.CallbackQuery):
					await bot.edit_message_text( f"💬 Добро пожаловать во вкладку <b>«{ConfigReplyKeyboard().MARKET[4:]}»</b>.\n\n"
													f" • На данный момент у вас <b>{len(MARKET_DATA_DB)}</b> товаров в корзине.\n\n"
													f"❕ Для просмотра полного <b>списка товаров</b> и <b>дополнительных деталей</b>, пожалуйста, нажмите на кнопку <b>«{ConfigInlineKeyboard().CHECK_MARKET[2:-2]}»</b>.",
													message_or_callbackQuery.from_user.id,
													message_or_callbackQuery.message.message_id,
													reply_markup = market_menu_users_inline_keyboard)
					
					await state.finish()
				else:
					logger.warning("⚠️ Произошел сбой с ISINSTANCE.")

			elif USER_VERSION_BOT != VERSION_BOT:
				if isinstance(message_or_callbackQuery, types.Message):
					await message_or_callbackQuery.answer(f"💬 <a href='https://t.me/{ConfigBot.USERNAME(message_or_callbackQuery)}'>{ConfigBot.USERLASTNAME(message_or_callbackQuery)}</a>! Рады сообщить, что вышла <b>новая версия</b> нашего бота с улучшениями и новыми возможностями.\n\n" 
															"❕ Для получения всех новинок и обновлений, пожалуйста, воспользуйтесь командой <b><code>/update</code></b>.\n\n" 
															"Спасибо за ваше внимание и активное использование нашего бота! 🤍")
					
				elif isinstance(message_or_callbackQuery, types.CallbackQuery):
					await bot.send_message(message_or_callbackQuery.message.chat.id, 
											f"💬 <a href='https://t.me/{ConfigBot.USERNAME(message_or_callbackQuery)}'>{ConfigBot.USERLASTNAME(message_or_callbackQuery)}</a>! Рады сообщить, что вышла <b>новая версия</b> нашего бота с улучшениями и новыми возможностями.\n\n" 
											"❕ Для получения всех новинок и обновлений, пожалуйста, воспользуйтесь командой <b><code>/update</code></b>.\n\n" 
											"Спасибо за ваше внимание и активное использование нашего бота! 🤍")
				else:
					logger.warning("⚠️ Произошел сбой с ISINSTANCE.")
			else:
				logger.warning("⚠️ USER_VERSION_BOT не ровняется к текущей версии бота.")
		else:
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{ConfigBot.USERNAME(message_or_callbackQuery)}] попытался зайти в маркет.")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик для просмотра товаров в корзине"""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "NONE_SEARCH", state = MarketState.CheckMarketState)
async def back_market_check_user_handler(callback_query: types.CallbackQuery, state: FSMContext) -> MarketState:
	"""Объявляем переменные с выводом данных о пользователе и данных маркета"""
	USER_DATA_DB = load_user_data()
	MARKET_DATA_DB = load_market_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID"""
		USER_ID = ConfigBot.USERID(callback_query)

		if is_user_in_data(USER_ID, USER_DATA_DB):
				await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)				

				""""Объявляем переменные о выводе клавиатуры меню маркета для пользователей"""
				market_menu_users_inline_keyboard = LoaderInlineKeyboards(callback_query).INLINE_KEYBOARDS_MARKETMENU_USERS

				await bot.send_message(callback_query.message.chat.id,
									   f"💬 Добро пожаловать во вкладку <b>«{ConfigReplyKeyboard().MARKET[4:]}»</b>.\n\n"
									   f" • На данный момент у вас <b>{len(MARKET_DATA_DB)}</b> товаров в корзине.\n\n"
									   f"❕ Для просмотра полного <b>списка товаров</b> и <b>дополнительных деталей</b>, пожалуйста, нажмите на кнопку <b>«{ConfigInlineKeyboard().CHECK_MARKET[2:-2]}»</b>.",
									   reply_markup = market_menu_users_inline_keyboard)
					
				await state.finish()
		else:
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{ConfigBot.USERNAME(callback_query)}] попытался войти для просмотра товаров из корзины.")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик для просмотра товаров в корзине"""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "CHECK_MARKET_USERS")
async def check_market_user_handler(callback_query: types.CallbackQuery) -> MarketState:
	"""Объявляем переменные с выводом данных о пользователе и данных маркета"""
	USER_DATA_DB = load_user_data()
	MARKET_DATA_DB = load_market_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID"""
		USER_ID = ConfigBot.USERID(callback_query)

		if is_user_in_data(USER_ID, USER_DATA_DB):
				"""Объявляем переменную с выводом клавиатуры для возвращения в меню маркета"""
				back_market_inline_keyboard = LoaderInlineKeyboards(callback_query).INLINE_KEYBOARDS_BACK_MARKET

				await bot.edit_message_text("💬 Для <b>просмотра</b> подробной информации о товаре введите его артикул из списка:\n\n"
											f"{ConfigBot.GETARTICLEMARKET(MARKET_DATA_DB, ConfigBot.USERID(callback_query))}\n\n"
											"Благодарим за вашу активность в управлении корзиной товаров.",
											callback_query.from_user.id,
											callback_query.message.message_id,
									   		reply_markup = back_market_inline_keyboard)

				"""Переходим в фазу, где вводят товар для добавления в корзину"""
				await MarketState.CheckMarketState.set()
		else:
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{ConfigBot.USERNAME(callback_query)}] попытался войти для просмотра товаров из корзины.")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

@dp.message_handler(state = MarketState.CheckMarketState)
async def check_item_market_user_handler(message: types.Message) -> str:
	"""Объявляем переменные с выводом данных о пользователе и данных маркета"""
	USER_DATA_DB = load_user_data()
	MARKET_DATA_DB = load_market_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID"""
		USER_ID = ConfigBot.USERID(message)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			"""Объявляем переменную c выводом информации о пользователя: USER_MESSAGE"""
			USER_MESSAGE = ConfigBot.USERMESSAGE(message)

			if is_market_in_data(USER_MESSAGE, MARKET_DATA_DB):
				"""Объявляем переменную с выводом клавиатуры для возвращения в список товаров маркета"""
				back_market_check_inline_keyboards = LoaderInlineKeyboards(message).INLINE_KEYBOARDS_BACK_MARKET_CHECK

				"""Объявляем переменную с выводом сообщения о информации товара из маркета"""
				INFO_ITEM_MARKET_MESSAGE = f"💬 Информация о товаре:\n\n" \
										   f"<a href='{ConfigBot.GETMARKET(USER_MESSAGE, 'URL_SITE')}'>{ConfigBot.GETMARKET(USER_MESSAGE, 'NAME_MARKET')}</a> • <code>{USER_MESSAGE}</code>\n\n" \
										   f" • <b>Комментарий:</b> {ConfigBot.GETMARKET(USER_MESSAGE, 'MESSAGE')}\n\n" \
										   f" • <b>Цена:</b> {ConfigBot.GETPRICE(USER_MESSAGE)} ₽\n\n" \
											"Если вам нужно найти еще один товар, вы можете ввести новый артикул и продолжить поиск."

				await bot.send_photo(message.chat.id, photo = f"{ConfigBot.GETMARKET(USER_MESSAGE, 'URL_PHOTO')}", caption = INFO_ITEM_MARKET_MESSAGE, reply_markup = back_market_check_inline_keyboards)
			
			else:
				await message.answer("⚠️ Извините, но похоже, что товар с указанным <b>артикулом</b> не существует в корзине.\n\n"
						  			 "Убедитесь, что вы ввели правильный артикул, и повторите попытку.")
		else:
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{ConfigBot.USERNAME(message)}] попытался войти для просмотра товаров из корзины.")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)