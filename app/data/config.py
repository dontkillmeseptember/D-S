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
			"""Вывод данные пользователя - Последние имя пользователя"""
			if isinstance(obj, (types.Message, types.CallbackQuery)):
				return obj.from_user.first_name if obj.from_user.username else None
			else:
				logger.warning("⚠️ Произошел сбой с ISINSTANCE.")
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)
	
	@classmethod
	def USERNAME(cls, obj) -> str:
		try:
			"""Вывод данные пользователя - Ссылку на профиль пользователя"""
			if isinstance(obj, (types.Message, types.CallbackQuery)):
				return obj.from_user.username if obj.from_user.username else None
			else:
				logger.warning("⚠️ Произошел сбой с ISINSTANCE.")
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)
	
	@classmethod
	def USERID(cls, obj) -> int:
		try:
			"""Выводим данные пользователя - USER_ID Пользователя"""
			if isinstance(obj, (types.Message, types.CallbackQuery)):
				return obj.from_user.id if obj.from_user.id else None
			else:
				logger.warning("⚠️ Произошел сбой с ISINSTANCE.")
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
				BOT_ID_USER = check_user_data_db.get("BOT_ID")

				return BOT_ID_USER
			else:
				logger.warning("⚠️ Произошел сбой с ISINSTANCE.")
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
				USER_NATION = check_user_data_db.get("NATION_USER")

				return USER_NATION
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
				USER_PASSWORD = check_user_data_db.get("USER_PASSWORD")

				return USER_PASSWORD
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
				USER_ROLE = check_user_data_db.get("USER_ROLE")

				return USER_ROLE
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
				USER_ROLE_NAME = check_user_data_db.get("NAME_USER_ROLE")

				return USER_ROLE_NAME
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def USERNAMEBOT(cls, obj) -> str:
		"""Выводим данных пользователя - USER_NAME Пользователя"""
		try:
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(obj)
			"""Выводим информацию о USER_NAME пользователя"""
			USER_BOT_NAME = check_user_data_db.get("USER_NAME")

			return USER_BOT_NAME
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)
			
	@classmethod
	def USERLASTNAMEBOT(cls, obj) -> str:
		"""Выводим данных пользователя - USER_LAST_NAME Пользователя"""
		try:
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(obj)
			"""Выводим информацию о USER_LAST_NAME пользователя"""
			USER_BOT_LAST_NAME = check_user_data_db.get("USER_LAST_NAME")

			return USER_BOT_LAST_NAME
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def USERVERSIONBOT(cls, obj) -> float:
		try:
			"""Выводим данных пользователя - VERSION_BOT Пользователя"""
			if isinstance(obj, (types.Message, types.CallbackQuery)):
				"""Получаем доступ к базе данных о пользователе"""
				USER_ID = ConfigBot.USERID(obj)
				check_user_data_db = check_user_data(USER_ID)
				"""Выводим информацию о VERSION_BOT пользователя"""
				VERSION_BOT = check_user_data_db.get("VERSION_BOT")

				return VERSION_BOT
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def USERSTATUSVERIFY(cls, obj) -> bool:
		try:
			"""Выводим данных пользователя - STATUS_VERIFY_USER Пользователя"""
			if isinstance(obj, (types.Message, types.CallbackQuery)):
				"""Получаем доступ к базе данных о пользователе"""
				USER_ID = ConfigBot.USERID(obj)
				check_user_data_db = check_user_data(USER_ID)
				"""Выводим информацию о STATUS_VERIFY_USER пользователя"""
				USER_STATUS_VERIFICATION = check_user_data_db.get("VERIFY_DATA", {}).get("STATUS_VERIFY_USER")

				return USER_STATUS_VERIFICATION
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def USERVERIFY(cls, obj) -> Union[bool, None]:
		try:
			"""Выводим данных пользователя - VERIFY_USER Пользователя"""
			if isinstance(obj, (types.Message, types.CallbackQuery)):
				"""Получаем доступ к базе данных о пользователе"""
				USER_ID = ConfigBot.USERID(obj)
				check_user_data_db = check_user_data(USER_ID)
				"""Выводим информацию о VERIFY_USER пользователя"""
				USER_VERIFICATION = check_user_data_db.get("VERIFY_DATA", {}).get("VERIFY_USER")

				return USER_VERIFICATION
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def USERVERIFYCODE(cls, obj) -> int:
		try:
			"""Выводим данных пользователя - VERIFY_CODE_USER Пользователя"""
			if isinstance(obj, (types.Message, types.CallbackQuery)):
				"""Получаем доступ к базе данных о пользователе"""
				USER_ID = ConfigBot.USERID(obj)
				check_user_data_db = check_user_data(USER_ID)
				"""Выводим информацию о VERIFY_CODE_USER пользователя"""
				BOT_VERIFICATION_CODE = check_user_data_db.get("VERIFY_DATA", {}).get("VERIFY_CODE_USER")

				return BOT_VERIFICATION_CODE
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def USERCONSIDERATIONVERIFY(cls, obj) -> True:
		try:
			"""Выводим данных пользователя - CONSIDERATION_VERIFY_USER Пользователя"""
			if isinstance(obj, (types.Message, types.CallbackQuery)):
				"""Получаем доступ к базе данных о пользователе"""
				USER_ID = ConfigBot.USERID(obj)
				check_user_data_db = check_user_data(USER_ID)
				"""Выводим информацию о CONSIDERATION_VERIFY_USER пользователя"""
				USER_CONSIDERATION_VERIFICATION = check_user_data_db.get("VERIFY_DATA", {}).get("CONSIDERATION_VERIFY_USER")

				return USER_CONSIDERATION_VERIFICATION
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def USERREGISTORWALLET(cls, obj) -> True:
		try:
			"""Выводим данных пользователя - REGISTOR_WALLET_USER Пользователя"""
			if isinstance(obj, (types.Message, types.CallbackQuery)):
				"""Получаем доступ к базе данных о пользователе"""
				USER_ID = ConfigBot.USERID(obj)
				check_user_data_db = check_user_data(USER_ID)
				"""Выводим информацию о REGISTOR_WALLET_USER пользователя"""
				USER_REGISTOR_WALLET = check_user_data_db.get("RSB_DATA", {}).get("REGISTOR_WALLET_USER")

				return USER_REGISTOR_WALLET
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def USERMESSAGE(cls, message) -> float:
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
				return len(obj)
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def GETCOUNTVERIFITEDUSERS(cls, user_data) -> int:
		"""Выводим количество верифицированных пользователей"""
		try:
			verified_users = [user for user in user_data.values() if user.get("VERIFY_DATA", {}).get("VERIFY_USER", False)]

			return len(verified_users)
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def GETCONSIDERATIONVERIFY(cls, user_data) -> Union[int, str]:
		"""Выводим информацию о пользователей которые имеют ключ "CONSIDERATION_VERIFY_USER": true"""
		try:
			user_info_list = []

			for USER_ID, user_info in user_data.items():
				if "VERIFY_DATA" in user_info and user_info["VERIFY_DATA"]["CONSIDERATION_VERIFY_USER"]:
					"""Объявляем переменные для вывода их в сообщения о пользователе"""
					USER_LAST_NAME = user_info["USER_LAST_NAME"]
					USER_NAME = user_info["USER_NAME"]
					USER_LINK_PROFILE = user_info["VERIFY_DATA"]["LINK_PROFILE_USER"]

					"""Добавление информации о пользователе в список"""
					user_info_list.append(f" • {len(user_info_list) + 1}: <a href=\"{USER_NAME}\">{USER_LAST_NAME}</a> — <a href=\"{USER_LINK_PROFILE}\">Ссылка на Профиль</a> — <code>{USER_ID}</code>")

			if user_info_list:
				return "\n".join(user_info_list)
			else:
				return " • Нет пользователей на рассмотрении для верификации."
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def GETRSB(cls, rsb_data, obj, users_or_admin, types) -> Union[str, int, float, None]:
		"""Выводим информацию о кошельке из базы данных"""
		try:
			if not users_or_admin:
				"""Объявляем переменные для доступа к базе данных пользователей и получение информации"""
				USER_ID = ConfigBot.USERID(types)

				RSB_DATA_DB = load_rsb_data()
				check_user_data_db = check_user_data(USER_ID)
				"""Выводим информацию о NUMBER_WALLET_USER пользователя"""
				USER_NUMBER_WALLET = check_user_data_db.get("RSB_DATA", {}).get("NUMBER_WALLET_USER")

				if is_rsb_in_data(USER_NUMBER_WALLET, RSB_DATA_DB):
					check_rsb_data_db = check_rsb_data(USER_NUMBER_WALLET)

					if obj == "WALLET":
						return USER_NUMBER_WALLET
					
					elif obj in ("CURRENT_ETH", "CURRENT_USD", "CURRENT_RUB"):
						return check_rsb_data_db.get("CURRENT", {}).get(obj)
					
					elif obj in ("INTEREST_USER_ONE", "INTEREST_USER_TWO"):
						return check_rsb_data_db.get("INTEREST", {}).get(obj)
					
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
						return check_rsb_data_db.get(obj, None)
				
				return None
			
			elif users_or_admin:
				check_rsb_data_db = check_rsb_data(rsb_data)

				if obj in ("CURRENT_ETH", "CURRENT_USD", "CURRENT_RUB"):
					return check_rsb_data_db.get("CURRENT", {}).get(obj)
					
				elif obj in ("INTEREST_USER_ONE", "INTEREST_USER_TWO"):
					return check_rsb_data_db.get("INTEREST", {}).get(obj)

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
					return check_rsb_data_db.get(obj, None)

			return None
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

	@classmethod
	def GETNUMBERWALLETRSB(cls, rsb_data, user_id) -> int:
		"""Выводим ID кошельков из базы данных RSB"""
		try:
			number_wallet_info_list = []

			"""Проверяем зарегистрирован пользователь в базе админов"""
			ADMIN_DATA_DB = load_admin_data()

			if is_admin_in_data(user_id, ADMIN_DATA_DB):
				for wallet_number, rsb_info in rsb_data.items():
					"""Выводим краткую информацию о ID кошельков"""
					ETH = rsb_info["ETH"]

					"""Добавление ID кошельков в список"""
					number_wallet_info_list.append(f" • <code>{wallet_number}</code> ~ <b>{ETH} ETH</b>")

			if number_wallet_info_list:
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
		except Exception as e:
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
			"""Объявляем переменную с выводом информации о товаре из корзины"""
			check_market_data_db = check_market_data(market_data)

			if obj in ("URL_PHOTO", "URL_SITE", "NAME_MARKET", "MESSAGE"):
				return check_market_data_db.get(obj, None)
			else:
				return None
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

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
					logger.critical("⚠️ Отказ доступа к информации о товаре.")
				
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
		except Exception as e:
			logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

			return None

	@classmethod
	def GETARTICLEMARKET(cls, market_data, user_id) -> int:
		try:
			"""Объявляем переменную с выводом информации о администрации"""
			ADMIN_DATA_DB = load_admin_data()

			article_info_list = []

			if is_admin_in_data(user_id, ADMIN_DATA_DB):
				for article_number, market_info in market_data.items():
					"""Подготовка данных для сообщения"""
					name_market = market_info["NAME_MARKET"]
					site_market = market_info["URL_SITE"]

					"""Добавление информации о товаре в список"""
					article_info_list.append(f" • <code>{article_number}</code>: {name_market} — <a href ='{site_market}'>Ссылка на сайт</a>")
			
			if not is_admin_in_data(user_id, ADMIN_DATA_DB):
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
	def TRANSLATETOENGLISH(cls, text: str) -> Translator:
		"""Функция для перевода текста на английский язык с использованием внешнего сервиса"""
		try:
			translator = Translator()
			translation = translator.translate(text, dest='en')

			return translation.text
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