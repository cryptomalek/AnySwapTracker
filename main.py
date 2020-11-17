import time
from datetime import datetime
import myDB
import myWeb3
import exchange_db
import CMC
import util
import Token, Network, Wallet


def loadExchangeData():
    for v in exchange_db.getVOL():
        exchange_db.addVOL(v)
        print(f'Querying trade volume for pair "{v.name}"')
    return


def loadMarketCapData():
    print('Querying marketcap info...')
    nonCircBalances = myWeb3.getCirc()
    mc = nonCircBalances[6] * anyPrice
    cmc_rank = CMC.getCMCRank(mc)
    print(f'Circulating supply: {nonCircBalances[6]}')
    print(f'cmc_rank: {cmc_rank}')
    print(f'mc: {mc}')
    myDB.addMarketcap(nonCircBalances[6], anyPrice, nonCircBalances[0], nonCircBalances[1], nonCircBalances[2], nonCircBalances[3], nonCircBalances[4], nonCircBalances[5], cmc_rank,
                      anyPrice / myWeb3.basePrices['FSN'])
    return


def loadNetworks():
    try:
        rows = myDB.getRows(Network.select_all_sql)
        if not rows:
            print('Failed to load Networks. Exiting...')
            return False
        for r in rows:
            n = Network.Network(r)
            myDB.networks.append(n)
        print("The number of Networks: ", len(rows))
        return True
    except Exception as e:
        util.error()
        print(e)
        return False


def loadWallets():
    try:
        rows = myDB.getRows(Wallet.select_all_sql)
        if not rows:
            print('Failed to load Wallets. Exiting...')
            return False
        for r in rows:
            wallet = Wallet.Wallet(r[0], r[1], r[2])
            myDB.wallets.append(wallet)
        print("The number of Wallets: ", len(rows))
        return True
    except Exception as e:
        util.error()
        print(e)
        return False


def loadTokens():
    try:
        rows = myDB.getRows(Token.select_all_sql)
        if not rows:
            print('Failed to load Tokens. Exiting...')
            return False
        for r in rows:
            token = Token.Token(r[0], r[1], r[2], r[3])
            myDB.tokens.append(token)
        print("The number of Tokens: ", len(rows))
        return True
    except Exception as e:
        util.error()
        print(e)
        return False


if __name__ == '__main__':
    if not loadNetworks() or not loadWallets() or not loadTokens():
        exit()
    while True:
        try:
            print(datetime.now())
            anyPrice = myWeb3.getAnyPrice()
            myWeb3.basePrices['ANY'] = anyPrice
            print(f'AnyPrice: {anyPrice}')
            for w in myDB.wallets:
                print(f'Querying balance data for {w.lp} (Address: {w.address})')
                network = Network.findNetwork(w.network)
                anyToken = Token.findToken(w.network, 'ANY')
                lpToken = Token.findToken(w.network, w.lp)
                baseToken = Token.findToken(w.network, w.baseTokenName)
                pairToken = Token.findToken(w.network, w.pairTokenName)
                anyBalance = myWeb3.getBalance(network.w3, w.address, anyToken.address, anyToken.decimals)
                lpBalance = myWeb3.getBalance(network.w3, w.address, lpToken.address, lpToken.decimals)
                lpTotalSupply = myWeb3.getTotalSupply(network.w3, lpToken.address)
                baseTotalSupply = myWeb3.getBalance(network.w3, lpToken.address, baseToken.address, baseToken.decimals)
                pairTotalSupply = myWeb3.getBalance(network.w3, lpToken.address, pairToken.address, pairToken.decimals)
                if lpToken.is_base_price:
                    basePrice = pairTotalSupply / baseTotalSupply
                    myWeb3.basePrices[baseToken.name] = basePrice
                    print(f'{baseToken.name} Price:  {basePrice}')
                else:
                    basePrice = myWeb3.basePrices[baseToken.name]
                myDB.addBalance(w.network, w.lp, anyBalance, lpBalance, lpTotalSupply, baseTotalSupply, pairTotalSupply, anyPrice, basePrice)
            loadExchangeData()
            loadMarketCapData()
            print('Completed', datetime.now())
        except Exception as error:
            util.error()
            print(error)
        time.sleep(600)
