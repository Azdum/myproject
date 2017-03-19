# -*- coding: utf-8 -*-
'''from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory('lib')
'''
from sqlalchemy import distinct
from pyramid.view import view_config
from pyramid.response import Response
from models import *
import models
import re

import uuid
import shutil

from pyramid.security import (
remember,
forget,
)

from pyramid.httpexceptions import (
HTTPFound,
HTTPNotFound,
)


@view_config(route_name='login',renderer='templates/order.jinja2')
def login(request):
	session = Session(bind = engine)
	login = request.params["login"]
	password = request.params["password"]
	user = session.query(User).filter_by(Login = login, Password = password ).first()
	message = []
	if user == None:
		message.append(u"Вы ввели не существующие данные")
	else:
		if session.query(TempOrder).filter_by(IdCustomer = request.authenticated_userid).first() == None:
			message.append(u"Вы ничего не выбрали")
		else:
			message.append(u"Ваш заказ успешно зарегестрирован")
			orders = session.query(TempOrder).filter_by(IdCustomer = request.authenticated_userid).all()
			session.query(TempOrder).filter_by(IdCustomer = request.authenticated_userid).delete(synchronize_session=False)
			for i in orders:
				order = Order(IdCustomer = login, IdProduct = i.IdProduct, Count = i.Count)
				session.add(order)
			session.commit()
	return { "message2" : message}


@view_config(route_name='register' , renderer='templates/order.jinja2')
def register(request):
	session = Session(bind = engine)
	login = request.params["login"]
	password = request.params["password"]
	mail = request.params["mail"]
	tel = request.params["tel"]
	confirm = request.params["confirm"]
	name = request.params["name"]
	secondName = request.params["secondName"]
	message = []
	if(password != confirm):
		message.append(u"Пароли не совпали")
	if session.query(User).filter_by(Login = login).first() != None:
		message.append(u"Такой пользователь уже существует")
	if(len(message) == 0):
		user = User(Login = login, Password = password, FirstName = name, SecondName = secondName, Tel = tel, Mail = mail )
		session.add(user)
		session.commit()
		message.append(u"Вы успешно зарегестрировались")
	if session.query(TempOrder).filter_by(IdCustomer = request.authenticated_userid).first() == None:
			message.append(u"Вы ничего не выбрали")
	else:
		message.append(u"Ваш заказ успешно зарегестрирован")
		orders = session.query(TempOrder).filter_by(IdCustomer = request.authenticated_userid).all()
		session.query(TempOrder).filter_by(IdCustomer = request.authenticated_userid).delete(synchronize_session=False)
		for i in orders:
			order = Order(IdCustomer = login, IdProduct = i.IdProduct, Count = i.Count)
			session.add(order)
		session.commit()
	return { "message" : message }


@view_config(route_name='home', renderer='templates/index.jinja2')
def index(request):
	session = Session(bind = engine)
	products = session.query(Product)
	if(request.method == "POST"):
		name = request.params["name"]
		products = products.filter(Product.Name.like('%' + name + '%'))
	#newProduct = Product(Name = "name", Picture = "Picture", Cost = "10")
	#session.add(newProduct)
	#session.commit()
	if request.authenticated_userid == None:
		headers = remember(request, str(models.countCustomer))
		models.countCustomer= models.countCustomer + 1;		
		return HTTPFound(location = request.route_url('home'), headers = headers)
	return { "Products" : products }


@view_config(route_name='buyProduct')
def buyProduct(request):
	idProduct = int(request.matchdict["id"])
	idCustomer = int(request.authenticated_userid)
	session = Session(bind = engine)
	if session.query(TempOrder).filter_by(IdProduct = idProduct, IdCustomer = idCustomer).first() == None:
		tempOrder = TempOrder(IdProduct = idProduct, IdCustomer = idCustomer, Count = 1)
		session.add(tempOrder)
		session.commit()
	return HTTPFound(location = request.route_url("home"))

@view_config(route_name='buy', renderer='templates/buy.jinja2')
def buy(request):
	idCustomer = request.authenticated_userid
	session = Session(bind = engine)
	data = []
	tempOrders = session.query(Product, TempOrder).filter(Product.id == TempOrder.IdProduct).all()
	for i in tempOrders:
		secondData = []
		for ii in i:
			secondData.append(ii)
		data.append(secondData)
	cost = 0;
	for i in data:
		tempCost = int(i[0].Cost) * i[1].Count
		cost = cost + tempCost
		i.append(tempCost)
	return { "Products" : data, "Cost" : cost }


@view_config(route_name='delete')
def delete(request):
	idProduct = int(request.matchdict["id"])
	idCustomer = int(request.authenticated_userid)
	session = Session(bind = engine)
	tempOrder = session.query(TempOrder).filter_by(id = idProduct, IdCustomer = idCustomer).first()
	if tempOrder != None:
		session.delete(tempOrder)
		session.commit()
	return HTTPFound(location = request.route_url("buy"))


@view_config(route_name='reload')
def reload(request):
	idProduct = int(request.matchdict["id"])
	print(idProduct)
	idCustomer = int(request.authenticated_userid)
	print(idCustomer)
	session = Session(bind = engine)
	print(session.query(TempOrder).all())
	tempOrder = session.query(TempOrder).filter_by(id = str(idProduct), IdCustomer = int(idCustomer)).first()
	print(tempOrder)
	if tempOrder != None:
		tempOrder.Count = request.params["count"]
		session.commit()
		print(1)
	return HTTPFound(location = request.route_url("buy"))


@view_config(route_name='order', renderer='templates/order.jinja2')
def order(request):
    return {}


@view_config(route_name='removeOrder')
def removeOrder(request):
		login = request.matchdict["id"]
		session = Session(bind = engine)
		session.query(Order).filter_by(IdCustomer = login).delete(synchronize_session=False)
		session.commit()
		return HTTPFound(location = request.route_url("admin"))


@view_config(route_name='admin', renderer='templates/admin.jinja2')
def admin(request):
	session = Session(bind= engine)
	data = []
	allOrder = session.query(Order).all()
	alllOrder = []
	for i in allOrder:
		alllOrder.append(i.IdCustomer)
	alllOrder = list(set(alllOrder))
	for idCustomer in alllOrder:
		cost = 0
		secondData = []
		user = session.query(User).filter( User.Login == (idCustomer.encode("utf-8"))).first()
		secondData.append(user)
		products = session.query(Product, Order).filter(Product.id == Order.IdProduct, Order.IdCustomer == user.Login ).all()
		newProduct = []
		for pr in products:
			ssData = []
			for prr in pr:
				ssData.append(prr)
			tempCost = int(pr[0].Cost) * pr[1].Count
			cost = cost+ tempCost
			ssData.append(tempCost)
			newProduct.append(ssData)
		secondData.append(newProduct)
		secondData.append(cost)
		data.append(secondData)
	if(session.query(Admin).filter_by(Login = request.authenticated_userid).first() != None):
		username = request.authenticated_userid
	else:
		username = None
	return { "all" : data , "username" : username}


@view_config(route_name='loginAdmin')
def loginAdmin(request):
	session = Session(bind = engine)
	admin = session.query(Admin).filter_by(Login = request.params['login'], Password = request.params["password"]).first()
	if admin != None:
		headers = remember(request, str(admin.Login))
		return HTTPFound(location = request.route_url('admin'), headers = headers)
	return HTTPFound(location = request.route_url('admin'))


@view_config(route_name='logoutAdmin')
def logoutAdmin(request):
	headers = forget(request)
	return HTTPFound(location = '/admin', headers = headers)

@view_config(route_name='products', renderer='templates/products.jinja2', permission= "add")
def products(request):
	session = Session(bind = engine)
	products = session.query(Product).all()
	return { "products" : products, "username" : request.authenticated_userid }

@view_config(route_name='deleteProduct')
def deleteProduct(request):
	session = Session(bind = engine)
	idProduct = int(request.matchdict["id"])
	session.query(Product).filter_by(id = idProduct).delete(synchronize_session=False)
	session.commit()
	return HTTPFound(location = request.route_url("products"))

@view_config(route_name='addProduct')
def addProduct(request):
	session = Session(bind = engine)
	if(request.POST['picture']) != "":
		filename = request.POST['picture'].filename
		input_file = request.POST["picture"].file
		file_path = os.path.join( 'webproject/static/images/uploads', filename)
		with open(file_path, 'wb') as output_file:
			shutil.copyfileobj(input_file, output_file)
		file_path = re.split(r'[/]', file_path, maxsplit = 1)[1]
	else:
		file_path = u"static/images/none.jpg"
	newProduct = Product(Name = request.params["name"], Cost = request.params["cost"], Picture = file_path)
	session.add(newProduct)
	session.commit()
	return HTTPFound(location = request.route_url("products"))