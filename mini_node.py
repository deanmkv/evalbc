import socket, time, bitcoin
from bitcoin.messages import msg_version, msg_verack, msg_addr, MsgSerializable, msg_getaddr, msg_pong, msg_ping
from bitcoin.net import CAddress
from linked_list import Linked_List, Link


# TODO this new implementation needs testing, and maybe debug statements to verify code works

class Wrapper(object):
	def __init__(self, a_socket):
		self.socks = a_socket

	def read(self, n):
		return self.socks.recv(n, socket.MSG_WAITALL)


class BitcoinSocket(object):  # TODO could add better debug statements
	client_ip = "1.1.1.1"  # TODO This value doesn't seem to matter, but we should make sure or use your IP address
							# or best case write code to find your public facing IP address
	_port_num = 8000

	def get_port():  # NOTE: this is not an instance method
		"""In the future this will allow a good way to support parallelization"""
		BitcoinSocket._port_num += 1
		return BitcoinSocket._port_num

	def __init__(self, link, timeout=10):
		"""Creates a socket and binds it to a free, unique port"""
		self.link = link
		self.results = Linked_List()
		self.my_socket = socket.socket()
		# bind socket to free port
		while True:
			self.port = BitcoinSocket.get_port()  # autoimcrement
			try:
				self.my_socket.bind(('',self.port)) 
				break;
			except OSError:  # if port is not free
				pass
		self.my_socket.settimeout(timeout)

	def connect(self):
		"""Connect to the destination, returning True on success"""
		try:
			self.my_socket.connect( (self.link.ip,self.link.port) )  # TODO test: add support for IP addresses that are offline
		except socket.timeout:
			return False
		return True

	def listen_until_addresses(self):
		"""Implements the Bitcoin protocol, sending info until it gets an addr message"""
		# Send Version packet
		self.my_socket.send( self._make_version_pkt().to_bytes() )

		# Try to get addresses
		self.my_socket.send(msg_getaddr().to_bytes())

		while not self._process_message():  # TODO set timeout or something for multiple addr messages
			pass
		self.my_socket.close()

	def get_results(self):
		"""Returns a linked list of all new potential nodes (needs pruning)."""
		return self.results

	def _make_version_pkt(self):
	    msg = msg_version()
	    msg.nVersion = 70002
	    msg.addrTo.ip = self.link.ip
	    msg.addrTo.port = self.link.port
	    msg.addrFrom.ip = BitcoinSocket.client_ip
	    msg.addrFrom.port = self.port
	    return msg

	# ...we don't need to tell people who we know about :)
	# def _make_addr_pkt(self, str_addrs ):
	#     msg = msg_addr()
	#     addrs = []
	#     for i in str_addrs:
	#         addr = CAddress()
	#         addr.port = 8333
	#         addr.nTime = int(time.time())
	#         addr.ip = i

	#         addrs.append( addr )
	#     msg.addrs = addrs
	#     return msg

	def _process_message(self):
		msg = MsgSerializable.stream_deserialize(Wrapper(s))

		if msg.command == b"version":  # TODO conglomerate these message strings into a dictionary
		    # Send Verack
		    print('version: ', msg.strSubVer, msg.nVersion)
		    s.send( msg_verack().to_bytes() )

		elif msg.command == b"verack":
		    print("verack: ", msg)

		elif msg.command == b"inv":
			print("inv: ", msg.inv)

		elif msg.command == b"ping":
			print("ping: ", msg)
			s.send(msg_pong(msg.nonce).to_bytes())

		elif msg.command == b"getheaders":
			print("getheaders received ")

		elif msg.command == b"addr":  # TODO this needs multi-message support
			print("addr: size ", len(msg.addrs))
			for address in msg.addrs:
				node = Link(address.ip, address.port)
				self.results.add(node)
			return True
		else:
		    print("something else: ", msg.command, msg)

		return False


bitcoin.SelectParams('mainnet') 
linked = Linked_List()  # of potential nodes
known_set = set()  # docs imply this is a hashset.  good nodes
known_bad = set()  # offline nodes
version_strings = {}  # string : count


# server_ip = "75.132.169.13"
# server_ip = "199.233.246.224"
server_ip = "94.112.102.36"
# server_ip = "95.191.251.158"
# server_ip = "188.230.153.108"
# server_ip = "186.159.101.96"
# server_ip = "76.170.160.69"
# server_ip = "70.15.155.219"
# server_ip = "81.64.219.50"
# server_ip = "73.20.98.44"

linked.add(Link(server_ip, 8333))

while linked.has_next():
	link = linked.pop()
	print('\nTarget: ', link.ip,':',link.port)

	bs = BitcoinSocket(link)
	if not bs.connect():
		continue
	bs.listen_until_addresses()
	linked.add_linked_list( bs.get_results() )  # TODO these results need to be pruned
	
