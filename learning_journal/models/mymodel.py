"""Model Implementation."""


from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
    Date
)

from .meta import Base


class Entries(Base):
    """Entries object."""\

    __tablename__ = "entries"
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    title1 = Column(Unicode)
    create_date = Column(Date)
    body = Column(Unicode)
