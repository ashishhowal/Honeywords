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
import json

from logger import _DEBUG, dlog

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
        greet = sock.recv(1024)
        dlog(greet)
        if greet == 'HELLO':
            return (True, sock)
        else:
            return (False, None)

    def _send(self, data, sock):
        dlog(data)
        data = str(data)
        sock.send(data)
        response = sock.recv(1024)
        return (sock, response)

    def put(self, uid, pid):
        status, sock = self._initSocket()
        dlog(status)
        dlog(sock)
        if status is True:
            data = {
                'method':self.PUT,
                'uid':uid,
                'pid':int(pid)
            }
            data = json.dumps(data)
            sock, resp = self._send(data, sock)
            d_resp = json.loads(resp)
            sock.close()
            if d_resp['status'] == "OK":
                return True
            elif d_resp['status'] == "FAIL":
                return False

    def get(self, uid):
        status, sock = self._initSocket()
        if status is True:
            data = {
                'method':self.GET,
                'uid':int(uid)
            }
            data = json.dumps(data)
            sock, resp = self._send(data, sock)
            d_resp = json.loads(resp)
            sock.close()
            if d_resp['status'] == "OK":
                return d_resp['pid']
            elif d_resp['status'] == "FAIL":
                return False

    def delete(self, uid):
        status, sock = self._initSocket()
        if status is True:
            data = {
                'method':self.DELETE,
                'uid':int(uid)
            }
            data = json.dumps(data)
            sock, resp = self._send(data, sock)
            d_resp = json.loads(resp)
            sock.close()
            if d_resp['status'] == "OK":
                return True
            elif d_resp['status'] == "FAIL":
                return False

if __name__ == '__main__':
    if _DEBUG is True:
        aux_cl = AuxClient('localhost',7812)