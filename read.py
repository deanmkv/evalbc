import json
from linked_list import Linked_List, Link 
from pprint import pprint


def read(filename):
	"""So this function takes in a param that is the filename of the file that contains our json info for IPs. Returns a list of links, check the ipv6 field to determine if ipv6 or ipv4"""
	with open(filename) as data_file:    
	    data = json.load(data_file)
	    results = []
	for obj in data["nodes"]:
		temp = obj.split(":")
		if len(temp) == 2:
			results.append(Link(temp[0],temp[1]))
		else:
			temp = obj.split("]")
			results.append(Link(temp[0][1:],temp[1],True))
	return results

if __name__=="__main__":
	lol = read("latest.json")
	for link in lol:
		print(link.ip,"->",link.port)