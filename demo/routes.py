
from .views import frontend
from aiohttp import web
import os


def setup_routes(app):
	app.router.add_route('GET', '/', frontend.index )
	app.router.add_route('GET', '/post', frontend.post)
	#app.router.add_route('GET', '/login', frontend.login)
	#app.router.add_route('POST', '/login', frontend.login_post)

	app.router.add_routes([
						web.get('/login', frontend.login, 				name='login'),
						web.post('/login', frontend.login_post),
						web.get('/signup', frontend.signup, 			name='signup'),
						web.post('/signup', frontend.signup_post, ),
						web.get('/logout', frontend.logout, 			name='logout'),
						web.post('/logout', frontend.logout_post, 		name="logout_post"),
						web.get('/admin/users', frontend.admin_users,   name='admin_user'),
						web.get('/admin', frontend.admin, 				name='admin'),
						web.get('/admin/users/{name}', frontend.edit_user, name='edit_user')
						

						])


def setup_static_routes(app):
	static_dir = str(app['config'].get('STATIC_DIR'))
	base_dir = eval(str(app['config'].get('BASE_DIR')))
	app.router.add_static('/static/', path=(base_dir + static_dir), name='static')
   
