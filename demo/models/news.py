from sqlalchemy import select, insert, update, delete, text
from .. import db, routes
import datetime
import aiohttp
import os
import asyncpgsa



class ObjMixin():
	''' Superclass'''
	@classmethod
	async def create(cls, request, **kwargs):
		self = cls()
		self._db = request.app['db']
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
		pass

	async def get_from_slug(self):
		pass

	async def get_from_title(self):
		pass

	async def get_all():
		pass

	def __str__(self):
		return f'объект {self.__class__} :{str(self._dict_obj)}'



class News(ObjMixin):

	@classmethod
	async def create(cls, request, **kwargs):
		self = await super().create(request, **kwargs)
		self.user_id 	 = self._dict_obj['user_id']
		self.category_id = self._dict_obj['category_id']
		self.text 		 = self._dict_obj['text']
		self.text_min 	 = self._dict_obj['text_min']
		self.date_created = self._dict_obj['date_created']
		self.date_change = self._dict_obj['date_change']
		self.description = self._dict_obj['description']
		self.likes 		 = self._dict_obj['likes']
		self.image 		 = self._dict_obj['image']
		self.moderation  = self._dict_obj['moderation']
		return self

	async def get_from_id(self):
		async with self._db.acquire() as conn:
			query = select([db.news]).where(db.news.c.id == self.id)
			_dict_obj = await conn.fetchrow(query)
			return _dict_obj

	async def get_from_slug(self):
		async with self._db.acquire() as conn:
			query = select([db.news]).where(db.news.c.slug == self.slug)
			_dict_obj = await conn.fetchrow(query)
			return _dict_obj

	async def get_from_title(self):
		async with self._db.acquire() as conn:
			query = select([db.news]).where(db.news.c.title == self.title)
			_dict_obj = await conn.fetchrow(query)
			return _dict_obj

	async def update(self, **kwargs):
		'''  '''
		self.slug 		= kwargs['slug'] 		if 'slug' in kwargs else 		self.slug
		self.title 		= kwargs['title'] 		if 'title' in kwargs else 		self.title
		self.user_id 	= kwargs['user_id'] 	if 'user_id' in kwargs else 	self.user_id
		self.category_id = kwargs['category_id'] if 'category_id' in kwargs else self.category_id
		self.text 		= kwargs['text'] 		if 'text' in kwargs else 		self.text
		self.description = kwargs['description'] if 'description' in kwargs else self.description
		self.text_min 	= kwargs['text_min'] 	if 'text_min' in kwargs else 	self.text_min 
		self.likes 		= kwargs['likes'] 		if 'likes' in kwargs else 		self.likes 
		self.image 		= kwargs['image'] 		if 'image' in kwargs else 		self.image
		self.moderation = kwargs['moderation'] 	if 'moderation' in kwargs else self.moderation

		async with self._db.acquire() as conn:
			query = update(
					db.news).where(
					db.news.c.id == int(self.id)).values({
					'title' 		: self.title,
					'slug'			: self.slug ,
					'user_id'		: int(self.user_id),
					'category_id' 	: int(self.category_id),
					'text'			: self.text ,
					'text_min' 		: self.text_min,
					'description' 	: self.description,
					'likes' 		: int(self.likes) ,
					'image'			: self.image,
					'moderation'	: bool(self.moderation),	
					})
			await conn.execute(query)
		return self

	async def insert(self, **kwargs):
		self.title = kwargs['title']
		self.slug = kwargs['slug']
		self.user_id = kwargs['user_id']
		self.category_id = kwargs['category_id']
		self.text = kwargs['text']
		self.text_min = kwargs['text_min']
		self.description = kwargs['description']
		self.moderation = kwargs['moderation'] if 'moderation' in kwargs['moderation'] else False
		self.image = kwargs['image'] if 'image' in kwargs['image'] else None
		async with self._db.acquire() as conn:
			query = db.news.insert({
						'title' 		: self.title,
						'slug'			: self.slug ,
						'user_id'		: int(self.user_id),
						'category_id' 	: int(self.category_id),
						'text'			: self.text ,
						'text_min' 		: self.text_min,
						'description' 	: self.description,
						'likes' 		: int(self.likes) ,
						'image'			: self.image,
						'moderation'	: bool(self.moderation),
					})
			await conn.execute(query)
		return self

	async def delete(self):
		async with self._db.acquire() as conn:
			query = db.news.delete().where(
	        	db.news.c.id == self.id)
			await conn.execute(query)

	@classmethod
	async def get_all(cls, request):
		async with request.app['db'].acquire() as conn:
			query = select([db.news])
			news = await conn.fetch(query)
		return news


class Category(ObjMixin):

	@classmethod
	async def create(cls, request, **kwargs):
		self = await super().create(request, **kwargs)
		return self

	async def get_from_id(self):
		async with self._db.acquire() as conn:
			query = select([db.category]).where(db.category.c.id == self.id)
			_dict_obj = await conn.fetchrow(query)
			return _dict_obj

	async def get_from_slug(self):
		async with self._db.acquire() as conn:
			query = select([db.category]).where(db.category.c.slug == self.slug)
			_dict_obj = await conn.fetchrow(query)
			return _dict_obj

	
	async def get_from_title(self):
		async with self._db.acquire() as conn:
			query = select([db.category]).where(db.category.c.title == self.title)
			_dict_obj = await conn.fetchrow(query)
			return _dict_obj

	async def update(self, **kwargs):
		self.slug = kwargs['slug'] if 'slug' in kwargs else self.slug
		self.title = kwargs['title'] if 'title' in kwargs else self.title
		async with self._db.acquire() as conn:
			query = update(db.category).where(
					db.category.c.id == int(self.id)).values({
					'title'	: self.title,
					'slug'	: self.slug 
					})
			await conn.execute(query)
		return self

	async def insert(self, title, slug):
		self.title = title
		self.slug = slug
		async with self._db.acquire() as conn:
			query = db.category.insert({
				'title'    : self.title,
				'slug'    : self.slug,
				})
			await conn.execute(query)
		return self

	async def delete(self):
		async with self._db.acquire() as conn:
			query = db.category.delete().where(
	        	db.category.c.id == self.id)
			await conn.execute(query)
				

	@classmethod
	async def get_all(cls, request, *fields):

		async with request.app['db'].acquire() as conn:
			if len(fields) == 1:
				query = text(f"Select {fields[0]} from category;")
			elif len(fields) == 2:
				query = text(f"Select {fields[0]} , {fields[1]} from category;")
			elif len(fields) == 3:
				query = text(f"Select {fields[0]} , {fields[1]}, {fields[2]} from category;")
			else:
				query = select([db.category] )
			users = await conn.fetch(query)
		return users


class NewsImage:

	@classmethod
	async def create(cls, request, **kwargs):
		self = cls()
		self._db = request.app['db']
		if 'id' in kwargs:
			self.id = kwargs['id']
			self._dict_obj = await self.get_from_id(self)
			if self._dict_obj is None:
				raise ValueError('не найдено')
			self.news_id = self._dict_obj['news_id']
			self.image = self._dict_obj['image']
		elif 'news_id' in kwargs:
			self.news_id = kwargs['news_id'] 
			self.images = await self.get_images()
		else:
			raise AttributeError('нужен id или news_id')
		
		return self

	async def get_from_id(self):
		async with self._db.acquire() as conn:
			query = select([db.news_image]).where(db.news_image.c.id == self.id)
			_dict_obj = await conn.fetchrow(query)
			return _dict_obj

	async def get_images(self):
		async with self._db.acquire() as conn:
			query = select([db.news_image]).where(db.news_image.c.news_id == self.news_id)
			images = await conn.fetch(query)
		return images

	
	async def insert(self, request, data):
		# data = await self.request.post()
		if data['jpg'] == b'':
			return
		jpg = data['jpg']
		filename = jpg.filename
		jpg_file = data['jpg'].file
		filename_generate = await self.generate_filename(data, filename)
		path = await routes.path_save_pic(request)
		path_jpg = os.path.join(path, filename_generate)
		try:
			with open(path_jpg, 'wb') as f:
				f.write(jpg_file.read())
		except FileNotFoundError:
			path_news = filename_generate.split('/')
			path_news = os.path.join(path, path_news[0])
			os.makedirs(path_news)
			with open(path_jpg, 'wb') as f:
				f.write(jpg_file.read())
		await self.save_pic_db(filename_generate)
		self.images = await self.get_images()
		return self


	async def save_pic_db(self, filename_generate):
		async with self._db.acquire() as conn:
			query = select([db.news_image]).where(
				(db.news_image.c.news_id == int(self.news_id)) & (db.news_image.c.image == filename_generate))
			image = await conn.fetchrow(query)
			if image == None:
				query = db.news_image.insert({
					'news_id' : int(self.news_id),
					'image' : filename_generate
				})
				await conn.execute(query)
		return

	
	
	async def delete(self, request, image):
		async with self._db.acquire() as conn:
			query = db.news_image.delete().where(db.news_image.c.image == image)
			await conn.execute(query)
		path = await routes.path_save_pic(request)
		try:
			os.remove(path + '/' + image)
		except FileNotFoundError:
			pass

	@staticmethod
	async def  generate_filename(data, filename):
	 	filename = data['slug'] + '_' + filename
	 	return "news_id_{0}/{1}".format(data['id'], filename)


	def __str__(self):
		return f'объект {self.__class__} :{str(self.images)}'






