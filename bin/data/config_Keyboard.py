from misc.libraries import dataclass

from data.user_db import check_user_data


@dataclass
class ConfigReplyKeyboard():
	"""Название кнопки для функций связанной с командой /start"""
	RUN_BOT: str = "🚀 Запустить Бот"

	"""Название кнопки для функций связанной с профилем"""
	PROFILE: str = "Ваш Профиль"

	"""@classmethod
	def PROFILE(cls, message) -> str:
		получаем айди пользователя
		user_id = message.from_user.id

		Получаем из базы данных информацию о пользователе
		check_user_data_db = check_user_data(user_id)

		Полуачем роль из базы данных о пользователе
		user_role = check_user_data_db.get("USER_PASSWORD")

		Создаем переменную с названием
		user_profile = f"{user_role} Ваш Профиль"

		return user_profile
	"""

@dataclass
class ConfigInlineKeyboard:
	"""Название кнопки для восстановления пароля от учетной записи пользователя"""
	RECOVERY_PASSWORD: str = "🔑 Восстановить Пароль"

@dataclass
class ConfigRoleUsers:
	"""Эмодзи для обычного пользователя"""
	USER_NAME: str = "Пользователь"
	USER: str = "💀"
	"""Эмодзи для администрации"""
	ADMIN_NAME: str = "Администрация"
	ADMIN: str = "🤵🏻"