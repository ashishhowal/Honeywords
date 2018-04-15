import json
from os import path, remove
from Crypto.Cipher import AES
from Crypto import Random
import hashlib

from logger import *

# Everything received here is )
class AuxIO:
    def __init__(self, config):
        self.config = config
        # Crypto.
        if not path.exists(config['crypto']['db_file']):
            self._initDatabase()


    # Decrypt Database and return it as a dictionary object from a json object
    def _secureOpen(self):
        crypto = self.config['crypto']
        db = open(crypto['db_file'],'rb').read()
        crypt = AES.new(hashlib.sha256(crypto['key']).digest(), AES.MODE_CBC, IV=db[:AES.block_size])
        plain = crypt.decrypt(db[AES.block_size:])
        # Remove padded spaces
        plain = plain.rstrip()
        dlog(plain)
        return json.loads(plain)

    # Send in data as string
    def _secureClose(self, data):
        crypto = self.config['crypto']
        data = str(data)
        IV = Random.new().read(AES.block_size)
        crypt = AES.new(hashlib.sha256(crypto['key']).digest(), AES.MODE_CBC, IV=IV)
        # Padding for the encryption
        while len(data) % 16 != 0:
            data += ' '

        cipher_text = crypt.encrypt(data)
        with open(crypto['db_file'], 'wb') as f:
            f.write(IV + cipher_text)
        return

    # Initialize database if not exists
    def _initDatabase(self):
        empty = """[]"""
        self._secureClose(empty)
        return

    # Add a row to the database
    def add(self, data):
        dict_db = self._secureOpen()
        dict_db.append(data)
        json_db = json.dumps(dict_db)
        dlog(json_db)
        self._secureClose(str(json_db))
        return

    # Get a specific row from the database. Returns the entire tuple
    def get(self, uid):
        db = self._secureOpen()
        for d in db:
            if int(d['uid']) == uid:
                return d
        return False

    # Removing involves making a whole new database. I know :/.
    def remove(self, uid):
        # Logic to remove a tuple
        db = self._secureOpen()
        new_db = [d for d in db if d['uid'] != uid]
        if len(db) == len(new_db):
            return False
        else:
            j_db = json.dumps(new_db)
            self._secureClose(str(j_db))
            return True

    # For debug purposes only.
    def _dropdatabase(self):
        remove(self.config['crypto']['db_file'])
        return 

if __name__ == '__main__':
    if _DEBUG is True:
        conf = open('config.json', 'r').read()
        conf = json.loads(conf)
        aio = AuxIO(conf)