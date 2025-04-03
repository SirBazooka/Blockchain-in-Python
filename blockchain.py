import hashlib
import json
from time import time

from uuid import uuid4


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        
        #Genesis block - a block with no predecessors. 
        self.new_block(previous_hash=1, proof=100)

    def new_block(self):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            # <int> the proof given by the Proof of Work algorithm
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        self.current_transaction = []

        self.chain.append(block)
        return block 

    def new_transaction(self, sender, recipient, amount):
        self.current_transacitons.append({
                'sender': sender,
                'recipient': recipient,
                'amount': amount,
            })
        return self.last_block['index'] + 1
        
    def proof_of_work(self, last_proof):
        # simple Proof of Work algorithm:
        # find a number y such that hashh(xy) contains leading 4 zeroes
        # where x is the prevous y 
        # so x is the previous proof and y is the new proof

        proof = 0
        while self.valid_proof(last_proof, proof) is False::
            proof += 1

        return proof

    @staticmethod
    def hash(block):
        #It is very important that we make sure the dictionary is ordered
        #or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    def valid_proof(last_proof, proof):
        #validation of the proof (does it contain 4 leading zeroes)
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        #for adjusting the difficulty of the algorithm
        #we chould modify the number of leading zeroess
        return guess_hashh[:4] == "0000"

    @property
    def last_block(self):
        return self.chain[-1]

