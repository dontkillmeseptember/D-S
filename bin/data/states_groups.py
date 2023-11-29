from misc.libraries import StatesGroup, State

"""Создаем StatesGroup для обработчика команды /start"""
class StartState(StatesGroup):
	"""Фаза для регистрации пользователя"""
	RegistrationUserState = State()
	"""Фаза для ввода нации/страны пользователя"""
	NationUserState = State()
	"""Фаза для восстановление пароля от учетной записи пользователя"""
	RecoveryPasswordState = State()