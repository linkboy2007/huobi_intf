# coding:utf8
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import tornado.autoreload
import os
from urls import urls

configs = {
     'template_path' : os.path.join(os.path.dirname(__file__), 'templates'),
     'static_path' : os.path.join(os.path.dirname(__file__), 'static'),
     'autoreload': True,
     'compress_response': True  #启用压缩，提高静态网页的加载速度
}

class CustomApplication(tornado.web.Application):
    def __init__(self, configs, urls):
        settings = configs
        handlers = urls
        super(CustomApplication, self).__init__(handlers=handlers, **settings)


def create_app():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(CustomApplication(configs, urls))
    http_server.listen(options.port)
    print('正在监听端口: ',options.port)
    #下边是自动autoreload代码
    instance = tornado.ioloop.IOLoop.instance() 
    tornado.autoreload.start(instance) 
    instance.start()
  
  
app = create_app

if __name__ == "__main__":
    app()
