from handlers.users.start_bot_func import start_command
from handlers.users.main_menu.user_profile.profile_func import profile_handler
from handlers.users.main_menu.main_menu_func import main_menu_handler
from handlers.users.main_menu.battlepass.run_battlepass_func import battlepass_handler
from handlers.users.main_menu.update.update_func import update_command
from handlers.users.main_menu.update.info_update_func import info_update_handler, update_tabs_handler
from handlers.users.main_menu.world_dinara.world_dinara_func import world_dinara_handler
from handlers.users.main_menu.world_dinara.market_func import market_handler
from handlers.users.main_menu.world_dinara.sport_func import sport_handler

from handlers.admins.loggin_admin_func import loggin_admin_command
from handlers.admins.help_admin_func import help_admin_command
from handlers.admins.debug_admin_func import debug_admin_command

from database.requests.info_update_db import load_update_data

from data.loader import dp

from misc.libraries import dataclass
from misc.loggers import logger

@dataclass
class LoaderHandlers():
	"""Загружает команду /start."""
	START_HANDLER: start_command
	"""Загружает обработчик для меню Профиля."""
	PROFILE_HANDLER: profile_handler
	"""Загружает обработчик для Главного Меню."""
	MAIN_MENU_HANDLER: main_menu_handler
	"""Загружает обработчик для меню Мир Динары."""
	WORLD_DINARA_HANDLER: world_dinara_handler
	"""Загружает обработчик для Корзины Товаров."""
	MARKET_HANDLER: market_handler
	"""Загружает обработчик для информации об обновление."""
	INFO_UPDATE_HANDLER: info_update_handler
	"""Загружает обработчик для обновления."""
	UPDATE_HANDLER: update_command
	"""Загружает обработчик для battlepass."""
	BATTLEPASS_HANDLER: battlepass_handler
	"""Загружает обработчик для Кодекса Силы."""
	SPORT_HANDLER: sport_handler

@dataclass
class LoaderAdminHandlers():
	"""Загружает команду !loggin_admin."""
	LOGGIN_ADMIN_HANDLER: loggin_admin_command
	"""Загружает команду !help."""
	HELP_ADMIN_HANDLER: help_admin_command
	"""Загружает команду !debug_admin."""
	DEBUG_ADMIN_HANDLER: debug_admin_command

async def Loader_Register_Handlers() -> LoaderHandlers:
	"""
	Регистрирует обработчики для загрузки данных и возвращает зарегистрированные обработчики.
	"""
	try:
		"""Объявляем переменную с выводом информации об обновлениях."""
		UPDATE_DATA_DB = load_update_data()

		DPS = [dp.register_message_handler(update_tabs_handler, lambda message, text = f"{UPDATE_DATA_ID['EMODJI_UPDATE']} • {UPDATE_DATA_ID['NAME_UPDATE']}": message.text == text) for ID_UPDATE, UPDATE_DATA_ID in UPDATE_DATA_DB.items() if ID_UPDATE is not None]

		return DPS
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

def Loader_Handlers() -> LoaderHandlers:
	try:
		return LoaderHandlers()
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

def Loader_Admin_Handlers() -> LoaderAdminHandlers:
	"""
	Создает и возвращает объект LoaderAdminHandlers или регистрирует ошибку, если возникает исключение.
	"""
	try:
		return LoaderAdminHandlers()
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)