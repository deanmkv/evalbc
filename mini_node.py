import socket, time, bitcoin
from bitcoin.messages import msg_version, msg_verack, msg_addr, MsgSerializable, msg_getaddr, msg_pong, msg_ping, msg_inv, msg_tx
from bitcoin.net import CAddress, CInv
from linked_list import Linked_List, Link



# TODO maybe debug statements to better understand what is happening

class Wrapper(object):
	def __init__(self, a_socket):
		self.socks = a_socket

	# TODO: consider changing this to handle mid-connection drop outs
	def read(self, n):
		# this shouldn't have to be a bug fix
		li = []
		total = 0
		while total < n:
			bytes_obj = self.socks.recv(n - total, socket.MSG_WAITALL) 
			li.append( bytes_obj )
			total += len(bytes_obj)
		return b''.join(li)
		# could have used bytes_obj += self.socks.recv(...), but that is n^2 time
		# return self.socks.recv(n, socket.MSG_WAITALL)


class BitcoinSocket(object):
	client_ip = "1.1.1.1"  # TODO This value doesn't seem to matter, but we should make sure or use your IP address
							# or best case write code to find your public facing IP address
	_port_num = 8000		# also, this port is the LAN port, not internet port, so the same issue is here

	def get_port():  # NOTE: this is not an instance method
		"""In the future this will allow a good way to support parallelization"""
		BitcoinSocket._port_num += 1
		return BitcoinSocket._port_num

	def __init__(self, link, timeout=10):
		"""Creates a socket and binds it to a free, unique port"""
		self.link = link
		self.results = Linked_List()
		self.my_socket = socket.socket()
		self.conn_ref = False
		# bind socket to free port
		ref_count = 0
		while True:
			self.port = BitcoinSocket.get_port()  # autoimcrement
			try:
				self.my_socket.bind(('',self.port)) 
				break;
			except OSError:  # if port is not free
				pass
				# print("os error")
			except ConnectionRefusedError:
				ref_count += 1
				if ref_count > 3:
					self.conn_ref = True
					break;
				print("conn refused, trying again")

		self.my_socket.settimeout(timeout)

	def connect(self):
		"""Connect to the destination, returning True on success"""
		try:
			self.my_socket.connect( (self.link.ip,self.link.port) )
		except socket.timeout:
			return False
		return True

	def listen_until_acked(self):
		# Send Version packet
		self.my_socket.send( self._make_version_pkt().to_bytes() )
		ver_rec = False
		verack_rec = False
		while not verack_rec and not ver_rec:
			res = self._process_message()
			if res == "version":
				ver_rec = True
			elif res == "verack":
				verack_rec = True 

	def send_transaction(self):
		import createTransaction
		tx = createTransaction.make_self_transaction()
		inv_msg = msg_inv()
		tx_inv = CInv() 
		tx_inv.type = 1
		tx_inv.hash = tx.GetHash()
		inv_msg.inv.append(tx_inv)
		self.my_socket.send(inv_msg.to_bytes())
		while self._process_message(transaction=tx) != "donedone":
			pass
		print("leaving send_transaction()")
		return tx_inv.hash

	def listen_until_addresses(self):
		"""Implements the Bitcoin protocol, sending info until it gets an addr message"""
		

		# Try to get addresses
		self.my_socket.send(msg_getaddr().to_bytes())

		while not self._process_message():  # TODO set timeout or something for multiple addr messages
			pass
		self.my_socket.close()

	def listen_forever(self):
		print("starting to listen forever")
		while True:
			self._process_message()

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

	def _process_message(self, **kwargs):
		msg = MsgSerializable.stream_deserialize(Wrapper(self.my_socket))

		if msg.command == b"version":  # TODO conglomerate these message strings into a dictionary
		    # Send Verack
		    print('version: ', msg.strSubVer, msg.nVersion)
		    self.my_socket.send( msg_verack().to_bytes() )
		    return "version"
		elif msg.command == b"verack":
		    print("verack: ", msg)
		    return "verack"
		elif msg.command == b"inv":
			print("inv: ", msg.inv)
			# print(dir(msg))
			# print(type(msg.inv))
		elif msg.command == b"ping":
			print("ping: ", msg)
			self.my_socket.send(msg_pong(msg.nonce).to_bytes())

		elif msg.command == b"getheaders":
			print("getheaders received ")

		elif msg.command == b"addr":  # TODO this needs multi-message support
			print("addr: size ", len(msg.addrs))
			for address in msg.addrs:
				node = Link(address.ip, address.port)
				self.results.add(node)
			return True
		elif msg.command == b"getdata":
			print("getdata: ", msg.inv)
			if 'transaction' not in kwargs:
				return False
			the_tx =  kwargs['transaction']
			for request in msg.inv:
				if request.hash == the_tx.GetHash():
					# new message to send transaction
					to_send = msg_tx()
					to_send.tx = the_tx
					self.my_socket.send(to_send.to_bytes())
					print("SENT OUR PC BRO TRANSACTION")
					return "donedone"
		else:
		    print("something else: ", msg.command, msg)

		return False

if __name__ == "__main__":

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
	server_ip = "67.172.198.9"
	# blockcypher ip address but we don't knowthe port so we can't connect
	# server_ip = "54.166.212.28"

	# linked.add(Link(server_ip, 8333))

	import sys
	if linked.has_next():
		for link in ip4list:
			print('\nTarget: ', link.ip,':',link.port)

			bs = BitcoinSocket(link)
			if bs.conn_ref or not bs.connect():
				sys.exit(0)
			# bs.listen_until_addresses()
			# linked.add_linked_list( bs.get_results() )  # TODO these results need to be pruned
			bs.listen_until_acked()
			bs.send_transaction()
			bs.listen_forever()

		print("done")

