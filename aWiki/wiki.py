import aiohttp
from html import unescape
# from client.kw import QueryDesigner
import aWiki.kw as kw
import aWiki.wiki_s as wiki_s

class Wiki:

	def __init__(self, lang='ru', session = None):
		if session is None:
			self.session = aiohttp.ClientSession()
		else:
			self.session = session

		self.url = f'https://{lang.lower()}.wikipedia.org/w/api.php'


	async def get_html(self, page, clear=True, *args, **kwargs):
		query_des = kw.QueryDesigner()
		query = await query_des.get_html(page, *args, **kwargs)
		try:
			data = await self._fetch(query)
		except:
			print('======get_html')
		return data


	async def opensearch(self, search, *args, **kwargs):
		query_des = kw.QueryDesigner()
		query = await query_des.opensearch(search, *args, **kwargs)
		try:
			data = await self._fetch(query)
		except:
			print('======opensearch')
		return data


	async def get_urls(self, gapfrom, *args, **kwargs):
		query_des = kw.QueryDesigner()
		query = await query_des.get_urls(gapfrom, *args, **kwargs)
		print(query)
		try:
			data = await self._fetch(query)
		except:
			print('======get_urls')
		return data

	async def get_media(self, titles, *args, **kwargs):
		query_des = kw.QueryDesigner()
		query = await query_des.get_media(titles, *args, **kwargs)
		try:
			data = await self._fetch(query)
		except:
			print('======get_media')
		return data

	async def get_extracts(self, titles, *args, **kwargs):
		query_des = kw.QueryDesigner()
		try:
			query = await query_des.get_extracts(titles, *args, **kwargs)
		except:
			print('======get_extracts')
		
		data = await self._fetch(query)
		return data





	async def _fetch(self, send):

		async with self.session.get(self.url, params=send) as response:
			# print('-----', response)
			if response.content_type == 'text/html':
				data = await response.text()
			if response.content_type == 'application/json':
				data =  await response.json()
			if response.content_type == 'text/xml':
				data = await response.text()
			if response.content_type == 'application/vnd.php.serialized':
				data = await response.text()
		return data


	async def close(self):
		"""Close the aiohttp Session"""
		await self.session.close()

	async def __aenter__(self):
		return self

	async def __aexit__(self, exception_type, exception_value, traceback):
		await self.close()



class WikiData(Wiki):

	async def get_extracts(self, titles, *args, **kwargs):

		data = await super().get_extracts(titles, *args, **kwargs)
		data = unescape(data)
		data = await wiki_s.Deser.get_extracts(data)
		return data

	async def get_html(self, page, clear=True, *args, **kwargs):
		data = await super().get_html(page, clear, *args, **kwargs)
		data = unescape(data)
		data = await wiki_s.Deser.get_html(data)
		return data

	async def get_urls(self, gapfrom, *args, **kwargs):
		data = await super().get_urls(gapfrom, *args,  **kwargs)
		data = unescape(data)
		data = await wiki_s.Deser.get_urls(data)
		return data

	async def get_media(self, titles, *args, **kwargs):
		data = await super().get_media(titles, *args, **kwargs)
		data = unescape(data)
		data = await wiki_s.Deser.get_media(data, *args, **kwargs)
		if data == []:
			return []
		query_img = "|".join([i["title"] for i in data])

		query = {
				'action' : 'query',
				'titles' : query_img,
				'format' : 'json',
				'prop'	 : 'imageinfo',
				'iiprop' : 'url',
				}

		data = await self._fetch(query)
		pages = data["query"]["pages"]
		urls = [img["imageinfo"][0]["url"] for img in pages.values()]
		return urls











