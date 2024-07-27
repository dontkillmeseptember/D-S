from data.loader import dp, bot
from data.config import ConfigBot
from data.config_Keyboard import ConfigInlineKeyboard
from data.loader_keyboard import LoaderInlineKeyboardsAdmin
from data.states_groups import DebugAdminState

from database.requests.user_db import load_user_data, is_user_in_data, save_user_data
from database.requests.admin_db import load_admin_data, is_admin_in_data
from database.requests.ration_db import load_ration_data, is_ration_in_data, save_ration_data

from misc.libraries import types, FSMContext
from misc.loggers import logger

"""Создаем обработчик для управления Рационом."""
@dp.callback_query_handler(lambda callback_data: callback_data.data == "RATION")
async def ration_admin_handler(callback_query: types.CallbackQuery, state: FSMContext) -> str:
	"""Объявляем переменные для вывода информации о пользователе и администрации."""
	ADMIN_DATA_DB = load_admin_data()
	USER_DATA_DB = load_user_data()

	try:
		"""Объявляем переменную с выводом информации о пользователе: USER_ID."""
		USER_ID = ConfigBot.USERID(callback_query)

		if is_user_in_data(USER_ID, USER_DATA_DB):
			if is_admin_in_data(USER_ID, ADMIN_DATA_DB):
				"""Объявляем переменную с выводом клавиатуры для меню управления рационом."""
				menu_ration_admin_inline_keyboard = LoaderInlineKeyboardsAdmin().INLINE_KEYBOARDS_RATION_MENU

				INFO_MENU_RATION_ADMIN_MESSAGE = f"💬 Добро пожаловать в <b>«{ConfigInlineKeyboard().RATION[2:-2]}»</b>.\n\n" \
												 f"Здесь вы можете легко управлять рационом, добавлять его и удалять.\n\n" \
												 f" • <b>{ConfigInlineKeyboard().ADD_RATION[2:]}:</b> Используйте эту кнопку для добавление <b>нового</b> рациона.\n\n" \
												 f" • <b>{ConfigInlineKeyboard().DELETE_RATION[:-2]}:</b> При необходимости вы можете <b>удалить</b> выбранный рацион из базы данных.\n\n" \
												 f" • <b>{ConfigInlineKeyboard().EDIT_RATION[2:-2]}:</b> Нажмите эту кнопку, чтобы <b>редактировать</b> рацион, которые в данный момент находятся в базе данных.\n\n" \
												 f"Управляйте с легкостью. Ваш комфорт - наша главная задача!"
				
				await bot.edit_message_text(INFO_MENU_RATION_ADMIN_MESSAGE,
											callback_query.from_user.id, 
											callback_query.message.message_id,
											reply_markup = menu_ration_admin_inline_keyboard)
			else:
				logger.error("⚠️ Произошла непредвиденная ошибка с проверкой, существует пользователь в базе данных администрации: %s", is_admin_in_data(USER_ID, ADMIN_DATA_DB))
		else:
			logger.error("⚠️ Произошла непредвиденная ошибка с проверкой на регистрацию пользователя: %s", is_user_in_data(USER_ID, USER_DATA_DB))
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)