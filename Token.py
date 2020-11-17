from web3 import Web3
import myWeb3
import myDB
import Network

select_all_sql = """SELECT network, name, address, is_base_price FROM token ORDER BY is_base_price, network, name"""


class Token:
    def __init__(self, network, name, address, is_base_price):
        self.network = network
        self.name = name
        self.address = Web3.toChecksumAddress(address)
        self.decimals = 0
        self.is_base_price = is_base_price
        return

    def __str__(self):
        return f"""network: {self.network}, name: {self.name}, address: {self.address}, is_base_price: {self.is_base_price}"""


def findToken(networkName, tokenName) -> Token:
    for t in myDB.tokens:
        if t.network == networkName and t.name == tokenName:
            if t.decimals == 0 and t.address != myWeb3.base_address:
                print(f'decimals for {tokenName} is not found. querying from the blockchain...')
                network = Network.findNetwork(networkName)
                t.decimals = myWeb3.getDecimals(network.w3, t.address)
                print(f'decimals: {t.decimals}')
            return t
    print(f'unable to find {tokenName}')
    return None
