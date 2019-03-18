import aiohttp
import asyncio
# from wiki import WikiData
import sys




async def main():

	sys.path.insert(0, '/home/kola/progr/project/aiohttp_site/client')
	import wiki
	async with wiki.Wiki() as w:
		b = await w.opensearch('%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%98%D0%B3%D1%80%D1%8B_%D0%B4%D0%BB%D1%8F_Xbox_360')
	print(b)


if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	task = [
			# loop.create_task(main3()),
			loop.create_task(main())

		]
	wait_tasks = asyncio.wait(task)
	loop.run_until_complete(wait_tasks)