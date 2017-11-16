from pony import orm

SQL_DEBUG = False
DATABASE = orm.Database()
DATABASE.bind(provider='sqlite', filename='database.sqlite', create_db=True)
orm.set_sql_debug(SQL_DEBUG)