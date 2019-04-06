import re
import asyncio
import asyncpgsa
import csv
from slugify import slugify
import os

csv_file ='xbox360market.csv'
static = 'img_ava_xbox360'
database_uri = 'postgresql://kola:test@localhost:5432/demo'


async def parse_csv(csv_file):
	with open(csv_file, newline='') as csvfile:
		spamreader = csv.reader(csvfile)
		title = []
		for row in spamreader:
			# print(row)
			row[0].split(',')
			title.append(row[0])
			print(row[0])
		return title


async def find_img():
	pass



async def main():
	titles = await parse_csv (csv_file)
	async with asyncpgsa.create_pool(dsn=database_uri) as conn:
		for tit in titles:
			print(tit)
			img = (static+'/'+tit+'.jpg')
			slug = slugify(tit)
			query = """insert into game_xbox360(title, slug, image, platform_id) values ($1, $2, $3, '1');"""
			print(query)
			await conn.execute(query, tit, slug, img )
			# print (tit, slug, img )



if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	task = [
			loop.create_task(main())

		]
	wait_tasks = asyncio.wait(task)
	loop.run_until_complete(wait_tasks)