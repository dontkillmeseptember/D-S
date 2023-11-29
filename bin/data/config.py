from misc.libraries import dataclass, os, load_dotenv, types, datetime, Translator, requests

from data.user_db import check_user_data

from keyboards.users.ReplyKeyboard.ReplyKeyboard_all import (
	create_start_keyboard,
	create_menu_keyboard
)

from keyboards.users.InlineKeyboard.InlineKeyboard_all import (
	create_recovery_inlinekeyboard
)

load_dotenv()

@dataclass
class ConfigBot:
	"""Вывод из env файла, версию бота"""
	VERSION: str = os.getenv("VERSION_BOT")
	"""Вывод из env файла, автора бота"""
	AUTHOR: str = os.getenv("AUTHOR_BOT")

	@classmethod
	def USERLASTNAME(cls, obj) -> bool:
		"""Вывод данных пользователя - Последние имя пользователя"""
		if isinstance(obj, types.Message):
			"""Возвращаем значение для types.Message"""
			return obj.from_user.first_name
		elif isinstance(obj, types.CallbackQuery):
			"""Возвращаем значение для types.CallbackQuery"""
			return obj.from_user.first_name
		else:
			raise ValueError("ERROR: 901, FILE: CONFIG, FUNC: USERLASTNAME")
	
	@classmethod
	def USERNAME(cls, obj) -> bool:
		"""Вывод данных пользователя - Ссылку на профиль пользователя"""
		if isinstance(obj, types.Message):
			"""Возвращаем значение для types.Message"""
			return obj.from_user.username if obj.from_user.username else None
		elif isinstance(obj, types.CallbackQuery):
			"""Возвращаем значение для types.CallbackQuery"""
			return obj.from_user.username if obj.from_user.username else None
		else:
			raise ValueError("ERROR: 901, FILE: CONFIG, FUNC: USERNAME")
	
	@classmethod
	def USERID(cls, obj) -> int:
		"""Выводим данных пользователя - USER_ID Пользователя"""
		if isinstance(obj, types.Message):
			"""Возвращаем значение для types.Message"""
			return obj.from_user.id
		elif isinstance(obj, types.CallbackQuery):
			"""Возвращаем значение для types.CallbackQuery"""
			return obj.from_user.id
		else:
			raise ValueError("ERROR: 901, FILE: CONFIG, FUNC: USERID")
	
	@classmethod
	def USERBOTID(cls, obj) -> int:
		"""Выводим данных пользователя - BOT_ID Пользователя"""
		if isinstance(obj, types.Message):
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(ConfigBot.USERID(obj))
			"""Выводим информацию о BOT_ID пользователя"""
			bot_id_user = check_user_data_db.get("BOT_ID")

			return bot_id_user
		if isinstance(obj, types.CallbackQuery):
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(ConfigBot.USERID(obj))
			"""Выводим информацию о BOT_ID пользователя"""
			bot_id_user = check_user_data_db.get("BOT_ID")

			return bot_id_user
		else:
			raise ValueError("ERROR: 901, FILE: CONFIG, FUNC: USERBOTID")
		
	@classmethod
	def USERNATION(cls, obj) -> str:
		"""Выводим данных пользователя - USER_NATION Пользователя"""
		if isinstance(obj, types.Message):
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(ConfigBot.USERID(obj))
			"""Выводим информацию о NATION_USER пользователя"""
			nation = check_user_data_db.get("NATION_USER")

			return nation
		if isinstance(obj, types.CallbackQuery):
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(ConfigBot.USERID(obj))
			"""Выводим информацию о NATION_USER пользователя"""
			nation = check_user_data_db.get("NATION_USER")

			return nation
		else:
			raise ValueError("ERROR: 901, FILE: CONFIG, FUNC: USERNATION")

	@classmethod
	def USERROLE(cls, obj) -> str:
		"""Выводим данных пользователя - USER_ROLE Пользователя"""
		if isinstance(obj, types.Message):
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(ConfigBot.USERID(obj))
			"""Выводим информацию о USER_ROLE пользователя"""
			smile = check_user_data_db.get("USER_ROLE")

			return smile
		if isinstance(obj, types.CallbackQuery):
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(ConfigBot.USERID(obj))
			"""Выводим информацию о USER_ROLE пользователя"""
			smile = check_user_data_db.get("USER_ROLE")

			return smile
		else:
			raise ValueError("ERROR: 901, FILE: CONFIG, FUNC: USERROLE")

	@classmethod
	def USERROLENAME(cls, obj) -> str:
		"""Выводим данных пользователя - NAME_USER_ROLE Пользователя"""
		if isinstance(obj, types.Message):
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(ConfigBot.USERID(obj))
			"""Выводим информацию о USER_ROLE пользователя"""
			role_name = check_user_data_db.get("NAME_USER_ROLE")

			return role_name
		if isinstance(obj, types.CallbackQuery):
			"""Получаем доступ к базе данных о пользователе"""
			check_user_data_db = check_user_data(ConfigBot.USERID(obj))
			"""Выводим информацию о USER_ROLE пользователя"""
			role_name = check_user_data_db.get("NAME_USER_ROLE")

			return role_name
		else:
			raise ValueError("ERROR: 901, FILE: CONFIG, FUNC: USERROLENAME")

	@classmethod
	def USERMESSAGE(cls, message) -> bool:
		"""Вводим сообщение пользователя для регистрации пароля и т.д."""
		return message.text

	@classmethod
	def GETCURRENTHOUR(cls) -> datetime:
		"""Переменные для вывода текущего времени пользователя"""
		date = datetime.datetime.now()
		current_hour = date.hour

		"""Выводим сообщение зависимости от времени суток, то есть если утро - Доброе утро, и т.д."""
		if 6 <= current_hour < 12:
			"""Выводим сообщение с добрым утром"""
			message_greeting = "Доброе утро"
			"""Возвращаем переменную с выводом сообщения"""
			return message_greeting
		elif 12 <= current_hour < 18:
			"""Выводим сообщение с добрый день"""
			message_greeting = "Добрый день"
			"""Возвращаем переменную с выводом сообщения"""
			return message_greeting
		elif 18 <= current_hour < 24:
			"""Выводим сообщение с добрый вечер"""
			message_greeting = "Добрый вечер"
			"""Возвращаем переменную с выводом сообщения"""
			return message_greeting
		else:
			"""Выводим сообщение с доброй ночи"""
			message_greeting = "Доброй ночи"
			"""Возвращаем переменную с выводом сообщения"""
			return message_greeting
	
	@classmethod
	def TRANSLATETOENGLISH(cls, text) -> Translator:
		"""Функция для перевода текста на английский язык с использованием внешнего сервиса"""
		try:
			"""Попытка выполнить перевод текста на английский язык"""
			translator = Translator()
			translation = translator.translate(text, dest='en')

			return translation.text
		except:
			print("ERROR: 404, FILE: LOADER, FUNC: TRANSLATE_TO_ENGLISH")

			return None
	
	@classmethod 
	def GETCOUNTRYINFO(cls, country_name) -> str:
		"""Функция ввода определение нации/страны"""
		try:
			"""Отправка запроса к внешнему API для получения информации о стране по её имени"""
			response = requests.get(f'https://restcountries.com/v2/name/{country_name}')
			"""Преобразование ответа в формат JSON"""
			data = response.json()

			"""Проверка успешности запроса (HTTP-код 200) и наличия данных"""
			if response.status_code == 200 and data:
				"""Возвращение информации о первой стране в списке (возможно, существует несколько стран с одинаковым именем)"""
				return data[0]
			else:
				"""В случае отсутствия данных или неудачного запроса, возврат значения None"""
				return None
		except:
			print("ERROR: 404, FILE: LOADER, FUNC: GET_COUNTRY_INFO")
		
			return None

@dataclass
class LoaderReplyKeyboards:
	def __init__(
			self,
			keyboards_start=None, 
			keyboards_menu=None
		):
		
		"""Выводим клавиатуру для обработчика /start"""
		self.KEYBOARDS_START = keyboards_start or create_start_keyboard()
		"""Выводим клавиатуру для главного меню"""
		self.KEYBOARDS_MENU = keyboards_menu or create_menu_keyboard()
		
@dataclass
class LoaderInlineKeyboards:
	def __init__(
			self,
			inline_keyboards_recovery=None
		):
	
		"""Выводим inline клавиатуру для восстановления пароля от учетной записи пользователя"""
		self.INLINE_KEYBOARDS_RECOVERY = inline_keyboards_recovery or create_recovery_inlinekeyboard()
