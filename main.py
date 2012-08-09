
import os

from sqlalchemy.orm import scoped_session, sessionmaker
from model import *

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type="int")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
        ]
        settings = dict(
            cookie_secret="some_secret",
            login_url="/auth/login",
            template_path=os.path.join(os.path.dirname(__file__),
                                "public","templates"),
            static_path=os.path.join(os.path.dirname(__file__),
                                "public","static"),
            xsrf_cookies=True,
            auto_escape="xhtml_escape",
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = scoped_session(sessionmaker(bind=engine))
        create_all()


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id:
            return None
        return self.db.query(Member).get(user_id)

class MainHandler(BaseHandler):
    def get(self):
        self.write('Welcome to Event-Organizer')


def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__=='__main__':
    main()
