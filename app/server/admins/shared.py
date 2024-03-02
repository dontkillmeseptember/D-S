from data.config import ConfigBot

from misc.libraries import AnyComponent, comps, GoToEvent
from misc.loggers import logger

"""Создаем главную страницу для админов."""
def main_page(*components: AnyComponent, title: str | None = None) -> list[AnyComponent]:
	try:
		return [
			comps.PageTitle(text = f"D & S Bot - {title}" if title else "D & S Bot"),
			comps.Navbar(
				title = f"🪷 D & S Bot • {ConfigBot().VERSION}",
				title_event = GoToEvent(url = "/"),
				start_links = [
					comps.Link(
						components = [comps.Text(text = "Список пользователей")],
						on_click = GoToEvent(url = "/users"),
						active = "startswith:/users",
					),
					comps.Link(
						components = [comps.Text(text = "Список администраторов")],
						on_click = GoToEvent(url = "/admins"),
						active = "startswith:/admins",
					),
					comps.Link(
						components = [comps.Text(text = "Список товаров в корзине")],
						on_click = GoToEvent(url = "/basket"),
						active = "startswith:/basket",
					),
					comps.Link(
						components = [comps.Text(text = "Список обновлений")],
						on_click = GoToEvent(url = "/update"),
						active = "startswith:/update",
					),
					comps.Link(
						components = [comps.Text(text = "Список кошельков")],
						on_click = GoToEvent(url = "/rsb"),
						active = "startswith:/rsb",
					),
				],
			),
			comps.Page(
				components = [
					*((comps.Heading(text= title),) if title else ()),
					*components
				]
			),
			comps.Footer(
				extra_text = "Ссылки на социальные сети.",
				links = [
					comps.Link(
						components = [comps.Text(text = "GitHub")], on_click = GoToEvent(url = "https://github.com/dontkillmeseptember/DSBot")
					)
				]
			)
		]
	except Exception as e:
		logger.error("⚠️ Произошла непредвиденная ошибка: %s", e)