from misc.libraries import BaseModel

class User(BaseModel):
	"""Модель данных пользователя."""
	id: int
	bot_id: int
	name: str
	profile: str
	nation: str
	user_role: str
	password: str
	verify: str