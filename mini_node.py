import socket, time, bitcoin
from bitcoin.messages import msg_version, msg_verack, msg_addr, MsgSerializable, msg_getaddr, msg_pong, msg_ping
from bitcoin.net import CAddress
from linked_list import Linked_List, Link

MY_PORT = 8333

bitcoin.SelectParams('mainnet') 
linked = Linked_List()
known_set = set()  # docs imply this is a hashset
known_bad = set()

class Wrapper(object):
	def __init__(self, a_socket):
		self.socks = a_socket

	def read(self, n):
		return self.socks.recv(n, socket.MSG_WAITALL)

def version_pkt(client_ip, link_obj):
    msg = msg_version()
    msg.nVersion = 70002
    msg.addrTo.ip = link_obj.ip
    msg.addrTo.port = link_obj.port
    msg.addrFrom.ip = client_ip
    msg.addrFrom.port = MY_PORT

    return msg

def addr_pkt( str_addrs ):
    msg = msg_addr()
    addrs = []
    for i in str_addrs:
        addr = CAddress()
        addr.port = 8333
        addr.nTime = int(time.time())
        addr.ip = i

        addrs.append( addr )
    msg.addrs = addrs
    return msg

def processMessage():
	msg = MsgSerializable.stream_deserialize(Wrapper(s))
	if msg.command == b"version":
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
	elif msg.command == b"addr":							# <-- Here
		print("addr: size ", len(msg.addrs))
		for address in msg.addrs:
			node = Link(address.ip, address.port)
			linked.add(node)
		return True
	else:
	    print("something else: ", msg.command, msg)

	return False

def bind_to_port(s):
	global MY_PORT
	while True:
		try:
			s.bind(('',MY_PORT))  # autoimcrement
			break;
		except OSError:
			MY_PORT += 1

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
# client_ip = "67.172.198.9"

client_ip = "1.1.1.1"  #seems to serve no purpose

linked.add(Link(server_ip, 8333))
# for each thing in linked list
while linked.has_next():
	link = linked.pop()
	print('\nTarget: ', link.ip,':',link.port)

	s = socket.socket()
	bind_to_port(s)
	s.connect( (link.ip,link.port) )  # TODO add support for IP addresses that are offline

	# Send Version packet
	s.send( version_pkt(client_ip, link).to_bytes() )

	# Try to get addresses
	s.send(msg_getaddr().to_bytes())
	while not processMessage():  # TODO set timeout or something for multiple addr messages
		pass
	print("Known set: ", len(known_set), "\nLinked list: ", len(linked))
	s.close()



# Send Addrs
# s.send( addr_pkt(["252.11.1.2", "EEEE:7777:8888:AAAA::1"]).to_bytes() )

# tcpkill -i wlan0 port 8333