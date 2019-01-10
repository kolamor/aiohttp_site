import asyncpgsa
from sqlalchemy import select, insert, update
from .. import db 

class User:

	@staticmethod
	async def get_user_from_id(news, request):
		user_dict = {}
		for new in news:
			user = await User.user_name(new['id'], request)
			user = {user['id'] : user['login']}
			user_dict.update(user)
		return user_dict	


	@staticmethod
	async def user_name(user_id, request):

		async with request.app['db'].acquire() as conn:
			query = select([db.user_d.c.login, db.user_d.c.id ]).where(db.user_d.c.id == user_id)
			user = await conn.fetchrow(query)
			
		return user