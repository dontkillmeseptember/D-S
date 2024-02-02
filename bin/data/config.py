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
	Union
)

from misc.loggers import logger

from data.user_db import check_user_data
from data.market_db import check_market_data
from data.admin_db import load_admin_data, is_admin_in_data
from data.rsb_db import check_rsb_data, is_rsb_in_data, load_rsb_data, save_rsb_data

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
			"""Вывод данных пользователя - Последние имя пользователя"""
			if isinstance(obj, (types.Message, types.CallbackQuery)):
				return obj.from_user.first_name
			
			else:
				logger.warning("⚠️ Произошел сбой с ISINSTANCE.")
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)
	
	@classmethod
	def USERNAME(cls, obj) -> bool:
		"""Вывод данных пользователя - Ссылку на профиль пользователя"""
		if isinstance(obj, types.Message):
			"""Возвращаем значение для types.Message"""
			return obj.from_user.username if obj.from_user.username else None
		elif isinstance(obj, types.CallbackQuery):
			"""Возвращаем значение для types.CallbackQuery"""
			return obj.from_user.username if obj.from_user.username else None
		else:
			raise ValueError("ERROR: 901, FILE: CONFIG, FUNC: USERNAME")
	
	@classmethod
	def USERID(cls, obj) -> int:
		"""Выводим данных пользователя - USER_ID Пользователя"""
		if isinstance(obj, types.Message):
			"""Возвращаем значение для types.Message"""
			return obj.from_user.id
		elif isinstance(obj, types.CallbackQuery):
			"""Возвращаем значение для types.CallbackQuery"""
			return obj.from_user.id
		else:
			raise ValueError("ERROR: 901, FILE: CONFIG, FUNC: USERID")

	@classmethod
	def USERBOTID(cls, obj) -> int:
		"""Выводим данных пользователя - BOT_ID Пользователя"""
		if isinstance(obj, types.Message):
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(ConfigBot.USERID(obj))
			"""Выводим информацию о BOT_ID пользователя"""
			bot_id_user = check_user_data_db.get("BOT_ID")

			return bot_id_user
		if isinstance(obj, types.CallbackQuery):
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(ConfigBot.USERID(obj))
			"""Выводим информацию о BOT_ID пользователя"""
			bot_id_user = check_user_data_db.get("BOT_ID")

			return bot_id_user
		else:
			raise ValueError("ERROR: 901, FILE: CONFIG, FUNC: USERBOTID")
		
	@classmethod
	def USERNATION(cls, obj) -> str:
		"""Выводим данных пользователя - USER_NATION Пользователя"""
		if isinstance(obj, types.Message):
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(ConfigBot.USERID(obj))
			"""Выводим информацию о NATION_USER пользователя"""
			nation = check_user_data_db.get("NATION_USER")

			return nation
		if isinstance(obj, types.CallbackQuery):
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(ConfigBot.USERID(obj))
			"""Выводим информацию о NATION_USER пользователя"""
			nation = check_user_data_db.get("NATION_USER")

			return nation
		else:
			raise ValueError("ERROR: 901, FILE: CONFIG, FUNC: USERNATION")

	@classmethod
	def USERPASSWORD(cls, obj) -> str:
		"""Выводим данных пользователя - USER_PASSWORD Пользователя"""
		if isinstance(obj, types.Message):
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(ConfigBot.USERID(obj))
			"""Выводим информацию о USER_PASSWORD пользователя"""
			password = check_user_data_db.get("USER_PASSWORD")

			return password
		if isinstance(obj, types.CallbackQuery):
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(ConfigBot.USERID(obj))
			"""Выводим информацию о USER_PASSWORD пользователя"""
			password = check_user_data_db.get("USER_PASSWORD")

			return password
		else:
			raise ValueError("ERROR: 901, FILE: CONFIG, FUNC: USERPASSWORD")

	@classmethod
	def USERROLE(cls, obj) -> str:
		"""Выводим данных пользователя - USER_ROLE Пользователя"""
		if isinstance(obj, types.Message):
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(ConfigBot.USERID(obj))
			"""Выводим информацию о USER_ROLE пользователя"""
			smile = check_user_data_db.get("USER_ROLE")

			return smile
		if isinstance(obj, types.CallbackQuery):
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(ConfigBot.USERID(obj))
			"""Выводим информацию о USER_ROLE пользователя"""
			smile = check_user_data_db.get("USER_ROLE")

			return smile
		else:
			raise ValueError("ERROR: 901, FILE: CONFIG, FUNC: USERROLE")

	@classmethod
	def USERROLENAME(cls, obj) -> str:
		"""Выводим данных пользователя - NAME_USER_ROLE Пользователя"""
		if isinstance(obj, types.Message):
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(ConfigBot.USERID(obj))
			"""Выводим информацию о NAME_USER_ROLE пользователя"""
			role_name = check_user_data_db.get("NAME_USER_ROLE")

			return role_name
		if isinstance(obj, types.CallbackQuery):
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(ConfigBot.USERID(obj))
			"""Выводим информацию о NAME_USER_ROLE пользователя"""
			role_name = check_user_data_db.get("NAME_USER_ROLE")

			return role_name
		else:
			raise ValueError("ERROR: 901, FILE: CONFIG, FUNC: USERROLENAME")

	@classmethod
	def USERNAMEBOT(cls, obj) -> str:
		"""Выводим данных пользователя - USER_NAME Пользователя"""
		try:
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(obj)
			"""Выводим информацию о USER_NAME пользователя"""
			user_name_bot = check_user_data_db.get("USER_NAME")

			return user_name_bot
		except:
			raise ValueError("ERROR: 901, FILE: CONFIG, FUNC: USERNAMEBOT")
			
	@classmethod
	def USERLASTNAMEBOT(cls, obj) -> str:
		"""Выводим данных пользователя - USER_LAST_NAME Пользователя"""
		try:
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(obj)
			"""Выводим информацию о USER_LAST_NAME пользователя"""
			user_last_name_bot = check_user_data_db.get("USER_LAST_NAME")

			return user_last_name_bot
		except:
			raise ValueError("ERROR: 901, FILE: CONFIG, FUNC: USERLASTNAMEBOT")
			

	@classmethod
	def USERVERSIONBOT(cls, obj) -> bool:
		"""Выводим данных пользователя - VERSION_BOT Пользователя"""
		if isinstance(obj, types.Message):
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(ConfigBot.USERID(obj))
			"""Выводим информацию о VERSION_BOT пользователя"""
			version = check_user_data_db.get("VERSION_BOT")

			return version
		if isinstance(obj, types.CallbackQuery):
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(ConfigBot.USERID(obj))
			"""Выводим информацию о VERSION_BOT пользователя"""
			version = check_user_data_db.get("VERSION_BOT")

			return version
		else:
			raise ValueError("ERROR: 901, FILE: CONFIG, FUNC: USERVERSIONBOT")

	@classmethod
	def USERSTATUSVERIFY(cls, obj) -> str:
		"""Выводим данных пользователя - STATUS_VERIFY_USER Пользователя"""
		if isinstance(obj, types.Message):
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(ConfigBot.USERID(obj))
			"""Выводим информацию о STATUS_VERIFY_USER пользователя"""
			status_verify = check_user_data_db.get("VERIFY_DATA", {}).get("STATUS_VERIFY_USER")

			return status_verify
		if isinstance(obj, types.CallbackQuery):
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(ConfigBot.USERID(obj))
			"""Выводим информацию о STATUS_VERIFY_USER пользователя"""
			status_verify = check_user_data_db.get("VERIFY_DATA", {}).get("STATUS_VERIFY_USER")

			return status_verify
		else:
			raise ValueError("ERROR: 901, FILE: CONFIG, FUNC: USERSTATUSVERIFY")

	@classmethod
	def USERVERIFY(cls, obj) -> Union[bool, None]:
		"""Выводим данных пользователя - VERIFY_USER Пользователя"""
		if isinstance(obj, types.Message):
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(ConfigBot.USERID(obj))
			"""Выводим информацию о VERIFY_USER пользователя"""
			verify = check_user_data_db.get("VERIFY_DATA", {}).get("VERIFY_USER")

			return verify
		if isinstance(obj, types.CallbackQuery):
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(ConfigBot.USERID(obj))
			"""Выводим информацию о VERIFY_USER пользователя"""
			verify = check_user_data_db.get("VERIFY_DATA", {}).get("VERIFY_USER")

			return verify
		else:
			raise ValueError("ERROR: 901, FILE: CONFIG, FUNC: USERVERIFY")

	@classmethod
	def USERVERIFYCODE(cls, obj) -> int:
		"""Выводим данных пользователя - VERIFY_CODE_USER Пользователя"""
		if isinstance(obj, types.Message):
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(ConfigBot.USERID(obj))
			"""Выводим информацию о VERIFY_CODE_USER пользователя"""
			verify_code = check_user_data_db.get("VERIFY_DATA", {}).get("VERIFY_CODE_USER")

			return verify_code
		if isinstance(obj, types.CallbackQuery):
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(ConfigBot.USERID(obj))
			"""Выводим информацию о VERIFY_CODE_USER пользователя"""
			verify_code = check_user_data_db.get("VERIFY_DATA", {}).get("VERIFY_CODE_USER")

			return verify_code
		else:
			raise ValueError("ERROR: 901, FILE: CONFIG, FUNC: USERVERIFYCODE")

	@classmethod
	def USERCONSIDERATIONVERIFY(cls, obj) -> True or False:
		"""Выводим данных пользователя - CONSIDERATION_VERIFY_USER Пользователя"""
		if isinstance(obj, types.Message):
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(ConfigBot.USERID(obj))
			"""Выводим информацию о CONSIDERATION_VERIFY_USER пользователя"""
			verify_code = check_user_data_db.get("VERIFY_DATA", {}).get("CONSIDERATION_VERIFY_USER")

			return verify_code
		if isinstance(obj, types.CallbackQuery):
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(ConfigBot.USERID(obj))
			"""Выводим информацию о CONSIDERATION_VERIFY_USER пользователя"""
			verify_code = check_user_data_db.get("VERIFY_DATA", {}).get("CONSIDERATION_VERIFY_USER")

			return verify_code
		else:
			raise ValueError("ERROR: 901, FILE: CONFIG, FUNC: USERCONSIDERATIONVERIFY")

	@classmethod
	def USERREGISTORWALLET(cls, obj) -> True or False:
		"""Выводим данных пользователя - REGISTOR_WALLET_USER Пользователя"""
		if isinstance(obj, types.Message):
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(ConfigBot.USERID(obj))
			"""Выводим информацию о REGISTOR_WALLET_USER пользователя"""
			registor_wallet = check_user_data_db.get("RSB_DATA", {}).get("REGISTOR_WALLET_USER")

			return registor_wallet
		if isinstance(obj, types.CallbackQuery):
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(ConfigBot.USERID(obj))
			"""Выводим информацию о REGISTOR_WALLET_USER пользователя"""
			registor_wallet = check_user_data_db.get("RSB_DATA", {}).get("REGISTOR_WALLET_USER")

			return registor_wallet
		else:
			raise ValueError("ERROR: 901, FILE: CONFIG, FUNC: USERREGISTORWALLET")

	@classmethod
	def USERMESSAGE(cls, message) -> bool:
		"""Вводим сообщение пользователя для регистрации пароля и т.д."""
		return message.text

	@classmethod
	def GETBOTID(cls) -> random:
		"""Генерация случайного 9-значного BOT_ID"""
		BOT_ID = ''.join(str(random.randint(0, 9)) for _ in range(9))
		
		return BOT_ID

	@classmethod
	def GETVERIFYCODE(cls) -> random:
		"""Генерируем четырехзначный код для верификации аккаунта"""
		VERIFY_CODE = ''.join(str(random.randint(0, 9)) for _ in range(4))

		return VERIFY_CODE

	@classmethod
	def GETLENUSERS(cls, obj) -> int:
		"""Выводим определенное количество чего-то"""
		try:
			"""Получаем количество зарегистрированных пользователей"""
			if isinstance(obj, (list, dict)):
				"""Получаем значение int и выводим его"""
				get_int_users = len(obj)

				return get_int_users
		except:
			raise ValueError("ERROR: 901, FILE: CONFIG, FUNC: GETLENUSERS")

	@classmethod
	def GETCOUNTVERIFITEDUSERS(cls, user_data) -> int:
		"""Выводим количество верифицированных пользователей"""
		try:
			verified_users = [user for user in user_data.values() if user.get("VERIFY_DATA", {}).get("VERIFY_USER", False)]

			return len(verified_users)
		except:
			raise ValueError("ERROR: 901, FILE: CONFIG, FUNC: GETCOUNTVERIFITEDUSERS")

	@classmethod
	def GETCONSIDERATIONVERIFY(cls, user_data) -> int and str:
		"""Выводим информацию о пользователей которые имеют ключ "CONSIDERATION_VERIFY_USER": true"""
		try:
			"""Счетчик для нумерации пользователей"""
			user_info_list = []

			for user_id, user_info in user_data.items():
				if "VERIFY_DATA" in user_info and user_info["VERIFY_DATA"]["CONSIDERATION_VERIFY_USER"]:
					"""Подготовка данных для сообщения"""
					last_name = user_info["USER_LAST_NAME"]
					user_name = user_info["USER_NAME"]
					link_profile = user_info["VERIFY_DATA"]["LINK_PROFILE_USER"]

					"""Добавление информации о пользователе в список"""
					user_info_list.append(f" • {len(user_info_list) + 1}: <a href=\"{user_name}\">{last_name}</a> — <a href=\"{link_profile}\">Ссылка на Профиль</a> — <code>{user_id}</code>")

			"""Если есть пользователи на рассмотрении, объединяем строки в одну строку"""
			if user_info_list:
				return "\n".join(user_info_list)
			else:
				return " • Нет пользователей на рассмотрении для верификации."
		except:
			raise ValueError("ERROR: 901, FILE: CONFIG, FUNC: GETCOUNTVERIFITEDUSERS")

	@classmethod
	def GETRSB(cls, rsb_data, obj, users_or_admin, types) -> bool:
		"""Выводим информацию о кошельке из базы данных"""
		try:
			try:
				if users_or_admin == False:
					"""Загружаем базу данных о RSB"""
					rsb_data_db = load_rsb_data()

					"""Получаем доступ к базе данных о пользователе"""
					check_user_data_db = check_user_data(ConfigBot.USERID(types))

					"""Выводим информацию о NUMBER_WALLET_USER пользователя"""
					number_wallet = check_user_data_db.get("RSB_DATA", {}).get("NUMBER_WALLET_USER")

					if is_rsb_in_data(number_wallet, rsb_data_db):
						"""Вводим из message номер кошелька и проверяем его"""
						check_rsb_data_db = check_rsb_data(number_wallet)

						if obj == "WALLET":
							return number_wallet

						elif obj == "ETH":
							ETH = check_rsb_data_db.get("ETH")
			
							return ETH
						elif obj == "USD":
							USD = check_rsb_data_db.get("USD")

							return USD
						elif obj == "RUB":
							RUB = check_rsb_data_db.get("RUB")

							return RUB
						elif obj == "CURRENT_ETH":
							CURRENT_ETH = check_rsb_data_db.get("CURRENT", {}).get("CURRENT_ETH")

							return CURRENT_ETH
						elif obj == "CURRENT_USD":
							CURRENT_USD = check_rsb_data_db.get("CURRENT", {}).get("CURRENT_USD")

							return CURRENT_USD
						elif obj == "CURRENT_RUB":
							CURRENT_RUB = check_rsb_data_db.get("CURRENT", {}).get("CURRENT_RUB")

							return CURRENT_RUB
						elif obj == "INTEREST_USER_ONE":
							INTEREST_USER_ONE = check_rsb_data_db.get("INTEREST", {}).get("INTEREST_USER_ONE")

							return INTEREST_USER_ONE
						elif obj == "INTEREST_USER_TWO":
							INTEREST_USER_TWO = check_rsb_data_db.get("INTEREST", {}).get("INTEREST_USER_TWO")

							return INTEREST_USER_TWO
						elif obj == "ALL_SUM_ETH":
							ALL_SUM_ETH_END = check_rsb_data_db.get("ALL_SUM_WALLET", {}).get("ALL_SUM_ETH_END")

							if ALL_SUM_ETH_END > 0:
								return ALL_SUM_ETH_END
							elif ALL_SUM_ETH_END == 0:
								ALL_SUM_ETH_START = check_rsb_data_db.get("ALL_SUM_WALLET", {}).get("ALL_SUM_ETH_START")

								return ALL_SUM_ETH_START
						elif obj == "ALL_SUM_USD":
							ALL_SUM_USD_END = check_rsb_data_db.get("ALL_SUM_WALLET", {}).get("ALL_SUM_USD_END")

							if ALL_SUM_USD_END > 0:
								return ALL_SUM_USD_END
							elif ALL_SUM_USD_END == 0:
								ALL_SUM_USD_START = check_rsb_data_db.get("ALL_SUM_WALLET", {}).get("ALL_SUM_USD_START")

								return ALL_SUM_USD_START
						elif obj == "ALL_SUM_RUB":
							ALL_SUM_RUB_END = check_rsb_data_db.get("ALL_SUM_WALLET", {}).get("ALL_SUM_RUB_END")

							if ALL_SUM_RUB_END > 0:
								return ALL_SUM_RUB_END
							elif ALL_SUM_RUB_END == 0:
								ALL_SUM_RUB_START = check_rsb_data_db.get("ALL_SUM_WALLET", {}).get("ALL_SUM_RUB_START")

								return ALL_SUM_RUB_START
					elif not is_rsb_in_data(number_wallet, rsb_data_db):
						return None
					
				elif users_or_admin == True:
					"""Вводим из message номер кошелька и проверяем его"""
					check_rsb_data_db = check_rsb_data(rsb_data)

					if obj == "ETH":
						ETH = check_rsb_data_db.get("ETH")

						return ETH
					elif obj == "USD":
						USD = check_rsb_data_db.get("USD")

						return USD
					elif obj == "RUB":
						RUB = check_rsb_data_db.get("RUB")

						return RUB
					elif obj == "CURRENT_ETH":
						CURRENT_ETH = check_rsb_data_db.get("CURRENT", {}).get("CURRENT_ETH")

						return CURRENT_ETH
					elif obj == "CURRENT_USD":
						CURRENT_USD = check_rsb_data_db.get("CURRENT", {}).get("CURRENT_USD")

						return CURRENT_USD
					elif obj == "CURRENT_RUB":
						CURRENT_RUB = check_rsb_data_db.get("CURRENT", {}).get("CURRENT_RUB")

						return CURRENT_RUB
					elif obj == "INTEREST_USER_ONE":
						INTEREST_USER_ONE = check_rsb_data_db.get("INTEREST", {}).get("INTEREST_USER_ONE")

						return INTEREST_USER_ONE
					elif obj == "INTEREST_USER_TWO":
						INTEREST_USER_TWO = check_rsb_data_db.get("INTEREST", {}).get("INTEREST_USER_TWO")

						return INTEREST_USER_TWO
					elif obj == "ALL_SUM_ETH":
						ALL_SUM_ETH_END = check_rsb_data_db.get("ALL_SUM_WALLET", {}).get("ALL_SUM_ETH_END")

						if ALL_SUM_ETH_END > 0:
							return ALL_SUM_ETH_END
						elif ALL_SUM_ETH_END == 0:
							ALL_SUM_ETH_START = check_rsb_data_db.get("ALL_SUM_WALLET", {}).get("ALL_SUM_ETH_START")

							return ALL_SUM_ETH_START
					elif obj == "ALL_SUM_USD":
						ALL_SUM_USD_END = check_rsb_data_db.get("ALL_SUM_WALLET", {}).get("ALL_SUM_USD_END")

						if ALL_SUM_USD_END > 0:
							return ALL_SUM_USD_END
						elif ALL_SUM_USD_END == 0:
							ALL_SUM_USD_START = check_rsb_data_db.get("ALL_SUM_WALLET", {}).get("ALL_SUM_USD_START")

							return ALL_SUM_USD_START
					elif obj == "ALL_SUM_RUB":
						ALL_SUM_RUB_END = check_rsb_data_db.get("ALL_SUM_WALLET", {}).get("ALL_SUM_RUB_END")

						if ALL_SUM_RUB_END > 0:
							return ALL_SUM_RUB_END
						elif ALL_SUM_RUB_END == 0:
							ALL_SUM_RUB_START = check_rsb_data_db.get("ALL_SUM_WALLET", {}).get("ALL_SUM_RUB_START")

							return ALL_SUM_RUB_START
				else:
					return None
			except:
				return None
		except:
			raise ValueError("ERROR: 901, FILE: CONFIG, FUNC: GETRSB")

	@classmethod
	def GETNUMBERWALLETRSB(cls, rsb_data, user_id) -> int:
		"""Проверяем зарегистрирован пользователь в базе админов"""
		admin_data_db = load_admin_data()

		"""Выводим ID кошельков из базы данных RSB"""
		try:
			"""Счетчик для нумерации ID Кошельков"""
			number_wallet_info_list = []

			if is_admin_in_data(user_id, admin_data_db):
				for wallet_number, rsb_info in rsb_data.items():
					"""Выводим краткую информацию о ID кошельков"""
					ETH = rsb_info["ETH"]

					"""Добавление ID кошельков в список"""
					number_wallet_info_list.append(f" • <code>{wallet_number}</code> ~ <b>{ETH} ETH</b>")

			"""Если есть ID кошельки в базе данных, объединяем строки в одну строку"""
			if number_wallet_info_list:
				return "\n".join(number_wallet_info_list)
			else:
				return " • В данный момент нету ID кошельков."
		except:
			raise ValueError("ERROR: 901, FILE: CONFIG, FUNC: GETARTICLEMARKET")
		
	@classmethod
	def GETETHTOUSD(cls) -> int:
		"""Выполняет расчет из ETH в USD"""
		try:
			url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
			response = requests.get(url)

			if response.status_code == 200:
				data = response.json()
				eth_to_usd_rate = data.get("ethereum", {}).get("usd")

				return eth_to_usd_rate
			else:
				return -1
		except:
			raise ValueError("ERROR: 901, FILE: CONFIG, FUNC: GETETHTOUSD")

	@classmethod
	def GETETHTORUB(cls) -> int:
		"""Выполняет расчет из ETH в RUB"""
		try:
			url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=rub"
			response = requests.get(url)
			
			if response.status_code == 200:
				data = response.json()
				eth_to_rub_rate = data.get("ethereum", {}).get("rub")

				return eth_to_rub_rate
			else:
				return -1
		except:
			raise ValueError("ERROR: 901, FILE: CONFIG, FUNC: GETETHTORUB")
		
	@classmethod
	def GETMARKET(cls, market_data, obj) -> bool:
		"""Выводим данные товаров из базы данных"""
		try:
			"""Вводим из message артикул пользователя и проверяем его"""
			check_market_data_db = check_market_data(market_data)

			try:
				if obj == "URL_PHOTO":
					URL_PHOTO = check_market_data_db.get("URL_PHOTO")

					return URL_PHOTO
				elif obj == "URL_SITE":
					URL_SITE = check_market_data_db.get("URL_SITE")

					return URL_SITE
				elif obj == "PRICE":
					PRICE = check_market_data_db.get("PRICE")
					"""Форматируем цену товара, чтобы она выглядела не 1400, а 1 400"""
					END_PRICE = "{:,}".format(PRICE).replace(',', ' ')

					return END_PRICE
				elif obj == "NAME_MARKET":
					NAME_MARKET = check_market_data_db.get("NAME_MARKET")

					return NAME_MARKET
				elif obj == "MESSAGE":
					MESSAGE = check_market_data_db.get("MESSAGE")

					return MESSAGE
			except:
				return None
		except:
			raise ValueError("ERROR: 901, FILE: CONFIG, FUNC: GETMARKET")

	@classmethod
	def GETPRICE(cls, art):
		"""Получение цены товара исходя из его ссылки на базу данных сайта"""
		try:
			"""Вводим из message артикул пользователя и проверяем его"""
			check_market_data_db = check_market_data(art)

			"""Получаем ссылку на товар из базы данных маркета"""
			URL_SITE = check_market_data_db.get("URL_SITE")

			if ConfigBot.CHECKWILDBERRIESLINK(URL_SITE) == True:
				"""Ссылка на базу данных JSON файл от WB, где мы берем цену товара"""
				url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=123585924&spp=27&nm={art}"

				"""Выполнение запроса по ссылке"""
				response = requests.get(url)

				"""Проверка статуса ответа"""
				if response.status_code == 200:
					json_data = response.json()
					
					if "data" in json_data and "products" in json_data["data"]:
						products = json_data["data"]["products"]
						
						for product in products:
							if "salePriceU" in product:
								sale_price = product["salePriceU"]
								sale_price = str(sale_price)
								sale_price = sale_price.rstrip("00")
								sale_price = int(sale_price)
								
								return sale_price
					else:
						return None
				else:
					raise ValueError("ERROR: 404, FILE: CONFIG, FUNC: GETPRICE, TESTING: RESPONSE")
				
			elif ConfigBot.CHECKLAMODALINK(URL_SITE) == True:
				"""Ссылка на базу данных JSON файл от Lamoda, где мы берем цену товара"""
				url = f"https://www.lamoda.ru/api/v1/product/get?sku={art}&city_aoid=6100000500000&is_hybrid_supported=true&size_id=0"

				"""Выполнение запроса по ссылке"""
				response = requests.get(url)

				"""Проверка статуса ответа"""
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
					raise ValueError("ERROR: 404, FILE: CONFIG, FUNC: GETPRICE, TESTING: RESPONSE")
			else:
				return None
		except:
			raise ValueError("ERROR: 901, FILE: CONFIG, FUNC: GETPRICE")

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
		except:
			print("ERROR: 404, FILE: CONFIG, FUNC: CHECKLAMODALINK")

			return None

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
		except:
			print("ERROR: 404, FILE: CONFIG, FUNC: CHECKWILDBERRIESLINK")

			return None

	@classmethod
	def GETARTICLEMARKET(cls, market_data, user_id) -> int:
		"""Проверяем зарегистрирован пользователь в базе админов"""
		admin_data_db = load_admin_data()

		"""Выводим артикулы из базы данных маркета"""
		try:
			"""Счетчик для нумерации артикулов"""
			article_info_list = []

			if is_admin_in_data(user_id, admin_data_db):
				for article_number, market_info in market_data.items():
					"""Подготовка данных для сообщения"""
					name_market = market_info["NAME_MARKET"]
					site_market = market_info["URL_SITE"]

					"""Добавление информации о товаре в список"""
					article_info_list.append(f" • <code>{article_number}</code>: {name_market} — <a href ='{site_market}'>Ссылка на сайт</a>")
			
			if not is_admin_in_data(user_id, admin_data_db):
				for article_number, market_info in market_data.items():
					"""Подготовка данных для сообщения"""
					name_market = market_info["NAME_MARKET"]

					"""Добавление информации о товаре в список"""
					article_info_list.append(f" • <code>{article_number}</code>: {name_market}")

			"""Если есть товар в корзине, объединяем строки в одну строку"""
			if article_info_list:
				return "\n".join(article_info_list)
			else:
				return " • В данный момент нету товаров в корзине"
		except:
			raise ValueError("ERROR: 901, FILE: CONFIG, FUNC: GETARTICLEMARKET")

	@classmethod
	def GETTIMENOW(cls) -> datetime:
		"""Переменная для вывода текущего времени пользователя и формативание его"""
		current_time = datetime.datetime.now().strftime("%Y\%m\%d • %H:%M:%S")

		return current_time

	@classmethod
	def GETCURRENTHOUR(cls) -> datetime:
		"""Переменные для вывода текущего времени пользователя"""
		date = datetime.datetime.now()
		current_hour = date.hour

		"""Выводим сообщение зависимости от времени суток, то есть если утро - Доброе утро, и т.д."""
		if 6 <= current_hour < 12:
			"""Выводим сообщение с добрым утром"""
			message_greeting = "Доброе утро"
			"""Возвращаем переменную с выводом сообщения"""
			return message_greeting
		elif 12 <= current_hour < 18:
			"""Выводим сообщение с добрый день"""
			message_greeting = "Добрый день"
			"""Возвращаем переменную с выводом сообщения"""
			return message_greeting
		elif 18 <= current_hour < 24:
			"""Выводим сообщение с добрый вечер"""
			message_greeting = "Добрый вечер"
			"""Возвращаем переменную с выводом сообщения"""
			return message_greeting
		else:
			"""Выводим сообщение с доброй ночи"""
			message_greeting = "Доброй ночи"
			"""Возвращаем переменную с выводом сообщения"""
			return message_greeting
	
	@classmethod
	def TRANSLATETOENGLISH(cls, text) -> Translator:
		"""Функция для перевода текста на английский язык с использованием внешнего сервиса"""
		try:
			"""Попытка выполнить перевод текста на английский язык"""
			translator = Translator()
			translation = translator.translate(text, dest='en')

			return translation.text
		except:
			print("ERROR: 404, FILE: LOADER, FUNC: TRANSLATE_TO_ENGLISH")

			return None
	
	@classmethod
	def CHECKVKPROFILELINK(cls, link) -> bool:
		"""
		Проверяет корректность ссылки на профиль ВКонтакте.
		Возвращает True, если ссылка корректна, иначе False.
		"""
		try:
			"""Проверка ссылки на профиль ВКонтакте"""
			vk_link_pattern = re.compile(r'^https?://(www\.)?vk\.com/(id\d+|.*[a-zA-Z].*)$')

			return bool(vk_link_pattern.match(link))
		except:
			print("ERROR: 404, FILE: CONFIG, FUNC: CHECKVKPROFILELINK")

			return None

	@classmethod 
	def GETCOUNTRYINFO(cls, country_name) -> str:
		"""Функция ввода определение нации/страны"""
		try:
			"""Отправка запроса к внешнему API для получения информации о стране по её имени"""
			response = requests.get(f'https://restcountries.com/v2/name/{country_name}')
			"""Преобразование ответа в формат JSON"""
			data = response.json()

			"""Проверка успешности запроса (HTTP-код 200) и наличия данных"""
			if response.status_code == 200 and data:
				"""Возвращение информации о первой стране в списке (возможно, существует несколько стран с одинаковым именем)"""
				return data[0]
			else:
				"""В случае отсутствия данных или неудачного запроса, возврат значения None"""
				return None
		except:
			print("ERROR: 404, FILE: LOADER, FUNC: GET_COUNTRY_INFO")
		
			return None