from data.loader import dp, bot
from data.config import ConfigBot, ConfigBotAsync
from data.config_Keyboard import ConfigReplyKeyboard
from data.loader_keyboard import LoaderReplyKeyboards

from database.requests.version_db import get_bot_version
from database.requests.user_db import load_user_data, is_user_in_data, save_user_data

from misc.libraries import types, RetryAfter
from misc.loggers import logger

"""Создаем обработчик команды /update"""
@dp.message_handler(commands=("update"))
async def update_command(message: types.Message) -> None:
	"""Объявляем переменные с выводом данных о пользователе, версии бота и клавиатуры."""
	USER_DATA_DB = load_user_data()
	VERSION_BOT = get_bot_version()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID."""
		USER_ID = ConfigBot.USERID(message)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			"""Объявляем переменную с выводом текущей версии пользователя."""
			USER_VERSION_BOT = ConfigBot.USERVERSIONBOT(message)

			if USER_VERSION_BOT == VERSION_BOT:
				await message.answer(f"💬 <a href='https://t.me/{ConfigBot.USERNAME(message)}'>{ConfigBot.USERLASTNAME(message)}</a>, благодарим вас за интерес к нашему боту.\n\n"
									 f"Мы рады сообщить, что вы уже используете <b>последнюю версию бота - v{VERSION_BOT}</b>\n\n"
									 f"Если у вас есть какие-либо вопросы или нужна помощь, не стесняйтесь обращаться к <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрации</b></a>.")
				
			elif USER_VERSION_BOT != VERSION_BOT:
				"""Объявляем переменную с выводом клавиатуры для обновления бота."""
				update_bot_reply_keyboard = LoaderReplyKeyboards(message).KEYBOARDS_UPDATE_BOT

				await message.answer(f"💬 <a href='https://t.me/{ConfigBot.USERNAME(message)}'>{ConfigBot.USERLASTNAME(message)}</a>, мы хотим сообщить вам, что вы используете <b>устаревшую версию бота - v{USER_VERSION_BOT}</b>.\n\n"
						 			 f"Для получения новых функций и улучшенного опыта, пожалуйста, обновите нашего бота до <b>последней версии - v{VERSION_BOT}</b>.\n\n"
									 f"❕ Чтобы обновить бота, нажмите на кнопку <b>«{ConfigReplyKeyboard().DOWNLOAD_UPDATE[2:] + VERSION_BOT}»</b>. Спасибо за ваше внимание к обновлениям.\n\nЕсли у вас есть какие-либо вопросы или нужна помощь, не стесняйтесь обращаться к <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрации</b></a>.", 
									 reply_markup = update_bot_reply_keyboard)

			else:
				logger.warning("⚠️ USER_VERSION_BOT не ровняется к текущей версии бота.")
		
		elif not is_user_in_data(USER_ID, USER_DATA_DB):
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{ConfigBot.USERNAME(message)}] попытался вести команду /update.")
		
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных.")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем главный обработчик для команды /update"""
@dp.message_handler(lambda message: message.text == ConfigReplyKeyboard().DOWNLOAD_UPDATE + ConfigBot().VERSION + " •")
async def update_handler(message: types.Message) -> None:
	"""Объявляем переменную с выводом информации о пользователе и версии бота."""
	USER_DATA_DB = load_user_data()
	VERSION_BOT = get_bot_version()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID."""
		USER_ID = ConfigBot.USERID(message)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			message_text = await message.answer("ㅤ")

			"""Отправляем сообщение и обновляем информацию о ходе выполнения этапа 1, 2 и 3."""
			await ConfigBotAsync.UPDATE_PROGRESS(msg = message_text, update_stage = 1, time_sleep = 5, version = VERSION_BOT, type = message)
			await ConfigBotAsync.UPDATE_PROGRESS(msg = message_text, update_stage = 2, time_sleep = 10, version = VERSION_BOT, type = message)
			await ConfigBotAsync.UPDATE_PROGRESS(msg = message_text, update_stage = 3, time_sleep = 5, version = VERSION_BOT, type = message)

			"""Удаляем последнее сообщение."""
			await bot.delete_message(message.chat.id, message_text.message_id)

			"""Объявляем переменную которая сохраняет новую версию бота для пользователя."""
			USER_DATA_DB[str(ConfigBot.USERID(message))]["VERSION_BOT"] = VERSION_BOT

			save_user_data(USER_DATA_DB)

			"""Отобразите конечное сообщение с помощью клавиатуры меню."""
			finish_update_reply_keyboards = LoaderReplyKeyboards(message).KEYBOARDS_FINISH_UPDATE

			await message.answer(f"🎉 Поздравляем, <a href='https://t.me/{ConfigBot.USERNAME(message)}'>{ConfigBot.USERLASTNAME(message)}</a>, обновление <b>v{VERSION_BOT}</b> успешно установлено!\n\n"
								 f"Теперь вы можете завершить процесс, нажав на кнопку <b>«{ConfigReplyKeyboard().FINISH_DOWNLOAD[2:-2]}»</b>. Спасибо за ваше терпение и использование наших обновлений.\n\n"
								 f"Если у вас есть какие-либо вопросы или нужна помощь, не стесняйтесь обращаться к <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрации</b></a>.",
								 reply_markup = finish_update_reply_keyboards)

		elif not is_user_in_data(USER_ID, USER_DATA_DB):
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{ConfigBot.USERNAME(message)}] попытался установить обновление.")

		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных.")
	except RetryAfter as e:
		logger.warning(f"У пользователя [@{ConfigBot.USERNAME(message)}] превышен контроль отправки сообщений. Повторите попытку через {e.timeout} секунд.")

	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)