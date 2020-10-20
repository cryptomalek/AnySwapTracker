#!/usr/bin/python

import psycopg2
import myWeb3
from config import config


def getTokens():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("""SELECT t.network, t.name, t.address FROM public.token t ORDER BY t.network, t.name """)
        rows = cur.fetchall()
        print("The number of Tokens: ", cur.rowcount)
        tokens = []
        for row in rows:
            tokens.append(myWeb3.Token(row[0], row[1], row[2]))
        cur.close()
        return tokens
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def getWallets():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("""SELECT t.network, t.lp, t.address FROM public.wallet t """)
        rows = cur.fetchall()
        print("The number of Wallets: ", cur.rowcount)
        tokens = []
        for row in rows:
            tokens.append(myWeb3.Wallet(row[0], row[1], row[2]))
        cur.close()
        return tokens
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def addBalance(network, lp, anyBalance, lpBalance, lpTotalSupply, baseTotalSupply, pairTotalSupply, anyPrice, basePrice):
    """ insert a new vendor into the vendors table """
    sql = f"""INSERT INTO public.balance (network, lp, anybalance, lpbalance, lptotalsupply, basetotalsupply, pairtotalsupply, anyprice, baseprice)
             VALUES('{network}', '{lp}', {anyBalance}, {lpBalance}, {lpTotalSupply}, {baseTotalSupply}, {pairTotalSupply}, {anyPrice}, {basePrice});"""
    execSql(sql)
    return


def addMarketcap(circ, price, swap_rewards, company_alloc, team_alloc, liq_rewards, awn_alloc, community_alloc):
    """ insert a new vendor into the vendors table """
    sql = f"""INSERT INTO public.marketcap (circ, price, company_alloc, team_alloc, liq_rewards, awn_alloc, community_alloc, swap_rewards)
             VALUES({circ}, {price}, {company_alloc}, {team_alloc}, {liq_rewards}, {awn_alloc}, {community_alloc}, {swap_rewards});"""
    execSql(sql)
    return


def execSql(sql):
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
