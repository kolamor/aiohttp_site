
from sqlalchemy import select, insert, update, delete, text
from .. import db, routes
import datetime
import aiohttp
import os
import asyncpgsa
from ..models.Base.BaseABC import ObjModel





class Xbox360(ObjModel):
	"""game_xbox360 = Table(
	'game_xbox360', meta,
	Column('id', Integer, primary_key=True),
	Column('title', VARCHAR, nullable=True),
	Column('slug', VARCHAR, nullable=True, unique=True),
	Column('description', Text),
	Column('image', Text),
	Column('rating', Integer),
	Column('screenshot', Text),
	Column('platform_id', Integer, ForeignKey('platform.id')),
	Column('torr_link', VARCHAR(255)),
	Column('active', BOOLEAN, default=True)
	"""
	db_table = db.game_xbox360

	@classmethod
	async def create(cls, database, **kwargs):
		self = await super().create(database, **kwargs)
		self.description = self._dict_obj['description']
		self.image 		 = self._dict_obj['image']
		self.rating		 = self._dict_obj['rating']
		self.screenshot = self._dict_obj['screenshot']
		self.platform_id = self._dict_obj['platform_id']
		self.torr_link = self._dict_obj['torr_link']
		self.active  = self._dict_obj['active']
		return self


	async def update(self, **kwargs):
		'''  '''
		self.slug 		= kwargs['slug'] 		if 'slug' in kwargs else 		self.slug
		self.title 		= kwargs['title'] 		if 'title' in kwargs else 		self.title
		self.description = kwargs['description'] if 'description' in kwargs else self.description
		self.image 		= kwargs['image'] 		if 'image' in kwargs else 		self.image
		self.rating		 = kwargs['rating'] 	if 'rating' in kwargs 	else	self.rating
		self.screenshot	= kwargs['screenshot'] if 'screenshot' in kwargs else	self.screenshot
		self.platform_id = kwargs['platform_id'] if 'platform_id' in kwargs else self.platform_id
		self.torr_link	= kwargs['torr_link'] 	if 'slug' in kwargs else 		self.torr_link
		self.active		= kwargs['active'] 		if 'active' in kwargs else 		self.active

		async with self._db.acquire() as conn:
			query = update(
					self.db_table).where(
					self.db_table.c.id == int(self.id)).values({
					'title' 		: self.title,
					'slug'			: self.slug ,
					'description' 	: self.description,
					'image'			: self.image,
					'screenshot'	: self.screenshot,
					'platform_id'	: int(self.platform_id),
					'torr_link'		: self.torr_link,
					'rating' 		: int(self.rating) ,
					'active'		: bool(self.active),
					})
			await conn.execute(query)
		return self

	@classmethod
	async def insert(cls, database, **kwargs):
		self = cls()
		self._db = database
		self.title = kwargs['title']
		self.slug = kwargs['slug']
		self.description = kwargs['description']
		self.image = kwargs['image'] if 'image' in kwargs else None
		self.screenshot = kwargs['screenshot']
		self.platform_id = kwargs['platform_id']
		self.torr_link = kwargs['torr_link']
		self.rating = kwargs['rating'] if 'rating' in kwargs else None
		self.active = kwargs['active'] if 'active' in kwargs else True
		async with self._db.acquire() as conn:
			query = cls.db_table.insert({
						'title' 		: self.title,
						'slug'			: self.slug ,
						'description' 	: self.description,
						'image'			: self.image,
						'screenshot'	: self.screenshot ,
						'platform_id'	: int(self.platform_id),
						'torr_link' 	: self.torr_link,
						'rating' 		: int(self.rating),
						'active'		: bool(self.active),
					})
			await conn.execute(query)
		self = await cls.create(database, slug = self.slug)
		return self

	async def delete(self):
		async with self._db.acquire() as conn:
			query = self.db_table.delete().where(
	        	self.db_table.c.id == self.id)
			await conn.execute(query)


