import asyncpgsa
from sqlalchemy import select, insert, update, text
from .. import db 

class User:

	@classmethod
	async def create(cls, request, **kwargs):
		self = cls()
		self._db = request.app['db']
		if 'id' in kwargs:
			self.id = kwargs['id']
			self._dict_obj = await self.get_from_id()
		elif 'login' in kwargs:
			self.login = kwargs['login']
			self._dict_obj = await self.get_from_login()
		elif 'email' in kwargs:
			self.email =kwargs['email']
			self._dict_obj = await self.get_from_email()
		else:
			raise AttributeError('нужен id или login или email')
		if self._dict_obj is None:
			raise ValueError('не найдено')
		self.id = self._dict_obj['id']
		self.login = self._dict_obj['login']
		self.email = self._dict_obj['email']
		self.password = self._dict_obj['password']
		self.admin_privilege = self._dict_obj['admin_privilege']

		return self

	async def get_from_id(self):
		async with self._db.acquire() as conn:
			query = select([db.user_d]).where(db.user_d.c.id == self.id)
			_dict_obj = await conn.fetchrow(query)
		return _dict_obj
			

	async def get_from_login(self):
		async with self._db.acquire() as conn:
			query = select([db.user_d]).where(db.user_d.c.login == self.login)
			_dict_obj = await conn.fetchrow(query)
		return _dict_obj

	async def get_from_email(self):
		async with self._db.acquire() as conn:
			query = select([db.user_d]).where(db.user_d.c.email == self.email)
			_dict_obj = await conn.fetchrow(query)
		return _dict_obj

	async def update(self, **kwargs):
		self.login = kwargs['login'] if 'login' in kwargs else self.login
		self.email = kwargs['email'] if 'email' in kwargs else self.email
		self.password = kwargs['password'] if 'password' in kwargs else self.password
		self.admin_privilege = kwargs['admin_privilege'] if 'admin_privilege' in kwargs else self.admin_privilege
		async with self._db.acquire() as conn:
			query = update(db.user_d).where(
					db.user_d.c.id == int(self.id)).values({
				'login'    : self.login,
				'email'    : self.email,
				'password'	: self.password,
				'admin_privilege' : bool(self.admin_privilege),
				})
			await conn.execute(query)
		return self

	
	@classmethod
	async def insert(cls, request, **kwargs):
		self = cls()
		self._db = request.app['db']
		self.login = kwargs['login']
		self.email = kwargs['email']
		self.password = kwargs['password']
		self.admin_privilege = kwargs['admin_privilege'] if 'admin_privilege' in kwargs else False
		async with self._db.acquire() as conn:
			query = db.user_d.insert({
				'login'    : self.login,
				'email'    : self.email,
				'password'	: self.password,
				'admin_privilege' : self.admin_privilege,
				})
			await conn.execute(query)
		return self

	async def delete(self):
		async with self._db.acquire() as conn:
			query = db.user_d.delete().where(
	        	db.user_d.c.id == self.id)
			await conn.execute(query)

	@classmethod
	async def get_all(cls, request, *fields):

		async with request.app['db'].acquire() as conn:
			if len(fields) == 1:
				query = text(f"Select {fields[0]} from user_d;")
			elif len(fields) == 2:
				query = text(f"Select {fields[0]} , {fields[1]} from user_d;")
			elif len(fields) == 3:
				query = text(f"Select {fields[0]} , {fields[1]}, {fields[2]} from user_d;")
			else:
				query = select([db.user_d] )
			users = await conn.fetch(query)
		return users
		

	def __str__(self):
		return f'объект {self.__class__} :{str(self._dict_obj)}'


