from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
    Date,
)

from .meta import Base

class Expense(Base):
    """ expense object."""
    __tablename__= "expenses"
    id = Coumn(Integer, primary)
    item= Column(Unicode)


class MyModel(Base):
    """."""
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    value = Column(Integer)
    category = Column(Unicode)
    date = Column(Date)
    description = Column(Unicode)


Index('my_index', MyModel.name, unique=True, mysql_length=255)
