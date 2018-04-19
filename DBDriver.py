'''
Driver class for all MySQL queries. This has to be used by any class wanting to operate on the database.
'''

from flask_mysqldb import MySQL

from logger import *

class DBDriver:
    def __init__(self, app, host, user, passwd, db):
        self.app = app
        app.config['MYSQL_HOST'] = host
        app.config['MYSQL_USER'] = user
        app.config['MYSQL_PASSWORD'] = passwd
        app.config['MYSQL_DB'] = db
        self.db = MySQL(app)

    # Returns the cursor and size of resultset
    def _exec(self, query):
        cursor = self.db.connection.cursor()
        res = cursor.execute(query)
        self.db.connection.commit()
        return (cursor, res)

    # Insert will take arguement a 'row', which will have user_name, password
    # Row will be a key value pair, key being attribute name and value being the value
    def insert(self, table, row):
        # Construct insert set
        ins_vec = """("""
        for r in row:
            ins_vec += r + ""","""

        ins_vec = ins_vec[:len(ins_vec)-1]
        ins_vec += """)"""

        ins = ins_vec[1:]
        ins = ins[:len(ins)-1]
        ins = ins.split(',')
        
        values = """('"""
        for i in range(0,len(row)):
            values += str(row[ins[i]])
            if len(row) - i != 1:
                values += """','"""
        values += """')"""

        # Construct query and execute
        query = """INSERT INTO """ + table + """ """ + ins_vec + """ VALUES"""+ values
        cur, res = self._exec(query)

        # Retrieve the last user_id
        return res
        
    def getUserBasePid(self, uid):
        query = """SELECT pid FROM passwords WHERE uid=""" + str(uid) + """ ORDER BY pid ASC LIMIT 1;""" 
        cur, res = self._exec(query)
        if res:
            base_pid = cur.fetchall()[0][0]
            return base_pid
        return False

    # Return the resultset as a list
    # Use this method to retrieve a list of passwords with the same user_id from the password table
    def _project(self, table, condition = 1):
        query = """SELECT * FROM """ + table + """ WHERE """ + condition
        dlog(query)
        cur, res = self._exec(query)

        if res != 0:
            resultset = cur.fetchall()
            return resultset
        else:
            return False

    def getUserID(self, user_name):
        table = 'users'
        condition = """user_name = '""" + str(user_name) + """'"""
        result = self._project(table, condition)
        dlog(result)
        if result is not False:
            return result[0][0]
        else:
            return False

    def getPassID(self, uid, password):
        table = 'passwords'
        condition = """uid=""" + str(uid) + """ AND password='""" + str(password) + """'"""
        result = self._project(table, condition)
        dlog(result)
        if result is not False:
            return result[0][0]
        else:
            return False