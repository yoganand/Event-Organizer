
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
            (r"/committee/(?P<id_>[^\/]+)", CommitteeHandler),
            (r"/member", MemberHandler),
            (r"/member/(?P<id_>[^\/]+)", MemberHandler),
            (r"/service", ServiceHandler),
            (r"/service/(?P<id_>[^\/]+)", ServiceHandler),
        ]
        settings = dict(
            cookie_secret="some_secret",
            login_url="/auth/login",
            template_path=os.path.join(os.path.dirname(__file__),
                                "public", "templates"),
            static_path=os.path.join(os.path.dirname(__file__),
                                "public", "static"),
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
    def get(self, id_=None):
        if not id_:
            committee_form = CommitteeForm()
            self.render('committee/new.html', form=committee_form)
            return
        committee = self.db.query(Committee).filter_by(id_=id_).first()
        self.render('committee/index.html',
                    committee=str(committee.name),
                    committee_id=id_)

    def post(self, id_=None):
        if 'Edit' in self.request.arguments:
            self._get(id_=id_)
            return
        elif 'Delete' in self.request.arguments:
            self._delete(id_)
            return
        _method = self.get_argument('_method', None)
        if _method == "put":
            self._put(id_)
            return
        committee_form = CommitteeForm(self)
        if committee_form.validate():
            committee = Committee(**committee_form.data)
            self.db.add(committee)
            self.db.commit()
            self.write('%s' % committee_form.name.data)
            return
        else:
            self.render('index.html', form=committee_form)

    def _get(self, id_=None):
        committee = self.db.query(Committee).filter_by(id_=id_).first()
        committee_form = CommitteeForm(name=committee.name)
        self.render('committee/edit.html', form=committee_form,
                   committee_id=id_)

    def _put(self, id_):
        committee = self.db.query(Committee).filter_by(id_=id_).first()
        if committee is not None:
            committee.name = self.get_argument('name', None)
            self.db.commit()
            self.redirect(id_)
            #self.write(committee.name)

    def _delete(self, id_):
        committee = self.db.query(Committee).filter_by(id_=id_).first()
        if committee is not None:
            self.db.delete(committee)
            self.db.commit()
        else:
            self.set_status(403)

class MemberHandler(BaseHandler):
    def get(self, id_=None):
        if not id_:
            member_form = MemberForm()
            self.render('member/new.html', form=member_form)
            return
        member = self.db.query(Member).filter_by(id_=id_).first()
        self.render('member/index.html',
                    member=str(member.name),
                    member_id=id_)

    def post(self, id_=None):
        if 'Edit' in self.request.arguments:
            self._get(id_=id_)
            return
        elif 'Delete' in self.request.arguments:
            self._delete(id_)
            return
        _method = self.get_argument('_method', None)
        if _method == "put":
            self._put(id_)
            return
        member_form = MemberForm(self)
        if member_form.validate():
            member = Member(**member_form.data)
            self.db.add(member)
            self.db.commit()
            self.write('%s' % member_form.name.data)
            return
        else:
            self.render('index.html', form=member_form)

    def _get(self, id_=None):
        member = self.db.query(Member).filter_by(id_=id_).first()
        member_form = MemberForm(name=member.name, phone=member.phone)
        self.render('member/edit.html', form=member_form,
                   member_id=id_)

    def _put(self, id_):
        member = self.db.query(Member).filter_by(id_=id_).first()
        if member is not None:
            member.name = self.get_argument('name', None)
            member.phone = self.get_argument('phone', None)
            self.db.commit()
            self.redirect(id_)
            #self.write(committee.name)

    def _delete(self, id_):
        member = self.db.query(Member).filter_by(id_=id_).first()
        if member is not None:
            self.db.delete(member)
            self.db.commit()
        else:
            self.set_status(403)


class ServiceHandler(BaseHandler):
    def get(self, id_=None):
        if not id_:
            service_form = ServiceForm()
            self.render('service/new.html', form=service_form)
            return
        service = self.db.query(Service).filter_by(id_=id_).first()
        self.render('service/index.html',
                    service=str(service.name),
                    service_id=id_)

    def post(self, id_=None):
        if 'Edit' in self.request.arguments:
            self._get(id_=id_)
            return
        elif 'Delete' in self.request.arguments:
            self._delete(id_)
            return
        _method = self.get_argument('_method', None)
        if _method == "put":
            self._put(id_)
            return
        service_form = ServiceForm(self)
        if service_form.validate():
            service = Service(**service_form.data)
            self.db.add(service)
            self.db.commit()
            self.write('%s' % service_form.name.data)
            return
        else:
            self.render('index.html', form=service_form)

    def _get(self, id_=None):
        service = self.db.query(Service).filter_by(id_=id_).first()
        service_form = ServiceForm(name=service.name)
        self.render('service/edit.html', form=service_form,
                   service_id=id_)

    def _put(self, id_):
        service = self.db.query(Service).filter_by(id_=id_).first()
        if service is not None:
            service.name = self.get_argument('name', None)
            self.db.commit()
            self.redirect(id_)
            #self.write(committee.name)

    def _delete(self, id_):
        service = self.db.query(Service).filter_by(id_=id_).first()
        if service is not None:
            self.db.delete(service)
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
