import json
from os import path
from Crypto.Cipher import AES
import hashlib

class AuxIO:
    def __init__(self, config):
        self.config = config
        # Crypto.
        # Note that i am directly loading the key into the object and not saving it to a variable.
        self.IV = "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
        self.crypt = AES.new(hashlib.sha256(config['crypto']['key']).digest(), AES.MODE_CBC, IV=self.IV)
        if not path.exists(config['crypto']['db_file']):
            self._initDatabase()


    # Decrypt Database and return it as a dictionary object from a json object
    def _secureOpen(self):
        crypto = self.config['crypto']
        db = open(crypto['db_file'],'rb').read()
        plain = self.crypt.decrypt(db)
        # Remove padded spaces
        plain = plain.rstrip()
        return json.loads(plain)

    # Send in data as string
    def _secureClose(self, data):
        crypto = self.config['crypto']
        data = str(data)
        # Padding for the encryption
        while len(data) % 16 != 0:
            data += ' '

        cipher_text = self.crypt.encrypt(data)
        with open(crypto['db_file'], 'wb') as f:
            f.write(cipher_text)
        return

    # Initialize database if not exists
    def _initDatabase(self):
        empty = """[]"""
        self._secureClose(empty)
        return

    # Add a row to the database
    def add(self, data):
        json_db = self._secureOpen()
        dict_db = json.loads(json_db)
        dict_db.append(data)
        json_db = json.dumps(dict_db)
        _secureClose(str(json_db))
        return

    # Get a specific row from the database. Returns the entire tuple
    def get(self, uid):
        json_db = self._secureOpen()
        dict_db = json.loads(json_db)

        for d in db:
            if int(d['uid']) == uid:
                return d

        return False