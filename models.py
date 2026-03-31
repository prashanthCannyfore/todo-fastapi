from sqlalchemy import Column, Integer, String, Boolean
from database import Base;

class Todo(Base):
    __tablename__ = "todos"
    id  = Column(Integer,primary_key=True,index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    completed = Column(Boolean, default=False)


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)