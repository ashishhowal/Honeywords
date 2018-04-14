'''
Auxiliary server client.
This class will handle communication with the aux server.
Protocol defined is like so:
    - PUT
        PUTs data into the auxiliary database
    - GET 
        GETs data from the auxiliary database
    - DELETE
        DELETEs data from the auxiliary database
'''
import socket

class AuxClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.PUT = 'PUT'
        self.GET = 'GET'
        self.DELETE = 'DELETE'

    def _initSocket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        greet = sock.recv()
        if greet is 'hello':
            return (True, sock)
        else:
            return (False, None)

    def _send(self, data):
        status, sock = self._initSocket()
        if status == True:
            sock.send(data)
            response = sock.recv(1024)
            return response

    def put(self, uid, pid):
        data = {
            'method':self.PUT,
            'user_id':uid,
            'pass_id':pid
        }
        data = json.loads(data)
        self._send(data)
        return

    def get(self, uid):
        data = {
            'method':self.GET,
            'user_id':uid
        }
        data = json.loads(data)
        resp = self._send(data)
        resp = json.dumps(resp)
        # some logic
        return

    def delete(self, uid):
        data = {
            'method':self.DELETE,
            'user_id':uid
        }
        data = json.loads(data)
        self._send(data)
        return