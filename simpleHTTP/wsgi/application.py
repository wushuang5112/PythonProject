#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""application.py"""

def simple_app(environ, start_response):
    """Simplest possible application object"""
    status = "200 OK"
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return ['Hello world!\n']

class my_app:
    """Netual Application"""
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response
    
    def __iter__(self):
        status = "200 OK"
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield "Hello World!\n"

class url_app:
    """Match Url Application"""
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response
    
    def __iter__(self):
        path = self.environ['PATH_INFO']
        if path == "/":
            return self.GET_index()
        elif path == "/hello":
            return self.GET_hello()
        else:
            return self.notfound()
    
    def GET_index(self):
        status = "200 OK"
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield "Welcome!\n" 
        
    def GET_hello(self):
        status = "200 OK"
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield "Hello World!\n"         
        
    def notfound(self):
        status = "404 Not Found"
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield "Not Found\n"

import re
class re_url_app:
    """Use Rexgex To Match Url Application"""
    urls = (
        ("/", "index"),
        ("/hello/(.*)", "hello"),
    )
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response
    
    def __iter__(self):
        path = self.environ['PATH_INFO']
        method = self.environ['REQUEST_METHOD']
        
        for pattern, name in self.urls:
            m = re.match('^' + pattern + '$', path)
            if m:
                # pass the matched groups as arguments to the function
                args = m.groups()
                funcname = method.upper() + '_' + name
                if hasattr(self, funcname):
                    func = getattr(self, funcname)
                    return func(*args)
        
        return self.notfound()
    
    def GET_index(self):
        status = "200 OK"
        response_headers = [('Content-type', 'text/plain')]
        start = self.start(status, response_headers)
        yield "Welcome!\n" 
        
    def GET_hello(self, name):
        status = "200 OK"
        response_headers = [('Content-type', 'text/plain')]
        start = self.start(status, response_headers)
        yield "Hello %s!\n" % name
        
    def notfound(self):
        status = "404 Not Found"
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield "Not Found\n"

class re_delegate_app:
    """Use Rexgex To Match Url Application"""
    urls = (
        ("/", "index"),
        ("/hello/(.*)", "hello"),
    )
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response
        self._headers = []
        self.status = '200 OK'
    
    def __iter__(self):
        result = self.delegate()
        self.start(self.status, self._headers)
        
        # 将返回值result(字符串 或者 字符串列表)转换为迭代对象
        if isinstance(result, basestring):
            return iter([result])
        else:
            return iter(result)

    def delegate(self):
        path = self.environ['PATH_INFO']
        method = self.environ['REQUEST_METHOD']
        
        for pattern, name in self.urls:
            m = re.match('^' + pattern + '$', path)
            if m:
                # pass the matched groups as arguments to the function
                args = m.groups()
                funcname = method.upper() + '_' + name
                if hasattr(self, funcname):
                    func = getattr(self, funcname)
                    return func(*args)
        
        return self.notfound()        

    def header(self, name, value):
        self._headers.append((name, value))

    def GET_index(self):
        self.header('Content-type', 'text/plain')
        return "Welcome!\n"
        
    def GET_hello(self, name):
        self.header('Content-type', 'text/plain')
        return "Hello %s!\n" % name
        
    def notfound(self):
        self.status = "404 Not Found"
        self.header('Content-type', 'text/plain')
        return "Not Found\n"

class my_simple_app:
    """my simple web framework"""
    headers = []
    def __init__(self, urls=(), fvars={}):
        self.urls = urls
        self.fvars = fvars
    
    def __call__(self, environ, start_response):
        self.status = "200 OK"
        del self.headers[:]
        
        result = self._delegate(environ)
        start_response(self.status, self.headers)
        
        # 将返回值result（字符串 或者 字符串列表）转换为迭代对象
        if isinstance(result, basestring):
            return iter([result])
        else:
            return iter(result)
        
    def _delegate(self, environ):
        path = environ['PATH_INFO']
        method = environ['REQUEST_METHOD']
        
        for pattern, name in self.urls:
            m = re.match('^' + pattern + '$', path)
            if m:
                # pass the matched groups as arguments to the function
                args = m.groups()
                funcname = method.uppper()
                klass = self._fvars.get(name)
                if hasattr(klass, funcname):
                    func = getattr(klass, funcname)
                    return func(klass(), *args)
        
        return self.notfound()      

    def notfound(self):
        self.status = "404 Not Found"
        self.header('Content-type', 'text/plain')
        return "Not Found\n"
    
    @classmethod
    def header(cls, name, value):
        cls.headers.append((name, value))