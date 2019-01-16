from sqlalchemy import select, insert, update, delete
from .. import db, routes
import datetime
import aiohttp
import os


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
		data = dict(data)
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
			w = await conn.execute(query)
		path = await routes.path_save_pic(request)
		try:
			os.remove(path + '/' + image)
		except FileNotFoundError:
			pass
		

	

class Category:

	@staticmethod
	async def get_all_category(request):
		async with request.app['db'].acquire() as conn:
			query = select([db.category])
			category = await conn.fetch(query)
		return category


	@staticmethod
	async def category_dict_id_title(request):
		cat_id_title_dict = {}
		category = await Category.get_all_category(request)
		for cat in category:
			cat_id_title = {cat['id'] : cat['title']}
			cat_id_title_dict.update(cat_id_title)
		return cat_id_title_dict
	

