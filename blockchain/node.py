from flask import Flask, jsonify, request
from .blockchain import Blockchain
from .database import Database
import time

app = Flask(__name__)
blockchain = Blockchain()
db = Database()

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar a saúde do nó"""
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time(),
        'blocks': len(blockchain.chain),
        'current_supply': blockchain.current_supply
    })

@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount', 'signature']
    if not all(k in values for k in required):
        return 'Missing values', 400

    success = blockchain.add_transaction(
        values['sender'],
        values['recipient'],
        values['amount'],
        values['signature']
    )

    if success:
        response = {'message': 'Transaction added successfully'}
        return jsonify(response), 201
    return 'Transaction failed', 400

@app.route('/mine', methods=['GET'])
def mine():
    success, result = blockchain.mine_pending_transactions(request.args.get('miner_address'))
    if success:
        response = {
            'message': 'New block mined',
            'block': {
                'index': result.index,
                'transactions': [t.__dict__ for t in result.transactions],
                'timestamp': result.timestamp,
                'previous_hash': result.previous_hash,
                'hash': result.hash
            }
        }
        return jsonify(response), 200
    return jsonify({'message': result}), 400

@app.route('/chain', methods=['GET'])
def get_chain():
    response = {
        'chain': [vars(block) for block in blockchain.chain],
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/balance/<address>', methods=['GET'])
def get_balance(address):
    balance = blockchain.get_balance(address)
    return jsonify({'address': address, 'balance': balance}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)