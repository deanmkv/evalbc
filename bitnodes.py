"""Gets the most recent nodes connected to the bitcoin network and writes a file to latest.json"""
import requests


req = requests.get("https://bitnodes.21.co/api/v1/snapshots/latest/")
if req.status_code == 200:
	with open("latest.json", 'w') as f:
		f.write(req.content.decode('utf-8'))