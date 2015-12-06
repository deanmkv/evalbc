import mini_node
import read
import OPsPerLink
import threading
import subprocess

def a_thread(*args, **kwargs):

	OPsPerLink.OPsPerLink(kwargs['link'])
	print("finished thread, %d remain" % threading.active_count())

if __name__=="__main__":
	subprocess.call("bash get_latest.sh", shell=True)
	ip4list = read.read("latest.json")
	print("starting to create all nodes")
	for link in ip4list:
		threading.Thread(target=a_thread, kwargs={'link':link}).start()
	
	print("waiting for all threads to complete")
	master_thread = threading.current_thread().ident
	for i in threading.enumerate():
		if master_thread != i.ident:
			i.join()

	OPsPerLink.print_lists()
	OPsPerLink.write_lists()