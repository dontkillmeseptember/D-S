from misc.libraries import logging, os

"""Создаем обработчик для вывода loggers"""
def setup_logger(logger_name, log_file, level=logging.INFO):
	"""Создаем директорию, если она не существует"""
	log_directory = os.path.dirname(log_file)
	
	if not os.path.exists(log_directory):
		os.makedirs(log_directory)

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
	logger.addHandler(file_handler)
	logger.addHandler(console_handler)
	
	return logger

logger = setup_logger(__name__, "app/misc/logs/Logs.log")