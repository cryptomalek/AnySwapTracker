import requests
import psycopg2
import myWeb3
from config import config


api_url = 'https://api.anyswap.exchange/ticker'


class VOLRecord:
    def __init__(self, base_id, quote_id, last_price, base_volume, quote_volume, isFrozen):
        self.base_id = base_id
        self.quote_id = quote_id
        self.last_price = last_price
        self.base_volume = base_volume
        self.quote_volume = quote_volume
        self.isFrozn = isFrozen
        self.name = self.base_id + '-' + self.quote_id.replace('_', '').replace(self.base_id, '')
        if self.base_id in myWeb3.basePrices:
            self.price = myWeb3.basePrices[self.base_id]
        elif 'USD' in self.base_id:
            self.price = 1
        else:
            raise Exception(f'Unrecognized base {self.base_id}')
        self.vol = float(self.quote_volume) * self.price
        return

    def __str__(self):
        return self.name.ljust(10) + f'${self.vol:,.0f}'


def getVOL():
    try:
        result = []
        resp = requests.get(api_url)
        for lp in resp.json().items():
            row = lp[1]
            rec = VOLRecord(row['base_id'], row['quote_id'], row['last_price'], row['base_volume'], row['quote_volume'], row['isFrozen'])
            result.append(rec)
        return result
    except Exception as error:
        print(error)
    return


def addVOL(rec: VOLRecord):
    sql = f"""INSERT INTO public.exchange_volume (base_id, quote_id, last_price, base_volume, quote_volume, isfrozen, lp, base_price, vol)
             VALUES('{rec.base_id}', '{rec.quote_id}', {rec.last_price}, {rec.base_volume}, {rec.quote_volume}, {rec.isFrozn}, '{rec.name}', {rec.price}, {rec.vol});"""
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
