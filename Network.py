from web3 import Web3
import myDB

select_all_sql = """SELECT network_id,
       network_symbol,
       network_name,
       block_explorer,
       gateway_url,
       token_block_explorer,
       address_block_explorer
from network"""


def select_network_sql(network_id: int) -> str:
    return f'{select_all_sql} WHERE network_id = {network_id}'


class Network:

    def __init__(self, row):
        self.id = row[0]
        self.symbol = row[1]
        self.name = row[2]
        self.block_explorer = row[3]
        self.gateway_url = row[4]
        self.token_block_explorer = row[5]
        self.address_block_explorer = row[6]
        self.w3 = Web3(Web3.HTTPProvider(self.gateway_url))
        return

    def __str__(self):
        return f'id: {self.id},symbol: {self.symbol}, name: {self.name}, block_explorer: {self.block_explorer}, gateway_url: {self.gateway_url}, token_block_explorer: {self.token_block_explorer}, ' \
               f'address_block_explorer: {self.address_block_explorer} '


def findNetwork(symbol: str) -> Network:
    for n in myDB.networks:
        if n.symbol == symbol:
            return n
    print(f'unable to find network {symbol}')
    return None
