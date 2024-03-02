from server.admins.shared import main_page

from database.requests.user_db import load_user_data

from data.config import ConfigBot
from data.configBaseModel import User

from misc.libraries import (
	FastAPI,
	Thread,
	uvicorn,
	FastUI,
	AnyComponent,
	HTMLResponse,
	prebuilt_html,
	comps,
	DisplayLookup,
	HTTPException,
	GoToEvent,
	BackEvent
)

app = FastAPI()

@app.get("/api/", response_model = FastUI, response_model_exclude_none = True)
def api_root() -> list[AnyComponent]:
	markdown = """
	Привет админ!
	"""

	return main_page(comps.Markdown(text = markdown))

@app.get("/api/users", response_model = FastUI, response_model_exclude_none = True)
def users_table() -> list[AnyComponent]:
	"""Вывод таблицы пользователей"."""
	return main_page(
		comps.Table(
			data = ConfigBot.LOADERUSERS(),
			data_model = User,
			columns = [
				DisplayLookup(field='id', title='USER_ID'),
				DisplayLookup(field='bot_id', title='BOT_ID'),
				DisplayLookup(field='name', title='Имя пользователей', on_click=GoToEvent(url='/user/{id}')),
				DisplayLookup(field='profile', title='Ссылка на профиль'),
				DisplayLookup(field='password', title='Пароль пользователя'),
				DisplayLookup(field='verify', title='Статус верификации'),
			]
		),
		comps.Button(text = "Удалить пользователя", on_click = GoToEvent(url = "/user/add")),
	)

@app.get("/api/user/{user_id}", response_model = FastUI, response_model_exclude_none = True)
def user_info(user_id: int) -> list[AnyComponent]:
	"""Вывод информации о пользователе."""
	try:
		user = next(u for u in ConfigBot.LOADERUSERS() if u.id == user_id)
	except StopIteration:
		raise HTTPException(status_code = 404, detail = "User not found")
	
	return main_page(
		comps.Page(
			components = [
				comps.Link(
					components = [
						comps.Text(text = "Назад")
					],

					on_click = BackEvent()
				),
				comps.Details(data = user)
			]
		)
	)

@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
	return HTMLResponse(prebuilt_html(title = "D & S Bot"))

@app.get('/{path:path}', status_code = 404)
async def api_404():
	return {'message': 'Not Found'}

def run():
	uvicorn.run(app, port = 8000, host = "127.0.0.1")

def keep_alive():
	t = Thread(target = run)
	t.start()