from data.user_db import create_user_file
from data.version_db import create_version_file
from data.admin_db import create_admin_file
from data.market_db import create_market_file
from data.rsb_db import create_rsb_file

from misc.libraries import dataclass, Bot, Dispatcher, MemoryStorage, os, load_dotenv
from misc.loggers import logger

load_dotenv()

@dataclass
class LoaderBot:
	"""Объявляем переменные для загрузки важных элементов бота"""
	BOT_TOKEN: str = os.getenv("API_TOKEN_BOT")
	PARSE: str = "HTML"
	WEP_PAGE: bool = True

	BOT = Bot(token = BOT_TOKEN,
		   	  parse_mode = PARSE,
			  disable_web_page_preview = WEP_PAGE)

@dataclass
class StorageBot:
	"""Объявляем переменную для хранения данных"""
	STORAGE = MemoryStorage()

@dataclass
class MyDispatcher:
	"""Объявляем переменную для создания бота в диспетчере"""
	DP = Dispatcher(LoaderBot.BOT, storage=StorageBot.STORAGE)

@dataclass
class CreateJSON:
	"""Создание JSON файла для сохранение данных пользователей"""
	CREATE_USER: create_user_file("users_data.json")
	"""Создание JSON файла для сохранение версии бота"""
	CREATE_VERSION: create_version_file("version_data.json")
	"""Создание JSON файла для сохранения данных админов"""
	CREATE_ADMIN: create_admin_file("admins_data.json")
	"""Создание JSON файла для сохранения данных о товарах"""
	CREATE_MARKET: create_market_file("market_data.json")
	"""Создание JSON файла для сохранения данных о банке"""
	CREATE_RSB: create_rsb_file("rsb_data.json")

"""Функция создания файлов JSON"""
def Create_JSON_file() -> CreateJSON:
	try:
		return CreateJSON()
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

"""Функция вывода bot"""
def bot_class() -> LoaderBot:
	try:
		return LoaderBot().BOT
	except AttributeError:
		logger.critical("⚠️ API_TOKEN_BOT не объявлена в переменном окружение")

"""Функция вывода dp"""
def dp_class() -> MyDispatcher:
	return MyDispatcher().DP

bot = bot_class()
dp = dp_class()