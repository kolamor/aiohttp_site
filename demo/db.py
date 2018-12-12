from sqlalchemy import (
	Table, Text, Integer, VARCHAR, MetaData, Column, BOOLEAN,
	)
import sqlalchemy as sa

__all__ = ('post',  )

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