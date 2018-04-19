'''
The purpose of this class is to perform all things related to decoy passwords.
'''
import json
import random

from DBDriver import *
from auxClient import *
from logger import *

class Honeywords:
    def __init__(self, app, configFile):
        self.app = app
        self.config = json.loads(configFile.read())
        mysql_config = self.config['mysql']
        self.db_driver = DBDriver(app, mysql_config['host'], mysql_config['user'], mysql_config['pass'], mysql_config['db'])

        # functionality for aux server
        aux_config = self.config['aux']
        self.aux_client = AuxClient(aux_config['host'], aux_config['port'])
        
        # Primitives for user validation
        self.attack_message = """ATTACK"""
        self.success_message = """SUCCESS"""
        self.fail_message ="""FAIL"""
    
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
    def addUser(self, username, password):
        # Generate fake passwords list
        pass_list = []
        honey_config = self.config['honeywords']
        for i in range(0, int(honey_config['decoy_count']) + 1):
            pass_list.append(self._generateDecoy(honey_config))

        # At random position in the list, add the real password
        position = random.randint(0, int(honey_config['decoy_count']))
        dlog(pass_list)
        dlog(position)
        pass_list[position] = password
        dlog(pass_list)

        # Perform database operations
        # First insert into 'users' table, then use the alloted user_id to insert into 'passwords' table
        db_config = self.config['database']
        self.db_driver.insert(db_config['user_table'], {'user_name':username})
        uid = self.db_driver.getUserID(username)

        # Write logic to insert into password table.
        for pwd in pass_list:
            self.db_driver.insert(db_config['pass_table'], {'uid':uid, 'password':pwd})

        # Aux insertion here.
        base_pid = self.db_driver.getUserBasePid(uid)
        dlog("base_pid: "+ str(base_pid))
        dlog("Pass Pos: " + str(base_pid + position))
        status = self.aux_client.put(int(uid), int(base_pid + position))
        if status is True:
            return True
        return False

    # Query the database for uid based on user_name
    # Query the database for pid based on password
    # Query the Auxiliary server for real pid
    # Check and return
    def validateUser(self, user_name, password):
        # Check with auxiliary server if the user password is correct.
        uid = self.db_driver.getUserID(user_name)
        # If no such user exists
        if uid is False:
            return self.fail_message
        dlog("UID: " + str(uid))
        pid = self.db_driver.getPassID(uid, password)

        # If password is not in the database, it is a failed login attempt due to incorrect password
        if pid is False:
            return self.fail_message
        
        # We are certain that the password exists, now if the aux_pid does not match the real pid, this is an attacker.
        else:
            # If password exists, check it's ID with the ID retrieved from auxiliary server
            aux_pid = self.aux_client.get(uid)

            # Legitimate login attempt.
            if pid == aux_pid:
                return self.success_message
            # Attacker's attempt
            else: 
                return self.attack_message

        # Should never reach here. But good practices and shiz.
        return False