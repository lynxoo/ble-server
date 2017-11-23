"""
    Module contains basic application's settings.
    
    module_author: Artur Malarz
    date: 14.11.2017
"""
import logging
from datetime import datetime

from pony import orm

ALLOW_ANY = False
LOGFILE = False
SQL_DEBUG = False
FLASK_DEBUG = True

DATABASE = orm.Database()
DATABASE.bind(provider='sqlite', filename='database.sqlite', create_db=True)
orm.set_sql_debug(SQL_DEBUG)

if LOGFILE:
    logging.basicConfig(filename="logs/{}_debug.txt".format(datetime.now().isoformat()),
                    format='%(asctime)s %(levelname)s >> %(message)s', level=logging.DEBUG)
else:
    logging.basicConfig(format='%(asctime)s %(levelname)s >> %(message)s', level=logging.DEBUG)