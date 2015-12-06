import mini_node
import read
import OPsPerLink
import threading
import subprocess

def a_thread(*args, **kwargs):

	OPsPerLink.OPsPerLink(kwargs['link'])

if __name__=="__main__":
	subprocess.call("bash get_latest.sh", shell=True)
	ip4list = read.read("latest.json")
	for link in ip4list:
		threading.Thread(target=a_thread, link=link).start()
	
	print("waiting for all threads to complete")
	for i in threading.enumerate():
		i.join()

	OPsPerLink.print_lists()
	OPsPerLink.write_lists()