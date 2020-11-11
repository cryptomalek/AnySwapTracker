from web3 import Web3
import json
import os

nonCircAddresses = ['0x3f7a5b59EbADA1BA45319eE2D6e8aAaaB7dC1862', '0x71c56B08F562F53d0fb617A23F94AB2c9f8e4703', '0xe29972f7a35d89E9EE40F36983021D96340C4863',
                    '0xa96a3A188dA5b1F958e75C169a4A5E22B63f3273', '0x2175546B3121e15FF270D974259644f865C670c3', '0xf2834163568277D4D3Aa93CF15E54700c91CA312']
nonCircBalances = []
w3e = Web3(Web3.HTTPProvider(
    'https://mainnet.infura.io/v3/25498f326072430f8a9f62f681e3a0da'))
w3b = Web3(Web3.HTTPProvider('https://bsc-dataseed1.binance.org:443'))
fsn_gateway_url = 'https://mainnetpublicgateway1.fusionnetwork.io:10000'
fsn_gateway_url = 'https://gw.redefi.tech'
w3f = Web3(Web3.HTTPProvider(fsn_gateway_url))
ftm_gateway_url = 'https://rpc.fantom.network/%27'
w3ftm = Web3(Web3.HTTPProvider(ftm_gateway_url))
fANY = '0x0c74199D22f732039e843366a236Ff4F61986B32'

with open('ERC20abi.json') as json_file:
    abi = json.load(json_file)


def getCirc():
    balance = 0
    nonCircBalances.clear()
    for i in range(6):
        contract = w3f.eth.contract(fANY, abi=abi)
        nonCircBalances.append(contract.functions.balanceOf(nonCircAddresses[i]).call() / 10 ** 18)
        balance += nonCircBalances[i]
    nonCircBalances.append(100000000.0 - balance)
    return nonCircBalances


class Token:
    def __init__(self, network, name, address):
        if network not in ('ETH', 'FSN', 'BSC'):
            raise Exception('Network shall be either ETH, FSN or BSC')
        self.network = network
        self.name = name
        self.address = Web3.toChecksumAddress(address)
        # self.totalSupply = getTotalSupply(self.network, self.address)
        return


class Wallet:
    def __init__(self, network, lp, address):
        if network not in ('ETH', 'FSN', 'BSC'):
            raise Exception('Network shall be either ETH, FSN or BSC')
        self.network = network
        self.address = address
        self.baseTokenName = lp.split('-')[0]
        self.pairTokenName = lp.split('-')[1]
        self.lp = lp
        # self.totalSupply = getTotalSupply(self.network, self.address)
        # self.totalBaseTokenSupply = getBalance(self.network, self.address, getTokenAddress(network, self.baseTokenName))
        # self.totalPairTokenSupply = getBalance(self.network, self.address, getTokenAddress(network, self.pairTokenName))
        return


class Address:
    def __init__(self, network, address, tokens):
        if network not in ('ETH', 'FSN', 'BSC'):
            raise Exception('Network shall be either ETH, FSN or BSC')
        self.network = network
        self.address = Web3.toChecksumAddress(address)
        self.tokens = tokens
        self.balance = getBalance(self.network, self.address, '0')
        self.tokensBalances = {}
        for token in self.tokens:
            self.tokensBalances[token.name] = getBalance(self.network, self.address, token.address)
        return


def getBalance(network, address, tokenAddress, decimals=0):
    w3 = None
    if network == 'ETH':
        w3 = w3e
    elif network == 'BSC':
        w3 = w3b
    elif network == 'FSN':
        w3 = w3f
    elif network == 'FTM':
        w3 = w3ftm
    if tokenAddress == '0x0000000000000000000000000000000000000000':
        balance = w3.eth.getBalance(address)
        return w3.fromWei(balance, 'ether')
    else:
        contract = w3.eth.contract(address=tokenAddress, abi=abi)
        balance = contract.functions.balanceOf(address).call()
        if decimals == 0:
            decimals = getDecimals(network, tokenAddress)
        return balance / (10 ** decimals)


def getTotalSupply(network, tokenAddress):
    w3 = None
    if network == 'ETH':
        w3 = w3e
    elif network == 'BSC':
        w3 = w3b
    elif network == 'FSN':
        w3 = w3f
    contract = w3.eth.contract(address=tokenAddress, abi=abi)
    balance = contract.functions.totalSupply().call()
    return w3.fromWei(balance, 'ether')


def getDecimals(network, tokenAddress):
    w3 = None
    if network == 'ETH':
        w3 = w3e
    elif network == 'BSC':
        w3 = w3b
    elif network == 'FSN':
        w3 = w3f
    else:
        raise Exception(f'unrecognized network: {network}')
    contract = w3.eth.contract(address=tokenAddress, abi=abi)
    return contract.functions.decimals().call()


def getPrice(token):
    base_address = '0x0000000000000000000000000000000000000000'
    fany_address = '0x0c74199D22f732039e843366a236Ff4F61986B32'
    fusdt_address = '0xC7c64aC6d46be3d6EA318ec6276Bb55291F8E496'
    busdt_address = '0x55d398326f99059fF775485246999027B3197955'
    fsn_any_address = '0x049DdC3CD20aC7a2F6C867680F7E21De70ACA9C3'
    fsn_usdt_address = '0x78917333bec47cEe1022b31A136D31FEfF90D6FB'
    bnb_usdt_address = '0x83034714666B0EB2209Aafc1B1CBB2AB9c6100Db'

    if token == 'FSN':
        return float(getBalance('FSN', fsn_usdt_address, fusdt_address)) / float(getBalance('FSN', fsn_usdt_address, base_address))
    elif token == 'BNB':
        return float(getBalance('BSC', bnb_usdt_address, busdt_address)) / float(getBalance('BSC', bnb_usdt_address, base_address))
    elif token == 'ANY':
        return float(getPrice('FSN') * float(getBalance('FSN', fsn_any_address, base_address))) / float(getBalance('FSN', fsn_any_address, fany_address))
    else:
        raise Exception(f'Unrecognized token in getPrice function: "{token}"')


def getFTMbalance():
    add = '0xB5BAfFb036576B46F45544174208FAa5b7dc1cfB'
    return float(getBalance('FTM', add, '0'))
