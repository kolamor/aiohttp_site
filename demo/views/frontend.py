import base64
from sqlalchemy import select, insert
from sqlalchemy.sql import text
# from sqlalchemy import and_, or_
import aiohttp
from aiohttp_jinja2 import template,  render_template
from .. import db 
import os

from aiohttp_session import get_session, session_middleware, setup

from ..models.news import News, Category, NewsImage
from ..models.user import User





@template('index.html')
async def index(request):
	
	site_name = request.app['config'].get('site_name')
	
		
	return { 'site_name': site_name }


async def post(request):
	async with request.app['db'].acquire() as conn:
		query = select([db.post.c.id, db.post.c.title, db.post.c.body ])
		result = await conn.fetch(query)

	async with request.app['db'].acquire() as conn:	
		query = select([db.user_d.c.login, db.user_d.c.admin_privilege ])
		result1 = await conn.fetch(query)
	return aiohttp.web.Response(body=str(result+result1))


class Chat(aiohttp.web.View):

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
		








	


		