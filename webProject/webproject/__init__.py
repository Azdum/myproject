# -*- coding: utf-8 -*-
from pyramid.config import Configurator


from pyramid.session import SignedCookieSessionFactory
from sqlalchemy import inspect
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Deny
from pyramid.security import Authenticated
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker

from models import *

my_session_factory = SignedCookieSessionFactory('itsaseekreet')

class MyFactory(object):
	def __init__(self, request):
		self.__acl__ = [(Allow, 'admin', "add")]

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    Base.metadata.create_all()
    session = Session(bind = engine)
    session.query(TempOrder).delete(synchronize_session=False)
    #admin = Admin(Login= "admin", Password = "admin")
    #session.add(admin)
    session.commit()


    config = Configurator(root_factory=MyFactory, settings=settings, session_factory=my_session_factory)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)



    config.add_route('home', '/')
    config.add_route('buy', '/buy')
    config.add_route('login', '/login')
    config.add_route('register', '/register')
    config.add_route('order', '/order')
    config.add_route('products', '/products')
    config.add_route('admin', '/admin')
    config.add_route('buyProduct', "/buyProduct/{id}")
    config.add_route('delete', "/delete/{id}")
    config.add_route('reload', "/reload/{id}")
    config.add_route('removeOrder', "/removeOrder/{id}")
    config.add_route('deleteProduct', "/deleteProduct/{id}")
    config.add_route('addProduct', "/addProduct")
    config.add_route('loginAdmin', "/loginAdmin")
    config.add_route('logoutAdmin', "/logoutAdmin")

    #авторизация и аутентификация
    authn_policy = AuthTktAuthenticationPolicy('sosecret', hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.scan()
    return config.make_wsgi_app()
