import time
from .block import Block
from .transaction import Transaction
from .database import Database

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.difficulty = 4
        self.mining_reward = 50
        self.max_supply = 60000
        self.current_supply = 0
        self.db = Database()
        self.load_chain()
        if not self.chain:
            self.create_genesis_block()

    def load_chain(self):
        blocks = self.db.get_all_blocks()
        for block_data in blocks:
            block = Block(
                block_data['index'],
                block_data['transactions'],
                block_data['timestamp'],
                block_data['previous_hash'],
                block_data['nonce']
            )
            block.hash = block_data['hash']
            self.chain.append(block)
            
            # Calculate current supply
            for tx in block_data['transactions']:
                if tx[1] == "Network":  # Mining reward transaction
                    self.current_supply += tx[3]

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.calculate_hash()
        self.chain.append(genesis_block)
        self.db.save_block(genesis_block)

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, sender, recipient, amount, signature):
        if self.verify_transaction(sender, amount, signature):
            transaction = Transaction(sender, recipient, amount)
            self.pending_transactions.append(transaction)
            return True
        return False

    def mine_pending_transactions(self, miner_address):
        if self.current_supply >= self.max_supply:
            return False, "Maximum supply reached"

        block = Block(
            len(self.chain),
            self.pending_transactions,
            time.time(),
            self.get_latest_block().hash
        )

        block.mine_block(self.difficulty)
        self.chain.append(block)
        
        # Save block to database
        self.db.save_block(block)
        
        # Reward transaction
        reward = self.calculate_mining_reward()
        self.current_supply += reward
        reward_transaction = Transaction("Network", miner_address, reward)
        self.pending_transactions = [reward_transaction]
        
        # Update miner's balance
        current_balance = self.db.get_wallet_balance(miner_address)
        self.db.update_wallet_balance(miner_address, current_balance + reward)
        
        return True, block

    def calculate_mining_reward(self):
        current_era = self.current_supply // 15000  # Every 15000 CHAI mined
        return self.mining_reward / (2 ** current_era)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def get_balance(self, address):
        return self.db.get_wallet_balance(address)

    def verify_transaction(self, sender, amount, signature):
        if sender == "Network":  # Mining reward transaction
            return True
        sender_balance = self.get_balance(sender)
        return sender_balance >= amount