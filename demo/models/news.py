from sqlalchemy import select, insert, update, delete
from .. import db, routes
import datetime
import aiohttp
import os
import asyncpgsa


class News:

	@staticmethod
	async def get_all_news(request):
		async with request.app['db'].acquire() as conn:
			query = select([db.news])
			news = await conn.fetch(query)
		return news

	@staticmethod
	async def get_news_from_slug(request, slug):
		async with request.app['db'].acquire() as conn:
			query = select([db.news]).where(db.news.c.slug == slug)
			news = await conn.fetchrow(query)
		return news

	@staticmethod
	async def edit_news(request, data):
		async with request.app['db'].acquire() as conn:
			query = update(
					db.news).where(
					db.news.c.id == int(data['id'])).values({
					'title' 		: data['title'],
					'slug'			: data['slug'],
					'user_id'		: int(data['user']),
					'category_id' 	: int(data['category']),
					'text'			: data['text'],
					'text_min' 		: data['text_min'],
					'description' 	: data['description'],
					
				})
			await conn.execute(query)
		await News.save_pic(request)
		return data

	@staticmethod
	async def save_pic(request):
		data = await request.post()
		if data['jpg'] == b'':
			return aiohttp.web.HTTPFound('/admin/news')
		jpg = data['jpg']
		filename = jpg.filename
		jpg_file = data['jpg'].file
		filename_generate = await News.generate_filename(data, filename)
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
		await News.save_pic_db(request, filename_generate, data['id'])
		return

	@staticmethod
	async def save_pic_db(request, filename_generate, news_id):
		async with request.app['db'].acquire() as conn:
			query = select([db.news_image]).where(
				(db.news_image.c.news_id == int(news_id)) & (db.news_image.c.image == filename_generate))
			image = await conn.fetchrow(query)
			if image == None:
				query = db.news_image.insert({
					'news_id' : int(news_id),
					'image' : filename_generate
				})
				await conn.execute(query)
		return

	@staticmethod
	async def  generate_filename(data, filename):
	 	filename = data['slug'] + '_' + filename
	 	return "news_id_{0}/{1}".format(data['id'], filename)

	@staticmethod
	async def get_images(request, news_id):
		async with request.app['db'].acquire() as conn:
			query = select([db.news_image.c.image]).where(db.news_image.c.news_id == news_id)
			images = await conn.fetch(query)
		return images

	@staticmethod
	async def del_image(request, image):
		async with request.app['db'].acquire() as conn:
			query = db.news_image.delete().where(db.news_image.c.image == image)
			await conn.execute(query)
		path = await routes.path_save_pic(request)
		try:
			os.remove(path + '/' + image)
		except FileNotFoundError:
			pass

class ObjMixin():

	@classmethod
	async def create(cls, request, **kwargs):
		self = cls()
		if 'id' in kwargs:
			self.id = kwargs['id']
			self._dict_obj = await cls.get_from_id(self, request)
		elif 'slug' in kwargs:
			self.slug = kwargs['slug']
			self._dict_obj = await cls.get_from_slug(self, request)
		elif 'title' in kwargs:
			self.title = kwargs['title']
			self._dict_obj = await cls.get_from_title(self, request)
		else:
			raise AttributeError('нужен id или slug или title')
		if self._dict_obj is None:
			raise ValueError('не найдено')
		self.id = self._dict_obj['id']
		self.title = self._dict_obj['title']
		self.slug = self._dict_obj['slug']


		return self
	
	async def get_from_id(self, request):
		pass

	async def get_from_slug(self, request):
		pass

	async def get_from_title(self, request):
		pass

	def __str__(self):
		return f'объект {self.__class__} :{str(self._dict_obj)}'



class News_(ObjMixin):

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

	async def get_from_id(self, request):
		async with request.app['db'].acquire() as conn:
			query = select([db.news]).where(db.news.c.id == self.id)
			_dict_obj = await conn.fetchrow(query)
			return _dict_obj

	async def get_from_slug(self, request):
		async with request.app['db'].acquire() as conn:
			query = select([db.news]).where(db.news.c.slug == self.slug)
			_dict_obj = await conn.fetchrow(query)
			return _dict_obj

	async def get_from_title(self, request):
		async with request.app['db'].acquire() as conn:
			query = select([db.news]).where(db.news.c.title == self.title)
			_dict_obj = await conn.fetchrow(query)
			return _dict_obj

	@staticmethod
	async def get_all_news(request):
		async with request.app['db'].acquire() as conn:
			query = select([db.news])
			news = await conn.fetch(query)
		return news

	

# class Category:

# 	@staticmethod
# 	async def get_all_category(request):
# 		async with request.app['db'].acquire() as conn:
# 			query = select([db.category])
# 			category = await conn.fetch(query)
# 		return category


# 	@staticmethod
# 	async def category_dict_id_title(request):
# 		cat_id_title_dict = {}
# 		category = await Category.get_all_category(request)
# 		for cat in category:
# 			cat_id_title = {cat['id'] : cat['title']}
# 			cat_id_title_dict.update(cat_id_title)
# 		return cat_id_title_dict

class Category(ObjMixin):

	@classmethod
	async def create(cls, request, **kwargs):
		self = await super().create(request, **kwargs)
		return self

	async def get_from_id(self, request):
		async with request.app['db'].acquire() as conn:
			query = select([db.category]).where(db.category.c.id == self.id)
			_dict_obj = await conn.fetchrow(query)
			return _dict_obj

	async def get_from_slug(self, request):
		async with request.app['db'].acquire() as conn:
			query = select([db.category]).where(db.category.c.slug == self.slug)
			_dict_obj = await conn.fetchrow(query)
			return _dict_obj

	async def get_from_title(self, request):
		async with request.app['db'].acquire() as conn:
			query = select([db.category]).where(db.category.c.title == self.title)
			_dict_obj = await conn.fetchrow(query)
			return _dict_obj

	@classmethod
	async def get_all_category(cls, request):
		async with request.app['db'].acquire() as conn:
			query = select([db.category])
			category = await conn.fetch(query)
		return category


class NewsImage:

	@classmethod
	async def create(cls, request, **kwargs):
		self = cls()
		if 'id' in kwargs:
			self.id = kwargs['id']
			self._dict_obj = await self.get_from_id(request)
			if self._dict_obj is None:
				raise ValueError('не найдено')
			self.news_id = self._dict_obj['news_id']
			self.image = self._dict_obj['image']
		elif 'news_id' in kwargs:
			self.news_id = kwargs['news_id'] 
			self.images = await self.get_images(request)
		else:
			raise AttributeError('нужен id или news_id')
		
		return self

	async def get_from_id(self, request):
		async with request.app['db'].acquire() as conn:
			query = select([db.news_image]).where(db.news_image.c.id == self.id)
			_dict_obj = await conn.fetchrow(query)
			return _dict_obj

	async def get_images(self, request):
		async with request.app['db'].acquire() as conn:
			query = select([db.news_image]).where(db.news_image.c.news_id == self.news_id)
			images = await conn.fetch(query)
		return images

	def __str__(self):
		return f'объект {self.__class__} :{str(self._dict_obj)}'





# class Category_:

# 	@classmethod
# 	async def create(cls, request, **kwargs):
# 		self = Category_()
# 		# self.db = request.app['db']
		
# 		if 'id' in kwargs:
# 			self.id = kwargs['id']
# 			await cls.get_category_dict_from_id(self, request)
# 		elif 'slug' in kwargs:
# 			self.slug = kwargs['slug']
# 			await cls.get_category_dict_from_slug(self, request)
# 		elif 'title' in kwargs:
# 			self.title = kwargs['title']
# 			await cls.get_category_dict_from_title(self, request)
# 		else:
# 			raise AttributeError('нужен id или slug или title')
# 		if self.category_dict is None:
# 			raise ValueError('не найдено')
# 		self.id = self.category_dict['id']
# 		self.title = self.category_dict['title']
# 		self.slug = self.category_dict['slug']

# 		return self

# 	async def get_category_dict_from_id(self, request):
# 		async with request.app['db'].acquire() as conn:
# 			query = select([db.category]).where(db.category.c.id == self.id)
# 			self.category_dict = await conn.fetchrow(query)

# 	async def get_category_dict_from_slug(self, request):
# 		async with request.app['db'].acquire() as conn:
# 			query = select([db.category]).where(db.category.c.slug == self.slug)
# 			self.category_dict = await conn.fetchrow(query)

# 	async def get_category_dict_from_title(self, request):
# 		async with request.app['db'].acquire() as conn:
# 			query = select([db.category]).where(db.category.c.slug == self.title)
# 			self.category_dict = await conn.fetchrow(query)

# 	@classmethod
# 	async def get_all_category(cls, request):
# 		async with request.app['db'].acquire() as conn:
# 			query = select([db.category])
# 			category = await conn.fetch(query)
# 		return category

# 	def __str__(self):
# 		return f'объект Category_ :{str(self.category_dict)}'
			
		 
	

