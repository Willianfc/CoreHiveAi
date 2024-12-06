import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_file="blockchain.db"):
        self.db_file = db_file
        self.init_database()

    def get_connection(self):
        return sqlite3.connect(self.db_file)

    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        # Create blocks table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS blocks (
            id INTEGER PRIMARY KEY,
            index INTEGER,
            timestamp REAL,
            previous_hash TEXT,
            hash TEXT,
            nonce INTEGER
        )
        ''')

        # Create transactions table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            block_id INTEGER,
            sender TEXT,
            recipient TEXT,
            amount REAL,
            timestamp REAL,
            FOREIGN KEY (block_id) REFERENCES blocks(id)
        )
        ''')

        # Create wallets table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS wallets (
            address TEXT PRIMARY KEY,
            public_key TEXT,
            balance REAL,
            created_at REAL
        )
        ''')

        conn.commit()
        conn.close()

    def save_block(self, block):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO blocks (index, timestamp, previous_hash, hash, nonce)
        VALUES (?, ?, ?, ?, ?)
        ''', (block.index, block.timestamp, block.previous_hash, block.hash, block.nonce))
        
        block_id = cursor.lastrowid
        
        # Save associated transactions
        for transaction in block.transactions:
            cursor.execute('''
            INSERT INTO transactions (block_id, sender, recipient, amount, timestamp)
            VALUES (?, ?, ?, ?, ?)
            ''', (block_id, transaction.sender, transaction.recipient, transaction.amount, block.timestamp))
        
        conn.commit()
        conn.close()

    def get_all_blocks(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM blocks ORDER BY index')
        blocks = cursor.fetchall()
        
        result = []
        for block in blocks:
            # Get transactions for this block
            cursor.execute('SELECT * FROM transactions WHERE block_id = ?', (block[0],))
            transactions = cursor.fetchall()
            
            block_data = {
                'index': block[1],
                'timestamp': block[2],
                'previous_hash': block[3],
                'hash': block[4],
                'nonce': block[5],
                'transactions': transactions
            }
            result.append(block_data)
        
        conn.close()
        return result

    def save_wallet(self, address, public_key):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT OR REPLACE INTO wallets (address, public_key, balance, created_at)
        VALUES (?, ?, 0, ?)
        ''', (address, public_key, time.time()))
        
        conn.commit()
        conn.close()

    def update_wallet_balance(self, address, new_balance):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        UPDATE wallets SET balance = ? WHERE address = ?
        ''', (new_balance, address))
        
        conn.commit()
        conn.close()

    def get_wallet_balance(self, address):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT balance FROM wallets WHERE address = ?', (address,))
        result = cursor.fetchone()
        
        conn.close()
        return result[0] if result else 0