import socket 
from thread import start_new_thread, allocate_lock

from auxIO import *
from logger import *

class AuxServer:
    def __init__(self, config):
        # Socket configurations
        self.server_socket = socket.socket()
        self.config = config
        self.server_socket.bind((config['server']['host'],config['server']['port']))

        # Server protocol messages
        self.hello_message = """HELLO"""
        self.put_message = """PUT"""
        self.get_message = """GET"""
        self.delete_message = """DELETE"""

        # File IO primitives
        self.aux_io = AuxIO(config)

        # Database concurrency measures
        self.db_lock = allocate_lock()

    # Dispatch method for the three defined methods
    def handle(self, conn):
        # Write logic to handle request
        conn.send(self.hello_message)
        req = conn.recv(1024)
        dlog(req)
        req = json.loads(req)
        # Everything this point on is dictionary

        if req['method'] == self.put_message:
            start_new_thread(self.handle_put, (req, conn, ))
        elif req['method'] == self.get_message:
            start_new_thread(self.handle_get, (req, conn, ))
        elif req['method'] == self.delete_message:
            start_new_thread(self.handle_delete, (req, conn, ))

        return

    # PUT Handler
    def handle_put(self, d_req, conn):
        # Put logic
        data = {
            'uid':d_req['uid'],
            'pid':d_req['pid']
        }

        self.db_lock.acquire()
        self.aux_io.add(data)
        self.db_lock.release()

        response = {'status':'OK'}
        conn.send(json.dumps(response))
        return

    # GET Handler
    def handle_get(self, d_req, conn):
        # Get Logic
        uid = d_req['uid']

        self.db_lock.acquire()
        res = self.aux_io.get(uid)
        self.db_lock.release()

        if res is not False:
            response = {'status':'OK','pid':res['pid']}
            conn.send(json.dumps(response))
        else:
            conn.send(json.dumps({'status':'FAIL'}))
        return

    def handle_delete(self, d_req, conn):
        uid = d_req['uid']

        self.db_lock.acquire()
        res = self.aux_io.remove(uid)
        self.db_lock.release()

        if res is not False:
            response = {'status':'OK'}
            conn.send(json.dumps(response))
        else:
            conn.send(json.dumps({'status':'FAIL'}))
        return

    # Start server.
    def serve_forever(self):
        self.server_socket.listen(5)        
        while True:
            try:
                conn, addr = self.server_socket.accept()
            except Exception as e:
                raise e
            self.handle(conn)
