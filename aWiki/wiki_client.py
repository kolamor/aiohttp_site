import aiohttp
import asyncio
import json
from html import unescape
import kw
# import urllib
import wiki
import wiki_s



#urllib.parse.urlencode()

# class ClientJson():

# 	url_ru = 'https://ru.wikipedia.org/w/api.php'
# 	#sen = 'action=query&format=json&prop=extracts&limit=1&titles=halo 3|linux'
# 	s_html = {'action' :  'query', 'format' : 'json', 'prop': 'extracts', 'titles' : 'halo 3', 'exintro' : 1 }

# 	url1 = 'https://ru.wikipedia.org/api/rest_v1/page/html/linux'


# 	url_en = 'https://en.wikipedia.org/w/api.php' # enwiki default api
# 	page_burl = 'https://en.wikipedia.org/wiki/' # enwiki default page url
# 	rest_burl = 'https://en.wikipedia.org/api/rest_v1/' # enwiki default REST url

# 	@classmethod
# 	async def _init(cls, **kwargs):
# 		self = cls()

# 		return self



async def  main3():
	async with wiki.WikiData() as w:
		b = await w.get_html('xbox', exintro = '')
		
		print('----', b)




async def main2():
	async with wiki.WikiData() as a:
	
		b = await a.get_extracts('xbox', exintro = '')
	

async def main():
	async with wiki.WikiData() as w:
		b = await w.get_media('xbox 360')
	# print(b)

async def main1():
	print('1')
	# wobj = WikiUtils(titles = 'xbox',  exintro = '')
	# wobj = kw.Search.get_extracts('xbox', exintro = '')
	wobj = kw.QueryDesigner()
	print('12',wobj)
	wobj = await wobj.get_extracts('xbox', exintro = '')


	# s = await wobj.get_html()
	client = await ClientJson._init()
	
	await client.wiki_f(wobj)
	print('---------', wobj)

	
if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	task = [
			# loop.create_task(main3()),
			loop.create_task(main())
			
		]
	wait_tasks = asyncio.wait(task)
	loop.run_until_complete(wait_tasks)