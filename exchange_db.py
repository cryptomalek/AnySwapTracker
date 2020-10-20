import requests
import psycopg2
import myWeb3
from config import config


api_url = 'https://api.anyswap.exchange/ticker'


class VOLRecord:
    def __init__(self, base_id, quote_id, last_price, base_volume, quote_volume, isFrozen, bnbPrice, fsnPrice):
        self.base_id = base_id
        self.quote_id = quote_id
        self.last_price = last_price
        self.base_volume = base_volume
        self.quote_volume = quote_volume
        self.isFrozn = isFrozen
        self.name = self.base_id + '-' + self.quote_id.replace('_', '').replace(self.base_id, '')
        if self.base_id == 'BNB':
            self.price = bnbPrice
        elif self.base_id == 'FSN':
            self.price = fsnPrice
        elif 'USD' in self.base_id:
            self.price = 1
        else:
            raise Exception(f'Unrecognized base {self.base_id}')
        self.vol = float(self.quote_volume) * self.price
        return

    def __str__(self):
        return self.name.ljust(10) + f'${self.vol:,.0f}'


def getVOL(fsnPrice, bnbPrice):
    try:
        result = []
        resp = requests.get(api_url)
        for lp in resp.json().items():
            row = lp[1]
            rec = VOLRecord(row['base_id'], row['quote_id'], row['last_price'], row['base_volume'], row['quote_volume'], row['isFrozen'], bnbPrice, fsnPrice)
            result.append(rec)
        return result
    except Exception as error:
        print(error)
    return


def addVOL(rec: VOLRecord):
    """ insert a new vendor into the vendors table """
    sql = f"""INSERT INTO public.exchange_volume (base_id, quote_id, last_price, base_volume, quote_volume, isfrozen, lp, base_price, vol)
             VALUES('{rec.base_id}', '{rec.quote_id}', {rec.last_price}, {rec.base_volume}, {rec.quote_volume}, {rec.isFrozn}, '{rec.name}', {rec.price}, {rec.vol});"""
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql) # , (network, lp, anyBalance, lpBalance, lpTotalSupply, baseTotalSupply, pairTotalSupply, anyPrice, basePrice))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
