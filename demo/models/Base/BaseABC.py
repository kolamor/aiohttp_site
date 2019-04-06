from sqlalchemy import select, insert, update, delete, text



class ObjModel():
	''' Base class for model'''

	db_table = None # name table - db.name

	@classmethod
	async def create(cls, database, **kwargs):
		self = cls()
		self._db = database
		if 'id' in kwargs:
			self.id = kwargs['id']
			self._dict_obj = await cls.get_from_id(self)
		elif 'slug' in kwargs:
			self.slug = kwargs['slug']
			self._dict_obj = await cls.get_from_slug(self)
		elif 'title' in kwargs:
			self.title = kwargs['title']
			self._dict_obj = await cls.get_from_title(self)
		else:
			raise AttributeError('нужен id или slug или title')
		if self._dict_obj is None:
			raise ValueError('не найдено')
		self.id = self._dict_obj['id']
		self.title = self._dict_obj['title']
		self.slug = self._dict_obj['slug']
		return self

	async def get_from_id(self):
		async with self._db.acquire() as conn:
			query = select([self.db_table]).where(self.db_table.c.id == self.id)
			_dict_obj = await conn.fetchrow(query)
			return _dict_obj

	async def get_from_slug(self):
		async with self._db.acquire() as conn:
			query = select([self.db_table]).where(self.db_table.c.slug == self.slug)
			_dict_obj = await conn.fetchrow(query)
			return _dict_obj

	async def get_from_title(self):
		async with self._db.acquire() as conn:
			query = select([self.db_table]).where(self.db_table.c.title == self.title)
			_dict_obj = await conn.fetchrow(query)
			return _dict_obj

	@classmethod
	async def get_all(cls, database):
		async with database.acquire() as conn:
			query = select([cls.db_table])
			data = await conn.fetch(query)
		return data

	async def delete(self):
		async with self._db.acquire() as conn:
			query = self.db_table.delete().where(
			self.db_table.c.id == self.id)
			await conn.execute(query)

	def __str__(self):
		return f'объект {self.__class__} :{str(self._dict_obj)}'