import requests
import json
from urllib.parse import urljoin
import os

class BlockchainConnection:
    def __init__(self, node_url=None):
        self.node_url = node_url or os.getenv('COREHIVEAI_NODE_URL', 'http://54.159.232.157:5000')
        self.api_key = os.getenv('COREHIVEAI_API_KEY', None)
        self.verify_connection()

    def verify_connection(self):
        try:
            response = requests.get(urljoin(self.node_url, '/health'))
            if response.status_code != 200:
                raise ConnectionError("Não foi possível conectar ao nó da blockchain")
        except Exception as e:
            raise ConnectionError(f"Erro ao conectar ao nó da blockchain: {str(e)}")

    def get_headers(self):
        headers = {'Content-Type': 'application/json'}
        if self.api_key:
            headers['X-API-Key'] = self.api_key
        return headers

    def get(self, endpoint):
        response = requests.get(
            urljoin(self.node_url, endpoint),
            headers=self.get_headers()
        )
        return self._handle_response(response)

    def post(self, endpoint, data):
        response = requests.post(
            urljoin(self.node_url, endpoint),
            headers=self.get_headers(),
            json=data
        )
        return self._handle_response(response)

    def _handle_response(self, response):
        if response.status_code in [200, 201]:
            return response.json()
        raise Exception(f"Erro na requisição: {response.status_code} - {response.text}")

# Singleton instance
connection = BlockchainConnection()