import base64
import hashlib
from sqlalchemy import select, insert, update
from sqlalchemy.sql import text
# from sqlalchemy import and_, or_
import aiohttp
from aiohttp_jinja2 import template,  render_template
from .. import db 
import os
from ..models.user import User
from ..models.news import News, Category

from aiohttp_session import get_session, session_middleware, setup




@template('/admin/admin.html')
async def admin(request):

	session = await get_session(request)
	await admin_privilege_valid(request)
	context ={
			'session' : session,
			'request' : request,

	}
	return context


@template('/admin/users.html')
async def admin_users(request):
	await admin_privilege_valid(request)
	session = await get_session(request)
	async with request.app['db'].acquire() as conn:
		query = select([db.user_d.c.login, db.user_d.c.password, db.user_d.c.email,
						db.user_d.c.admin_privilege, db.user_d.c.id ] )
		users = await conn.fetch(query)
				
	context = {
				'users' : users,
				'request' : request,
				'session' : session,
		}
	return context


@template('/admin/edit_user.html')
async def edit_user(request):
	await admin_privilege_valid(request)
	name = request.match_info.get('name')
	async with request.app['db'].acquire() as conn:
		query = select([ db.user_d ] ).where(db.user_d.c.login == name)
		user = await conn.fetchrow(query)
		
		context = {'name' : name,
			'request' : request,
			'user' : user,
			
			'session' : request.session,
	 }
	return context

async def edit_user_post(request):
	name = request.match_info.get('name')
	user_id = await edit_user_db(request, name)

	async with request.app['db'].acquire() as conn:
		query = select([ db.user_d ] ).where(db.user_d.c.id == user_id)
		user = await conn.fetchrow(query)
		
	context = {
		'name' : user['login'],
		'session' : request.session,
		'user' : user,
		
		'request' : request, 
	}
	return render_template('/admin/edit_user.html', request, context)


@template('/admin/admin_news.html')
async def admin_news(request):
	
	news = await News.get_all_news(request)
	category = await Category.category_dict_id_title(request)
	user_dict = await User.get_user_from_id(news, request)

	context ={
			'news' : news,
			'session' : request.session,
			'user' : user_dict,
			'category' : category,
			'request' : request,
		}

	return context

@template('/admin/edit_news.html')
async def admin_edit_news(request):
	slug = request.match_info.get('slug')
	news = await News.get_news_from_slug(request, slug)
	context ={
			'news' : news,
			'session' : request.session,
			
			}
	return context

async def admin_edit_news_post(request):
	data = await request.post()
	
	q = await News.edit_news(request, data)
	news = await News.get_news_from_slug(request, data['slug'])
	context = {
		'session' : request.session,
		'news' : news,
	}
	return render_template('/admin/edit_news.html', request, context)











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