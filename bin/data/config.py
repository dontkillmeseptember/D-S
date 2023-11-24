from misc.libraries import dataclass, os, load_dotenv

from keyboards.users.keyboards_all import create_start_keyboard

load_dotenv()

@dataclass
class ConfigBot:
	"""Вывод из env файла, версию бота"""
	VERSION: str = os.getenv("VERSION_BOT")

@dataclass
class LoaderKeyboards:
    """Выводим клавиатуры для обработчика /start"""

    def __init__(self, keyboards_start=None):
        self.KEYBOARDS_START = keyboards_start or create_start_keyboard()