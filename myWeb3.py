from web3 import Web3
import json
import Network, Token

nonCircAddresses = ['0x3f7a5b59EbADA1BA45319eE2D6e8aAaaB7dC1862', '0x71c56B08F562F53d0fb617A23F94AB2c9f8e4703', '0xe29972f7a35d89E9EE40F36983021D96340C4863',
                    '0xa96a3A188dA5b1F958e75C169a4A5E22B63f3273', '0x2175546B3121e15FF270D974259644f865C670c3', '0xf2834163568277D4D3Aa93CF15E54700c91CA312']
nonCircBalances = []
basePrices = {}

fany_address = '0x0c74199D22f732039e843366a236Ff4F61986B32'
base_address = '0x0000000000000000000000000000000000000000'

with open('ERC20abi.json') as json_file:
    abi = json.load(json_file)


def getCirc():
    balance = 0
    nonCircBalances.clear()
    for i in range(6):
        w3f = Network.findNetwork('FSN').w3
        contract = w3f.eth.contract(fany_address, abi=abi)
        nonCircBalances.append(contract.functions.balanceOf(nonCircAddresses[i]).call() / 10 ** 18)
        balance += nonCircBalances[i]
    nonCircBalances.append(100000000.0 - balance)
    return nonCircBalances


def getBalance(w3: Web3.HTTPProvider, address, tokenAddress, decimals):
    if tokenAddress == base_address or tokenAddress == '0':
        balance = w3.eth.getBalance(address)
        return float(w3.fromWei(balance, 'ether'))
    else:
        contract = w3.eth.contract(address=tokenAddress, abi=abi)
        balance = contract.functions.balanceOf(address).call()
        return float(balance / (10 ** decimals))


def getTotalSupply(w3: Web3.HTTPProvider, tokenAddress: str) -> float:
    contract = w3.eth.contract(address=tokenAddress, abi=abi)
    balance = contract.functions.totalSupply().call()
    return float(w3.fromWei(balance, 'ether'))


def getDecimals(w3: Web3.HTTPProvider, tokenAddress) -> int:
    contract = w3.eth.contract(address=tokenAddress, abi=abi)
    return contract.functions.decimals().call()


def getAnyPrice():
    fsn_usdt_address = '0x78917333bec47cEe1022b31A136D31FEfF90D6FB'
    fusdt_address = '0xC7c64aC6d46be3d6EA318ec6276Bb55291F8E496'
    fsn_any_address = '0x049DdC3CD20aC7a2F6C867680F7E21De70ACA9C3'
    w3f = Network.findNetwork('FSN').w3
    fsnPrice = float(getBalance(w3f, fsn_usdt_address, fusdt_address, 6)) / float(getBalance(w3f, fsn_usdt_address, base_address, 0))
    return float(fsnPrice * float(getBalance(w3f, fsn_any_address, base_address, 0))) / float(getBalance(w3f, fsn_any_address, fany_address, 18))
