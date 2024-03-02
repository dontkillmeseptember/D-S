from misc.libraries import StatesGroup, State

"""Создаем StatesGroup для обработчика команды /start"""
class StartState(StatesGroup):
	"""Фаза для регистрации пользователя"""
	RegistrationUserState = State()
	"""Фаза для ввода нации/страны пользователя"""
	NationUserState = State()
	"""Фаза для восстановление пароля от учетной записи пользователя"""
	RecoveryPasswordState = State()

"""Создаем StatesGroup для обработчика команды !loggin_admin"""
class LoggInAdminState(StatesGroup):
	"""Фаза для ввода пароля от учетной записи пользователя"""
	UserPasswordState = State()
	"""Фаза для ввода секретного пароля от входа в базу админов"""
	SecretPasswordState = State()

"""Создаем StatesGroup для обработчика вкладки "Ваш Профиль" для пользователей"""
class ProfileState(StatesGroup):
	"""Фаза для ввода индивидуального кода и ссылку на соц сеть."""
	SendCodeAndSocialState = State()
	"""Фаза для ввода пароля от учетной записи пользователя."""
	SendUserPasswordState = State()
	"""Фаза для ввода слово ПОДТВЕРЖДАЮ для удаления аккаунта пользователя."""
	SendApprovedState = State()
	"""Фаза для ввода номера кошелька для подключения к балансу ETH."""
	SendNumberWalletState = State()
	"""Фаза для обратного возвращения в профиль или продолжение вводить номер кошелька."""
	SendNumberWalletAndBackProfileState = State()
	
"""Создаем StatesGroup для обработчика команды !debug_admin"""
class DebugAdminState(StatesGroup):
	"""Фаза для ввода USER_ID от администрации для верификации пользователя."""
	VerifyUsersForAdminState = State()
	"""Фаза для ввода товара в корзину товаров от администрации."""
	AddMarketForAdminState = State()
	"""Фаза для ввода артикула товара, чтобы удалить его из корзины товаров."""
	DeleteMarketForAdminState = State()
	"""Фаза для ввода артикула товара, чтобы посмотреть товар из корзины."""
	CheckMarketForAdminState = State()
	"""Фаза для ввода и просмотра товара из корзины товаров."""
	ViewingMarketForAdminState = State()
	"""Фаза для ввода ID кошелька, чтобы добавить его в RSB."""
	AddRSBForAdminState = State()
	"""Фаза для ввода ID кошелька, чтобы удалить его из RSB."""
	DeleteRSBForAdminState = State()
	"""Фаза для ввода ID кошелька, чтобы начать его редактировать из RSB."""
	ReditRSBForAdminState = State()
	"""Фаза для ввода ETH, чтобы добавить его в нужный кошелек RSB."""
	AddEthReditRSBForAdminState = State()
	"""Фаза для ввода Общего Бюджета, чтобы добавить его в нужный кошелек RSB."""
	AddBudgetReditRSBForAdminState = State()
	"""Фаза для ввода Вкладка в Кошелек, чтобы добавить его в нужный кошелек RSB."""
	AddInterestRSBForAdminState = State()
	"""Фаза для ввода информации об обновлении бота."""
	AddUpdateForAdminState = State()
	"""Фаза для ввода ID обновления, чтобы удалить его из базы данных."""
	DeleteUpdateForAdminState = State()
	"""Фаза для ввода информации об управлении бота."""
	AddSportForAdminState = State()
	"""Фаза для ввода ID упражнения, чтобы удалить его из базы данных."""
	DeleteSportForAdminState = State()

"""Создаем StatesGroup для обработчика вкладки "Корзина Товаров" для пользователей"""
class MarketState(StatesGroup):
	"""Фаза для ввода артикула товара, чтобы посмотреть товар из корзины."""
	CheckMarketState = State()