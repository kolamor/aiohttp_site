import base64
from aiohttp import web
import jinja2
import aiohttp_jinja2
import asyncpgsa
from .routes import setup_routes

from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp_session import setup, get_session, session_middleware
from .models.user import User





async def create_app(config:dict):
	app = web.Application()
	
	app['config'] = config
	aiohttp_jinja2.setup(
		app,
		loader = jinja2.PackageLoader('demo', 'templates'),
		#context_processors=[current_user_ctx_processor],
		)

	secret_key = base64.urlsafe_b64decode(app['config'].get('secret_key'))
	setup(app, EncryptedCookieStorage(secret_key))

	setup_routes(app)
	app.on_startup.append(on_start)
	app.on_cleanup.append(on_shutdown)

	setup_middlewares(app)


	return app




async def on_start(app):
	config = app['config']
	app['db'] = await asyncpgsa.create_pool(dsn=config['database_uri'])


async def on_shutdown(app):
	await app['db'].close()


def setup_middlewares(app):
	app.middlewares.append(user_session_middleware)


@web.middleware
async def user_session_middleware(request, handler):
	request.session = await get_session(request)
	response = await handler(request)
	return response


async def current_user_ctx_processor(request):
	session = await get_session(request)
	user = None
	is_anonymous = True
	if 'user' in session:
		user_id = session['user']['_id']
		user = await User.get_user_by_id(db=request.app['db'], user_id=user_id)
		if user:
			is_anonymous = not bool(user)
	return {
			'current_user' : user,
			'is_anonymous' : is_anonymous
	}