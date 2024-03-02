from data.loader import dp, bot
from data.config import ConfigBot
from data.config_Keyboard import ConfigReplyKeyboard, ConfigInlineKeyboard
from data.loader_keyboard import LoaderInlineKeyboards
from data.states_groups import MarketState

from database.requests.sport_db import load_sport_data
from database.requests.user_db import load_user_data, is_user_in_data
from database.requests.version_db import get_bot_version

from misc.libraries import types, FSMContext, Union
from misc.loggers import logger

@dp.message_handler(lambda message: message.text == f"{ConfigReplyKeyboard().SPORT}")
async def sport_handler(message: types.Message) -> None:
	"""Объявляем переменные с выводом данных о пользователе, данных спорта и версии бота."""
	USER_DATA_DB = load_user_data()
	SPORT_DATA_DB = load_sport_data()
	VERSION_BOT = get_bot_version()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID."""
		USER_ID = ConfigBot.USERID(message)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			"""Объявляем переменную с выводом текущей версии пользователя."""
			USER_VERSION_BOT = ConfigBot.USERVERSIONBOT(message)

			if USER_VERSION_BOT == VERSION_BOT:
				"""Объявляем переменные с выводом информации о пользователе: SELECTED_SPORT_USER."""
				USER_SPORT = ConfigBot.USERSELECTEDSPORT(message)

				if not USER_SPORT:
					"""Выводим клавиатуру для отображения вкладок с упражнениями."""
					menu_sport_inline_keyboard = LoaderInlineKeyboards().INLINE_KEYBOARDS_MENU_SPORT

					await message.answer(f"💬 Добро пожаловать во вкладку <b>«{ConfigReplyKeyboard().SPORT[5:]}»</b>.\n\n"
						  				 "Выберите те <b>упражнения</b>, которые вас интересуют и подходят вам.\n\n",
										 reply_markup = menu_sport_inline_keyboard)

				elif USER_SPORT:
					print("Пользователь выбрал спорт.")

			elif USER_VERSION_BOT != VERSION_BOT:
				await message.answer(f"💬 <a href='https://t.me/{ConfigBot.USERNAME(message)}'>{ConfigBot.USERLASTNAME(message)}</a>! Рады сообщить, что вышла <b>новая версия</b> нашего бота с улучшениями и новыми возможностями.\n\n" 
									 "❕ Для получения всех новинок и обновлений, пожалуйста, воспользуйтесь командой <b><code>/update</code></b>.\n\n" 
									 "Спасибо за ваше внимание и активное использование нашего бота! 🤍")

			else:
				logger.warning("⚠️ USER_VERSION_BOT не ровняется к текущей версии бота.")

		elif not is_user_in_data(USER_ID, USER_DATA_DB):
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{ConfigBot.USERNAME(message)}] попытался зайти в маркет.")

		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных.")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)