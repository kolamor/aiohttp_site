import base64
# import hashlib
from sqlalchemy import select, insert, update
from sqlalchemy.sql import text
# from sqlalchemy import and_, or_
import aiohttp
from aiohttp_jinja2 import template,  render_template
from .. import db 
import os
from aiohttp_session import get_session, session_middleware, setup
from cryptography.fernet import Fernet

from ..models.user import User


class Login(aiohttp.web.View):
   

	@template('/auth/login.html')
	async def get ( self):
		session = await get_session(self.request)
		secret_key = self.request.app['config'].get('secret_key')
		secret_key1 = base64.urlsafe_b64decode(self.request.app['config'].get('secret_key'))
		
		return {'session' : session,
					'secret_key' : secret_key1,
					'request' : self.request,
					}

	async def post(self):
		data = await self.request.post()
		
		# password = hashlib.sha256(data['password'].encode('utf8')).hexdigest()
		# cipher = Fernet(request.app['config'].get('secret_key'))
		# password = cipher.encript(data['password'])
		try:
			user = await User.create(self.request, login = data['username'])
		except ValueError:
			location = self.request.app.router['login'].url_for()
			return aiohttp.web.HTTPFound(location=location)
		if user.password == data['password']:
			session = await get_session(self.request)
			session['user'] = user.login
			location = self.request.app.router['login'].url_for()
			return aiohttp.web.HTTPFound(location=location)
		else:
			
			location = self.request.app.router['login'].url_for()
			return aiohttp.web.HTTPFound(location=location)


@template('/auth/signup.html')
async def signup(request):
	session = await get_session(request)
	return {'session' : session }

async def signup_post(request):
	data = await request.post()
	if data['password'] != data['password_control']:
		location = request.app.router['signup'].url_for()
		context = {"valid" : "not valid"} 
		return render_template('signup.html', request, context)

	# key = (request.app['config'].get('secret_key').encode('utf8'))
	# cipher = Fernet(key)
	# password = cipher.encrypt(bytes(data['password'].encode('utf8')))
	
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
			await conn.execute(query)
			session = await get_session(request)
			session['user'] = data['username']
			location = request.app.router['login'].url_for()
			return aiohttp.web.HTTPFound(location=location)

		if data['username'] in result['login']:
			context = {"valid" : "Есть такой пользователь"}
		elif data['email'] in result['email']:
			context = {"valid" : "Есть такой email"}
		return render_template('signup.html', request, context)



@template('/auth/logout.html')
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
	session = await get_session(request)
	del session['user']
	location = request.app.router['login'].url_for()
	return aiohttp.web.HTTPFound(location=location)