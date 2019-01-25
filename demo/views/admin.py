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




class Admin(aiohttp.web.View):

	@template('/admin/admin.html')
	async def get(self):

		await admin_privilege_valid(self.request)
		context ={
				'session' : self.request.session,
				'request' : self.request,
		}
		return context


class AdminUsers(aiohttp.web.View):

	@template('/admin/users.html')
	async def get(self):
		await admin_privilege_valid(self.request)
		users = await User.get_all(self.request)
		context = {
					'users' : users,
					'request' : self.request,
					'session' : self.request.session,
			}
		return context


class AdminEditUsers(aiohttp.web.View):

	@template('/admin/edit_user.html')
	async def get(self):
		await admin_privilege_valid(self.request)
		name = self.request.match_info.get('name')
		user = await User.create(self.request, login=name )
		context = {'name' : name,
			'request' : self.request,
			'user'	: user,
			'session' : self.request.session,
		 }
		return context

	async def post(self):
		name = self.request.match_info.get('name')
		user = await User.create(self.request, login=name)
		data = await self.request.post()

		if 'delete' in data :
			await user.delete()
			location = self.request.app.router['admin_user'].url_for()
			raise aiohttp.web.HTTPFound(location=location)

		if 'admin_privilege' not in data:
			user = await user.update(**data, admin_privilege=False)
		user = await user.update(**data)
		context = {
			'name' : user.login,
			'session' : self.request.session,
			'user' : user,
			'request' : self.request, 
		}
		return render_template('/admin/edit_user.html', self.request, context)

class AdminNews(aiohttp.web.View):

	@template('/admin/admin_news.html')
	async def get(self):
		news = await News.get_all(self.request)
		user = await User.get_all(self.request, 'id', 'login')
		
		""""""
		category = await Category.get_all(self.request)

		
		context = {
		'category': category,
		'user': user,
		'news': news,
		'request' : self.request,
		'session' : self.request.session,
		}
		return context

@template('/admin/edit_news.html')
async def admin_edit_news(request):
	
	slug = request.match_info.get('slug')
	news = await News.get_news_from_slug(request, slug)
	images = await News.get_images(request, news['id'])
	
	context ={
			'news' : news,
			'session' : request.session,
			'images'  : images
			
			}
	return context

async def admin_edit_news_post(request):
	data = await request.post()
	if 'image_del' in data:
		await News.del_image(request, data['image_del'])
		slug = request.match_info.get('slug')
		location = request.path
		raise aiohttp.web.HTTPFound(location=location)
	
	await News.edit_news(request, data)
	news = await News.get_news_from_slug(request, data['slug'])
	images = await News.get_images(request, news['id'])
	
	context = {
		'session' : request.session,
		'news' : news,
		'images' : images
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



# async def edit_user_db(request, name):
# 	data = await request.post()
# 	data = dict(data)
# 	async with request.app['db'].acquire() as conn:
# 		query = select([db.user_d]).where(db.user_d.c.id == int(data['id']))
# 		user = await conn.fetchrow(query)
# 		try:
# 			val_admin_privilege = data.pop('admin_privilege')
# 			query = update(db.user_d).where(db.user_d.c.id == user['id']).values({
# 											'admin_privilege' : bool(val_admin_privilege)})
# 		except KeyError as e:
# 			query = update(db.user_d).where(db.user_d.c.id == user['id']).values({
# 											'admin_privilege' : False })
# 		await conn.execute(query)		

# 		if '' not in data.values():
# 			query = update(db.user_d).where(db.user_d.c.id == user['id']).values({
# 					'login'    : data['login'],
# 					'email'    : data['email'],
# 					'password' : data['password']})
# 			await conn.execute(query)
# 	return user['id']



class CreateNews(aiohttp.web.View):
	
	@template('/admin/create_news.html')
	async def get(self):

		session = await get_session(self)
		print('--', session)
		context = {
			'session' : session,
			'news'	: news,
		}
		return context
	