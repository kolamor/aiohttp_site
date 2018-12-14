
from sqlalchemy import select, insert, update
import aiohttp
from aiohttp_jinja2 import template,  render_template
from aiohttp_session import get_session
from .. import db 



async def admin_privilege_valid(request):
	session = await get_session(request)

	async with request.app['db'].acquire() as conn:
		try:
			query = select([db.user_d]).where(db.user_d.c.login == session['user'])
			user = await conn.fetchrow(query)
		except KeyError:
			location = request.app.router['login'].url_for()
			raise aiohttp.web.HTTPFound(location=location)
			
	if user['admin_privilege'] == False:
		location = request.app.router['login'].url_for()
		raise aiohttp.web.HTTPFound(location=location)
	else:
		return user



async def edit_user_db(request, name):
	data = await request.post()
	data = dict(data)
	async with request.app['db'].acquire() as conn:
		query = select([db.user_d]).where(db.user_d.c.id == int(data['id']))
		user = await conn.fetchrow(query)
		try:
			val_admin_privilege = data.pop('admin_privilege')
			query = update(db.user_d).where(db.user_d.c.id == user['id']).values({
											'admin_privilege' : bool(val_admin_privilege)})
		except KeyError as e:
			query = update(db.user_d).where(db.user_d.c.id == user['id']).values({
											'admin_privilege' : False })
		await conn.execute(query)		

		if '' not in data.values():
			query = update(db.user_d).where(db.user_d.c.id == user['id']).values({
					'login'    : data['login'],
					'email'    : data['email'],
					'password' : data['password']})
			await conn.execute(query)
	return user['id']