__author__ = 'RunzeZhao'
import sys
if sys.version_info.major < 3:
    sys.stderr.write('Sorry, Python 3.x required by this example.\n')
    sys.exit(1)

import hashlib

from bitcoin import SelectParams, base58
from bitcoin.core import b2lx, b2x, lx, COIN, COutPoint, CMutableTxOut, CMutableTxIn, CMutableTransaction, Hash160
from bitcoin.core.script import CScript, OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG, SignatureHash, SIGHASH_ALL
from bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret, P2PKHBitcoinAddress

SelectParams('mainnet')

randomness = None
rand_open = False

def get_randomness(filename):
	global rand_open
	global randomness
	if rand_open:
		return randomness
	with open(filename, 'r') as f:
		randomness = bytes(f.readline().strip(), 'utf-8')
	rand_open = True
	return randomness

def make_self_transaction():
	words = get_randomness('keys.txt')
	# seckey = CBitcoinSecret.from_secret_bytes(our_keys[1])
	h = hashlib.sha256(words).digest()
	seckey = CBitcoinSecret.from_secret_bytes(h)
	input_hashes = [('08f7e2c1238cc9b918649e40d72815f32be6dc1ad538cb25331bd1f1c58a5f46',0),
	('8642baa47de6ece50c2800221e5bc7eefd7adf4158f24af31fdcfa185cb54fce', 1)]
	address = P2PKHBitcoinAddress.from_pubkey(seckey.pub)  # "1F26pNMrywyZJdr22jErtKcjF8R3Ttt55G"
	return make_transaction(0.00092, input_hashes, address, seckey)

def make_transaction(sum_inputs, input_hashes, output_addr, seckey, mining_fee=0.00005): #TODO add change address?
	"""all values in btc. input_hashes is a list of tuples (tx_hash, vout).
		output_addr is P2PKHBitcoinAddress"""
	

	# key = CBitcoinSecret("L4vB5fomsK8L95wQ7GFzvErYGht49JsCPJyJMHpB4xGM6xgi2jvG")
	# print(type(address), address)
	# print(address)
	# print (CBitcoinAddress(address).to_scriptPubKey())
	# print(dir(seckey))
	# print("Secret key: ", seckey)
	# print("Public key: ", base58.encode(seckey.pub))
	# print(base58.encode(Hash160(seckey.pub)))
	# print('~',type(our_keys), our_keys)
	# print('~',type(seckey), seckey)
	# print('~',type(seckey.pub), seckey.pub)

	src_money = []
	sum_of_src_money = 0

	for tx_tup in input_hashes:
		# takes a transaction hash, like you would see on blockchain.info
		txid = lx(tx_tup[0])

		# vout points at which address we are using, 0 for the first and 1 for the second
		vout = tx_tup[1]

		# Create the txin structure, which includes the outpoint. The scriptSig
		# defaults to being empty.
		txin = CMutableTxIn(COutPoint(txid, vout))
		# print(COutPoint(txid, vout))
		# print(dir(txin))
		# print(txin)
		# print(txin.prevout)
		src_money.append(txin)

		# TODO add queries to blockcypher to get the sum_of_src_money

	#LOCKING SCRIPT
	# We also need the scriptPubKey of the output we're spending because
	# SignatureHash() replaces the transaction scriptSig's with it.
	#
	# Here we'll create that scriptPubKey from scratch using the pubkey that
	# corresponds to the secret key we generated above.
	txin_scriptPubKey = CScript([OP_DUP, OP_HASH160, output_addr, OP_EQUALVERIFY, OP_CHECKSIG])
	# print(b2x(txin_scriptPubKey))

	# Create the txout. This time we create the scriptPubKey from a Bitcoin
	# address.
	txout = CMutableTxOut((sum_inputs - mining_fee) * COIN,output_addr.to_scriptPubKey())

	# Create the unsigned transaction.
	tx = CMutableTransaction(src_money, [txout])
	

	i = 0
	while i < len(src_money):
		# Calculate the signature hash for that transaction.
		sighash = SignatureHash(txin_scriptPubKey, tx, i, SIGHASH_ALL)

		# print sighash in hex (2 ways)
		# import binascii
		# print('~', binascii.hexlify(sighash))
		# import codecs
		# print(codecs.encode(sighash, 'hex'))

		# Now sign it. We have to append the type of signature we want to the end, in
		# this case the usual SIGHASH_ALL.
		sig = seckey.sign(sighash) + bytes([SIGHASH_ALL])
		# print(sig)
		# print(b2x(sig))
		# for txin in src_money:
		# Set the scriptSig of our transaction input appropriately.
		txin = src_money[i]
		txin.scriptSig = CScript([sig, seckey.pub])

		# Verify the signature worked. This calls EvalScript() and actually executes
		# the opcodes in the scripts to see if everything worked out. If it doesn't an
		# exception will be raised.
		VerifyScript(txin.scriptSig, txin_scriptPubKey, tx, i, (SCRIPT_VERIFY_P2SH,))
		i += 1

	# Done! Print the transaction to standard output with the bytes-to-hex
	# function.
	# send the message printed out to other nodes and they will receive the transaction
	# print("Raw TX: ", b2x(tx.serialize()))
	# print("TX hash: ", b2lx(tx.GetHash()))
	return tx

if __name__ == "__main__":
	# tx = make_transaction()
	# junk = tx.serialize()
	# print(type(junk))
	from bitcoin.core import Hash
	# print(hashlib.sha256(hashlib.sha256((junk)).digest()).hexdigest())
	from bitcoin.core import b2x, x
	# print(b2x(Hash(tx.serialize())))
	# import sys
	# sys.exit(0)
	# print(type(tx))
	# print(tx.GetHash(), type(tx.GetHash()))
	# print(base58.encode(tx.GetHash()))
	# print(base58.decode(hash(tx)))

	# submitted_tx = ""

	# print(b2x(Hash(x(submitted_tx))))
	(make_self_transaction())
