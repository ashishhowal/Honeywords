#!/usr/bin/env python

import json

from auxServer import *

print "Starting Auxiliary Server."
conf = open('config.json', 'r').read()
server = AuxServer(json.loads(conf))

server.serve_forever()