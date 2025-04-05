import hashlib
import json
from time import time
from uuid import uuid4
from textwrap import dedent
from flask import Flask, jsonify, request
from urllib.parse import urlparse 
import requests

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        
        # Genesis block - a block with no predecessors. 
        self.new_block(previous_hash=1, proof=100)

    #registering a new node
    #add a new node to the list of the nodes
    def register_node(self, address):
       parsed_url = urlparse(address)
       self.node.add(parsed_url.netloc)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            # <int> the proof given by the Proof of Work algorithm
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        self.current_transactions = []

        self.chain.append(block)
        return block 

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
                'sender': sender,
                'recipient': recipient,
                'amount': amount,
            })
        return self.last_block['index'] + 1
        
    def proof_of_work(self, last_proof):
        # simple Proof of Work algorithm:
        # find a number y such that hash(xy) contains leading 4 zeroes
        # where x is the previous y 
        # so x is the previous proof and y is the new proof

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    #used for determining if a note is valid or not 
    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n--------------------\n")
            #checking if the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False
            
            #checking if the proof of work is correct 
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            currect_index +=1

        return True 
            
    def resolve_conflicts(self):
        #this is the Consensus Algorithm
        #it resolves conflicts by replacing our chain with the longest one in the network 
        #returns True if our chan was replaced and False if it was not 
    
        neighbours = self.nodes
        new_chain = None

        max_length = len(self.chain)

        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.valid_chain(chain):
                    max_length = length 
                    new_chain = chain

        #replace the chain if we discovered a new valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False
        

    @staticmethod
    def valid_proof(last_proof, proof):
        # validation of the proof (does it contain 4 leading zeroes)
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        # for adjusting the difficulty of the algorithm
        # we could modify the number of leading zeroes
        return guess_hash[:4] == "0000"

    @staticmethod
    def hash(block):
        # It is very important that we make sure the dictionary is ordered
        # or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    @property
    def last_block(self):
        return self.chain[-1]






# Flask server config 

app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    # run the proof of work algorithm to get the next proof
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # after finding a proof, the user gets a reward
    # the sender is "0" - this node has mined a new coin
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # forge a new block and add it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }

    return jsonify(response), 200
  
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # check that the required fields are in the POST
    required = ['sender', 'recipient', 'amount']
    if not all(i in values for i in required):
        return 'missing values', 400
    
    # creating a new transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction will be added to the Block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
