import mini_node
import read
import OPsPerLink

if __name__=="__main__":
	ip4list = read.read("latest.json")
	for link in ip4list:
		print('\nTarget: ', link.ip,':',link.port)
		OPsPerLink.OPsPerLink(link)