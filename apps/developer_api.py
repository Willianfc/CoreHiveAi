from flask import Flask, jsonify, request
import sys
sys.path.append('..')
from blockchain.blockchain import Blockchain
from blockchain.wallet import Wallet
from functools import wraps
import os

app = Flask(__name__)
blockchain = Blockchain()

# Configuração básica de segurança
API_KEY = os.getenv('COREHIVEAI_API_KEY', 'seu-api-key-aqui')

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key and api_key == API_KEY:
            return f(*args, **kwargs)
        return jsonify({"error": "API key inválida"}), 401
    return decorated

@app.route('/api/stats', methods=['GET'])
@require_api_key
def get_stats():
    """Retorna estatísticas da blockchain"""
    return jsonify({
        'total_blocks': len(blockchain.chain),
        'current_supply': blockchain.current_supply,
        'max_supply': blockchain.max_supply,
        'difficulty': blockchain.difficulty,
        'mining_reward': blockchain.calculate_mining_reward(),
        'network_hashrate': calculate_network_hashrate()
    })

@app.route('/api/blocks', methods=['GET'])
@require_api_key
def get_blocks():
    """Retorna todos os blocos da blockchain"""
    start = request.args.get('start', type=int, default=0)
    limit = request.args.get('limit', type=int, default=50)
    
    blocks = [{
        'index': block.index,
        'timestamp': block.timestamp,
        'transactions': [t.__dict__ for t in block.transactions],
        'hash': block.hash,
        'previous_hash': block.previous_hash,
        'nonce': block.nonce
    } for block in blockchain.chain[start:start+limit]]
    
    return jsonify(blocks)

@app.route('/api/transactions/pending', methods=['GET'])
@require_api_key
def get_pending_transactions():
    """Retorna transações pendentes"""
    return jsonify([t.__dict__ for t in blockchain.pending_transactions])

@app.route('/api/address/<address>/history', methods=['GET'])
@require_api_key
def get_address_history(address):
    """Retorna histórico de transações de um endereço"""
    transactions = []
    for block in blockchain.chain:
        for tx in block.transactions:
            if tx.sender == address or tx.recipient == address:
                transactions.append({
                    'block': block.index,
                    'timestamp': block.timestamp,
                    'transaction': tx.__dict__
                })
    return jsonify(transactions)

def calculate_network_hashrate():
    """Calcula o hashrate aproximado da rede"""
    if len(blockchain.chain) < 2:
        return 0
    
    recent_blocks = blockchain.chain[-10:]
    if len(recent_blocks) < 2:
        return 0
    
    time_diff = recent_blocks[-1].timestamp - recent_blocks[0].timestamp
    if time_diff == 0:
        return 0
    
    total_difficulty = sum(2 ** blockchain.difficulty for _ in recent_blocks)
    return total_difficulty / time_diff

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, ssl_context='adhoc')