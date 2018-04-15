#!/usr/bin/env python

import json
import traceback

from auxServer import *

print "Starting Auxiliary Server."
conf = open('config.json', 'r').read()

server = AuxServer(json.loads(conf))

try:
    server.serve_forever()
except Exception as e:
    traceback.print_exc()
    print e