from misc.libraries import dataclass

from keyboards.users.ReplyKeyboard.ReplyKeyboard_all import (
	create_start_keyboard,
	create_menu_keyboard,
	create_world_menu_keyboard,
	create_update_keyboard,
	create_finish_update_keyboard
)

from keyboards.users.InlineKeyboard.InlineKeyboard_all import (
	create_recovery_inlinekeyboard,
	create_profilemenu_inlinekeyboard,
	create_back_profile_inlinekeyboard,
	create_marketmenu_users_inlinekeyboard,
	create_back_market_users_inlinekeyboard,
	create_back_market_check_users_inlinekeyboard
)

from keyboards.admins.InlineKeyboard.InlineKeyboardAdmin_all import (
	create_debugmenu_inlinekeyboard,
	create_debugmenu_inlinekeyboard_next,
	create_back_inlinekeyboard,
	create_back_verify_inlinekeyboard,
	create_menu_market_admin_inlinekeyboard,
	create_back_market_inlinekeyboard,
	create_back_debug_market_inlinekeyboard,
	create_menu_rsb_admin_inlinekeyboard,
	create_back_rsb_inlinekeyboard,
	create_menu_redit_rsb_admin_inlinekeyboard,
	create_back_redit_rsb_admin_inlinekeybard
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
			keyboards_finish_update=None
		):
		
		"""Выводим клавиатуру для обработчика /start"""
		self.KEYBOARDS_START = keyboards_start or create_start_keyboard()
		"""Выводим клавиатуру для Главного Меню"""
		self.KEYBOARDS_MENU = keyboards_menu or create_menu_keyboard(message)
		"""Выводим клавиатуру для Мир Динары"""
		self.KEYBOARDS_WORLD_MENU = keyboards_world_menu or create_world_menu_keyboard(message)
		"""Выводим клавиатуру для обработчика /update"""
		self.KEYBOARDS_UPDATE_BOT = keyboards_update_bot or create_update_keyboard()
		"""Выводим клавиатуру для завершения обновления бота"""
		self.KEYBOARDS_FINISH_UPDATE = keyboards_finish_update or create_finish_update_keyboard()
		
@dataclass
class LoaderInlineKeyboards:
	def __init__(
			self,
			message=None,
			inline_keyboards_recovery=None,
			inline_keyboards_profilemenu=None,
			inline_keyboards_back_profilemenu=None,
			inline_keyboards_marketmenu_users=None,
			inline_keyboards_back_market=None,
			inline_keyboards_back_market_check=None
		):
	
		"""Выводим inline клавиатуру для восстановления пароля от учетной записи пользователя"""
		self.INLINE_KEYBOARDS_RECOVERY = inline_keyboards_recovery or create_recovery_inlinekeyboard()
		"""Выводим inline клавиатуру для меню вкладки "Ваш Профиль" для пользователей"""
		self.INLINE_KEYBOARDS_BACK_PROFILEMENU = inline_keyboards_back_profilemenu or create_back_profile_inlinekeyboard()
		self.INLINE_KEYBOARDS_PROFILEMENU = inline_keyboards_profilemenu or create_profilemenu_inlinekeyboard(message)
		"""Выводим inline клавиатуру для меню вкладки "Корзина Товаров" для пользователей"""
		self.INLINE_KEYBOARDS_MARKETMENU_USERS = inline_keyboards_marketmenu_users or create_marketmenu_users_inlinekeyboard()
		"""Выводим inline клавиатуру для кнопки назад в фазе во вкладке "Корзина Товаров" для пользователей"""
		self.INLINE_KEYBOARDS_BACK_MARKET = inline_keyboards_back_market or create_back_market_users_inlinekeyboard()
		"""Выводим inlone клавиатуру для кнопки отменить поиск товаров во вкладке "Корзина товаров" для пользователей"""
		self.INLINE_KEYBOARDS_BACK_MARKET_CHECK = inline_keyboards_back_market_check or create_back_market_check_users_inlinekeyboard()

@dataclass
class LoaderInlineKeyboardsAdmin:
	def __init__(
			self,
			inline_keyboards_debugmenu=None,
			inline_keyboards_debugmenu_two=None,
			inline_keyboards_back=None,
			inline_keyboards_back_verify=None,
			inline_keyboards_menumarket=None,
			inline_keyboards_back_market=None,
			inline_keyboards_back_market_debug_market=None,
			inline_keyboards_menursb=None,
			inline_keyboards_backrsb=None,
			inline_keyboards_reditmenu=None,
			inline_keyboards_back_redit_menu=None
		):
	
		"""Выводим inline клавиатуру для меню вкладки "Панель Управления" для администрации"""
		self.INLINE_KEYBOARDS_DEBUGMENU = inline_keyboards_debugmenu or create_debugmenu_inlinekeyboard()
		self.INLINE_KEYBOARDS_DEBUGMENU_TWO = inline_keyboards_debugmenu_two or create_debugmenu_inlinekeyboard_next()
		"""Выводим inline клавиатуру для кнопки назад"""
		self.INLINE_KEYBOARDS_BACK = inline_keyboards_back or create_back_inlinekeyboard()
		"""Выводим inline клавиатуру для кнопки назад в фазе верификации пользователя"""
		self.INLINE_KEYBOARDS_BACK_VERIFY = inline_keyboards_back_verify or create_back_verify_inlinekeyboard()
		"""Выводим inline клавиатуру для меню управления корзиной товаров"""
		self.INLINE_KEYBOARDS_MENUMARKET = inline_keyboards_menumarket or create_menu_market_admin_inlinekeyboard()
		"""Выводим inline клавиатуру для кнопки назад в фазе добавления товаров в корзину"""
		self.INLINE_KEYBOARDS_BACK_MARKET = inline_keyboards_back_market or create_back_market_inlinekeyboard()
		"""Выводим Inline клавиатуру для кнопки назад в фазе просмотра товаров в корзине"""
		self.INLINE_KEYBOARDS_BACK_DEBUG_MARKET = inline_keyboards_back_market_debug_market or create_back_debug_market_inlinekeyboard()
		"""Выводим Inline клавиатуру для меню управление RSB - Банком"""
		self.INLINE_KEYBOARDS_MENURSB = inline_keyboards_menursb or create_menu_rsb_admin_inlinekeyboard()
		"""Выводим Inline клавиатуру для кнопки назад в фазе добавление номера кошелька в RSB"""
		self.INLINE_KEYBOARDS_BACKRSB = inline_keyboards_backrsb or create_back_rsb_inlinekeyboard()
		"""Выводим Inline клавиатуру для меню в редактирование кошелька"""
		self.INLINE_KEYBOARDS_REDITMENU = inline_keyboards_reditmenu or create_menu_redit_rsb_admin_inlinekeyboard()
		self.INLINE_KEYBOARDS_BACK_REDIT_MENU = inline_keyboards_back_redit_menu or create_back_redit_rsb_admin_inlinekeybard()

