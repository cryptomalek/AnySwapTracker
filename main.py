from web3 import Web3
import time
from datetime import datetime
import myDB
import myWeb3
import exchange_db
import CMC


def getTokenAddress(network, tokenName, tokensList):
    for t in tokensList:
        if t.network == network and t.name == tokenName:
            return Web3.toChecksumAddress(t.address)
    return '0'


if __name__ == '__main__':
    print(myWeb3.getFTMbalance())
    exit()
    tokens = myDB.getTokens()
    wallets = myDB.getWallets()
    while True:
        try:
            anyPrice = myWeb3.getPrice('ANY')
            fsnPrice = myWeb3.getPrice('FSN')
            bnbPrice = myWeb3.getPrice('BNB')
            print(datetime.now())
            print(f'ANY Price: {anyPrice}\nFSN Price: {fsnPrice}\nBNB Price: {bnbPrice}')
            for v in exchange_db.getVOL(fsnPrice, bnbPrice):
                exchange_db.addVOL(v)
                print(f'Querying trade volume for pair "{v.name}"')
            for w in wallets:
                print(f'Querying balance data for {w.lp} (Address: {w.address})')
                network = w.network
                w.address = Web3.toChecksumAddress(w.address)
                lp = w.lp
                anyAddress = getTokenAddress(network, 'ANY', tokens)
                lpAddress = getTokenAddress(network, lp, tokens)
                baseTokenAddress = getTokenAddress(network, w.baseTokenName, tokens)
                pairTokenAddress = getTokenAddress(network, w.pairTokenName, tokens)
                anyBalance = myWeb3.getBalance(network, w.address, anyAddress)
                lpBalance = myWeb3.getBalance(network, w.address, lpAddress)
                lpTotalSupply = myWeb3.getTotalSupply(network, lpAddress)
                baseTotalSupply = myWeb3.getBalance(network, lpAddress, baseTokenAddress)
                pairTotalSupply = myWeb3.getBalance(network, lpAddress, pairTokenAddress)
                if network == "FSN":
                    basePrice = fsnPrice
                else:
                    basePrice = bnbPrice
                myDB.addBalance(network, lp, anyBalance, lpBalance, lpTotalSupply, baseTotalSupply, pairTotalSupply, anyPrice, basePrice)
            # circ, price, company_alloc, team_alloc, liq_rewards, awn_alloc, community_alloc, swap_rewards
            print('Querying marketcap info...')
            nonCircBalances = myWeb3.getCirc()
            mc = nonCircBalances[6] * anyPrice
            cmc_rank = CMC.getCMCRank(mc)
            print(f'Circulating supply: {nonCircBalances[6]}')
            print(f'cmc_rank: {cmc_rank}')
            print(f'mc: {mc}')
            myDB.addMarketcap(nonCircBalances[6], anyPrice, nonCircBalances[0], nonCircBalances[1], nonCircBalances[2], nonCircBalances[3], nonCircBalances[4], nonCircBalances[5], cmc_rank,
                              anyPrice / fsnPrice)
            print('Completed', datetime.now())
        except Exception as error:
            print(error)
        time.sleep(600)
    exit()
