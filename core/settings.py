"""
    Module contains basic application's settings.
    
    module_author: Artur Malarz
    date: 14.11.2017
"""

from pony import orm

ALLOW_ANY = True
NAME_VALIDATION = True
LOGFILE = True
SQL_DEBUG = False
FLASK_DEBUG = True
ATTEMPTS = 5
TIMEOUT = 30

DATABASE = orm.Database()
DATABASE.bind(provider='sqlite', filename='database.sqlite', create_db=True)
orm.set_sql_debug(SQL_DEBUG)
