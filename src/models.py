from sqlalchemy import (Column, Integer, String, ForeignKey, 
    Text, DateTime)
from sqlalchemy.orm import relationship
import datetime
from database import Base

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key= True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    posts = relationship("Post", lazy= True, backref="author")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key= True, index=True)
    author_id = Column(Integer, ForeignKey("authors.id"))
    title = Column(String)
    text = Column(Text)
    date = Column(DateTime, default=datetime.datetime.now)
    comments = relationship("Comment", lazy=True, backref="post")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    title = Column(String)
    text = Column(Text)
    date = Column(DateTime, default=datetime.datetime.now)
    commenter_id = Column(Integer, ForeignKey("authors.id"))
