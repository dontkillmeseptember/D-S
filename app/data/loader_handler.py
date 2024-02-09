from handlers.users.start_bot_func import start_command
from handlers.users.main_menu.user_profile.profile_func import profile_handler
from handlers.users.main_menu.main_menu_func import main_menu_handler
from handlers.users.main_menu.world_dinara.world_dinara_func import world_dinara_handler
from handlers.users.main_menu.world_dinara.market_func import market_handler

from handlers.admins.loggin_admin_func import loggin_admin_command
from handlers.admins.help_admin_func import help_admin_command
from handlers.admins.debug_admin_func import debug_admin_command

from misc.libraries import dataclass
from misc.loggers import logger

@dataclass
class LoaderHandlers():
	"""Загружает команду /start"""
	START_HANDLER: start_command
	"""Загружает обработчик для меню Профиля"""
	PROFILE_HANDLER: profile_handler
	"""Загружает обработчик для Главного Меню"""
	MAIN_MENU_HANDLER: main_menu_handler
	"""Загружает обработчик для меню Мир Динары"""
	WORLD_DINARA_HANDLER: world_dinara_handler
	"""Загружает обработчик для Корзины Товаров"""
	MARKET_HANDLER: market_handler

@dataclass
class LoaderAdminHandlers():
	"""Загружает команду !loggin_admin"""
	LOGGIN_ADMIN_HANDLER: loggin_admin_command
	"""Загружает команду !help"""
	HELP_ADMIN_HANDLER: help_admin_command
	"""Загружает команду !debug_admin"""
	DEBUG_ADMIN_HANDLER: debug_admin_command

def Loader_Handlers() -> LoaderHandlers:
	try:
		return LoaderHandlers()
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)

def Loader_Admin_Handlers() -> LoaderAdminHandlers:
	try:
		return LoaderAdminHandlers()
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)