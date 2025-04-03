import hashlib
import json
from time import time


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
        
    @staticmethod
    def hash(block):
        #It is very important that we make sure the dictionary is ordered
        #or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]
