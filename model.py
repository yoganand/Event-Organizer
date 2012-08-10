

from sqlalchemy import create_engine
from sqlalchemy import (Table, Column, Integer, Float, String, 
            Date, DateTime, ForeignKey)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:////home/yoganand/work/Event-Organizer/test.db',
                       echo=True)
Base = declarative_base()

member_committee_table = Table('member_committee', Base.metadata,
	Column('member_id',Integer,ForeignKey('member.id')),
	Column('committee_id',Integer,ForeignKey('committee.id'))
)

committee_service_table = Table('committee_service', Base.metadata,
	Column('service_id',Integer,ForeignKey('service.id')),
	Column('committee_id',Integer,ForeignKey('committee.id'))
)


class Member(Base):
    __tablename__ = 'member'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    committee = relationship("Committee",
                      secondary=member_committee_table,
                      backref="members")

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

    id = Column(Integer, primary_key=True)
    name = Column(String)
    committee = relationship("Committee",
                    secondary=committee_service_table,
                    backref="services")

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return self.name

def create_all():
    Base.metadata.create_all(engine)

if __name__=='__main__':
    from sqlalchemy.orm import sessoinmaker
    Session = sessionmaker(bind=engine)
    session = Session()
