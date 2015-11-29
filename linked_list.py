class Linked_List(object):
	def __init__(self):
		self.start = None
		self.end = None
		self.length = 0

	def add(self, link):
		self.length += 1
		if self.start is None:
			self.start = link
			self.end = link
			return
		self.end.set_next(link)
		self.end = link

	def add_linked_list(self, linked):
		"""Destructive on other linked list (by design)"""
		if self.start is None:
			self.start = linked.start
			self.end = linked.end
			self.length = linked.length
			return
		self.end.set_next(linked.start)
		self.end = linked.end
		self.length += linked.length
		linked.clear()

	def pop(self):
		if self.start is None:
			raise IndexError
		toRet = self.start
		self.start = self.start.next
		self.length -= 1
		return toRet

	def has_next(self):
		return self.start is not None

	def clear(self):  # relying on the garbage collector
		self.start = None
		self.end = None
		self.length = 0

	def __str__(self):
		ret = ''
		cur_node = self.start
		while cur_node is not None:
			ret +=  str(cur_node) +' -> '
			cur_node = cur_node.next
		return ret

	def __len__(self):
		return self.length

class Link(object):
	def __init__(self, ip, port):
		self.next = None
		self.ip = ip
		self.port = port

	def set_next(self, other_link):
		self.next = other_link

	def __str__(self):
		return '(' + self.ip + ':' + str(self.port) + ')'

	def __eq__(self, other):
		if not isinstance(other, self.__class__):
			return False
		return self.ip == other.ip and self.port == other.port

	def __ne__(self, other):
		if not isinstance(other, self.__class__):
			return True
		return self.ip != other.ip or self.port != other.port

	def __hash__(self):
		return hash((self.ip, self.port))

# tests
if __name__ == "__main__":
	def test_combine():
		# for combining linked lists
		ll = Linked_List()
		alink = Link("192.168.1.1", 8333)
		ll.add(alink)
		alink = Link("192.168.1.2", 8333)
		ll.add(alink)

		l2 = Linked_List()
		alink = Link("192.168.1.100", 8333)
		l2.add(alink)
		alink = Link("192.168.1.101", 8333)
		l2.add(alink)

		ll.add_linked_list(l2)
		print('~',ll)
		print('~',l2)

	test_combine()
	import sys
	sys.exit(0)

	ll = Linked_List()

	try: 
		ll.pop()
	except IndexError as e:
		print("pass")

	alink = Link("192.168.1.1", 8333)
	ll.add(alink)
	print(ll)

	alink = Link("192.168.1.2", 8333)
	ll.add(alink)
	print(ll)

	node = ll.pop()
	print ("removed ", node)
	print(ll)
	node = ll.pop()
	print ("removed ", node)
	print(ll)

	try: 
		ll.pop()
	except IndexError as e:
		print("pass")

	# alink = Link("192.168.1.3", 8333)
	# alink = Link("192.168.1.4", 8333)
	# alink = Link("192.168.1.5", 8333)
	# alink = Link("192.168.1.6", 8333)
	# ll.add(alink)