from database.requests.user_db import create_user_file
from database.requests.version_db import create_version_file
from database.requests.admin_db import create_admin_file
from database.requests.market_db import create_market_file
from database.requests.rsb_db import create_rsb_file
from database.requests.info_update_db import create_update_file
from database.requests.sport_db import create_sport_file
from database.requests.ration_db import create_ration_file
from database.requests.memory_diary_db import Create_Memory_Diary_File

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
	"""Создание JSON файла для сохранение данных пользователей."""
	CREATE_USER = create_user_file("users_data.json")
	"""Создание JSON файла для сохранение версии бота"""
	CREATE_VERSION = create_version_file("version_data.json")
	"""Создание JSON файла для сохранения данных админов."""
	CREATE_ADMIN = create_admin_file("admins_data.json")
	"""Создание JSON файла для сохранения данных о товарах."""
	CREATE_MARKET = create_market_file("market_data.json")
	"""Создание JSON файла для сохранения данных о банке."""
	CREATE_RSB = create_rsb_file("rsb_data.json")
	"""Создание JSON файла для сохранения данных об обновлениях."""
	CREATE_UPDATE = create_update_file("update_data.json")
	"""Создание JSON Файла для сохранения данных о спорте."""
	CREATE_SPORT = create_sport_file("sport_data.json")
	"""Создание JSON Файла для сохранения данных об рационе."""
	CREATE_RATION = create_ration_file("ration_data.json")
	"""Создание JSON Файла для хранение данных об сообщениях в дневнике памяти."""
	CREATE_MEMORY_DIARY = Create_Memory_Diary_File("memory_diary_data.json")

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