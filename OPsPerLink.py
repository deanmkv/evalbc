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
            # print("retrying api call for the ",x+1,"th time")
            time.sleep(2)
            r = "still exception after 5 API calls"
    if r == "still exception after 5 API calls":
        notInDB.append(link)
    elif r != "still exception after 5 API calls" and r.json()['receive_count'] == 0:
        inDBZeroCount.append(link)
    elif r != "still exception after 5 API calls" and r.json()['receive_count'] > 0:
        inDBMoreThanOneCount.append(link)
    
    # bs.listen_forever()
    return

def print_lists():
    print("notInDB: ", notInDB)
    print("inDBZeroCount: ", inDBZeroCount)
    print("inDBMoreThanOneCount: ", inDBMoreThanOneCount)
    print("timeouts: ", timeouts)

def write_lists():
    if len(inDBMoreThanOneCount) > 0:
        with open("dbone.txt", 'w') as f:
            for i in inDBMoreThanOneCount:
                f.write(str(i), '\n')
    else:
        print("Nothing in inDBMoreThanOneCount")

    if len(inDBZeroCount) > 0:
        with open("dbzero.txt", 'w') as f:
            for i in inDBZeroCount:
                f.write(str(i), '\n')
    else:
        print("Nothing in inDBZeroCount")
    
    if len(timeouts) > 0:
        with open("timeouts.txt", 'w') as f:
            for i in timeouts:
                f.write(str(i), '\n')
    else:
        print("Nothing in timeouts")

    if len(notInDB) > 0:
        with open("dbnone.txt", 'w') as f:
            for i in notInDB:
                f.write(str(i), '\n')
    else:
        print("Nothing in notInDB")
        
    
if __name__ == "__main__":
    l1 = linked_list.Link("67.172.198.9",8333)
    print("here")
    OPsPerLink(l1)