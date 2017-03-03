from jinja2 import Environment, FileSystemLoader
from wsgiref.simple_server import make_server

def app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    path = environ['PATH_INFO']
    fs = FileSystemLoader('templates')
    return [Environment(loader=fs).get_template(path).render(link=path).encode('utf-8')]

if name == '__main__':
     make_server('localhost', 8000, app).server_forever()