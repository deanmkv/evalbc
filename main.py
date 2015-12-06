import mini_node
import read
import OPsPerLink
import threading
import subprocess

if __name__=="__main__":
	subprocess.call("bash get_latest.sh", shell=True)
	ip4list = read.read("latest.json")
	for link in ip4list:
		print('\nTarget: ', link.ip,':',link.port)
		OPsPerLink.OPsPerLink(link)