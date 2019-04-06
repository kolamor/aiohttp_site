
from sqlalchemy import select, insert, update, delete, text
from .. import db, routes
import datetime
import aiohttp
import os
import asyncpgsa
from ..models.Base.BaseABC import ObjModel




class Platform(ObjModel):
	""" platform = Table(
	'platform', meta,
	Column('id', Integer, primary_key=True),
	Column('title', VARCHAR, nullable=True),
	Column('slug', VARCHAR, nullable=True, unique=True),
	Column('description', Text),
	Column('image', Text)
	)
	"""
	db_table = db.platform

	@classmethod
	async def create(cls, database, **kwargs):
		self = await super().create(database, **kwargs)
		self.description = self._dict_obj['description']
		self.image 		 = self._dict_obj['image']
		return self


	async def update(self, **kwargs):
		'''  '''
		self.slug 		= kwargs['slug'] 		if 'slug' in kwargs else 		self.slug
		self.title 		= kwargs['title'] 		if 'title' in kwargs else 		self.title
		self.description = kwargs['description'] if 'description' in kwargs else self.description
		self.image 		= kwargs['image'] 		if 'image' in kwargs else 		self.image

		async with self._db.acquire() as conn:
			query = update(
					self.db_table).where(
					self.db_table.c.id == int(self.id)).values({
					'title' 		: self.title,
					'slug'			: self.slug ,
					'description' 	: self.description,
					'image'			: self.image,
					})
			await conn.execute(query)
		return self

	@classmethod
	async def insert(cls, database, **kwargs):
		self = cls()
		self._db = database
		self.title = kwargs['title']
		self.slug = kwargs['slug']
		self.description = kwargs['description'] if 'description' in kwargs else None
		self.image = kwargs['image'] if 'image' in kwargs else None
		async with self._db.acquire() as conn:
			query = self.db_table.insert({
						'title' 		: self.title,
						'slug'			: self.slug ,
						'description' 	: self.description,
						'image'			: self.image,
					})
			await conn.execute(query)
		self = await cls.create(database, slug = self.slug)
		return self

	async def delete(self):
		async with self._db.acquire() as conn:
			query = self.db_table.delete().where(
	        	self.db_table.c.id == self.id)
			await conn.execute(query)

