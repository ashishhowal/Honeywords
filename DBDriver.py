'''
Driver class for all MySQL queries. This has to be used by any class wanting to operate on the database.
'''

from flask_mysqldb import MySQL

class DBDriver:
    def __init__(self, app, host, user, passwd, db):
        self.app = app
        app.config['MYSQL_HOST'] = host
        app.config['MYSQL_USER'] = user
        app.config['MYSQL_PASSWORD'] = passwd
        app.config['MYSQL_DB'] = db
        self.db = MySQL(app)

    def _exec(self, query):
        cursor = self.db.connection.cursor()
        return (cursor, cursor.execute(query))

    def create(self):
        return

    def insert(self):
        return

    def read(self):
        return