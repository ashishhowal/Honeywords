'''
The purpose of this class is to perform all things related to decoy passwords.
'''
import json

from DBDriver import *

class Honeywords:
    def __init__(self, app, configFile):
        self.app = app
        self.config = json.loads(configFile.read())
        mysql_config = self.config['mysql']
        self.db_driver = DBDriver(app, mysql_config['host'], mysql_config['user'], mysql_config['pass'], mysql_config['db'])

        # add functionality for aux server
        return
    
    def addUser(self):
        # Add user with decoy passwords
        return

    def validateUser(self):
        # Check with auxiliary server if the user password is correct.
        return

    def _checkConnection(self):
        # Check connection with Auxiliary server
        return

    