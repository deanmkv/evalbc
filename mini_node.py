import socket, time, bitcoin
from bitcoin.messages import msg_version, msg_verack, msg_addr, MsgSerializable, msg_getaddr, msg_pong, msg_ping
from bitcoin.net import CAddress


PORT = 8333

bitcoin.SelectParams('mainnet') 

class Wrapper(object):
	def __init__(self, a_socket):
		self.socks = a_socket

	def read(self, n):
		return self.socks.recv(n, socket.MSG_WAITALL)

def version_pkt(client_ip, server_ip):
    msg = msg_version()
    msg.nVersion = 70002
    msg.addrTo.ip = server_ip
    msg.addrTo.port = PORT
    msg.addrFrom.ip = client_ip
    msg.addrFrom.port = PORT

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

#BytesIO.tell() returns the current position in the buffer. could use this to append to buffer
def processMessage():
	# bytes_obj = s.recv(8192)
	# print("read %d bytes" % len(bytes_obj))
	# msg = MsgSerializable.stream_deserialize(io.BytesIO(bytes_obj))
	msg = MsgSerializable.stream_deserialize(Wrapper(s))
	if msg.command == b"version":
	    # Send Verack
	    print('sending my verack')
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
	elif msg.command == b"addr":
		print("addr: ")
		for address in msg.addrs:
			print(address.ip)
	else:
	    print("something else: ", msg.command, msg)

server_ip = "75.132.169.13"
# client_ip = "67.172.198.9"
client_ip = "1.1.1.1"

s = socket.socket()
s.bind(('',8333))
s.connect( (server_ip,PORT) )






# Get Version reply
# temp = s.recv(1924)
# print(type(temp))
import io

# Send Version packet
s.send( version_pkt(client_ip, server_ip).to_bytes() )
processMessage()  # one for getting verack
processMessage()  # one for sending version
s.send(msg_getaddr().to_bytes())
processMessage()
processMessage()
processMessage()
processMessage()
processMessage()
# processMessage()

# Get Verack
# print(s.recv(1024))
# msg = msg_verack.msg_deser(io.BytesIO(s.recv(1924)))
# print (msg)

# Send Addrs
# s.send( addr_pkt(["252.11.1.2", "EEEE:7777:8888:AAAA::1"]).to_bytes() )

time.sleep(1)
s.close()

# tcpkill -i wlan0 port 8333