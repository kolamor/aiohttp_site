import re
import asyncio
import asyncpgsa
from slugify import slugify

async def parse():
	with open('xbox360.md', 'r') as f:
		titles=[]
		for a in f.read().splitlines():
			a = re.sub(r'\s+', ' ', a)
			if len(a)>2:
				titles.append(a)
	return titles


async def main():
	titles = await parse()
	database_uri = 'postgresql://kola:test@localhost:5432/demo'
	await insertdb(database_uri, titles)


async def insertdb(database_uri, titles):
	async with asyncpgsa.create_pool(dsn=database_uri) as conn:
		for tit in titles:
			slug = slugify(tit)
			query = f"insert into game(title, slug, platform_id) values ('{tit}', '{slug}', '1');"
			# print(tit, '+++', slug)
			await conn.execute(query)


if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	task = [
			loop.create_task(main())

		]
	wait_tasks = asyncio.wait(task)
	loop.run_until_complete(wait_tasks)