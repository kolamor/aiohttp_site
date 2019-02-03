import aiohttp

class WS(aiohttp.web.View):

	async def get(self):

		ws = aiohttp.web.WebSocketResponse()
		await ws.prepare(self.request)
		print('ws-')
		async for msg in ws:
			print('--', msg)
			if msg.type == aiohttp.WSMsgType.TEXT:
				if msg.data == 'close':
					await ws.close()
				else:
					await ws.send_str(msg.data + '/answer')
			elif msg.type == aiohttp.WSMsgType.ERROR:
				print('ws connection closed with exception %s' % ws.exception())

		print('websocket connection closed')
		return ws