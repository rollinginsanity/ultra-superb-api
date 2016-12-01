#Get the base directory that this application is running in.
import os
basedir = os.path.abspath(os.path.dirname(__file__))

#SQLAlchemy Paths
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'api.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_migrations')
