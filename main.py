import mini_node
import read
import OPsPerLink
import threading
import subprocess

def a_thread(*args, **kwargs):

	OPsPerLink.OPsPerLink(kwargs['link'])
	print("finish, %d remain" % threading.active_count())

def custom_list():
	from linked_list import Link
	li = []
	with open("ips.txt", 'r') as f:
		for i in f:
			word = i.strip()
			index= word.find(':')
			l = Link(word[0:index], word[index+1:])
			li.append(l)
	# print(li)
	return li

if __name__=="__main__":
	subprocess.call("bash get_latest.sh", shell=True)
	ip4list = read.read("latest.json")
	# ip4list = custom_list()
	print("starting to create all nodes")
	unique_id = 10000  # start here to ensure len() = 5
	for link in ip4list:
		# a_thread(link=link)  # use only this line for single-threaded
		th = threading.Thread(target=a_thread, kwargs={'link':link})
		th.name = unique_id
		th.start()
		unique_id += 1
	
	print("waiting for all threads to complete")
	master_thread = threading.current_thread().ident
	for i in threading.enumerate():
		if master_thread != i.ident:
			i.join()

	OPsPerLink.print_lists()
	OPsPerLink.write_lists()