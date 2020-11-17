from web3 import Web3
select_all_sql = """SELECT network, lp, address FROM wallet ORDER BY is_base_price DESC"""


class Wallet:
    def __init__(self, network, lp, address):
        self.network = network
        self.address = Web3.toChecksumAddress(address)
        self.baseTokenName = lp.split('-')[0]
        self.pairTokenName = lp.split('-')[1]
        self.lp = lp
        return

    def __str__(self):
        return f"""network: {self.network}, address: {self.address}, baseTokenName: {self.baseTokenName}, pairTokenName: {self.pairTokenName}, lp: {self.lp}"""
