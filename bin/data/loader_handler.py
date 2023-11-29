from misc.libraries import dataclass

from handlers.users.start_bot_func import start_command
from handlers.users.main_menu.profile_func import profile_handler

@dataclass
class LoaderHandlers():
	"""Загружает команду /start"""
	START_HANDLER: start_command
	"""Загружает обработчик для меню профиля"""
	PROFILE_HANDLER: profile_handler

"""Функция вывода bot"""
def Loader_Handlers() -> LoaderHandlers:
	try:
		loader_handlers_handlers = LoaderHandlers()

		return loader_handlers_handlers
	except:
		raise ValueError("ERROR: 404, FILE: LOADER_HANDLER, FUNC: LOADER_HANDLERS")