from application import my_simple_app

urls = (
    ("/", "index"),
    ("/hello/(.*)", "hello")
)

wsgiapp = my_simple_app(urls, globals())
class index:
    def GET(self):
        my_simple_app.header('Content-type', 'text/plain')
        return "Welcome\n"

class hello:
    def GET(self, name):
        my_simple_app.header('Content-type', 'text/plain')
        return "Hello %s!\n" % name

if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    httpd = make_server("", 8086, wsgiapp)
    
    sa = httpd.socket.getsockname()
    print "http://{0}:{1}/".format(*sa)
    
    httpd.serve_forever()