
from .views import frontend, auth, admin
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
					web.get('/admin/news/{slug}', admin.admin_edit_news, name='admin_edit_news'),
					web.post('/admin/news/{slug}', admin.admin_edit_news_post ),
					web.get('/admin/create_news', admin.CreateNews, name='create_news'),
					
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

   
