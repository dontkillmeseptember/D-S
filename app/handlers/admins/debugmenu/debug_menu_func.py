from data.loader import dp, bot
from data.config import ConfigBot
from data.loader_keyboard import LoaderInlineKeyboardsAdmin

from database.requests.version_db import get_bot_version
from database.requests.user_db import load_user_data, is_user_in_data
from database.requests.admin_db import load_admin_data, is_admin_in_data
from database.requests.market_db import load_market_data
from database.requests.rsb_db import load_rsb_data
from database.requests.info_update_db import load_update_data
from database.requests.sport_db import load_sport_data

from misc.libraries import types, FSMContext
from misc.loggers import logger

@dp.message_handler(lambda message: message.text in ["!debug_admin", "!dg", "!DEBUG_ADMIN", "!dg_admin"])
@dp.callback_query_handler(lambda callback_data: callback_data.data in ["BACK_DEBUG", "BACK_DEBUG_INLINE_KEYBOARD_TWO", "BACK_DEBUG_INLINE_KEYBOARD_THREE"])
async def debug_admin_command(message_or_callbackQuery: types.Message | types.CallbackQuery, state: FSMContext) -> str:
	"""Объявляем переменные о выводе информации пользователей, администрации, текущий версии бота, информации о корзине и информации о банке"""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()
	VERSION_BOT = get_bot_version()
	MARKET_DATA_DB = load_market_data()
	RSB_DATA_DB = load_rsb_data()
	UPDATE_DATA_DB = load_update_data()
	SPORT_DATA_DB = load_sport_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID"""
		USER_ID = ConfigBot.USERID(message_or_callbackQuery)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			"""Объявляем переменную с выводом текущей версии пользователя"""
			USER_VERSION_BOT = ConfigBot.USERVERSIONBOT(message_or_callbackQuery)

			if USER_VERSION_BOT == VERSION_BOT:
				if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
					"""Объявляем переменную с выводом сообщения об информации в управление ботом"""
					INFO_DEBUG_MENU_ADMIN_MESSAGE = f"💬 Добро пожаловать в <b>«Панель Управления»</b>, <a href='https://t.me/{ConfigBot.USERNAME(message_or_callbackQuery)}'>{ConfigBot.USERLASTNAME(message_or_callbackQuery)}</a>.\n\n" \
													 "<b>Информация об пользователях:</b>\n" \
													f" • Количество зарегистрированных пользователей: <b>{ConfigBot.GETLENUSERS(USER_DATA_DB)}</b>\n" \
													f" • Количество верифицированных пользователей: <b>{ConfigBot.GETCOUNTVERIFITEDUSERS(USER_DATA_DB)}</b>\n\n" \
													 "<b>Информация об магазине:</b>\n" \
													f" • Количество товаров в корзине: <b>{ConfigBot.GETLENUSERS(MARKET_DATA_DB)}</b>\n\n" \
													 "<b>Информация об кодексе силы:</b>\n" \
													f" • Количество упражнений: <b>{ConfigBot.GETLENUSERS(SPORT_DATA_DB)}</b>\n\n" \
													 "<b>Информация об мессенджере:</b>\n" \
													f" • Количество отправленных сообщений: <b>{...}</b>\n\n" \
													 "<b>Информация об RSB:</b>\n" \
													f" • Количество зарегистрированных кошельков: <b>{ConfigBot.GETLENUSERS(RSB_DATA_DB)}</b>\n\n" \
													 "<b>Информация об обновлениях:</b>\n" \
													f" • Количество вышедших обновлений: <b>{ConfigBot.GETLENUSERS(UPDATE_DATA_DB)}</b>\n" \
													f" • Текущая версия бота: <b>v{ConfigBot().VERSION}</b>\n\n" \
													f"Управляйте с легкостью. Ваш комфорт - наша главная задача!"
					
					if isinstance(message_or_callbackQuery, types.Message):
						"""Объявляем переменную с выводом клавиатуры для меню управления ботом."""
						debug_menu_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_DEBUGMENU

						await message_or_callbackQuery.answer(INFO_DEBUG_MENU_ADMIN_MESSAGE, reply_markup = debug_menu_inline_keyboard)
					
						await state.finish()

					elif isinstance(message_or_callbackQuery, types.CallbackQuery):
						match message_or_callbackQuery.data:
							case "BACK_DEBUG":
								"""Объявляем переменную с выводом клавиатуры для меню управления ботом."""
								debug_menu_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_DEBUGMENU
							
							case "BACK_DEBUG_INLINE_KEYBOARD_TWO":
								"""Объявляем переменную с выводом клавиатуры для главного меню управления ботом вторая част."""
								debug_menu_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_DEBUGMENU_TWO
							
							case "BACK_DEBUG_INLINE_KEYBOARD_THREE":
								"""Объявляем переменную с выводом клавиатуры для главного меню управления ботом третья часть."""
								debug_menu_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_DEBUGMENU_THREE

						await bot.edit_message_text(INFO_DEBUG_MENU_ADMIN_MESSAGE, message_or_callbackQuery.from_user.id, message_or_callbackQuery.message.message_id, reply_markup = debug_menu_inline_keyboard)

						await state.finish()

					else:
						logger.error("⚠️ Произошла непредвиденная ошибка с проверкой isinstance: %s", isinstance)

				elif not is_admin_in_data(USER_ID, ADMIN_DATA_DB):
					"""Объявляем переменную с выводом сообщения о том что пользователь не админ"""
					INFO_USER_IS_NOT_ADMIN_MESSAGE = f"💬 Извините, <a href='https://t.me/{ConfigBot.USERNAME(message_or_callbackQuery)}'>{ConfigBot.USERLASTNAME(message_or_callbackQuery)}</a>, но у вас нет прав на использование этой команды."

					if isinstance(message_or_callbackQuery, types.Message):
						await message_or_callbackQuery.answer(INFO_USER_IS_NOT_ADMIN_MESSAGE)

					elif isinstance(message_or_callbackQuery, types.CallbackQuery):
						await bot.edit_message_text(INFO_USER_IS_NOT_ADMIN_MESSAGE, message_or_callbackQuery.from_user.id, message_or_callbackQuery.message.message_id)

					else:
						logger.error("⚠️ Произошла непредвиденная ошибка с проверкой isinstance: %s", isinstance)
				else:
					logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
			
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
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой версии бота: %s", USER_VERSION_BOT)

		elif not is_user_in_data(USER_ID, USER_DATA_DB):
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{ConfigBot.USERNAME(message_or_callbackQuery)}] попытался зайти в debug_admin.")
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик для следующей страницы inline клавиатуры в Debug_Admin."""
@dp.callback_query_handler(lambda callback_data: callback_data.data in ["NEXT_DEBUG", "BACK_DEBUG_TWO", "NEXT_DEBUG_THREE"])
async def next_debug_callback(callback_query: types.CallbackQuery):
	try:
		if callback_query.data in ["NEXT_DEBUG", "BACK_DEBUG_TWO"]:
			"""Объявляем переменную с выводом клавиатуры для главного меню управления ботом вторая част."""
			next_debug_menu_admin_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_DEBUGMENU_TWO
		
		elif callback_query.data == "NEXT_DEBUG_THREE":
			"""Объявляем переменную с выводом клавиатуры для главного меню управления ботом третья часть."""
			next_debug_menu_admin_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_DEBUGMENU_THREE

		await bot.edit_message_reply_markup(
			chat_id = callback_query.from_user.id,
			message_id = callback_query.message.message_id,
			reply_markup = next_debug_menu_admin_inline_keyboard
		)
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)