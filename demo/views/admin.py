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
from ..models.news import News, Category, NewsImage

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
		users_data = await User.get_all(self.request, 'id', 'login')
		category_data = await Category.get_all(self.request, 'id', 'title')
		users = {}
		category ={}
		for user in users_data:
			users.update({user['id']: user['login']})
		for cat in category_data:
			category.update({cat['id']: cat['title']})		
		context = {
		'category': category,
		'user': users,
		'news': news,
		'request' : self.request,
		'session' : self.request.session,
		}
		return context


class AdminEditNews(aiohttp.web.View):

	@template('/admin/edit_news.html')
	async def get(self):
		
		slug = self.request.match_info.get('slug')
		news = await News.create(self.request, slug=slug)
		images = await NewsImage.create(self.request, news_id=news.id)
		print(images)

		context ={
				'news' : news,
				'session' : self.request.session,
				'images'  : images.images
				
				}
		return context

	async def post(self):
		data = await self.request.post()
		slug = self.request.match_info.get('slug')
		news = await News.create(self.request, slug=slug)
		images = await NewsImage.create(self.request, news_id=news.id)
		if 'image_del' in data:
			await images.delete(self.request, data['image_del'])
			location = self.request.path
			raise aiohttp.web.HTTPFound(location=location)

		news = await news.update(**data)
		await images.insert(self.request, data)
		context = {
			'session' : self.request.session,
			'news' : news,
			'images' : images.images
		}
		return render_template('/admin/edit_news.html', self.request, context)


	

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
	