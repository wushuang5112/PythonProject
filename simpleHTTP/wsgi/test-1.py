from wsgiref.simple_server import make_server,demo_app

"""
http://127.0.0.1:8086/
能打印hello world
能打印应用服务环境变量
"""

httpd = make_server('', 8086, demo_app)
sa = httpd.socket.getsockname()
print 'http://{0}:{1}/'.format(*sa)

httpd.serve_forever()