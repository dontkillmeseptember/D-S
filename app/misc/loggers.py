from misc.libraries import logging, os

def setup_logger(logger_name, log_file, level=logging.INFO):
	"""
	Функция для настройки логгера с указанным именем, файлом журнала и необязательным уровнем ведения журнала.
	Возвращает сконфигурированный логгер.
	"""

	"""Создаем каталог для журнала"""
	os.makedirs(os.path.dirname(log_file), exist_ok=True)

	"""Создаем логгер"""
	logger = logging.getLogger(logger_name)
	logger.setLevel(level)

	"""Создаем обработчик для вывода в файл"""
	file_handler = logging.FileHandler(log_file, encoding="utf-8")
	
	"""Создаем обработчик для вывода в терминал"""
	console_handler = logging.StreamHandler()

	"""Создаем форматтер"""
	formatter = logging.Formatter("%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]")
	
	"""Настраиваем обработчик"""
	file_handler.setFormatter(formatter)
	console_handler.setFormatter(formatter)
	
	"""Добавляем обработчик к логгеру"""
	for handler in [file_handler, console_handler]:
		handler.setFormatter(formatter)
		logger.addHandler(handler)
	
	return logger

logger = setup_logger(__name__, "app/misc/logs/Logs.log")