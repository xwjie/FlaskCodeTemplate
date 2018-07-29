from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    _password = Column(String(50), unique=False)

    def __init__(self, name=None, password=None):
        self.name = name
        self._password = password

    def __repr__(self):
        return '<User %r>' % (self.name)

    #
    #@property
    def _serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }