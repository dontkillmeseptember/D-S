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
	asyncio
)

from misc.loggers import logger

from database.requests.user_db import check_user_data
from database.requests.market_db import check_market_data
from database.requests.admin_db import load_admin_data, is_admin_in_data
from database.requests.rsb_db import check_rsb_data, is_rsb_in_data, load_rsb_data

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
	def USERSTATUSVERIFY(cls, obj) -> str:
		try:
			"""Выводим данных пользователя - STATUS_VERIFY_USER Пользователя"""
			if isinstance(obj, (types.Message, types.CallbackQuery)):
				"""Получаем доступ к базе данных о пользователе"""
				USER_ID = ConfigBot.USERID(obj)
				check_user_data_db = check_user_data(USER_ID)
				"""Выводим информацию о STATUS_VERIFY_USER пользователя"""
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
	def GETCONSIDERATIONVERIFY(cls, user_data) -> str:
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
	def GETRSB(cls, rsb_data, obj, users_or_admin, types) -> str:
		"""Выводим информацию о кошельке из базы данных"""
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

@dataclass
class ConfigBotAsync:
	@classmethod
	async def UPDATEPROGRESS(cls, msg = None, update_stage = None, time_sleep = None, version = None, type = None) -> None:
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