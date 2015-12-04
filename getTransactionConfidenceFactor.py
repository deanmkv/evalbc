import blockcypher

#use this method to get the transaction confidence factor given the hash of the transaction
def getTransactionConfidenceFactor(txID):
    transaction = blockcypher.get_transaction_details(txID, api_key='d78e7b0f0c88597200452313a1c32fc9')
    print(transaction['confidence'])
    if 'receive_count' in transaction:
    	print(transaction['receive_count'])
    else:
    	print('No receive_count')

if __name__ == "__main__":
	getTransactionConfidenceFactor("c52e036fd70785415f5b205e7a472b7538e0d6c4a3c14edc106183068089c279")
	getTransactionConfidenceFactor("42e039a611fc4bcc1b0b991853ebd82f4827723352238c91a61ff39660c0531c")