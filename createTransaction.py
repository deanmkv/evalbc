__author__ = 'RunzeZhao'
import sys
if sys.version_info.major < 3:
    sys.stderr.write('Sorry, Python 3.x required by this example.\n')
    sys.exit(1)

import hashlib

from bitcoin import SelectParams, base58
from bitcoin.core import b2x, lx, COIN, COutPoint, CMutableTxOut, CMutableTxIn, CMutableTransaction, Hash160
from bitcoin.core.script import CScript, OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG, SignatureHash, SIGHASH_ALL
from bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret, P2PKHBitcoinAddress

SelectParams('mainnet')

def get_randomness(filename):
	with open(filename, 'r') as f:
		randomness = bytes(f.readline().strip(), 'utf-8')
	return randomness

def make_transaction():
	words = get_randomness('keys.txt')
	# seckey = CBitcoinSecret.from_secret_bytes(our_keys[1])
	h = hashlib.sha256(words).digest()
	seckey = CBitcoinSecret.from_secret_bytes(h)

	# key = CBitcoinSecret("L4vB5fomsK8L95wQ7GFzvErYGht49JsCPJyJMHpB4xGM6xgi2jvG")
	address = P2PKHBitcoinAddress.from_pubkey(seckey.pub)  # "1F26pNMrywyZJdr22jErtKcjF8R3Ttt55G"
	print(type(address), address)
	message = "screw Carly Rae"
	print(address)
	# print (CBitcoinAddress(address).to_scriptPubKey())
	# print(dir(seckey))
	# print("Secret key: ", seckey)
	# print("Public key: ", base58.encode(seckey.pub))
	# print(base58.encode(Hash160(seckey.pub)))
	# print('~',type(our_keys), our_keys)
	# print('~',type(seckey), seckey)
	# print('~',type(seckey.pub), seckey.pub)


	# takes a transaction hash, like you would see on blockchain.info
	txid = lx('08f7e2c1238cc9b918649e40d72815f32be6dc1ad538cb25331bd1f1c58a5f46')

	# vout points at which address we are using, 0 for the first and 1 for the second
	vout = 0

	# Create the txin structure, which includes the outpoint. The scriptSig
	# defaults to being empty.
	txin = CMutableTxIn(COutPoint(txid, vout))

	# We also need the scriptPubKey of the output we're spending because
	# SignatureHash() replaces the transaction scriptSig's with it.
	#
	# Here we'll create that scriptPubKey from scratch using the pubkey that
	# corresponds to the secret key we generated above.
	txin_scriptPubKey = CScript([OP_DUP, OP_HASH160, Hash160(seckey.pub), OP_EQUALVERIFY, OP_CHECKSIG])

	# Create the txout. This time we create the scriptPubKey from a Bitcoin
	# address.
	txout = CMutableTxOut(0.00002 * COIN,address.to_scriptPubKey())

	# Create the unsigned transaction.
	tx = CMutableTransaction([txin], [txout])

	# Calculate the signature hash for that transaction.
	sighash = SignatureHash(txin_scriptPubKey, tx, 0, SIGHASH_ALL)

	# Now sign it. We have to append the type of signature we want to the end, in
	# this case the usual SIGHASH_ALL.
	sig = seckey.sign(sighash) + bytes([SIGHASH_ALL])

	# Set the scriptSig of our transaction input appropriately.
	txin.scriptSig = CScript([sig, seckey.pub])

	# Verify the signature worked. This calls EvalScript() and actually executes
	# the opcodes in the scripts to see if everything worked out. If it doesn't an
	# exception will be raised.
	VerifyScript(txin.scriptSig, txin_scriptPubKey, tx, 0, (SCRIPT_VERIFY_P2SH,))

	# Done! Print the transaction to standard output with the bytes-to-hex
	# function.
	# send the message printed out to other nodes and they will receive the transaction
	print(b2x(tx.serialize()))

	return tx

if __name__ == "__main__":
	make_transaction()