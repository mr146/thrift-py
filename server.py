#!/usr/bin/env python

import sys, glob
import urllib
sys.path.append('gen-py')
from HTMLParser import HTMLParser

from getnodes import GetNodes
from getnodes.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

class LinksCollector(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.refs = []

	def handle_starttag(self, tag, attrs):
		if tag == 'a':
			for attr in attrs:
				if attr[0] == 'href':
					self.refs.append(attr[1])

	def get_refs(self):
		return self.refs

def getNode(url, default = ""):
	if url.startswith("http"):
		spl = url.split('/')
		return spl[2]
	return default

class GetNodesHandler:
	def getNodes(self, url):
		selfNode = getNode(url)
		connection = urllib.urlopen(url)
		encoding = connection.headers.getparam('charset')
		collector = LinksCollector()
		root = collector.feed(connection.read().decode(encoding))
		refs = collector.get_refs()
		result = []
		for ref in refs:
			node = getNode(ref, selfNode)
			if node != selfNode:
				result.append(node)
		return result

handler = GetNodesHandler()
processor = GetNodes.Processor(handler)
transport = TSocket.TServerSocket(port=9090)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
server.serve()