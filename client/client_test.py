import aiohttp
import asyncio
import json

class ClientWS():
	"""docstring for ClientWS"""
	test_json = { "test" : "test"}
	url = "http://localhost:5000/websocket/ws"

	

	@classmethod
	async def _init(cls, **kwargs):
		self = cls()

		return self


	async def test_ws(self, send_json = None):
		self.send_json = self.test_json
		async with aiohttp.ClientSession() as session:
			await self._fetch(session)

		return self


	async def _fetch(self, session):
		async with session.ws_connect(self.url) as ws:
			await ws.send_json(self.send_json, compress=None, dumps=json.dumps)
			print('Запрос: ', self.send_json)
			async for msg in ws:
				if msg.type == aiohttp.WSMsgType.TEXT:
					print('Text: ',  msg.data)
					if msg.data == 'close cmd':
						await ws.close()
						break
					else:
						pass
				elif msg.type == aiohttp.WSMsgType.ERROR:
					break
				elif msg.type == aiohttp.WSMsgType.PING:
					await ws.pong()
				elif msg.type == aiohttp.WSMsgType.BINARY:
					pass


async def main():
	client = await ClientWS._init()
	print('---', client)
	await client.test_ws()

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	task = [
			loop.create_task(main()),
			
		]
	wait_tasks = asyncio.wait(task)
	loop.run_until_complete(wait_tasks)
	# loop.run_until_complete(main())
		