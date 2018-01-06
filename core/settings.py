"""
    Module contains basic application's settings.
    
    module_author: Artur Malarz
    date: 14.11.2017
"""

from pony import orm

WALLPOINT_NAME = 'WALLPOINT1'
ALLOW_ANY = False
NAME_VALIDATION = False
LOGFILE = True
SQL_DEBUG = False
FLASK_DEBUG = True
ATTEMPTS = 5
TIMEOUT = 30

DATABASE = orm.Database()
#DATABASE.bind(provider='sqlite', filename='database.sqlite', create_db=True)
DATABASE.bind(provider='mysql', host='localhost', user='ble_user', passwd='', db='ble_data')
orm.set_sql_debug(SQL_DEBUG)
