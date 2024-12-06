import os

# Configurações da Blockchain
DIFFICULTY = 4
MINING_REWARD = 50
MAX_SUPPLY = 60000
BLOCK_TIME = 600  # 10 minutos

# Configurações do Banco de Dados
DB_FILE = os.getenv('COREHIVEAI_DB_FILE', 'blockchain.db')

# Configurações do Nó
NODE_HOST = '0.0.0.0'
NODE_PORT = 5000
NODE_URL = os.getenv('COREHIVEAI_NODE_URL', 'http://54.159.232.157:5000')

# Configurações de Segurança
API_KEY = os.getenv('COREHIVEAI_API_KEY', 'sua-chave-api-aqui')
SSL_CERT = os.getenv('COREHIVEAI_SSL_CERT', None)
SSL_KEY = os.getenv('COREHIVEAI_SSL_KEY', None)

# Configurações de Backup
BACKUP_INTERVAL = 6  # horas
BACKUP_S3_BUCKET = os.getenv('COREHIVEAI_BACKUP_BUCKET', 'corehiveai-backups')

# Configurações de Log
LOG_LEVEL = os.getenv('COREHIVEAI_LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('COREHIVEAI_LOG_FILE', 'blockchain.log')