from data.loader import dp
from data.config import ConfigBot
from data.config_Keyboard import ConfigRoleUsers, ConfigVerifyUsers
from data.states_groups import LoggInAdminState

from database.requests.user_db import load_user_data, is_user_in_data, save_user_data
from database.requests.admin_db import load_admin_data, is_admin_in_data, save_admin_data

from misc.libraries import types, FSMContext
from misc.loggers import logger

"""Создаем обработчик команды !loggin_admin"""
@dp.message_handler(lambda message: message.text == "!loggin_admin")
async def loggin_admin_command(message: types.Message) -> LoggInAdminState:
	"""Объявляем переменную с выводом данных о пользователе"""
	USER_DATA_DB = load_user_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID"""
		USER_ID = ConfigBot.USERID(message)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			"""Объявляем переменную с выводом данных о администрации"""
			ADMIN_DATA_DB = load_admin_data()

			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				await message.answer(f"💬 <a href='https://t.me/{ConfigBot.USERNAME(message)}'>{ConfigBot.USERLASTNAME(message)}</a>, кажется, вы уже зарегистрированы в базе администраторов.\n\n"
						  				f"Если у вас возникли вопросы или вам требуется дополнительная помощь, не стесняйтесь обращаться к <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрации</b></a>")
			
			elif not is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				await message.answer(f"💬 <a href='https://t.me/{ConfigBot.USERNAME(message)}'>{ConfigBot.USERLASTNAME(message)}</a>, для регистрации в базе администраторов, пожалуйста, введите <b>пароль</b> от вашей текущей учетной записи.\n\n"
						  				"Это необходимо для подтверждения вашей личности и обеспечения безопасности административных функций.")
					
				"""Переходим в фазу, где вводят пароль от учетной записи"""
				await LoggInAdminState.UserPasswordState.set()
			
			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации.")
		else:
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{ConfigBot.USERNAME(message)}] попытался вести команду !loggin_admin.")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчика фазы, где пользователь вводит пароль от учетной записи"""
@dp.message_handler(state = LoggInAdminState.UserPasswordState)
async def user_password_handler(message: types.Message) -> LoggInAdminState:
	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_PASSWORD, USER_MESSAGE"""
		USER_PASSWORD = ConfigBot.USERPASSWORD(message)
		USER_MESSAGE = ConfigBot.USERMESSAGE(message)

		if USER_PASSWORD == USER_MESSAGE:
			await message.answer(f"💬 Отлично, <a href='https://t.me/{ConfigBot.USERNAME(message)}'>{ConfigBot.USERLASTNAME(message)}</a>! Пароль от вашей учетной записи успешно <b>подтвержден</b>.\n\n"
								 f"Теперь, для завершения процесса регистрации в базе данных администраторов, введите секретный пароль. ")
			
			"""Переходим в фазу, где вводят секретный пароль для доступа"""
			await LoggInAdminState.SecretPasswordState.set()

		elif USER_PASSWORD != USER_MESSAGE:
			await message.answer(f"⚠️ Кажется, что пароль введен <b>неверно</b>. Пожалуйста, проверьте свои данные и попробуйте еще раз.\n\n"
								 f"❕ Если у вас возникли проблемы с доступом, вы можете связаться с нашей <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрацией</b></a>.")
		
		else:
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{ConfigBot.USERNAME(message)}] попытался вести пароль от учетной записи.")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчик фазы, где пользователь вводит секретный пароль от базы данных администрации"""
@dp.message_handler(state = LoggInAdminState.SecretPasswordState)
async def secret_password_handler(message: types.Message, state: FSMContext) -> FSMContext:
	"""Объявляем переменную с выводом данных о пользователе и о администрации"""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_MESSAGE, USER_ID"""
		USER_MESSAGE = ConfigBot.USERMESSAGE(message)
		USER_ID = ConfigBot.USERID(message)

		if ConfigBot().SECRET_PASSWORD == USER_MESSAGE:
			ADMIN_DATA_DB[str(USER_ID)] = {
				"USER_LAST_NAME": ConfigBot.USERLASTNAME(message),
				"USER_NAME": f"https://t.me/{ConfigBot.USERNAME(message)}",
				"TIME_REGISTOR": ConfigBot.GETTIMENOW()
			}

			save_admin_data(ADMIN_DATA_DB)

			USER_DATA_DB[str(ConfigBot.USERID(message))]["VERIFY_DATA"]["STATUS_VERIFY_USER"] = ConfigVerifyUsers().YES_VERIFY_USER
			USER_DATA_DB[str(ConfigBot.USERID(message))]["VERIFY_DATA"]["VERIFY_USER"] = True
			USER_DATA_DB[str(ConfigBot.USERID(message))]["VERIFY_DATA"]["CONSIDERATION_VERIFY_USER"] = False
			USER_DATA_DB[str(ConfigBot.USERID(message))]["VERIFY_DATA"]["VERIFY_TIME_USER"] = ConfigBot.GETTIMENOW()
			USER_DATA_DB[str(ConfigBot.USERID(message))]["USER_ROLE"] = ConfigRoleUsers().ADMIN
			USER_DATA_DB[str(ConfigBot.USERID(message))]["NAME_USER_ROLE"] = ConfigRoleUsers().ADMIN_NAME

			save_user_data(USER_DATA_DB)

			await message.answer(f"💬 Поздравляем, <a href='https://t.me/{ConfigBot.USERNAME(message)}'>{ConfigBot.USERLASTNAME(message)}</a>! Вы успешно ввели секретный пароль и завершили регистрацию в базе администраторов.\n\nТеперь у вас есть доступ к функциям администратора.\n\n"
								 "❕ Для получения списка доступных команд администрации, введите <b><code>!help</code></b>.")

			await state.finish()

		elif ConfigBot().SECRET_PASSWORD != USER_MESSAGE:
			await message.answer("⚠️ Извините, но похоже, что введен неверный <b>секретный пароль</b>.\n\n"
								 "Пожалуйста, убедитесь, что вы вводите правильные данные, и повторите попытку.")
			
		else:
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{ConfigBot.USERNAME(message)}] попытался вести секретный пароль.")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)