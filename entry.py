import argparse
import asyncio
import aiohttp
from aiohttp_session import setup, get_session, session_middleware

from demo.settings import load_config
from demo import create_app




try:
	import uvloop
	asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
	print("uvloop is not install")

parser = argparse.ArgumentParser(description='Demo prodject')
parser.add_argument('--host', help='Host to listen', default='0.0.0.0')
parser.add_argument('--port', help='Port to accept connections', default='5000')
parser.add_argument('--reload',
		action='store_true',
		help='Autoreload code on change')
parser.add_argument('-c', '--config', type=argparse.FileType('r'),
		help='Path to congifuration file')

args = parser.parse_args()
app = create_app(config=load_config(args.config))

if args.reload:
	print('Start with code reload')
	import aioreloader
	# app = aiohttp.web.Application()
	aioreloader.start()




# async def curent_user_ctx_processor(request):
# 	session = await get_session(request)
# 	user = None
# 	is_anonymus = True
# 	if 'user' in session:
# 		user_id = session['user']['_id']
# 		user = await User.get_user_by_id(db=request.app['db'], user_id=user_id)
# 		if user:
# 			is_anonymus = not bool(user)
# 	return dict(curent_user=user, is_anonymus=is_anonymus)


# async def user_session_maiddleware(request, handler):
# 	request.session = await get_session(request)
# 	response = await handler(request)
# 	return response


if __name__ == '__main__':
	aiohttp.web.run_app(app, host=args.host, port=args.port)