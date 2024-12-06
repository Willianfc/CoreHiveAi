import sys
sys.path.append('..')
from blockchain.wallet import Wallet
import requests
import json
import cmd
import os

class WalletManager(cmd.Cmd):
    intro = 'Bem-vindo ao Gerenciador de Carteira CoreHiveAI (CHAI). Digite help para ver os comandos.'
    prompt = 'CHAI> '

    def __init__(self, node_url="http://54.159.232.157:5000"):
        super().__init__()
        self.wallet = Wallet()
        self.node_url = node_url

    def do_create(self, arg):
        'Cria uma nova carteira'
        print(f"Nova carteira criada!")
        print(f"Endereço: {self.wallet.get_address()}")
        print("\nIMPORTANTE: Guarde seu endereço em um local seguro!")

    def do_balance(self, arg):
        'Consulta o saldo da carteira'
        try:
            response = requests.get(f"{self.node_url}/balance/{self.wallet.get_address()}")
            if response.status_code == 200:
                balance = response.json()['balance']
                print(f"Saldo: {balance} CHAI")
                print(f"Endereço: {self.wallet.get_address()}")
            else:
                print("Erro ao consultar saldo")
        except Exception as e:
            print(f"Erro: {e}")

    def do_send(self, arg):
        'Envia CHAI para outro endereço: send <endereço_destino> <quantidade>'
        try:
            recipient, amount = arg.split()
            amount = float(amount)
            
            if amount <= 0:
                print("Erro: A quantidade deve ser maior que zero")
                return

            current_balance = self.wallet.get_balance()
            if amount > current_balance:
                print(f"Erro: Saldo insuficiente. Saldo atual: {current_balance} CHAI")
                return
            
            transaction = {
                'sender': self.wallet.get_address(),
                'recipient': recipient,
                'amount': amount,
                'signature': self.wallet.sign_transaction({
                    'sender': self.wallet.get_address(),
                    'recipient': recipient,
                    'amount': amount
                })
            }
            
            response = requests.post(
                f"{self.node_url}/new_transaction",
                json=transaction
            )
            
            if response.status_code == 201:
                print("Transação enviada com sucesso!")
                print(f"Novo saldo: {self.wallet.get_balance()} CHAI")
            else:
                print("Erro ao enviar transação:", response.json())
        except ValueError:
            print("Formato inválido. Use: send <endereço_destino> <quantidade>")
        except Exception as e:
            print(f"Erro: {e}")

    def do_history(self, arg):
        'Mostra o histórico de transações da carteira'
        try:
            response = requests.get(f"{self.node_url}/api/address/{self.wallet.get_address()}/history")
            if response.status_code == 200:
                transactions = response.json()
                if not transactions:
                    print("Nenhuma transação encontrada")
                    return
                
                print("\nHistórico de Transações:")
                for tx in transactions:
                    print(f"\nBloco: {tx['block']}")
                    print(f"Data: {time.ctime(tx['timestamp'])}")
                    print(f"De: {tx['transaction']['sender']}")
                    print(f"Para: {tx['transaction']['recipient']}")
                    print(f"Valor: {tx['transaction']['amount']} CHAI")
            else:
                print("Erro ao buscar histórico")
        except Exception as e:
            print(f"Erro: {e}")

    def do_exit(self, arg):
        'Sair do gerenciador de carteira'
        return True

if __name__ == '__main__':
    WalletManager().cmdloop()