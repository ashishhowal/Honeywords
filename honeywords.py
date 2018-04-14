'''
The purpose of this class is to perform all things related to decoy passwords.
'''
import json
import random

from DBDriver import *
from auxClient import *

class Honeywords:
    def __init__(self, app, configFile):
        self.app = app
        self.config = json.loads(configFile.read())
        mysql_config = self.config['mysql']
        self.db_driver = DBDriver(app, mysql_config['host'], mysql_config['user'], mysql_config['pass'], mysql_config['db'])

        # functionality for aux server
        aux_config = self.config['aux']
        self.aux_client = AuxClient(aux_config['host'], aux_config['pass'])
        return
    
    # Retrieves a random password from the given dictionary
    def _generateDecoy(self, config):
        # Load Configurations and the Dictionary
        pass_list = open(config['dictionary'], 'r')
        dict_len = int(config['dict_length'])

        # Seek to random location in dictionary file and give that password
        seek = random.randint(1,dict_len)
        # Get random offset from chosen location
        offset = random.randint(1,20)
        pass_list.seek(seek)
        pass_list.next()
        for i in range(0,offset - 1):
            pass_list.next()
        decoy = pass_list.next()

        # Remove the linefeed at the end and return
        return decoy.replace('\n','')

    # Add user with decoy passwords
    def addUser(self, password):
        # Generate fake passwords list
        pass_list = []
        honey_config = self.config['honeywords']
        for i in range(0, int(honey_config['decoy_count']) + 1):
            pass_list.append(self._generateDecoy(honey_config))

        # At random position in the list, add the real password
        position = random.randint(0,int(honey_config['decoy_count']) + 1)
        pass_list[position] = password

        # Perform database operations
        

        return

    def validateUser(self):
        # Check with auxiliary server if the user password is correct.
        return

    def _checkConnection(self):
        # Check connection with Auxiliary server
        return

