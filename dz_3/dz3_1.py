from wsgiref.simple_server import make_server

def app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    path = environ['PATH_INFO']
    if path == '':
        path = 'index.html'
    file = open(path, 'r')
    return [file.read()]

class Middleware(object):
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        page = self.app(environ, start_response)[0]
        if (page.find('<body>') > 0 and page.find('</body>') > 0):
            n1, n2 = page.split('<body>')
            page = n1 + '<body>\n' "\t\t<div class='top'>Middleware TOP</div>" + n2
            n1, n2 = page.split('</body>')
            page = n1 + "\t<div class='bottom'>Middleware BOTTOM</div>\n" + '\t</body>' + n2           
        return page

make_server('127.0.0.1', 8000, Middleware(app)).serve_forever()