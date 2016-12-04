from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
o_auth_access_token = Table('o_auth_access_token', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('token_value', String(length=64)),
    Column('grant', String(length=128)),
    Column('creation_date', DateTime(timezone=True)),
)

o_auth_refresh_token = Table('o_auth_refresh_token', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('token_value', String(length=64)),
    Column('grant', String(length=128)),
    Column('creation_date', DateTime(timezone=True)),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('password', String(length=128)),
    Column('creation_date', DateTime(timezone=True)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['o_auth_access_token'].create()
    post_meta.tables['o_auth_refresh_token'].create()
    post_meta.tables['user'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['o_auth_access_token'].drop()
    post_meta.tables['o_auth_refresh_token'].drop()
    post_meta.tables['user'].drop()
