import base64
from sqlalchemy import select, insert
from sqlalchemy.sql import text
# from sqlalchemy import and_, or_
import aiohttp
from aiohttp_jinja2 import template,  render_template
from .. import db 
import os

from aiohttp_session import get_session, session_middleware, setup



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







	


		