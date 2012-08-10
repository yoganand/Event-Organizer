
import os

from sqlalchemy.orm import scoped_session, sessionmaker
from model import *
from forms import *

import uimodules

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
            (r"/committee", CommitteeHandler),
            (r"/committee/(?P<committee_id>[^\/]+)", CommitteeHandler),
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
            ui_modules=uimodules,
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = scoped_session(sessionmaker(bind=engine))


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

class CommitteeHandler(BaseHandler):
    def get(self,committee_id=None):
        if not committee_id:
            committee_form = CommitteeForm()
            self.render('index.html', form=committee_form)
            return
        committee = self.db.query(Committee).filter_by(id=committee_id).first()
        self.write(committee)
        #committee_form = CommitteeForm(name=committee.all()[0])
        #self.render('index.html', form=committee_form)

    def post(self):
        committee_form = CommitteeForm(self)
        if committee_form.validate():
            committee = Committee(**committee_form.data)
            self.db.add(committee)
            self.db.commit()
            self.write('%s' % committee_form.name.data)
        else:
            self.render('index.html', form=committee_form)

    def put(self, committee_id):
        committee = self.db.query(Committee).fiter_by(id=committee_id).first()
        if committee is not None:
            committee.name = self.request.body['name']
            self.db.commit()
            self.write(committee)

    def delete (self, committee_id):
        committee = self.db.query(Committee).filter_by(id=committee_id).first()
        if committee is not None:
            self.db.delete(committee)
            self.db.commit()
        else:
            self.set_status(403)
            

def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__=='__main__':
    main()
