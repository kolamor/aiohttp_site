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
	async def get(self):
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


class Signup(aiohttp.web.View):

	@template('/auth/signup.html')
	async def get(self):
		context = {'request' : self.request}
		return  context

	async def post(self):
		data = await self.request.post()
		if data['password'] != data['password_control']:
			location = request.app.router['signup'].url_for()
			context = {"valid" : "not valid"} 
			return render_template('/auth/signup.html', request, context)

		# key = (request.app['config'].get('secret_key').encode('utf8'))
		# cipher = Fernet(key)
		# password = cipher.encrypt(bytes(data['password'].encode('utf8')))
		try:
			user = await User.create(self.request, login=data['username'])
		except ValueError:
			user = None
		try:
			email = await User.create(self.request, email=data['email'])
		except ValueError:
			email = None
		if user is not None:
			context = {"valid" : "Есть такой пользователь"}
		elif email is not None:
			context = {"valid" : "Есть такой email"}
		elif user is None and email is None:
			user = await User.insert(self.request, **data, login=data['username'])
			self.request.session['user'] = data['username']
			context ={'valid' : 'Успешно'}
		con = {'request' : self.request}
		context.update(con)
		return render_template('/auth/signup.html', self.request, context)



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