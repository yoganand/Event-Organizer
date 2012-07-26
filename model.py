
from sqlalchemy.ext.declarative import delcarative_base
from sqlalchemy import Column, Integer, Float, String, Date, Datetime

base = declarative_base()

class Member(Base):
    __tablename__ = 'member'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)

    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def __repr__(self):
        return self.name


class Committee(Base):
    __tablename__ = 'committee'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return self.name


class Service(Base):
    __tablename__ = 'service'

    id = Column(Integer, primary_key)
    name = Column(String)

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return self.name
