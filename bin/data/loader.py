from misc.libraries import dataclass, Bot, Dispatcher, MemoryStorage, os, load_dotenv

from data.user_db import create_user_file
from data.version_db import create_version_file

load_dotenv()

@dataclass
class LoaderBot:
	"""Переменные для загрузки бота"""
	BOT_TOKEN: str = os.getenv("API_TOKEN_BOT")
	PARSE: str = "HTML"
	WEP_PAGE: bool = True

	BOT = Bot(token=BOT_TOKEN, parse_mode=PARSE, disable_web_page_preview=WEP_PAGE)

@dataclass
class StorageBot:
	"""Переменная для хранения данных"""
	STORAGE = MemoryStorage()

@dataclass
class MyDispatcher:
	"""Переменная для запуска бота"""
	DP = Dispatcher(LoaderBot.BOT, storage=StorageBot.STORAGE)

@dataclass
class CreateJSON:
	"""Создание JSON файла для сохранение данных пользователей"""
	CREATE_USER: create_user_file("users_data.json")
	"""Создание JSON файла для сохранение версии бота"""
	CREATE_VERSION: create_version_file("version_data.json")

"""Функция создания файлов JSON"""
def Create_JSON_file() -> CreateJSON:
	try:
		Create_JSON = CreateJSON()

		return Create_JSON
	except:
		raise ValueError("VERSION_BOT не установлена в переменных окружения")

"""Функция вывода bot"""
def bot_class() -> LoaderBot:
	try:
		loader_bot_instance = LoaderBot().BOT

		return loader_bot_instance
	except:
		raise ValueError("API_TOKEN_BOT не установлена в переменных окружения")

"""Функция вывода dp"""
def dp_class() -> MyDispatcher:
	my_dispatcher = MyDispatcher().DP

	return my_dispatcher

bot = bot_class()
dp = dp_class()