import datetime
import hashlib
import json
from flask import Flask, jsonify

# Part 1: Create a Blockchain

class Blockchain:
    def __init__(self):
        self.chain = []  # Initialize blockchain as an empty list
        # Create the genesis block with proof=1 and previous_hash='0'
        self.create_block(proof=1, previous_hash='0')
        
    def create_block(self, proof, previous_hash):
        # Create a new block and add it to the chain
        block = {
            'index': len(self.chain) + 1,  # Position of the block in the chain
            'timestamp': str(datetime.datetime.now()),  # Current timestamp
            'proof': proof,  # Proof given by proof of work algorithm
            'previous_hash': previous_hash  # Hash of the previous block
        }
        self.chain.append(block)  # Add the new block to the chain
        return block
    
    def get_previous_block(self):
        # Return the last block in the chain
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        # Proof of Work algorithm:
        # Find a number new_proof such that hash(new_proof^2 - previous_proof^2) starts with '0000'
        new_proof = 1
        check_proof = False
        
        while not check_proof:
            # Calculate hash operation
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            # Check if hash starts with 4 zeros
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1  # Increment and try again
        return new_proof
    
    def hash(self, block):
        # Create a SHA-256 hash of a block
        encoded_block = json.dumps(block, sort_keys=True).encode()  # Convert block dict to JSON string and encode
        return hashlib.sha256(encoded_block).hexdigest()  # Return hash digest
    
    def is_chain_valid(self, chain):
        # Check if the blockchain is valid by verifying hashes and proofs
        previous_block = chain[0]  # Start from the genesis block
        block_index = 1
        
        while block_index < len(chain):
            block = chain[block_index]
            # Check if previous_hash of current block matches hash of previous block
            if block['previous_hash'] != self.hash(previous_block):
                return False
            
            # Check proof of work validity
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            
            previous_block = block
            block_index += 1
        
        return True  # If all checks pass, the chain is valid
    

# Initialize Flask app
app = Flask(__name__)

# Prevent jsonify from pretty-printing (to save bandwidth)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Create a blockchain instance
blockchain = Blockchain()

# Route to mine a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()  # Get last block
    previous_proof = previous_block['proof']  # Get proof of last block
    proof = blockchain.proof_of_work(previous_proof)  # Find proof for new block
    previous_hash = blockchain.hash(previous_block)  # Hash of last block
    block = blockchain.create_block(proof, previous_hash)  # Create new block
    
    # Prepare response with block details
    response = {
        'message': "Congratulations, you’ve mined a block",
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200  # Return JSON response with HTTP 200 OK

# Route to get the full blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

# Route to check if the blockchain is valid
@app.route('/is_valid', methods=['GET'])
def is_valid():
    validation = blockchain.is_chain_valid(blockchain.chain)  # Validate chain
    response = {'is_valid': validation}
    return jsonify(response), 200

# Run the Flask app on all network interfaces, port 5000
app.run(host='0.0.0.0', port=5000)
