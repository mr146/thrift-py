#!/usr/bin/env python

import sys, glob
sys.path.append('gen-py')

from getnodes import GetNodes
from getnodes.ttypes import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from collections import defaultdict

try:
	transport = TSocket.TSocket('localhost', 9090)
	transport = TTransport.TBufferedTransport(transport)
	protocol = TBinaryProtocol.TBinaryProtocol(transport)
	client = GetNodes.Client(protocol)
	transport.open()
	f = open('urls')

	results = defaultdict(int)
	for url in f:
		nodes = client.getNodes(url)
		for node in nodes:
			results[node] += 1

	vmax = 0
	ans = ''
	for k, v in results.iteritems():
		if v > vmax:
			vmax = v
			ans = k

	print ans
	transport.close()
except Thrift.TException, tx:
	print(tx.message)