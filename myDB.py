#!/usr/bin/python

import psycopg2
import myWeb3
from config import config
import util

networks = []
tokens = []
wallets = []


def getRows(sql):
    conn = None
    rows = []
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        util.error()
        print(error)
        rows = []
    finally:
        if conn is not None:
            conn.close()
    return rows


def addBalance(network, lp, anyBalance, lpBalance, lpTotalSupply, baseTotalSupply, pairTotalSupply, anyPrice, basePrice):
    """ insert a new vendor into the vendors table """
    sql = f"""INSERT INTO public.balance (network, lp, anybalance, lpbalance, lptotalsupply, basetotalsupply, pairtotalsupply, anyprice, baseprice)
             VALUES('{network}', '{lp}', {anyBalance}, {lpBalance}, {lpTotalSupply}, {baseTotalSupply}, {pairTotalSupply}, {anyPrice}, {basePrice});"""
    execSql(sql)
    return


def addMarketcap(circ, price, swap_rewards, company_alloc, team_alloc, liq_rewards, awn_alloc, community_alloc, cmc_rank, fsnprice):
    """ insert a new vendor into the vendors table """
    sql = f"""INSERT INTO public.marketcap (circ, price, company_alloc, team_alloc, liq_rewards, awn_alloc, community_alloc, swap_rewards, cmc_rank, fsnprice)
             VALUES({circ}, {price}, {company_alloc}, {team_alloc}, {liq_rewards}, {awn_alloc}, {community_alloc}, {swap_rewards}, {cmc_rank}, {fsnprice});"""
    execSql(sql)
    return


def execSql(sql):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        util.error()
        print(error)
    finally:
        if conn is not None:
            conn.close()
