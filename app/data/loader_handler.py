from handlers.users.start_bot_func import start_command
from handlers.users.main_menu.main_menu_func import main_menu_handler
from handlers.users.main_menu.battlepass.run_battlepass_func import battlepass_handler
from handlers.users.main_menu.update.update_func import update_command
from handlers.users.main_menu.update.info_update_func import info_update_handler, update_tabs_handler
from handlers.users.main_menu.world_dinara.world_dinara_func import world_dinara_handler
from handlers.users.main_menu.world_dinara.market_func import market_handler
from handlers.users.main_menu.world_dinara.sport_func import sport_handler

from handlers.users.main_menu.user_profile.profile_func import profile_handler
from handlers.users.main_menu.user_profile.profile_sport_func import change_sport_users_handler
from handlers.users.main_menu.user_profile.profile_notify_func import notify_user_handler
from handlers.users.main_menu.user_profile.profile_rsb_func import rsb_bank_user_handler
from handlers.users.main_menu.user_profile.profile_delete_func import delete_account_handler
from handlers.users.main_menu.user_profile.profile_verify_func import verify_handler

from handlers.admins.loggin_admin_func import loggin_admin_command
from handlers.admins.help_admin_func import help_admin_command

from handlers.admins.debugmenu.debug_menu_func import debug_admin_command
from handlers.admins.debugmenu.debug_menu_sport import sport_admin_handler
from handlers.admins.debugmenu.debug_menu_update import update_admin_handler
from handlers.admins.debugmenu.debug_menu_RSB import rsb_admin_handler
from handlers.admins.debugmenu.debug_menu_market import market_admin_handler
from handlers.admins.debugmenu.debug_menu_verify_users import add_verify_handler
from handlers.admins.debugmenu.debug_menu_ration import ration_admin_handler

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

@dataclass
class LoaderDebugMenuHandlers():
	"""Загружает обработчик для меню debug."""
	DEBUG_MENU_HANDLER: debug_admin_command
	"""Загружает обработчик для меню Кодекса Силы."""
	DEBUG_MENU_SPORT_HANDLER: sport_admin_handler
	"""Загружает обработчик для меню Обновлений."""
	DEBUG_MENU_UPDATE_HANDLER: update_admin_handler
	"""Загружает обработчик для меню RSB."""
	DEBUG_MENU_RSB_HANDLER: rsb_admin_handler
	"""Загружает обработчик для меню Маркета."""
	DEBUG_MENU_MARKET_HANDLER: market_admin_handler
	"""Загружает обработчик для меню Верификации."""
	DEBUG_MENU_VERIFY_HANDLER: add_verify_handler
	"""Загружает обработчик для меню Рациона."""
	DEBUG_MENU_RATION_HANDLER: ration_admin_handler

@dataclass
class LoaderProfileFunctionsHandlers():
	"""Загружает обработчик для функции изменения упражнения."""
	PROFILE_SPORT_FUNCTIONS_HANDLER: change_sport_users_handler
	"""Загружает обработчик для функции управления уведомлениями."""
	PROFILE_NOTIFY_FUNCTIONS_HANDLER: notify_user_handler
	"""Загружает обработчик для функции просмотра RSB."""
	PROFILE_RSB_FUNCTIONS_HANDLER: rsb_bank_user_handler
	"""Загружает обработчик для функции удаления аккаунта."""
	PROFILE_DELETE_ACCOUNT_HANDLER: delete_account_handler
	"""Загружает обработчик для функции верификации."""
	PROFILE_VERIFY_USERS_HANDLER: verify_handler

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

def Loader_DebugMenu_Handlers() -> LoaderDebugMenuHandlers:
	"""
	Создает и возвращает объект LoaderDebugMenuHandlers или регистрирует ошибку, если возникает исключение.
	"""
	try:
		return LoaderDebugMenuHandlers()
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)