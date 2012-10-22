
from model import *
from wtforms import *
from wtforms.validators import *
from wtforms.ext.sqlalchemy.fields import (QuerySelectField,
                                           QuerySelectMultipleField)

from utils import MultiValueDict


class BaseForm(Form):
    def __init__(self, handler=None, obj=None, prefix='',
                formdata=None, **kwargs):
        if handler:
            formdata = MultiValueDict()
            for name in handler.request.arguments.keys():
                formdata.setlist(name, handler.get_arguments(name))
        Form.__init__(self, formdata, obj=obj, prefix=prefix, **kwargs)


class CommitteeForm(BaseForm):
    name = TextField('name', validators=[Required()])
    members = QuerySelectField(query_factory=get_members)


class MemberForm(BaseForm):
    name = TextField('name', validators=[Required()])
    phone = TextField('phone')
    #members = QuerySelectField()


class ServiceForm(BaseForm):
    name = TextField('name', validators=[Required()])
