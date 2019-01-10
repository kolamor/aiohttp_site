from sqlalchemy import (
	Table, Text, Integer, VARCHAR, MetaData, Column, BOOLEAN, ForeignKey, DateTime
	)
import sqlalchemy as sa
from sqlalchemy.sql import func 
import datetime

from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles




__all__ = ('post', 'news' )


meta = MetaData()
post = Table(
	'post', meta,
	Column('id', Integer, primary_key=True),
	Column('title', VARCHAR, nullable=True),
	Column('body', Text,)
	)

user_d = Table(
	'user_d', meta,
	sa.Column('id', sa.Integer, primary_key=True),
	sa.Column('login', sa.VARCHAR, nullable=True ),
	sa.Column('password', sa.Text, nullable=True),
	sa.Column('email', sa.Text, nullable=True),
	sa.Column('admin_privilege', sa.BOOLEAN, ),
	)

session = Table(
	'session',  meta,
	Column('id', Integer, primary_key=True),
	Column('user_ses', VARCHAR, ),
	Column('session_num', Text,)
	)

category = Table(
	'category', meta,
	Column('id', Integer, primary_key=True),
	Column('title', VARCHAR, nullable=True),
	Column('slug', VARCHAR, nullable=True, unique=True),
	)


tag = Table(
	'tag', meta,
	Column('id', Integer, primary_key=True),
	Column('title', VARCHAR, nullable=True),
	Column('slug', VARCHAR, nullable=True, unique=True),
	)


news = Table(
	'news', meta,
	Column('id', Integer, primary_key=True),
	Column('title', VARCHAR, nullable=True),
	Column('slug', VARCHAR, nullable=True, unique=True),
	Column('user_id', Integer, ForeignKey("user_d.id")),
	Column('category_id', Integer, ForeignKey('category.id')),
	Column('text', Text),
	Column('text_min', Text),
	Column('date_created', DateTime(timezone=True), server_default=func.now()),
	Column('date_change', DateTime(timezone=True), server_default=func.now(), onupdate=datetime.datetime.now),
	Column('description', VARCHAR(250)),
	Column('likes', Integer, default=0),
	Column('image', VARCHAR(250)),
	Column('moderation', BOOLEAN, default=False)

	)

news_image = Table(
	'news_image', meta,
	Column('id', Integer, primary_key=True),
	Column('news_id', Integer, ForeignKey('news.id')),
	Column('image', VARCHAR(250)),
	)





