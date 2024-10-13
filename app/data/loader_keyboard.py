from misc.libraries import dataclass

from keyboards.users.ReplyKeyboard.ReplyKeyboard_all import (
	create_start_keyboard,
	create_menu_keyboard,
	create_world_menu_keyboard,
	create_update_keyboard,
	create_finish_update_keyboard,
	create_info_update_keyboard
)

from keyboards.users.InlineKeyboard.InlineKeyboard_all import (
	create_recovery_inlinekeyboard,
	skip_phase_nation_inlinekeyboard,
	create_profilemenu_inlinekeyboard,
	create_notify_inlinekeyboard,
	create_back_profile_inlinekeyboard,
	create_marketmenu_users_inlinekeyboard,
	create_back_market_users_inlinekeyboard,
	create_back_market_check_users_inlinekeyboard,
	create_sport_menu_inlinekeyboard,
	create_change_sport_inlinekeyboard,
	create_memory_diary_inlinekeyboard
)

from keyboards.admins.InlineKeyboard.InlineKeyboardAdmin_all import (
	create_debugmenu_inlinekeyboard,
	create_debugmenu_inlinekeyboard_next,
	create_debugmenu_inlinekeyboard_next_three,
	create_back_inlinekeyboard,
	create_back_verify_inlinekeyboard,
	create_menu_market_admin_inlinekeyboard,
	create_back_market_inlinekeyboard,
	create_back_debug_market_inlinekeyboard,
	create_menu_rsb_admin_inlinekeyboard,
	create_back_rsb_inlinekeyboard,
	create_menu_redit_rsb_admin_inlinekeyboard,
	create_back_redit_rsb_admin_inlinekeybard,
	create_menu_update_admin_inlinekeyboard,
	create_menu_edit_update_admin_inlinekeyboard,
	create_back_edit_update_inlinekeyboard,
	create_back_update_inlinekeyboard,
	create_menu_sport_admin_inlinekeyboard,
	create_back_sport_inlinekeyboard,
	create_menu_edit_sport_admin_inlinekeyboard,
	create_back_edit_sport_admin_inlinekeybard,
	create_menu_ration_admin_inlinekeyboard,
	create_back_ration_inlinekeyboard,
	create_menu_edit_ration_admin_inlinekeyboard,
	create_menu_edit_weekday_admin_inlinekeyboard
)

@dataclass
class LoaderReplyKeyboards:
	def __init__(
			self,
			message=None,
			keyboards_start=None,
			keyboards_menu=None,
			keyboards_world_menu=None,
			keyboards_update_bot=None,
			keyboards_finish_update=None,
			keyboards_info_update=None
		):
		
		"""Выводим клавиатуру для обработчика /start."""
		self.KEYBOARDS_START = keyboards_start or create_start_keyboard()
		"""Выводим клавиатуру для Главного Меню."""
		self.KEYBOARDS_MENU = keyboards_menu or create_menu_keyboard(message)
		"""Выводим клавиатуру для Мир Динары."""
		self.KEYBOARDS_WORLD_MENU = keyboards_world_menu or create_world_menu_keyboard(message)
		"""Выводим клавиатуру для обработчика /update."""
		self.KEYBOARDS_UPDATE_BOT = keyboards_update_bot or create_update_keyboard()
		"""Выводим клавиатуру для завершения обновления бота."""
		self.KEYBOARDS_FINISH_UPDATE = keyboards_finish_update or create_finish_update_keyboard()
		"""Выводим клавиатуру для информации об обновлениях бота."""
		self.KEYBOARDS_INFO_UPDATE = keyboards_info_update or create_info_update_keyboard()
		
@dataclass
class LoaderInlineKeyboards:
	def __init__(
			self,
			message=None,
			inline_keyboards_recovery=None,
			inline_keyboards_skip_phase_nation=None,
			inline_keyboards_profilemenu=None,
			inline_keyboards_notifymenu=None,
			inline_keyboards_back_profilemenu=None,
			inline_keyboards_marketmenu_users=None,
			inline_keyboards_back_market=None,
			inline_keyboards_back_market_check=None,
			inline_keyboards_menu_sport=None,
			inline_keyboards_shange_sport=None
		):
	
		self.INLINE_KEYBOARDS_RECOVERY = inline_keyboards_recovery or create_recovery_inlinekeyboard()

		self.INLINE_KEYBOARDS_SKIP_PHASE_NATION = inline_keyboards_skip_phase_nation or skip_phase_nation_inlinekeyboard()

		self.INLINE_KEYBOARDS_BACK_PROFILEMENU = inline_keyboards_back_profilemenu or create_back_profile_inlinekeyboard()
		self.INLINE_KEYBOARDS_PROFILEMENU = inline_keyboards_profilemenu or create_profilemenu_inlinekeyboard(message)
		self.INLINE_KEYBOARDS_NOTIFYMENU = inline_keyboards_notifymenu or create_notify_inlinekeyboard(message)
		self.INLINE_KEYBOARDS_CHANGESPORT = inline_keyboards_shange_sport or create_change_sport_inlinekeyboard(message)

		self.INLINE_KEYBOARDS_MARKETMENU_USERS = inline_keyboards_marketmenu_users or create_marketmenu_users_inlinekeyboard()

		self.INLINE_KEYBOARDS_BACK_MARKET = inline_keyboards_back_market or create_back_market_users_inlinekeyboard()

		self.INLINE_KEYBOARDS_BACK_MARKET_CHECK = inline_keyboards_back_market_check or create_back_market_check_users_inlinekeyboard()

		self.INLINE_KEYBOARDS_MENU_SPORT = inline_keyboards_menu_sport or create_sport_menu_inlinekeyboard()

@dataclass
class LoaderInlineKeyboardsMemoryDiary:
	def __init__(
			self,
			year = None,
			month = None,
			inline_keyboards_memory_days = None
		):

		self.INLINE_KEYBOARDS_MEMORY_DAYS = inline_keyboards_memory_days or create_memory_diary_inlinekeyboard(year, month)

@dataclass
class LoaderInlineKeyboardsAdmin:
	def __init__(
			self,
			inline_keyboards_debugmenu=None,
			inline_keyboards_debugmenu_two=None,
			inline_keyboards_debugmenu_three=None,
			inline_keyboards_back=None,
			inline_keyboards_back_verify=None,
			inline_keyboards_menumarket=None,
			inline_keyboards_back_market=None,
			inline_keyboards_back_market_debug_market=None,
			inline_keyboards_menursb=None,
			inline_keyboards_backrsb=None,
			inline_keyboards_reditmenu=None,
			inline_keyboards_back_redit_menu=None,
			inline_keyboards_updatemenu=None,
			inline_keyboards_back_update_menu=None,
			inline_keyboards_edit_menu_update=None,
			inline_keyboards_back_edit_update_menu=None,
			inline_keyboards_sport_menu=None,
			inline_keyboards_back_sport_menu=None,
			inline_keyboards_edit_menu_sport=None,
			inline_keyboards_back_edit_sport_menu=None,
			inline_keyboards_ration_menu=None,
			inline_keyboards_back_ration_menu=None,
			inline_keyboards_edit_menu_ration=None,
			inline_keyboards_edit_weekdays_menu_ration=None
		):
	
		"""Выводим inline клавиатуру для меню вкладки "Панель Управления" для администрации."""
		self.INLINE_KEYBOARDS_DEBUGMENU = inline_keyboards_debugmenu or create_debugmenu_inlinekeyboard()
		self.INLINE_KEYBOARDS_DEBUGMENU_TWO = inline_keyboards_debugmenu_two or create_debugmenu_inlinekeyboard_next()
		self.INLINE_KEYBOARDS_DEBUGMENU_THREE = inline_keyboards_debugmenu_three or create_debugmenu_inlinekeyboard_next_three()

		"""Выводим inline клавиатуру для кнопки назад."""
		self.INLINE_KEYBOARDS_BACK = inline_keyboards_back or create_back_inlinekeyboard()

		"""Выводим inline клавиатуру для кнопки назад в фазе верификации пользователя."""
		self.INLINE_KEYBOARDS_BACK_VERIFY = inline_keyboards_back_verify or create_back_verify_inlinekeyboard()

		"""Выводим inline клавиатуру для меню управления корзиной товаров."""
		self.INLINE_KEYBOARDS_MENUMARKET = inline_keyboards_menumarket or create_menu_market_admin_inlinekeyboard()

		"""Выводим inline клавиатуру для кнопки назад в фазе добавления товаров в корзину."""
		self.INLINE_KEYBOARDS_BACK_MARKET = inline_keyboards_back_market or create_back_market_inlinekeyboard()

		"""Выводим Inline клавиатуру для кнопки назад в фазе просмотра товаров в корзине."""
		self.INLINE_KEYBOARDS_BACK_DEBUG_MARKET = inline_keyboards_back_market_debug_market or create_back_debug_market_inlinekeyboard()

		"""Выводим Inline клавиатуру для меню управление RSB - Банком."""
		self.INLINE_KEYBOARDS_MENURSB = inline_keyboards_menursb or create_menu_rsb_admin_inlinekeyboard()

		"""Выводим Inline клавиатуру для кнопки назад в фазе добавление номера кошелька в RSB."""
		self.INLINE_KEYBOARDS_BACKRSB = inline_keyboards_backrsb or create_back_rsb_inlinekeyboard()

		"""Выводим Inline клавиатуру для меню в редактирование кошелька."""
		self.INLINE_KEYBOARDS_REDITMENU = inline_keyboards_reditmenu or create_menu_redit_rsb_admin_inlinekeyboard()
		self.INLINE_KEYBOARDS_BACK_REDIT_MENU = inline_keyboards_back_redit_menu or create_back_redit_rsb_admin_inlinekeybard()

		"""Выводим Inline клавиатуру для меню вкладки "Управления Обновлениями" для администрации."""
		self.INLINE_KEYBOARDS_UPDATEMENU = inline_keyboards_updatemenu or create_menu_update_admin_inlinekeyboard()
		self.INLINE_KEYBOARDS_BACK_UPDATE_MENU = inline_keyboards_back_update_menu or create_back_update_inlinekeyboard()
		self.INLINE_KEABOARDS_EDIT_MENU_UPDATE = inline_keyboards_edit_menu_update or create_menu_edit_update_admin_inlinekeyboard()
		self.INLINE_KEYBOARDS_BACK_EDIT_UPDATE_MENU = inline_keyboards_back_edit_update_menu or create_back_edit_update_inlinekeyboard()

		"""Выводим Inline клавиатуру для меню вкладки "Управлениями Кодексом Силы" для администрации."""
		self.INLINE_KEYBOARDS_SPORT_MENU = inline_keyboards_sport_menu or create_menu_sport_admin_inlinekeyboard()
		self.INLINE_KEYBOARDS_BACK_SPORT_MENU = inline_keyboards_back_sport_menu or create_back_sport_inlinekeyboard()
		self.INLINE_KEYBOARDS_EDIT_MENU_SPORT = inline_keyboards_edit_menu_sport or create_menu_edit_sport_admin_inlinekeyboard()
		self.INLINE_KEYBOARDS_BACK_EDIT_SPORT_MENU = inline_keyboards_back_edit_sport_menu or create_back_edit_sport_admin_inlinekeybard()

		"""Выводим Inline клавиатуру для меню вкладки "Управления Рационом" для администрации."""
		self.INLINE_KEYBOARDS_RATION_MENU = inline_keyboards_ration_menu or create_menu_ration_admin_inlinekeyboard()
		self.INLINE_KEYBOARDS_BACK_RATION_MENU = inline_keyboards_back_ration_menu or create_back_ration_inlinekeyboard()
		self.INLINE_KEYBOARDS_EDIT_RATION_MENU = inline_keyboards_edit_menu_ration or create_menu_edit_ration_admin_inlinekeyboard()
		self.INLINE_KEYBOARDS_EDIT_WEEKDAYS_RATION_MENU = inline_keyboards_edit_weekdays_menu_ration or create_menu_edit_weekday_admin_inlinekeyboard()

# @dataclass
# class LoaderInlineKeyboardsAdmin:
#     def __init__(self, inline_keyboards = None):
#         self.INLINE_KEYBOARDS = inline_keyboards or {
#             'DEBUGMENU': create_debugmenu_inlinekeyboard(),
#             'DEBUGMENU_TWO': create_debugmenu_inlinekeyboard_next(),
#             'DEBUGMENU_THREE': create_debugmenu_inlinekeyboard_next_three(),
#             'BACK': create_back_inlinekeyboard(),
#             'BACK_VERIFY': create_back_verify_inlinekeyboard(),
#             'MENUMARKET': create_menu_market_admin_inlinekeyboard(),
#             'BACK_MARKET': create_back_market_inlinekeyboard(),
#             'BACK_DEBUG_MARKET': create_back_debug_market_inlinekeyboard(),
#             'MENURSB': create_menu_rsb_admin_inlinekeyboard(),
#             'BACKRSB': create_back_rsb_inlinekeyboard(),
#             'REDITMENU': create_menu_redit_rsb_admin_inlinekeyboard(),
#             'BACK_REDIT_MENU': create_back_redit_rsb_admin_inlinekeybard(),
#             'UPDATEMENU': create_menu_update_admin_inlinekeyboard(),
#             'BACK_UPDATE_MENU': create_back_update_inlinekeyboard(),
#             'EDIT_MENU_UPDATE': create_menu_edit_update_admin_inlinekeyboard(),
#             'BACK_EDIT_UPDATE_MENU': create_back_edit_update_inlinekeyboard(),
#             'SPORT_MENU': create_menu_sport_admin_inlinekeyboard(),
#             'BACK_SPORT_MENU': create_back_sport_inlinekeyboard(),
#             'EDIT_MENU_SPORT': create_menu_edit_sport_admin_inlinekeyboard(),
#             'BACK_EDIT_SPORT_MENU': create_back_edit_sport_admin_inlinekeybard(),
#             'RATION_MENU': create_menu_ration_admin_inlinekeyboard()
#         }