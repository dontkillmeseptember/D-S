from data.loader import dp
from data.config import ConfigBot
from data.config_Keyboard import ConfigReplyKeyboard

from database.requests.ration_db import load_ration_data
from database.requests.user_db import load_user_data, is_user_in_data, save_user_data
from database.requests.version_db import get_bot_version

from misc.libraries import types
from misc.loggers import logger

@dp.message_handler(lambda Message: Message.text == f"{ConfigReplyKeyboard().RATION}")
async def Ration_Handler(Message: types.Message) -> None:
	USER_DATA_DB = load_user_data()
	VERSION_BOT = get_bot_version()

	try:
		USER_ID = ConfigBot.USERID(Message)
		USER_NAME = ConfigBot.USERNAME(Message)
		USER_LAST_NAME = ConfigBot.USERLASTNAME(Message)

		USER_WEEKDAY = ConfigBot.GET_CURRENT_DAY()
		RATION_SELECT_USER = ConfigBot.RATION_SELECT_USERS()

		START_MESSAGE = f"<a href='https://t.me/{USER_NAME}'>{USER_LAST_NAME}</a>"

		if is_user_in_data(USER_ID, USER_DATA_DB):
			USER_VERSION_BOT = ConfigBot.USERVERSIONBOT(Message)

			WEEKDAYS_TRANSLATION_RUSSIAN = {
				"MONDAY": "Понедельник",
				"TUESDAY": "Вторник",
				"WEDNESDAY": "Среда",
				"THURSDAY": "Четверг",
				"FRIDAY": "Пятница",
				"SATURDAY": "Суббота",
				"SUNDAY": "Воскресенье"
			}

			if USER_VERSION_BOT == VERSION_BOT:
				if RATION_SELECT_USER:
					await Message.answer(f" • {WEEKDAYS_TRANSLATION_RUSSIAN.get(USER_WEEKDAY, '')} • {ConfigBot.GET_RATION(RATION_SELECT_USER, 'EMOJI_RATION')} {ConfigBot.GET_RATION(RATION_SELECT_USER, 'NAME_RATION')}\n\n"
														f"{ConfigBot.GET_RATION(RATION_SELECT_USER, 'DESCRIPTION_RATION', USER_WEEKDAY)}\n\n"
														f" • 🌇 Завтрак — 8:00 AM:\n"
														f"    ↳ <a href='{ConfigBot.GET_RATION(RATION_SELECT_USER, 'BREAKFAST_LINK_RECIPE', USER_WEEKDAY)}'>{ConfigBot.GET_RATION(RATION_SELECT_USER, 'BREAKFAST', USER_WEEKDAY)}</a>\n\n"
														f" • 🏙️ Обед — 3:00 PM:\n"
														f"    ↳ <a href='{ConfigBot.GET_RATION(RATION_SELECT_USER, 'LUNCH_LINK_RECIPE', USER_WEEKDAY)}'>{ConfigBot.GET_RATION(RATION_SELECT_USER, 'LUNCH', USER_WEEKDAY)}</a>\n\n"
														f" • 🌃 Ужин — 11:30 PM:\n"
														f"    ↳ <a href='{ConfigBot.GET_RATION(RATION_SELECT_USER, 'DINNER_LINK_RECIPE', USER_WEEKDAY)}'>{ConfigBot.GET_RATION(RATION_SELECT_USER, 'DINNER', USER_WEEKDAY)}</a>\n\n"
														"❕ Рацион обновляется ровно в <b>00:00</b> по <b>МСК</b>.")
					
					# await ConfigBotAsync.SAVE_MESSAGE_ID(user_id = USER_ID, send_message = SEND_MESSAGE)
				
				elif not RATION_SELECT_USER:
					await Message.answer(f"{START_MESSAGE}, в настоящее время <b>администратор еще не зарегистрировал выбранный рацион</b>.\n\n"
						  				  " • Мы уведомим вас, когда рацион будет доступен.\n\n"
										  "Благодарим за ваше внимание и заботу о своем здоровье! 🤍")
			
			elif not USER_VERSION_BOT == VERSION_BOT:
				await Message.answer(f"💬 {START_MESSAGE}! Рады сообщить, что вышла <b>новая версия</b> нашего бота с улучшениями и новыми возможностями.\n\n" 
									 "❕ Для получения всех новинок и обновлений, пожалуйста, воспользуйтесь командой <b><code>/update</code></b>.\n\n" 
									 "Спасибо за ваше внимание и активное использование нашего бота! 🤍")
			
			else:
				logger.warning("⚠️ USER_VERSION_BOT не ровняется к текущей версии бота.")

		elif not is_user_in_data(USER_ID, USER_DATA_DB):
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{USER_NAME}] попытался зайти в кодекс силы.")

		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных.")

	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)