
import logging
import os
import peewee

from peewee import *
from playhouse.postgres_ext import *
from playhouse.db_url import connect as peewee_connect

from colibris import settings


# migrations live in the project root package
MIGRATIONS_DIR = os.path.join(settings.PROJECT_PACKAGE_DIR, 'migrations')

logger = logging.getLogger(__name__)
_database = None


def get_database():
    global _database

    if _database is None:
        logger.debug('initializing db connection')
        _database = peewee_connect(settings.DATABASE, autorollback=True)
        _database.connect()

    return _database


class Model(peewee.Model):
    # this is currently necessary for aiohttp-apispec request data validation
    def __iter__(self):
        return ((k, v) for (k, v) in self.__data__.items())

    def update_fields(self, fields):
        for n, v in fields.items():
            setattr(self, n, v)

    class Meta:
        database = get_database()