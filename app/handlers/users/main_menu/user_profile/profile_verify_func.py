from data.loader import dp, bot
from data.config import ConfigBot
from data.config_Keyboard import ConfigVerifyUsers
from data.loader_keyboard import LoaderInlineKeyboards, LoaderReplyKeyboards
from data.states_groups import ProfileState

from database.requests.user_db import load_user_data, is_user_in_data, save_user_data

from misc.loggers import logger
from misc.libraries import types, FSMContext

"""Создаем обработчик для верификации аккаунта пользователей"""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "VERIFY_ACCOUNT")
async def verify_handler(callback_query: types.CallbackQuery) -> ProfileState:
	"""Объявляем переменные с выводом данных о пользователе"""
	USER_DATA_DB = load_user_data()

	try:
		"""Объявляем переменную c выводом информации о пользователя: USER_ID"""
		USER_ID = ConfigBot.USERID(callback_query)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			"""Объявляем переменную c выводом информации о пользователя: USER_VERIFY"""
			USER_VERIFICATION = ConfigBot.USERVERIFY(callback_query)

			if USER_VERIFICATION is None or USER_VERIFICATION is False:
				"""Объявляем переменную c выводом информации о пользователя: USER_VERIFY"""
				USER_CONSIDERATION_VERIFICATION = ConfigBot.USERCONSIDERATIONVERIFY(callback_query)

				if USER_CONSIDERATION_VERIFICATION is None or USER_CONSIDERATION_VERIFICATION is False:
					await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
					
					VERIFICATION_CODE = ConfigBot.GETVERIFYCODE()

					"""Объявляем переменную с выводом сообщение о информации для верификации"""
					INFO_VERIFICATION_MESSAGE = f"💬 Для верификации вашего аккаунта, отправьте нам <b>четырехзначный код</b>, который мы выслали вам, а также предоставьте ссылку на <b>ваш профиль</b> в социальной сети ВКонтакте.\n\n" \
									f" • Ваш индивидуальный код: <b><code>{VERIFICATION_CODE}</code></b>\n\n" \
									f"Эти шаги необходимы для обеспечения безопасности вашей учетной записи."

					"""Сохраняем индивидуальный код пользователя в базу данных"""
					USER_DATA_DB[str(USER_ID)]["VERIFY_DATA"]["VERIFY_CODE_USER"] = VERIFICATION_CODE

					save_user_data(USER_DATA_DB)

					""""Объявляем переменные о выводе клавиатуры для возвращения обратно в профиль"""
					back_profile_inline_keyboard = LoaderInlineKeyboards(callback_query).INLINE_KEYBOARDS_BACK_PROFILEMENU

					await bot.send_message(chat_id = callback_query.message.chat.id, text = INFO_VERIFICATION_MESSAGE, reply_markup = back_profile_inline_keyboard)

					"""Переходим фазу, где пользователь вводит код и соц сеть"""
					await ProfileState.SendCodeAndSocialState.set()

				elif USER_CONSIDERATION_VERIFICATION:
					time_verify_message = f"💬 <a href='https://t.me/{ConfigBot.USERNAME(callback_query)}'>{ConfigBot.USERLASTNAME(callback_query)}</a>! Ваш аккаунт в настоящий момент проходит процесс <b>верификации</b>.\n\n" \
										   "Пожалуйста, ожидайте подтверждения от <b>администрации</b>. Этот процесс может занять некоторое время. Благодарим за терпение и понимание!\n\n" \
										  f"Если у вас возникли вопросы или вам требуется дополнительная помощь, не стесняйтесь обращаться к нашей <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрации</b></a>"

					await bot.send_message(chat_id = callback_query.message.chat.id, text = time_verify_message)

			elif USER_VERIFICATION:
				logger.warning(f"⚠️ Верифицированный пользователь [@{ConfigBot.USERNAME(callback_query)}] попытался верифицировать аккаунт.")
		else:
			logger.warning(f"⚠️ Незарегистрированный пользователь [@{ConfigBot.USERNAME(callback_query)}] попытался верифицировать аккаунт.")
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Создаем обработчика фазы, где пользователь вводит индивидуальный код"""
@dp.message_handler(state = ProfileState.SendCodeAndSocialState)
async def user_code_social_handler(message: types.Message, state: FSMContext) -> FSMContext:
	"""Объявляем переменные с выводом данных о пользователе"""
	USER_DATA_DB = load_user_data()

	try:
		"""Объявляем переменную о выводе информации пользователя и для разделения сообщений от пользователя"""
		USER_MESSAGE = ConfigBot.USERMESSAGE(message)
		PARTS = USER_MESSAGE.split()

		if len(PARTS) == 2:
			"""Объявляем переменные о выводе информации пользователя и выводе переменной с разделенной сообщения"""
			USER_VERIFICATION_CODE = ConfigBot.USERVERIFYCODE(message)
			INDIVIDUAL_CODE, VK_LINK = PARTS

			if USER_VERIFICATION_CODE == INDIVIDUAL_CODE and ConfigBot.CHECKVKPROFILELINK(VK_LINK):
				"""Объявляем переменные о выводе клавиатуры для возвращения в главное меню"""
				main_menu_reply_keyboard = LoaderReplyKeyboards(message).KEYBOARDS_MENU

				USER_DATA_DB[str(ConfigBot.USERID(message))]["VERIFY_DATA"]["STATUS_VERIFY_USER"] = ConfigVerifyUsers().CONSIDERATION_VERIFY_USER
				USER_DATA_DB[str(ConfigBot.USERID(message))]["VERIFY_DATA"]["CONSIDERATION_VERIFY_USER"] = True
				USER_DATA_DB[str(ConfigBot.USERID(message))]["VERIFY_DATA"]["LINK_PROFILE_USER"] = VK_LINK
				USER_DATA_DB[str(ConfigBot.USERID(message))]["VERIFY_DATA"]["VERIFY_TIME_USER"] = ConfigBot.GETTIMENOW()

				save_user_data(USER_DATA_DB)

				await message.answer(f"💬 Отлично, <a href='https://t.me/{ConfigBot.USERNAME(message)}'>{ConfigBot.USERLASTNAME(message)}</a>, ваш аккаунт в настоящее время находится на <b>рассмотрении</b> администрации.\n\n"
						 			  "Мы получили ваш <b>индивидуальный код</b> и ссылку на <b>ваш профиль</b> в ВКонтакте, и сейчас проводим необходимые проверки.\n\n"
									  "Пожалуйста, ожидайте окончательного решения. благодарим вас за предоставленную информацию и терпение.\n\n"
									 f"Если у вас возникли вопросы или вам требуется дополнительная помощь, не стесняйтесь обращаться к нашей <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрации</b></a>", reply_markup=main_menu_reply_keyboard)

				await state.finish()

			else:
				"""Проверка на неверный индивидуальный код, некорректную ссылку и в случае, если код и ссылка неверны"""
				if USER_VERIFICATION_CODE != INDIVIDUAL_CODE and ConfigBot.CHECKVKPROFILELINK(VK_LINK):
					await message.answer("⚠️ Неверный <b>индивидуальный код</b>. Пожалуйста, попробуйте снова.\n\n"
						  				f"Если у вас возникли вопросы или вам требуется дополнительная помощь, не стесняйтесь обращаться к нашей <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрации</b></a>")

				elif USER_VERIFICATION_CODE == INDIVIDUAL_CODE and not ConfigBot.CHECKVKPROFILELINK(VK_LINK):
					await message.answer("⚠️ Некорректная ссылка на <b>ваш профиль</b> ВКонтакте. Пожалуйста, попробуйте снова.\n\n"
						  				f"Если у вас возникли вопросы или вам требуется дополнительная помощь, не стесняйтесь обращаться к нашей <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрации</b></a>")

				elif USER_VERIFICATION_CODE != INDIVIDUAL_CODE and not ConfigBot.CHECKVKPROFILELINK(VK_LINK):
					await message.answer("⚠️ Неверный <b>индивидуальный код</b> и некорректная ссылка на <b>ваш профиль</b>. Пожалуйста, попробуйте снова.\n\n"
						  				f"Если у вас возникли вопросы или вам требуется дополнительная помощь, не стесняйтесь обращаться к нашей <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрации</b></a>")
				
				else:
					raise ValueError("ERROR: 404, FILE: PROFILE_FUNC, FUNC: USER_CODE_SOCIAL_HANDLER, TESTING: ConfigBot.USERVERIFYCODE(message)")
		elif len(PARTS) != 2:
			await message.answer("⚠️ Пожалуйста, введите <b>индивидуальный код</b> и ссылку на <b>ваш профиль</b> через пробел.\n\n"
								f"Если у вас возникли вопросы или вам требуется дополнительная помощь, не стесняйтесь обращаться к нашей <a href='https://t.me/{ConfigBot().AUTHOR}'><b>администрации</b></a>")
		else:
			logger.warning("⚠️ PARTS Не ровняется к двум: %s", len(PARTS))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)