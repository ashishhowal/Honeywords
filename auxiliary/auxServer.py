import socket 
from thread import start_thread, allocate_lock

from auxIO import *

class AuxServer:
    def __init__(self, config):
        # Socket configurations
        self.server_socket = socket.socket()
        self.config = config
        self.server_socket.bind((self.host,self.port))

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
        req = json.loads(req)

        if req['method'] == self.put_message:
            thread.start_thread(target = self.handle_put, (req, conn, ))
        elif req['method'] == self.get_message:
            thread.start_thread(target = self.handle_get, (req, conn, ))
        elif req['delete'] == self.delete_message:
            thread.start_thread(target = self.handle_delete, (req, conn, ))

        return

    # PUT Handler
    def handle_put(self, req, conn):
        # Put logic
        dict_req = json.loads(req)
        data = {
            'uid':data['uid'],
            'pid':data['pid']
        }

        lock.acquire()
        self.aux_io.add(data)
        lock.release()

        response = {'status':'OK'}
        conn.send(json.dumps(response))
        return

    # GET Handler
    def handle_get(self, req, conn):
        # Get Logic
        dict_req = json.loads(req)
        uid = data['uid']

        lock.acquire()
        res = self.aux_io.get(uid)
        lock.release()

        if res is not False:
            response = {'status':'OK','pid':res['pid']}
            conn.send(json.dumps(response))
        conn.send(json.dumps({'status':'FAIL'}))
        return

    def handle_delete(self, req, conn):
        # delete logic
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
