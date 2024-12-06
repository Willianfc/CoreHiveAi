import sys
sys.path.append('..')
from blockchain.blockchain import Blockchain
from blockchain.wallet import Wallet
import requests
import time
import threading
import os

class Miner:
    def __init__(self, node_url="http://54.159.232.157:5000"):
        self.wallet = Wallet()
        self.node_url = node_url
        self.mining = False

    def start_mining(self):
        self.mining = True
        print(f"Iniciando mineração... Endereço do minerador: {self.wallet.get_address()}")
        
        while self.mining:
            try:
                response = requests.get(f"{self.node_url}/mine")
                if response.status_code == 200:
                    block = response.json()
                    print(f"Bloco minerado com sucesso! Hash: {block['block']['hash']}")
                    print(f"Recompensa enviada para: {self.wallet.get_address()}")
                    print(f"Saldo atual: {self.wallet.get_balance()} CHAI")
                else:
                    print("Erro na mineração:", response.json()['message'])
                    if "Maximum supply reached" in response.json()['message']:
                        print("Fornecimento máximo atingido. Encerrando mineração.")
                        self.mining = False
                        break
            except Exception as e:
                print(f"Erro durante a mineração: {e}")
                time.sleep(5)

    def stop_mining(self):
        self.mining = False
        print("Mineração interrompida.")

if __name__ == "__main__":
    miner = Miner()
    try:
        miner.start_mining()
    except KeyboardInterrupt:
        miner.stop_mining()
        print("\nMineração finalizada pelo usuário.")