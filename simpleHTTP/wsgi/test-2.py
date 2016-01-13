#!/usr/bin/env python
#-*- coding:utf-8 -*-

from wsgiref.simple_server import make_server
from application import simple_app as app
from application import my_app, url_app, re_url_app, re_delegate_app

"""
http://127.0.0.1:8086/
能打印hello world
能打印应用服务环境变量
"""
if __name__ == "__main__":
    # 原生态函数类
    #httpd = make_server('', 8086, app)
    # 使用类管理
    #httpd = make_server('', 8086, my_app)
    # 使用类并通过URL控制进程流
    #httpd = make_server('', 8086, url_app)
    # 通过正则来控制URL
    #httpd = make_server('', 8086, re_url_app)
    httpd = make_server('', 8086, re_delegate_app)
    sa = httpd.socket.getsockname()
    print 'http://{0}:{1}/'.format(*sa)
    
    httpd.serve_forever()