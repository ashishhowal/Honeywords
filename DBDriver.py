from flask_mysqldb import MySQL

class DBDriver:
    def __init__(self, app, host, user, passwd, db):
        self.APP = app
        app.config['MYSQL_HOST'] = host
        app.config['MYSQL_USER'] = user
        app.config['MYSQL_PASSWORD'] = passwd
        app.config['MYSQL_DB'] = db
        self.DB = MySQL(app)

    def _exec(self, query):
        cursor = self.DB.connection.cursor()
        return (cursor, cursor.execute(query))

