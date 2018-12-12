import base64
from sqlalchemy import select, insert
from sqlalchemy.sql import text
# from sqlalchemy import and_, or_
import aiohttp
from aiohttp_jinja2 import template,  render_template
from .. import db 
import os

from aiohttp_session import get_session, session_middleware, setup
from ..models.admin import admin_privilege_valid


@template('index.html')
async def index(request):
	site_name = request.app['config'].get('site_name')
	return { 'site_name': site_name }


async def post(request):
	async with request.app['db'].acquire() as conn:
		query = select([db.post.c.id, db.post.c.title, db.post.c.body ])
		result = await conn.fetch(query)

	async with request.app['db'].acquire() as conn:	
		query = select([db.user_d.c.login, db.user_d.c.admin_privilege ])
		result1 = await conn.fetch(query)
	return aiohttp.web.Response(body=str(result+result1))



@template('login.html')
async def login ( request):
	session = await get_session(request)
	
	secret_key = request.app['config'].get('secret_key')
	secret_key1 = base64.urlsafe_b64decode(request.app['config'].get('secret_key'))
	request = request
	return {'session' : session,
				'secret_key' : secret_key1,
				'request' : request,
				}

async def login_post(request):
	data = await request.post()
	print('4',data)
	user = data['username']
	password = data['password']
	async with request.app['db'].acquire() as conn:
		# query = text("SELECT * FROM user_d WHERE login = '{}';".format(user))
		query = select([db.user_d]).where(db.user_d.c.login == user)
		product = await conn.fetchrow(query)
		try:
			user_data = dict(product)
		except TypeError:
			user_data = {}
	
	if user == user_data.get('login') and password == user_data.get('password'):
		session = await get_session(request)
		session['user'] = user_data.get('login')
		location = request.app.router['login'].url_for()
		return aiohttp.web.HTTPFound(location=location)
	else:
		print('none')
		location = request.app.router['login'].url_for()
		return aiohttp.web.HTTPFound(location=location)

@template('signup.html')
async def signup(request):
	session = await get_session(request)
	return {'session' : session }

async def signup_post(request):
	data = await request.post()
	if data['password'] != data['password_control']:
		location = request.app.router['signup'].url_for()
		context = {"valid" : "not valid"} 
		return render_template('signup.html', request, context)
	async with request.app['db'].acquire() as conn:
		try:
			query = select([db.user_d]).\
				where ((db.user_d.c.login == data['username'])
					| (db.user_d.c.email == data['email'] ))	
		except:
			pass
		result = await conn.fetchrow(query)
		if result is None:
			query = db.user_d.insert({
				'login'    : data['username'],
				'email'    : data['email'],
				'password' : data['password']
				})
			
			result1 = await conn.execute(query)
			session = await get_session(request)
			session['user'] = data['username']
			location = request.app.router['login'].url_for()
			return aiohttp.web.HTTPFound(location=location)

		if data['username'] in result['login']:
			context = {"valid" : "Есть такой пользователь"}
		elif data['email'] in result['email']:
			context = {"valid" : "Есть такой email"}
		return render_template('signup.html', request, context)



@template('logout.html')
async def logout(request):
	session = await get_session(request)
	if  'user' not in session:
		location = request.app.router['login'].url_for()
		return aiohttp.web.HTTPFound(location=location)
	return {'session' : session,
			'request' : request,
			}


async def logout_post(request):
	data = await request.post()
	print(data)
	session = await get_session(request)
	del session['user']
	location = request.app.router['login'].url_for()
	return aiohttp.web.HTTPFound(location=location)


@template('admin.html')
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
	print (dir(request))
	name = request.match_info.get('name')
	async with request.app['db'].acquire() as conn:
		query = select([ db.user_d ] ).where(db.user_d.c.login == name)
		print('--', query)
		user = await conn.fetchrow(query)
	return {'name' : name,
			'request' : request,
			'user' : user,
			'session' : request.session,
	 }



		
	


		