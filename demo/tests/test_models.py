import unittest
import asyncio
import asyncpgsa
from ..models.platform import Platform



db_url = 'postgresql://kola:test@localhost:5432/demo'


class TModel():

	def setUp(self):
		self.loop = asyncio.new_event_loop()
		asyncio.set_event_loop(None)
		async def func():
			self._db = await asyncpgsa.create_pool(dsn=db_url)
		self.loop.run_until_complete(func())

	def tearDown(self):
		async def func():
			await self._db.close()
		self.loop.run_until_complete(func())

		self.loop.close()

class TestModelPlatform_Insert(TModel, unittest.TestCase):



	def tearDown(self):
		async def func():
			async with self._db.acquire() as conn:
				query = "delete from platform where (slug = 'test1');"
				await conn.execute(query)
			await self._db.close()
		self.loop.run_until_complete(func())

		self.loop.close()

	def test_insert(self):
		async def func():
			data = {'title' : 'test1',
					 'slug' : 'test1',
					 'description' : 't_discr',
					 'image' : 'aaa'}
			ins = await Platform.insert(self._db, **data)
			async with self._db.acquire() as conn:
				query = "select * from platform where(slug = 'test1');"
				row = await conn.fetchrow(query)
			self.assertEqual(ins._dict_obj, row)
			d = dict(ins._dict_obj)
			d.pop('id')
			self.assertEqual(d, data)
		self.loop.run_until_complete(func())




class TestModelPlatform(TModel, unittest.TestCase):


	def test_create(self):
		async def func():
			plat_slug = await Platform.create(self._db, slug = 'test')
			plat_title = await Platform.create(self._db, title = 'test')
			self.assertEqual(plat_slug.__dict__, plat_title.__dict__)
		self.loop.run_until_complete(func())


class TestModelPlatform_Delete(TModel, unittest.TestCase):

	def setUp(self):
		self.loop = asyncio.new_event_loop()
		asyncio.set_event_loop(None)
		async def func():
			self._db = await asyncpgsa.create_pool(dsn=db_url)
			async with self._db.acquire() as conn:
				query = "insert into platform (title, slug) values ('t', 't');"
				await conn.execute(query)
		self.loop.run_until_complete(func())

	def test_delete(self):
		async def func():
			plat_slug = await Platform.create(self._db, slug = 't')
			await plat_slug.delete()
			with self.assertRaises(ValueError):
				plat_slug = await Platform.create(self._db, slug = 't')

		self.loop.run_until_complete(func())



if __name__ == '__main__':
    unittest.main()