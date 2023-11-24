from misc.libraries import dataclass

from handlers.users.start_bot_func import start_command

@dataclass
class LoaderHandlers():
	"""Загружает команду /start"""
	START_HANDLER: start_command

"""Функция вывода bot"""
def Loader_Handlers() -> LoaderHandlers:
	try:
		loader_handlers_handlers = LoaderHandlers()

		return loader_handlers_handlers
	except:
		raise ValueError("ERROR")