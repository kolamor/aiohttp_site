
from .views import frontend, auth, admin, ws_server
from aiohttp import web
import os


def setup_routes(app):
	app.router.add_route('GET', '/', frontend.index )
	app.router.add_route('GET', '/post', frontend.post)
	#app.router.add_route('GET', '/login', frontend.login)
	#app.router.add_route('POST', '/login', frontend.login_post)

	app.router.add_routes([
					web.get('/login', auth.Login, 						name='login'),
					web.post('/login', auth.Login),
					web.get('/signup', auth.Signup, 					name='signup'),
					web.post('/signup', auth.Signup, ),
					web.get('/logout', auth.logout, 					name='logout'),
					web.post('/logout', auth.logout_post, 				name="logout_post"),
					
					web.get('/admin/users', admin.AdminUsers,   		name='admin_user'),
					web.get('/admin', admin.Admin, 						name='admin'),
					web.get('/admin/users/{name}', admin.AdminEditUsers, 	name='admin_edit_user'),
					web.post('/admin/users/{name}', admin.AdminEditUsers, ),
					web.get('/admin/news', admin.AdminNews, 			name='admin_news'),
					web.get('/admin/news/{slug}', admin.AdminEditNews, name='admin_edit_news'),
					web.post('/admin/news/{slug}', admin.AdminEditNews ),
					web.get('/admin/create_news', admin.AdminCreateNews, name='create_news'),
					web.post('/admin/create_news', admin.AdminCreateNews),

					web.get('/websocket/ws', ws_server.WS, name='ws'),
					])


def setup_static_routes(app):
	static_dir = str(app['config'].get('STATIC_DIR'))
	base_dir = eval(str(app['config'].get('BASE_DIR')))
	app.router.add_static('/static/', path=(base_dir + static_dir), name='static')


async def path_save_pic(request):
	static_dir = str(request.app['config'].get('STATIC_DIR'))
	base_dir = eval(str(request.app['config'].get('BASE_DIR')))
	path = (base_dir + static_dir)
	return path

   
