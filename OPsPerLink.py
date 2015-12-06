__author__ = 'RunzeZhao'
import mini_node
import sys
import requests
import time
import linked_list
import subprocess
import socket

notInDB = []
inDBZeroCount = []
inDBMoreThanOneCount = []
timeouts = []

def OPsPerLink(link):
    try:
        bs = mini_node.BitcoinSocket(link)
        if bs.conn_ref or not bs.connect():
            sys.exit(0)
        bs.listen_until_acked()
        txHash = bs.send_transaction()
    except:
        print("An error occured", link)
        timeouts.append(link)
        return

    for x in range(0,5):
        try:
            r = requests.get('https://api.blockcypher.com/v1/btc/main/txs/' + txHash)
        except:
            print("retrying api call for the ",x+1,"th time")
            time.sleep(2)
            r = "still exception after 5 API calls"
    if r == "still exception after 5 API calls":
        notInDB.append(link)
    elif r != "still exception after 5 API calls" and r.json()['receive_count'] == 0:
        inDBZeroCount.append(link)
    elif r != "still exception after 5 API calls" and r.json()['receive_count'] > 0:
        inDBMoreThanOneCount.append(link)
    print("notInDB: ", notInDB)
    print("inDBZeroCount: ", inDBZeroCount)
    print("inDBMoreThanOneCount: ", inDBMoreThanOneCount)
    print("timeouts: ", timeouts)
    if len(inDBMoreThanOneCount) > 0 or len(inDBZeroCount) > 0:
        with open("filename.txt", 'w') as f:
            f.write("anything please")
    # bs.listen_forever()
    return

if __name__ == "__main__":
    l1 = linked_list.Link("67.172.198.9",8333)
    print("here")
    OPsPerLink(l1)