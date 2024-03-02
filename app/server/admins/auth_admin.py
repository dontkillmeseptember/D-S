from misc.libraries import AnyComponent, components, GoToEvent, dataclass, Any, BaseModel, EmailStr, Field, SecretStr, FastAPI, FastUI, fastui_form, AuthEvent

from typing import Annotated, Literal, TypeAlias

from misc.loggers import logger

app = FastAPI()

@dataclass
class User:
	email: str | None
	password: dict[str, Any]

users = [
	User(email="admin", password="admin"),
]

"""Создаем вход для админов в отображение базы данных"""
def auth_login_admin() -> list[AnyComponent]:
	return [
		components.Heading(text = "Регистрация", level = 2),
		components.ModelForm(model = LoginForm, submit_url = "/api/login", display_mode = "page"),
		components.Footer(
			extra_text = "Ссылки на социальные сети.",
			links = [
				components.Link(
					components = [components.Text(text = "GitHub")], on_click = GoToEvent(url = "https://github.com/dontkillmeseptember/DSBot")
				)
			]
		)
	]

class LoginForm(BaseModel):
	email: EmailStr = Field(
		title = "Электронная почта", 
		description = "Введите электронную почту от вашей учетной записи.",
		json_schema_extra={'autocomplete': 'email'}
	)
	password: SecretStr = Field(
		title = "Пароль",
		description = "Введите пароль от вашей учетной записи.",
		json_schema_extra={'autocomplete': 'email'}
	)

@app.post('/login', response_model=FastUI, response_model_exclude_none=True)
async def login_form_post(form: Annotated[LoginForm, fastui_form(LoginForm)]) -> list[AnyComponent]:
	user = User(email=form.email, password="Admin")
	token = user.encode_token()
	return [components.FireEvent(event=AuthEvent(token=token, url='/auth/profile'))]

