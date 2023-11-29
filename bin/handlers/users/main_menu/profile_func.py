from data.loader import dp, bot
from data.config import LoaderReplyKeyboards, ConfigBot, LoaderInlineKeyboards
from data.config_Keyboard import ConfigReplyKeyboard, ConfigRoleUsers

from data.user_db import load_user_data, is_user_in_data, save_user_data, check_user_data
from data.states_groups import StartState

from misc.libraries import types, FSMContext, random

from keyboards.users.ReplyKeyboard.ReplyKeyboard_all import hide_keyboard

@dp.message_handler(lambda message: message.text == f"{ConfigReplyKeyboard().PROFILE}")
async def profile_handler(message: types.Message):
	"""Загружаем базу данных о пользователе"""
	user_data_db = load_user_data()

	try:
		"""Проверяем есть ли пользователь в базе данных"""
		if is_user_in_data(ConfigBot.USERID(message), user_data_db):
			"""Выводим информацию о фотографии пользователя"""
			photo = await bot.get_user_profile_photos(ConfigBot.USERID(message))
			"""Выводим первую фотографию пользователя"""
			photo_user = photo.photos[0][-1].file_id

			"""Создаем сообщение с информацией о пользователе"""
			profile_message = "💬 Ваша текущая информация о профиле.\n\n" \
							f" • Ваше имя на текущий момент: <b>{ConfigBot.USERLASTNAME(message)}</b>\n" \
							f" • Ваше имя пользователя: <b>@{ConfigBot.USERNAME(message)}</b>\n\n" \
							f" • Ваша страна проживания: <b>{ConfigBot.USERNATION(message)}</b>\n\n" \
							f" • Ваш <b>USER_ID</b>: <code>{ConfigBot.USERID(message)}</code>\n" \
							f" • Ваш <b>BOT_ID</b>: <code>{ConfigBot.USERBOTID(message)}</code>\n\n" \
							f" • Ваша роль на данный момент: {ConfigBot.USERROLE(message)} <b>{ConfigBot.USERROLENAME(message)}</b>"
			
			"""Проверяем есть ли фотография у пользователя или нет"""
			if photo.photos:
				await message.answer_photo(photo=photo_user, caption=profile_message)
			elif not photo.photos:
				await message.answer(profile_message)
			else:
				await message.answer("В ДАННЫЙ МОМЕНТ ПРОФИЛЬ НЕДОСТУПЕН")
		else:
			raise ValueError("ERROR: 161, TEXT: НЕЗАРЕГИСТРИРОВАННЫЙ ПОЛЬЗОВАТЕЛЬ ПОПЫТАЛСЯ ПОЛУЧИТЬ ИНФОРМАЦИЮ О ПРОФИЛЕ")
	except:
		raise ValueError("ERROR: 404, FILE: PROFILE_FUNC, FUNC: PROFILE_HANDLER")