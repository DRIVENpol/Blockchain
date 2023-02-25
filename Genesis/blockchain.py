#Import libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify

# The blockchain
class DRIVEN_Blockchain:
    
    def __init__(self):
        self.chain = []
        # Create the genesis block
        self.createBlock(proof = 1, prevHash = "0")   
        
    # Create the block & push it to the chain
    def createBlock(self, proof, prevHash):
        block = {
                'block_index': len(self.chain) + 1,
                'block_timestamp': str(datetime.datetime.now()),
                'mining_proof': proof,
                'prev_block_hash': prevHash
                }
        self.chain.append(block)
        return block
    
    
    # Fetch the data from the last mined block
    def fetch_last_block(self):
        return self.chain[-1]
    
    
    # Proof of work
    def pow(self, prevProof):
        final_proof = 1
        is_proof = False
        
        while is_proof is False:
            # Edit later the hash operation to make it more difficult
            # for miners to mine a block
            hash_op = hashlib.sha256(str(final_proof ** 2 - prevProof ** 2).encode()).hexdigest()
            if hash_op[:4] == '0000':
                is_proof = True
            else: 
                final_proof += 1
            
        return final_proof
        
        
    # Return the cryptographic hash of one block
    def get_cryptographic_hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    # Validate the blockchain
    def validate_blockchain(self, chain):
        prev_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['prev_block_hash'] != self.get_cryptographic_hash(prev_block):
                return False
            prev_proof = prev_block['mining_proof']
            current_proof = block['mining_proof']
            hash_op = hashlib.sha256(str(current_proof ** 2 - prev_proof ** 2).encode()).hexdigest()
            if hash_op[:4] != '0000':
                return False
            prev_block = block
            block_index += 1
        return True
            
            
# The flask web app
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Initialize the blockchain
blockchain = DRIVEN_Blockchain()  

# Mine a block (request)     
@app.route('/mine_new_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.fetch_last_block()
    previous_proof = previous_block['mining_proof']
    proof = blockchain.pow(previous_proof)
    previous_hash = blockchain.get_cryptographic_hash(previous_block)
    block = blockchain.createBlock(proof, previous_hash)
    response = {'message': 'New block mined!',
                'index': block['block_index'],
                'timestamp': block['block_timestamp'],
                'proof': block['mining_proof'],
                'previous_hash': block['prev_block_hash']}
    return jsonify(response), 200
            
# Get full blockchain (request)     
@app.route('/get_blockchain', methods = ['GET'])
def get_full_chain():
    response = {
                'chain': blockchain.chain,
                'length': len(blockchain.chain)
                }
    return jsonify(response), 200

# Run the blockchain on local node
app.run(host = '0.0.0.0', port = 5001)