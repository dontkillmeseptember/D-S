from data.config_Keyboard import ConfigReplyKeyboard

from misc.libraries import (
	dataclass,
	os,
	load_dotenv,
	types,
	datetime,
	Translator,
	requests,
	random,
	re,
	asyncio,
	Union,
	calendar
)

from misc.loggers import logger

from database.requests.user_db import check_user_data, load_user_data, save_user_data
from database.requests.market_db import check_market_data
from database.requests.admin_db import load_admin_data, is_admin_in_data
from database.requests.rsb_db import check_rsb_data, is_rsb_in_data, load_rsb_data
from database.requests.sport_db import check_sport_data
from database.requests.info_update_db import check_update_data
from database.requests.ration_db import check_ration_data
from database.requests.memory_diary_db import Check_Memory_Diary_Data

from data.configBaseModel import User

load_dotenv()

@dataclass
class ConfigBot:
	"""Объявляем переменные с выводом данных для конфигурации бота"""
	VERSION: str = os.getenv("VERSION_BOT")
	AUTHOR: str = os.getenv("AUTHOR_BOT")
	SECRET_PASSWORD: str = os.getenv("SECRET_PASSWORD")

	@classmethod
	def USERLASTNAME(cls, obj) -> str:
		try:
			"""Вывод данные пользователя - Последние имя пользователя"""
			if isinstance(obj, (types.Message, types.CallbackQuery)):
				return obj.from_user.first_name if obj.from_user.username else None
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)
	
	@classmethod
	def USERNAME(cls, obj) -> str:
		try:
			"""Вывод данные пользователя - Ссылку на профиль пользователя"""
			if isinstance(obj, (types.Message, types.CallbackQuery)):
				return obj.from_user.username if obj.from_user.username else None
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)
	
	@classmethod
	def USERID(cls, obj) -> int:
		try:
			"""Выводим данные пользователя - USER_ID Пользователя"""
			if isinstance(obj, (types.Message, types.CallbackQuery)):
				return obj.from_user.id if obj.from_user.id else None
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def USERBOTID(cls, obj) -> int:
		try:
			"""Выводим данные пользователя - BOT_ID Пользователя"""
			if isinstance(obj, (types.Message, types.CallbackQuery)):
				"""Получаем доступ к базе данных о пользователе"""
				USER_ID = ConfigBot.USERID(obj)
				check_user_data_db = check_user_data(USER_ID)
				"""Выводим информацию о BOT_ID пользователя"""
				return check_user_data_db.get("BOT_ID")
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)
	
	@classmethod
	def USERNATION(cls, obj) -> str:
		try:
			"""Выводим данных пользователя - USER_NATION Пользователя"""
			if isinstance(obj, (types.Message, types.CallbackQuery)):
				"""Получаем доступ к базе данных о пользователе"""
				USER_ID = ConfigBot.USERID(obj)
				check_user_data_db = check_user_data(USER_ID)
				"""Выводим информацию о NATION_USER пользователя"""
				return check_user_data_db.get("NATION_USER")
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def USERPASSWORD(cls, obj) -> str:
		try:
			"""Выводим данных пользователя - USER_PASSWORD Пользователя"""
			if isinstance(obj, (types.Message, types.CallbackQuery)):
				"""Получаем доступ к базе данных о пользователе"""
				USER_ID = ConfigBot.USERID(obj)
				check_user_data_db = check_user_data(USER_ID)
				"""Выводим информацию о USER_PASSWORD пользователя"""
				return check_user_data_db.get("USER_PASSWORD")
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def USERROLE(cls, obj) -> str:
		try:
			"""Выводим данных пользователя - USER_ROLE Пользователя"""
			if isinstance(obj, (types.Message, types.CallbackQuery)):
				"""Получаем доступ к базе данных о пользователе"""
				USER_ID = ConfigBot.USERID(obj)
				check_user_data_db = check_user_data(USER_ID)
				"""Выводим информацию о USER_ROLE пользователя"""
				return check_user_data_db.get("USER_ROLE")
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def USERROLENAME(cls, obj) -> str:
		try:
			"""Выводим данных пользователя - NAME_USER_ROLE Пользователя"""
			if isinstance(obj, (types.Message, types.CallbackQuery)):
				"""Получаем доступ к базе данных о пользователе"""
				USER_ID = ConfigBot.USERID(obj)
				check_user_data_db = check_user_data(USER_ID)
				"""Выводим информацию о NAME_USER_ROLE пользователя"""
				return check_user_data_db.get("NAME_USER_ROLE")
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def GETMESSAGEID(cls, obj) -> int:
		try:
			"""Выводим данные пользователя - PREVIOUS_MESSAGE_ID Пользователя"""
			if isinstance(obj, (types.Message, types.CallbackQuery)):
				"""Получаем доступ к базе данных о пользователе"""
				USER_ID = ConfigBot.USERID(obj)
				check_user_data_db = check_user_data(USER_ID)
				"""Выводим информацию о PREVIOUS_MESSAGE_ID пользователя"""
				return check_user_data_db.get("STATES_USER", {}).get("PREVIOUS_MESSAGE_ID")
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def USERNAMEBOT(cls, obj) -> str:
		"""Выводим данных пользователя - USER_NAME Пользователя"""
		try:
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(obj)
			"""Выводим информацию о USER_NAME пользователя"""
			return check_user_data_db.get("USER_NAME")
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)
			
	@classmethod
	def USERLASTNAMEBOT(cls, obj) -> str:
		"""Выводим данных пользователя - USER_LAST_NAME Пользователя"""
		try:
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(obj)
			"""Выводим информацию о USER_LAST_NAME пользователя"""
			return check_user_data_db.get("USER_LAST_NAME")
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def USERVERSIONBOT(cls, obj) -> str:
		try:
			"""Выводим данных пользователя - VERSION_BOT Пользователя"""
			if isinstance(obj, (types.Message, types.CallbackQuery)):
				"""Получаем доступ к базе данных о пользователе"""
				USER_ID = ConfigBot.USERID(obj)
				check_user_data_db = check_user_data(USER_ID)
				"""Выводим информацию о VERSION_BOT пользователя"""
				return check_user_data_db.get("VERSION_BOT")
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def USERSELECTEDSPORT(cls, obj) -> str:
		"""Выводим данных пользователя - SELECTED_SPORT_USER Пользователя."""
		try:
			if isinstance(obj, (types.Message, types.CallbackQuery)):
				"""Получаем доступ к базе данных о пользователе."""
				USER_ID = ConfigBot.USERID(obj)
				check_user_data_db = check_user_data(USER_ID)
				"""Выводим информацию о SELECTED_SPORT_USER пользователя."""
				return check_user_data_db.get("SELECTED_SPORT", {}).get("SELECTED_SPORT_USER")
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)
	
	@classmethod
	def USERSELECTEDSPORTNAME(cls, obj) -> str:
		"""Выводим данных пользователя - SELECTED_SPORT_NAME Пользователя."""
		try:
			if isinstance(obj, (types.Message, types.CallbackQuery)):
				"""Получаем доступ к базе данных о пользователе."""
				USER_ID = ConfigBot.USERID(obj)
				check_user_data_db = check_user_data(USER_ID)
				"""Выводим информацию о SELECTED_SPORT_NAME пользователя."""
				return check_user_data_db.get("SELECTED_SPORT", {}).get("SELECTED_SPORT_NAME")
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def USERSTATUSSPORTID(cls, obj) -> str:
		"""Выводим данных пользователя - STATUS_USER Пользователя."""
		try:
			if isinstance(obj, (types.Message, types.CallbackQuery)):
				"""Получаем доступ к базе данных о пользователе."""
				USER_ID = ConfigBot.USERID(obj)
				check_user_data_db = check_user_data(USER_ID)
				"""Выводим информацию о STATUS_USER пользователя."""
				return check_user_data_db.get("STATES_USER", {}).get("SPORT_ID")
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)
	
	@classmethod
	def RATION_SELECT_USERS(cls) -> str:
		"""Выводим данные пользователя - RATION_SELECT для Пользователей."""
		try:
			"""Получаем доступ к базе данных о пользователе."""
			check_ration_data_db = check_ration_data("RATION_MAIN")
			"""Выводим информацию о RATION_SELECT пользователя."""
			return check_ration_data_db.get("RATION_SELECT")
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def STATUS_USER_RATION_ID(cls, obj) -> str:
		"""Выводим данных пользователя - STATUS_RATION Пользователя."""
		try:
			if isinstance(obj, (types.Message, types.CallbackQuery)):
				"""Получаем доступ к базе данных о пользователе."""
				USER_ID = ConfigBot.USERID(obj)
				check_user_data_db = check_user_data(USER_ID)
				"""Выводим информацию о STATUS_RATION пользователя."""
				return check_user_data_db.get("STATES_USER", {}).get("RATION_ID")
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)
	
	@classmethod
	def STATUS_USER_WEEKDAY_ID(cls, obj) -> str:
		"""Выводим данных пользователя - STATUS_WEEKDAY Пользователя."""
		try:
			if isinstance(obj, (types.Message, types.CallbackQuery)):
				"""Получаем доступ к базе данных о пользователе."""
				USER_ID = ConfigBot.USERID(obj)
				check_user_data_db = check_user_data(USER_ID)
				"""Выводим информацию о STATUS_WEEKDAY пользователя."""
				return check_user_data_db.get("STATES_USER", {}).get("WEEKDAY_ID")
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def USERSTATUSVERIFY(cls, obj) -> str:
		"""Выводим данных пользователя - STATUS_VERIFY_USER Пользователя."""
		try:
			if isinstance(obj, (types.Message, types.CallbackQuery)):
				"""Получаем доступ к базе данных о пользователе."""
				USER_ID = ConfigBot.USERID(obj)
				check_user_data_db = check_user_data(USER_ID)
				"""Выводим информацию о STATUS_VERIFY_USER пользователя."""
				return check_user_data_db.get("VERIFY_DATA", {}).get("STATUS_VERIFY_USER")
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def USERVERIFY(cls, obj) -> str:
		try:
			"""Выводим данных пользователя - VERIFY_USER Пользователя"""
			if isinstance(obj, (types.Message, types.CallbackQuery)):
				"""Получаем доступ к базе данных о пользователе"""
				USER_ID = ConfigBot.USERID(obj)
				check_user_data_db = check_user_data(USER_ID)
				"""Выводим информацию о VERIFY_USER пользователя"""
				return check_user_data_db.get("VERIFY_DATA", {}).get("VERIFY_USER")
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def USERVERIFYCODE(cls, obj) -> str:
		try:
			"""Выводим данных пользователя - VERIFY_CODE_USER Пользователя"""
			if isinstance(obj, (types.Message, types.CallbackQuery)):
				"""Получаем доступ к базе данных о пользователе"""
				USER_ID = ConfigBot.USERID(obj)
				check_user_data_db = check_user_data(USER_ID)
				"""Выводим информацию о VERIFY_CODE_USER пользователя"""
				return check_user_data_db.get("VERIFY_DATA", {}).get("VERIFY_CODE_USER")
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def USERCONSIDERATIONVERIFY(cls, obj) -> str:
		try:
			"""Выводим данных пользователя - CONSIDERATION_VERIFY_USER Пользователя"""
			if isinstance(obj, (types.Message, types.CallbackQuery)):
				"""Получаем доступ к базе данных о пользователе"""
				USER_ID = ConfigBot.USERID(obj)
				check_user_data_db = check_user_data(USER_ID)
				"""Выводим информацию о CONSIDERATION_VERIFY_USER пользователя"""
				return check_user_data_db.get("VERIFY_DATA", {}).get("CONSIDERATION_VERIFY_USER")
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def USERREGISTORWALLET(cls, obj) -> str:
		try:
			"""Выводим данных пользователя - REGISTOR_WALLET_USER Пользователя"""
			if isinstance(obj, (types.Message, types.CallbackQuery)):
				"""Получаем доступ к базе данных о пользователе"""
				USER_ID = ConfigBot.USERID(obj)
				check_user_data_db = check_user_data(USER_ID)
				"""Выводим информацию о REGISTOR_WALLET_USER пользователя"""
				return check_user_data_db.get("RSB_DATA", {}).get("REGISTOR_WALLET_USER")
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def USERSTATUSUPDATEID(cls, obj) -> str:
		try:
			"""Выводим данные пользователя - UPDATE_ID Пользователя."""
			if isinstance(obj, (types.Message, types.CallbackQuery)):
				"""Получаем доступ к базе данных о пользователе."""
				USER_ID = ConfigBot.USERID(obj)
				check_user_data_db = check_user_data(USER_ID)
				"""Выводим информацию о UPDATE_ID пользователя."""
				return check_user_data_db.get("STATES_USER", {}).get("UPDATE_ID")
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def USERMESSAGE(cls, message) -> str:
		"""Вводим сообщение пользователя для регистрации пароля и т.д."""
		return message.text

	@classmethod
	def GETBOTID(cls) -> str:
		"""Генерация случайного 9-значного BOT_ID"""		
		return ''.join(str(random.randint(0, 9)) for _ in range(9))

	@classmethod
	def GETVERIFYCODE(cls) -> str:
		"""Генерируем четырехзначный код для верификации аккаунта"""
		return ''.join(str(random.randint(0, 9)) for _ in range(4))

	@classmethod
	def GETLENUSERS(cls, obj) -> int:
		"""Выводим определенное количество чего-то"""
		try:
			"""Получаем количество зарегистрированных пользователей"""
			return len(obj) if isinstance(obj, (list, dict)) else 0
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def GETCOUNTVERIFITEDUSERS(cls, user_data) -> int:
		"""Выводим количество верифицированных пользователей"""
		try:
			return sum(1 for user in user_data.values() if user.get("VERIFY_DATA", {}).get("VERIFY_USER", False))
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def GETCONSIDERATIONVERIFY(cls, user_data, keyboards = False) -> Union[bool, str]:
		"""Выводим информацию о пользователей которые имеют ключ "CONSIDERATION_VERIFY_USER": true"""
		try:
			user_info_list = [f" • {i+1}: <a href=\"{user_info['USER_NAME']}\">{user_info['USER_LAST_NAME']}</a> — <a href=\"{user_info['VERIFY_DATA']['LINK_PROFILE_USER']}\">Ссылка на Профиль</a> — <code>{user_id}</code>" for i, (user_id, user_info) in enumerate(user_data.items()) if "VERIFY_DATA" in user_info and user_info["VERIFY_DATA"]["CONSIDERATION_VERIFY_USER"]]

			if keyboards:
				return bool(user_info_list)
			else:
				return "\n".join(user_info_list) if user_info_list else " • Нет пользователей на рассмотрении для верификации."
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def GETNOTIFY(cls, obj, users_or_admin, types) -> Union[bool, str]:
		"""Выводим информацию об уведомлениях."""
		try:
			"""Объявляем переменные для доступа к базе данных пользователей и получаем информацию об их уведомления."""
			USER_ID = ConfigBot.USERID(types)

			"""Выводим информацию об уведомлениях пользователя."""
			check_user_data_db = check_user_data(USER_ID)

			if not users_or_admin and obj in ("NOTIFY_RATION", "NOTIFY_SPORT", "NOTIFY_UPDATE"):
				return check_user_data_db.get("NOTIFY_DATA", {}).get("USER_NOTIFY", {}).get(obj)
			
			elif users_or_admin and obj == "NOTIFY_RUN":
				return check_user_data_db.get("NOTIFY_DATA", {}).get("ADMIN_NOTIFY", {}).get(obj)
			
			elif obj in ("NOTIFY_RATION", "NOTIFY_SPORT", "NOTIFY_UPDATE"):
				return check_user_data_db.get("NOTIFY_DATA", {}).get("USER_NOTIFY", {}).get(obj)

		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def GET_MEMORY_DIARY(cls, memory_diary_id) -> str:
		try:
			CHECK_MEMORY_DIARY_DB = Check_Memory_Diary_Data(memory_diary_id)

			return CHECK_MEMORY_DIARY_DB.get("MESSAGE")
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def GETUPDATE(cls, update_id, obj) -> str:
		"""Выводим информацию об обновлении."""
		try:
			check_update_data_db = check_update_data(update_id)

			if obj in ("NAME_UPDATE", "MESSAGE_UPDATE", "DATA_UPDATE", "URL_UPDATE"):
				return check_update_data_db.get(obj)
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def GET_RATION(cls, ration_id, obj, weekday_user = None) -> str:
		"""Выводим информацию о Рационе."""
		try:
			check_ration_data_db = check_ration_data(ration_id)

			if obj in ("NAME_RATION", "EMOJI_RATION", "CREATE_TIME_RATION"):
				return check_ration_data_db.get(obj)
			
			if obj in ("DESCRIPTION_RATION"):
				return check_ration_data_db.get("WEEKDAY", {}).get(f"{weekday_user}").get(f"DESCRIPTION_{weekday_user}")
			
			if obj in ("BREAKFAST", "BREAKFAST_LINK_RECIPE", "LUNCH", "LUNCH_LINK_RECIPE", "DINNER", "DINNER_LINK_RECIPE"):
				return check_ration_data_db.get("WEEKDAY", {}).get(f"{weekday_user}").get(obj)
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def GET_WEEKDAY(cls, ration_id, weekday_id, obj) -> str:
		"""Выводим информацию о дне Недели."""
		try:
			check_ration_data_db = check_ration_data(ration_id)

			if obj in (f"DESCRIPTION_{weekday_id}"):
				return check_ration_data_db.get("WEEKDAY", {}).get(weekday_id, {}).get(obj)
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def GETSPORT(cls, sport_id, obj) -> str:
		"""Выводим информацию о спорте."""
		try:
			check_sport_data_db = check_sport_data(sport_id)

			if obj in ("NAME_SPORT", "MESSAGE_SPORT", "DATA_SPORT"):
				return check_sport_data_db.get(obj)
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def GETSELECTEDSPORT(cls, type, sport_data) -> str:
		"""Выводим информацию о выбранном спорте."""
		try:
			"""Объявляем переменные с выводом информации о пользователе: USER_SPORT."""
			USER_SPORT = ConfigBot.USERSELECTEDSPORT(type)

			if USER_SPORT:
				"""Создаем цикл который выводит нужную информацию о спорте который выбрал пользователь."""
				for ID_SPORT, SPORT_DATA_ID in sport_data.items():
					TEXT = f"{SPORT_DATA_ID['CALLBACK_DATA_SPORT']}"

					if ConfigBot.USERSELECTEDSPORTNAME(type) == TEXT:
						return f" • Ваш спорт: {SPORT_DATA_ID['EMODJI_SPORT']} <b>{SPORT_DATA_ID['NAME_SPORT'][2:]}</b>\n\n"
			
			elif not USER_SPORT:
				return ""
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def GETRSB(cls, rsb_data, obj, users_or_admin, types) -> str:
		"""Выводим информацию о кошельке из базы данных."""
		try:
			if not users_or_admin:
				"""Объявляем переменные для доступа к базе данных пользователей и получение информации"""
				USER_ID = ConfigBot.USERID(types)
				RSB_DATA_DB = load_rsb_data()

				"""Выводим информацию о NUMBER_WALLET_USER пользователя"""
				check_user_data_db = check_user_data(USER_ID)
				USER_NUMBER_WALLET = check_user_data_db.get("RSB_DATA", {}).get("NUMBER_WALLET_USER")

				if is_rsb_in_data(USER_NUMBER_WALLET, RSB_DATA_DB):
					check_rsb_data_db = check_rsb_data(USER_NUMBER_WALLET)

					if obj == "WALLET":
						return USER_NUMBER_WALLET
					
					elif obj in ("CURRENT_ETH", "CURRENT_USD", "CURRENT_RUB"):
						return check_rsb_data_db.get("CURRENT", {}).get(obj)
					
					elif obj in ("INTEREST_USER_ONE", "INTEREST_USER_TWO"):
						return check_rsb_data_db.get("INTEREST", {}).get(obj)
					
					elif obj in ("ALL_SUM_ETH", "ALL_SUM_USD", "ALL_SUM_RUB"):
						AMOUNT_TYPE = obj.split("_")[-1]
						AMOUNT = check_rsb_data_db.get("ALL_SUM_WALLET", {}).get(f"ALL_SUM_{AMOUNT_TYPE}_END")

						if AMOUNT > 0:
							return AMOUNT
						
						elif AMOUNT == 0:
							START_AMOUNT = check_rsb_data_db.get("ALL_SUM_WALLET", {}).get(f"ALL_SUM_{AMOUNT_TYPE}_START")

							return START_AMOUNT

					else:
						return check_rsb_data_db.get(obj, None)
				
				return None
			
			elif users_or_admin:
				check_rsb_data_db = check_rsb_data(rsb_data)

				if obj in ("CURRENT_ETH", "CURRENT_USD", "CURRENT_RUB"):
					return check_rsb_data_db.get("CURRENT", {}).get(obj)
					
				elif obj in ("INTEREST_USER_ONE", "INTEREST_USER_TWO"):
					return check_rsb_data_db.get("INTEREST", {}).get(obj)

				elif obj in ("ALL_SUM_ETH", "ALL_SUM_USD", "ALL_SUM_RUB"):
					AMOUNT_TYPE = obj.split("_")[-1]
					AMOUNT = check_rsb_data_db.get("ALL_SUM_WALLET", {}).get(f"ALL_SUM_{AMOUNT_TYPE}_END")

					if AMOUNT > 0:
						return AMOUNT
					
					elif AMOUNT == 0:
						START_AMOUNT = check_rsb_data_db.get("ALL_SUM_WALLET", {}).get(f"ALL_SUM_{AMOUNT_TYPE}_START")

						return START_AMOUNT
				else:
					return check_rsb_data_db.get(obj, None)

			return None
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def GETNUMBERWALLETRSB(cls, rsb_data, user_id) -> str:
		"""Выводим ID кошельков из базы данных RSB"""
		try:
			"""Проверяем зарегистрирован пользователь в базе админов"""
			ADMIN_DATA_DB = load_admin_data()

			if is_admin_in_data(user_id, ADMIN_DATA_DB):
				"""Выводим краткую информацию о ID кошельков"""
				number_wallet_info_list = [f" • <code>{wallet_number}</code> ~ <b>{rsb_info['ETH']} ETH</b>" for wallet_number, rsb_info in rsb_data.items()]
					
				return "\n".join(number_wallet_info_list)
			else:
				return " • В данный момент нету ID кошельков."
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def GETUSDTORUB(cls) -> int:
		"""Выполняет расчет из USD в RUB"""
		try:
			URL = "https://api.exchangerate-api.com/v4/latest/USD"
			response = requests.get(URL)

			if response.status_code == 200:
				data = response.json()

				return data.get("rates", {}).get("RUB")
			else:
				return -1
		except requests.exceptions.RequestException as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def GETRUBTOUSD(cls) -> int:
		"""Выполняет расчет из RUB в USD"""
		try:
			URL = "https://api.exchangerate-api.com/v4/latest/RUB"
			response = requests.get(URL)

			if response.status_code == 200:
				data = response.json()

				return data.get("rates", {}).get("USD")
			else:
				return -1
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def GETETHTOUSD(cls) -> int:
		"""Выполняет расчет из ETH в USD"""
		try:
			URL = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
			response = requests.get(URL)

			if response.status_code == 200:
				data = response.json()

				return data.get("ethereum", {}).get("usd")
			else:
				return -1
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def GETETHTORUB(cls) -> int:
		"""Выполняет расчет из ETH в RUB"""
		try:
			URL = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=rub"
			response = requests.get(URL)
			
			if response.status_code == 200:
				data = response.json()

				return data.get("ethereum", {}).get("rub")
			else:
				return -1
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)
		
	@classmethod
	def GETMARKET(cls, market_data, obj) -> bool:
		"""Выводим данные товаров из базы данных"""
		try:
			return check_market_data(market_data).get(obj, None) if obj in ("URL_PHOTO", "URL_SITE", "NAME_MARKET", "MESSAGE") else None
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def GETPRICE(cls, art):
		"""Выводим цену из базы данных"""
		try:
			"""Объявляем переменную с выводом информации о цене"""
			check_market_data_db = check_market_data(art)

			"""Объявляем переменную с выводом ссылки на сайт магазина"""
			URL_SITE = check_market_data_db.get("URL_SITE")

			if ConfigBot.CHECKWILDBERRIESLINK(URL_SITE):
				"""Ссылка на базу данных JSON файл от Wildberries, где мы берем цену товара"""
				URL = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=123585924&spp=27&nm={art}"

				"""Выполнение запроса по ссылке"""
				response = requests.get(URL)

				if response.status_code == 200:
					json_data = response.json()
					products = json_data["data"]["products"]
					
					for product in products:
						if "salePriceU" in product:
							SALE_PRICE = int(str(product["salePriceU"]).rstrip("00"))

							return SALE_PRICE
					
					return None
				else:
					logger.critical("⚠️ Отказ доступа к информации о товаре.")
				
			elif ConfigBot.CHECKLAMODALINK(URL_SITE):
				"""Ссылка на базу данных JSON файл от Lamoda, где мы берем цену товара"""
				URL = f"https://www.lamoda.ru/api/v1/product/get?sku={art}&city_aoid=6100000500000&is_hybrid_supported=true&size_id=0"

				"""Выполнение запроса по ссылке"""
				response = requests.get(URL)

				if response.status_code == 200:
					json_data = response.json()
					
					if "prices" in json_data:
						prices = json_data["prices"]
						
						if "original" in prices and "price" in prices["original"]:
							price = prices["original"]["price"]
							
							return price
					else:
						return None
				else:
					logger.critical("⚠️ Отказ доступа к информации о товаре.")
			else:
				return None
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def CHECKLAMODALINK(cls, link) -> bool:
		"""
		Проверяет корректность ссылки на lamoda.ru.
		Возвращает True, если ссылка корректна, иначе False.
		"""
		try:
			"""Проверка ссылки на lamoda.ru"""
			lamoda_link_pattern = re.compile(r'^https?://(www\.)?lamoda\.ru(.*)$')

			return bool(lamoda_link_pattern.match(link))
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def CHECKWILDBERRIESLINK(cls, link) -> bool:
		"""
		Проверяет корректность ссылки на wildberries.ru.
		Возвращает True, если ссылка корректна, иначе False.
		"""
		try:
			"""Проверка ссылки на wildberries.ru"""
			wildberries_link_pattern = re.compile(r'^https?://(www\.)?wildberries\.ru(.*)$')

			return bool(wildberries_link_pattern.match(link))
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

			return None

	@classmethod
	def GETARTICLEMARKET(cls, market_data, user_id) -> int:
		"""Выводим данные товаров из базы данных."""
		try:
			"""Объявляем переменную о выводе информации о администрации."""
			ADMIN_DATA_DB = load_admin_data()
			ARTICLE_INFO_LIST = []

			for ARTICLE_ID, MARKET_DATA_ID in market_data.items():
				NAME_MARKET = MARKET_DATA_ID["NAME_MARKET"]
				SITE_MARKET = MARKET_DATA_ID.get("URL_SITE")

				if is_admin_in_data(user_id, ADMIN_DATA_DB):
					if SITE_MARKET:
						ARTICLE_INFO_LIST.append(f" • <code>{ARTICLE_ID}</code>: {NAME_MARKET} — <a href ='{SITE_MARKET}'>Ссылка на сайт</a>;")
					else:
						ARTICLE_INFO_LIST.append(f" • <code>{ARTICLE_ID}</code>: {NAME_MARKET}")
				else:
					ARTICLE_INFO_LIST.append(f" • <code>{ARTICLE_ID}</code>: {NAME_MARKET}")

			if ARTICLE_INFO_LIST:
				return "\n".join(ARTICLE_INFO_LIST)
			else:
				return " • В данный момент нету товаров в корзине."
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)
	
	@classmethod
	def GET_ID_RATION(cls, ration_data) -> str:
		"""Выводим данные о рационах из базы данных."""
		try:
			ID_RATION_LIST = []

			for ID_RATION, RATION_DATA_ID in ration_data.items():
				if ID_RATION == "RATION_MAIN":
					continue

				NAME_RATION = RATION_DATA_ID["NAME_RATION"]
				EMOJI_RATION = RATION_DATA_ID["EMOJI_RATION"]

				ID_RATION_LIST.append(f" • [ <code>{ID_RATION}</code> ]: {NAME_RATION} • {EMOJI_RATION}")

			if ID_RATION_LIST:
				return "\n\n".join(ID_RATION_LIST)
			else:
				return " • В данный момент нету рационов."
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)
	
	@classmethod
	def GET_MEALS_WEEKDAY(cls, ration_data, ration_id, weekday_id) -> str:
		"""Выводим данные о блюдах из базы данных."""
		try:
			MEALS_LIST = []

			for ID_RATION, RATION_DATA_ID in ration_data.items():
				if ID_RATION == ration_id:
					if "WEEKDAY" in RATION_DATA_ID:
						for ID_WEEKDAY, WEEKDAY_DATA_ID in RATION_DATA_ID["WEEKDAY"].items():
							if ID_WEEKDAY == weekday_id:
								BREAKFAST = WEEKDAY_DATA_ID["BREAKFAST"]
								BREAKFAST_LINK = WEEKDAY_DATA_ID["BREAKFAST_LINK_RECIPE"]
								LUNCH = WEEKDAY_DATA_ID["LUNCH"]
								LUNCH_LINK = WEEKDAY_DATA_ID["LUNCH_LINK_RECIPE"]
								DINNER = WEEKDAY_DATA_ID["DINNER"]
								DINNER_LINK = WEEKDAY_DATA_ID["DINNER_LINK_RECIPE"]

								MEALS_LIST.append(f" • [ <code>BREAKFAST</code> ]: <a href='{BREAKFAST_LINK}'>{BREAKFAST if BREAKFAST is not None else 'В данный момент нету блюд.'}</a>")
								MEALS_LIST.append(f" • [ <code>LUNCH</code> ]: <a href='{LUNCH_LINK}'>{LUNCH if LUNCH is not None else 'В данный момент нету блюд.'}</a>")
								MEALS_LIST.append(f" • [ <code>DINNER</code> ]: <a href='{DINNER_LINK}'>{DINNER if DINNER is not None else 'В данный момент нету блюд.'}</a>")

			if MEALS_LIST:
				return "\n\n".join(MEALS_LIST)
			else:
				return " • В данный момент нету блюд."
		
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def TRANSTALED_WEEKDAY(cls, weekday_id) -> str:
		"""Переводим недели на русском языке."""
		try:
			WEEKDAYS_TRANSLATION_RUSSIAN = {
				"MONDAY": "Понедельника",
				"TUESDAY": "Вторника",
				"WEDNESDAY": "Среды",
				"THURSDAY": "Четверга",
				"FRIDAY": "Пятницы",
				"SATURDAY": "Субботы",
				"SUNDAY": "Воскресенья"
			}

			return WEEKDAYS_TRANSLATION_RUSSIAN.get(weekday_id, "")
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def LENS_WEEKDAY(cls, ration_data, weekday_id, types) -> int:
		"""Выводим данные о днях недели из базы данных."""
		try:
			ID_WEEKDAY_LIST = []

			for ID_RATION, RATION_DATA_ID in ration_data.items():
				if ConfigBot.STATUS_USER_RATION_ID(types) == ID_RATION:
					if "WEEKDAY" in RATION_DATA_ID:
						for ID_WEEKDAY, WEEKDAY_DATA_ID in RATION_DATA_ID["WEEKDAY"].items():
							if weekday_id == ID_WEEKDAY:
								RATION_BREAKFAST = WEEKDAY_DATA_ID["BREAKFAST"]
								RATION_LUNCH = WEEKDAY_DATA_ID["LUNCH"]
								RATION_DINNER = WEEKDAY_DATA_ID["DINNER"]

								COUNT_NON_NULL_MEALS = sum(meal is not None for meal in [RATION_BREAKFAST, RATION_LUNCH, RATION_DINNER])

								ID_WEEKDAY_LIST.append(str(COUNT_NON_NULL_MEALS))
			
			return " ".join(ID_WEEKDAY_LIST)

		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def GET_ID_WEEKDAY(cls, ration_data, types) -> str:
		"""Выводим данные о днях недели из базы данных."""
		try:
			ID_WEEKDAY_LIST = []

			WEEKDAYS_TRANSLATION_RUSSIAN = {
				"MONDAY": "Понедельник",
				"TUESDAY": "Вторник",
				"WEDNESDAY": "Среда",
				"THURSDAY": "Четверг",
				"FRIDAY": "Пятница",
				"SATURDAY": "Суббота",
				"SUNDAY": "Воскресенье"
			}

			for ID_RATION, RATION_DATA_ID in ration_data.items():
				if ConfigBot.STATUS_USER_RATION_ID(types) == ID_RATION:
					if "WEEKDAY" in RATION_DATA_ID:
						for ID_WEEKDAY, WEEKDAY_DATA_ID in RATION_DATA_ID["WEEKDAY"].items():
							RATION_BREAKFAST = WEEKDAY_DATA_ID["BREAKFAST"]
							RATION_LUNCH = WEEKDAY_DATA_ID["LUNCH"]
							RATION_DINNER = WEEKDAY_DATA_ID["DINNER"]

							COUNT_NON_NULL_MEALS = sum(meal is not None for meal in [RATION_BREAKFAST, RATION_LUNCH, RATION_DINNER])

							TRANSLATION_WEEKDAY = WEEKDAYS_TRANSLATION_RUSSIAN.get(ID_WEEKDAY, "")
							ID_WEEKDAY_LIST.append(
								f" • [ <code>{ID_WEEKDAY}</code> ]: {TRANSLATION_WEEKDAY} • {f'<b>{COUNT_NON_NULL_MEALS}</b> — ' if COUNT_NON_NULL_MEALS > 0 else 'Нету блюд'}"
								f"{f'<i>«{RATION_BREAKFAST}»</i>, ' if RATION_BREAKFAST is not None else ''}"
								f"{f'<i>«{RATION_LUNCH}»</i>, ' if RATION_LUNCH is not None else ''}"
								f"{f'<i>«{RATION_DINNER}»</i>' if RATION_DINNER is not None else ''}"
							)

			if ID_WEEKDAY_LIST:
				return "\n\n".join(ID_WEEKDAY_LIST)

		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def GETIDSPORT(cls, sport_data) -> str:
		"""Выводим данные об упражнениях из базы данных."""
		try:
			ID_SPORT_LIST = []

			for ID_SPORT, SPORT_DATA_ID in sport_data.items():
				NAME_SPORT = SPORT_DATA_ID["NAME_SPORT"]
				MESSAGE_SPORT = SPORT_DATA_ID["MESSAGE_SPORT"]

				"""Ограничиваем вывод сообщения до 50 символов и добавляем многоточие в конце."""
				TRUNCATED_MESSAGE = MESSAGE_SPORT[:55] + "..." if len(MESSAGE_SPORT) > 55 else MESSAGE_SPORT

				ID_SPORT_LIST.append(f" • <code>{ID_SPORT}</code>: {NAME_SPORT[2:] } — «{TRUNCATED_MESSAGE[2:]}»")

			if ID_SPORT_LIST:
				return "\n\n".join(ID_SPORT_LIST)
			else:
				return " • В данный момент нету упражнений."
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def GETWORKOUT(cls, sport_data, types) -> str:
		"""Выводим данные об тренировках из базы данных."""
		try:
			WORKOUT_LIST = []

			for ID_SPORT, SPORT_DATA_ID in sport_data.items():
				if ConfigBot.USERSELECTEDSPORTNAME(types) == SPORT_DATA_ID["CALLBACK_DATA_SPORT"]:
					if "WORKOUTS" in SPORT_DATA_ID:
						for WORKOUT_ID, WORKOUT_DATA_ID in SPORT_DATA_ID["WORKOUTS"].items():
							EMODJI_WORKOUT = WORKOUT_DATA_ID["EMODJI_WORKOUT"]
							NAME_WORKOUT = WORKOUT_DATA_ID["NAME_WORKOUT"]
							TERN_WORKOUT = WORKOUT_DATA_ID["TERN_WORKOUT"]

							WORKOUT_LIST.append(f"     <b>↳</b>{EMODJI_WORKOUT} <b>{NAME_WORKOUT}</b> — {TERN_WORKOUT}")

			if WORKOUT_LIST:
				return "\n".join(WORKOUT_LIST)
			else:
				return "     <b>↳</b> В данный момент нету тренировок."
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def GETIDWORKOUTS(cls, sport_data) -> str:
		"""Выводим данные об тренировках из базы данных."""
		try:
			ID_WORKOUT_LIST = []

			for ID_SPORT, SPORT_DATA_ID in sport_data.items():
				if "WORKOUTS" in SPORT_DATA_ID:
					for WORKOUT_ID, WORKOUT_DATA_ID in SPORT_DATA_ID["WORKOUTS"].items():
						NAME_WORKOUT = WORKOUT_DATA_ID["NAME_WORKOUT"]
						TERN_WORKOUT = WORKOUT_DATA_ID["TERN_WORKOUT"]

						ID_WORKOUT_LIST.append(f" • <code>{WORKOUT_ID}</code>: {NAME_WORKOUT} — {TERN_WORKOUT}")
			
			if ID_WORKOUT_LIST:
				return "\n".join(ID_WORKOUT_LIST)
			else:
				return " • В данный момент нету тренировок."
		
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def GETIDUPDATE(cls, update_data) -> str:
		"""Выводим данные об обновлений из базы данных."""
		try:
			ID_UPDATE_LIST = []

			for ID_UPDATE, UPDATE_DATA_ID in update_data.items():
				NAME_UPDATE = UPDATE_DATA_ID["NAME_UPDATE"]
				SITE_UPDATE = UPDATE_DATA_ID.get("URL_UPDATE")

				ID_UPDATE_LIST.append(f" • <code>{ID_UPDATE}</code>: {NAME_UPDATE} — <a href='{SITE_UPDATE}'>Ссылка на описание обновления</a>;")
			
			if ID_UPDATE_LIST:
				return "\n\n".join(ID_UPDATE_LIST)
			else:
				return " • В данный момент нету обновлений."
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def GETTIMENOW(cls) -> datetime:
		try:
			return datetime.datetime.now().strftime("%Y\%m\%d • %H:%M:%S")
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def GETCURRENTHOUR(cls) -> str:
		"""Объявляем переменные для определенного текущего времени пользователя"""
		CURRENT_HOUR = datetime.datetime.now().hour

		try:
			if 6 <= CURRENT_HOUR < 12:
				return "Доброе утро"
			elif 12 <= CURRENT_HOUR < 18:
				return "Добрый день"
			elif 18 <= CURRENT_HOUR < 24:
				return "Добрый вечер"
			else:
				return "Доброй ночи"
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)
	
	@classmethod
	def GET_CURRENT_DAY(cls) -> str:
		"""Объявляем переменные для определенного текущего дня пользователя."""
		try:
			current_date = datetime.datetime.now()
			day_of_week = current_date.weekday()
			return calendar.day_name[day_of_week].upper()
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)
	
	@classmethod
	def GET_USER_DAY_YEAR_MONTH(cls, obj) -> str:
		"""Объявляем переменные для определенного текущего дня пользователя."""
		try:
			CURRENT_DATE = datetime.datetime.now()
			
			if obj == "day":
				return CURRENT_DATE.day
			
			elif obj == "year":
				return CURRENT_DATE.year
			
			elif obj == "month":
				return CURRENT_DATE.month
			
			else:
				return None
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)
	
	@classmethod
	def TRANSLATETOENGLISH(cls, text: str) -> Translator:
		"""Функция для перевода текста на английский язык с использованием внешнего сервиса"""
		try:
			translator = Translator()
			translation = translator.translate(text, dest='en').text

			return translation
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

			return None
	
	@classmethod
	def CHECKVKPROFILELINK(cls, link) -> bool:
		"""
		Проверяет корректность ссылки на профиль ВКонтакте.
		Возвращает True, если ссылка корректна, иначе False.
		"""
		try:
			vk_link_pattern = re.compile(r'^https?://(www\.)?vk\.com/(id\d+|.*[a-zA-Z].*)$')

			return bool(vk_link_pattern.match(link))
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

			return None

	@classmethod 
	def GETCOUNTRYINFO(cls, country_name: str) -> str:
		"""Функция ввода определение нации/страны"""
		try:
			response = requests.get(f'https://restcountries.com/v2/name/{country_name}')

			"""Проверка успешности запроса (HTTP-код 200) и наличия данных"""
			if response.status_code == 200:
				data = response.json()

				if data:
					return data[0]
				else:
					logger.warning("⚠️ API вернул пустой ответ для страны: %s", country_name)
			else:
				logger.error("⚠️ Неудачный запрос к API. Код: %d", response.status_code)
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)
		
		return None
	
	@classmethod
	def LOADERUSERS(cls):
		try:
			"""Загрузка данных пользователей из базы данных."""
			USER_DATA_DB = load_user_data()

			return [
				User(
					id=user_id,
					bot_id=user_id_data.get("BOT_ID"),
					name=user_id_data.get("USER_LAST_NAME"),
					profile=user_id_data.get("USER_NAME"),
					nation=user_id_data.get("NATION_USER"),
					user_role=user_id_data.get("NAME_USER_ROLE"),
					password=user_id_data.get("USER_PASSWORD"),
					verify=user_id_data.get("VERIFY_DATA", {}).get("STATUS_VERIFY_USER")
				)
				for user_id, user_id_data in USER_DATA_DB.items()
				if isinstance(user_id_data.get("USER_LAST_NAME"), str)
			]	
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

@dataclass
class ConfigBotAsync:
	@classmethod
	async def UPDATE_PROGRESS(cls, msg = None, update_stage = None, time_sleep = None, version = None, type = None) -> list:
		"""Асинхронная функция для обновления прогресса с текстом сообщения и этапом обновления в качестве параметров.
		
		Args:
		- msg (Optional[str]): Текст сообщения для обновления.
		- update_stage (Optional[int]): Этап процесса обновления.
		- time_sleep (Optional[int]): Время ожидания во время процесса обновления.
		- version (Optional[str]): Версия обновления.
		- type (Optional[object]): Тип отправки сообщения.
		"""
		try:
			loading_symbols = ["⠋", "⠙", "⠴", "⠦"]
			loading_symbols_two = ["....", "...", "..", "."]

			for _ in range(time_sleep):
				for symbol, symbol_two in zip(loading_symbols, loading_symbols_two):
					from data.loader import bot

					await asyncio.sleep(0.001)
					
					if update_stage == 1:
						send_message = f"💬 Установка обновления - <b>v{version}</b>.\n\n" \
										f" • {symbol} Проверка подключения к <b>GitHub</b>{symbol_two}\n\n" \
										"Мы стремимся предоставить вам лучший опыт использования."
						
					elif update_stage == 2:
						send_message = f"💬 Установка обновления - <b>v{version}</b>.\n\n" \
										f" • <b>Проверка подключения к GitHub.</b>\n" \
										f" • {symbol} Скачивание обновления с <b>GitHub</b>{symbol_two}\n\n" \
										"Мы стремимся предоставить вам лучший опыт использования."

					else:
						send_message = f"💬 Установка обновления - <b>v{version}</b>.\n\n" \
										f" • <b>Проверка подключения к GitHub.</b>\n" \
										f" • <b>Скачивание обновления с GitHub.</b>\n" \
										f" • {symbol} Установка обновления в процессе{symbol_two}\n\n" \
										"Мы стремимся предоставить вам лучший опыт использования."

					await bot.edit_message_text(text = send_message,
												chat_id = type.chat.id, 
												message_id = msg.message_id)
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)
		
	@classmethod
	async def NOTIFY_ADMINS(cls, database_users = None) -> None:
		"""Асинхронная функция для отправки сообщения о запуске бота всем админам."""
		try:
			from data.loader import bot

			for USER_ID, USER_DATA in database_users.items():
				"""Получаем информацию об пользователе: NOTIFY_ADMINS, USER_LAST_NAME, USER_NAME"""
				USER_LAST_NAME = USER_DATA["USER_LAST_NAME"]
				USER_NAME = USER_DATA["USER_NAME"]
				NOTIFY_ADMINS = USER_DATA["NOTIFY_DATA"].get("ADMIN_NOTIFY", {}).get("NOTIFY_RUN", False)

				if NOTIFY_ADMINS:	
					await bot.send_message(chat_id = int(USER_ID), text = f"🔔 • {ConfigBot.GETCURRENTHOUR()}, <a href='{USER_NAME}'>{USER_LAST_NAME}</a>, бот запущен в <b><i>{ConfigBot.GETTIMENOW()}</i></b>")
				
				elif not NOTIFY_ADMINS:
					pass
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)
	
	@classmethod
	async def NOTIFY_UPDATE_USERS(cls, database_users = None, env_version = None) -> None:
		"""Асинхронная функция для отправки сообщения о обновлении бота всем пользователям."""
		try:
			from data.loader import bot

			for USER_ID, USER_DATA in database_users.items():
				"""Получаем информацию об пользователе: USER_LAST_NAME, USER_NAME"""
				USER_LAST_NAME = USER_DATA["USER_LAST_NAME"]
				USER_NAME = USER_DATA["USER_NAME"]
				NOTIFY_UPDATE = USER_DATA["NOTIFY_DATA"].get("USER_NOTIFY", {}).get("NOTIFY_UPDATE", False)

				if NOTIFY_UPDATE:
					await bot.send_message(chat_id = int(USER_ID), text = f"💬 <a href='{USER_NAME}'>{USER_LAST_NAME}</a>! Рады сообщить, что вышла <b>новая версия - v{env_version}</b> нашего бота с улучшениями и новыми возможностями.\n\n"
																		f"❕ Для получения всех новинок и обновлений, пожалуйста, воспользуйтесь командой <b><code>/update</code></b>.\n\n"
																		f"Спасибо за ваше внимание и активное использование нашего бота! 🤍")
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)
	
	@classmethod
	async def NOTIFY_SELECT_RATION(cls, types = None, database_users = None, database_admins = None, name_ration = None) -> None:
		"""Асинхронная функция для отправки сообщения о выборе рациона."""
		try:
			from data.loader import bot

			for USER_DATA_ID in database_users:
				if USER_DATA_ID != ConfigBot(types).USERID and USER_DATA_ID not in database_admins:
					await bot.send_message(int(USER_DATA_ID), text = f"🔔 <a href='{ConfigBot.USERNAMEBOT(int(USER_DATA_ID))}'>{ConfigBot.USERLASTNAMEBOT(int(USER_DATA_ID))}</a>, мы рады сообщить вам, что администратор выбрал Рацион.\n\n"
							                                         f" • <b>Название Рациона:</b> [ <i>{name_ration}</i> ]\n\n"
																	 f"Для просмотра подробностей рациона, зайдите во вкладку <i><b>«{ConfigReplyKeyboard().RATION[4:]}»</b></i>.")
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	async def RELOAD_HANDLERS_FOR_UPDATE(cls, database_update = None, handler = None) -> None:
		"""Асинхронная функция обновления хандлеров для выпущенных новых обновлений."""
		try:
			from data.loader import dp

			for ID_UPDATE, UPDATE_DATA_ID in [(ID, DATA_ID) for ID, DATA_ID in database_update.items() if ID is not None]:
				dp.register_message_handler(handler, lambda message, text=f"{UPDATE_DATA_ID['EMODJI_UPDATE']} • {UPDATE_DATA_ID['NAME_UPDATE']}": message.text == text)
				
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	async def DELETE_MESSAGE_USERS_AND_ADMINS(cls, types = None, message_id = None) -> None:
		"""Асинхронная функция для удаления сообщений пользователей или админам."""
		try:
			from data.loader import bot

			if isinstance(message_id, int):
				await bot.delete_message(types.chat.id, message_id)
				await types.delete()
			
			elif message_id is None:
				return message_id
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)
	
	@classmethod
	async def SAVE_MESSAGE_ID(cls, user_id = None, send_message = None) -> None:
		"""Асинхронная функция для сохранения ID отправленного сообщения."""
		try:
			USER_DATA_DB = load_user_data()

			USER_DATA_DB[str(user_id)]["STATES_USER"]["PREVIOUS_MESSAGE_ID"] = send_message.message_id

			save_user_data(USER_DATA_DB)
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)