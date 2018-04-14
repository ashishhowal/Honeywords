import socket 
from thread import start_thread, allocate_lock

from auxIO import *

class AuxServer:
    def __init__(self, host, port, config):
        # Socket configurations
        self.host = host
        self.port = port
        self.server_socket = socket.socket()
        self.config = config
        self.server_socket.bind((self.host,self.port))

        # Server protocol messages
        self.hello_message = """HELLO"""
        self.put_message = """PUT"""
        self.get_message = """GET"""
        self.delete_message = """DELETE"""

        # Database concurrency measures
        self.db_lock = allocate_lock()

    # Dispatch method for the three defined methods
    def handle(self, conn):
        # Write logic to handle request
        conn.send(self.hello_message)
        req = conn.recv(1024)
        req = json.loads(req)

        if req['method'] == self.put_message:
            thread.start_thread(target = self.handle_put, (req, ))
        elif req['method'] == self.get_message:
            thread.start_thread(target = self.handle_get, (req, ))
        elif req['delete'] == self.delete_message:
            thread.start_thread(target = self.handle_delete, (req, ))

        return

    # PUT Handler
    def handle_put(self, req):
        # Put logic
        return

    # GET Handler
    def handle_get(self, req):
        # Get Logic
        return

    def handle_delete(self, req):
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


if __name__ == '__main__':
    print "Starting Auxiliary Server."