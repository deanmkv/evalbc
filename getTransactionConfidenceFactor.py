#use this method to get the transaction confidence factor given the hash of the transaction
def getTransactionConfidenceFactor(txID):
    transaction = blockcypher.get_transaction_details(txID, api_key='d78e7b0f0c88597200452313a1c32fc9')
    print(transaction['confidence'])

getTransactionConfidenceFactor("c52e036fd70785415f5b205e7a472b7538e0d6c4a3c14edc106183068089c279")