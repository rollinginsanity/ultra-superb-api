#https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
from migrate.versioning import api
from ultraSuperbAPI.config import SQLALCHEMY_DATABASE_URI
from ultraSuperbAPI.config import SQLALCHEMY_MIGRATE_REPO
from ultraSuperbAPI.api import db
import os.path
db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))
