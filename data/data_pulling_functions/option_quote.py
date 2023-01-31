import pandas as pd
import requests
from functools import lru_cache

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'}

@lru_cache(maxsize=50)
def get_strikes(symbol, calls_or_puts):
    URL = f'https://finance.yahoo.com/quote/{symbol}/options?straddle=false'
    read = requests.get(url=URL, headers=headers)
    tables = pd.read_html(read.text)
    
    calls = tables[0].copy()
    puts = tables[1].copy()
    
    if calls_or_puts == 'call':
        call_strikes = calls['Strike']
        return call_strikes
    
    elif calls_or_puts == 'put':
        put_strikes = puts['Strike']
        return put_strikes


@lru_cache(maxsize=50)
def get_expiration_dates(symbol):
    """Scrapes the expiration dates from each option chain for input ticker
       @param: ticker"""
    #spoof headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/39.0.2171.95 Safari/537.36'}
    site = f'https://finance.yahoo.com/quote/{symbol}/options?p={symbol}'
    resp = requests.get(url=site, headers=headers)
    html = resp.text
    splits = html.split("</option>")
    dates = [elt[elt.rfind(">"):].strip(">") for elt in splits]
    dates = [elt for elt in dates if elt != '']
    return dates


def for_calendar(symbol, strike, calls_or_puts):
    '''
    
    :param symbol: stock symbol
    :param strike: a valid strike price
    :param calls_or_puts: do you want the calls or puts
    :return: the quotes for the symbol with all dates at that strike price
    '''
    if strike:
        URL = f'https://finance.yahoo.com/quote/{symbol}/options?strike={strike}&straddle=false'
        read = requests.get(url=URL, headers=headers)
        tables = pd.read_html(read.text)
        if calls_or_puts == 'call':
            calls = tables[0].copy()
            return calls
        elif calls_or_puts == 'put':
            put = tables[1].copy()
            return put
        elif calls_or_puts == 'both':
            return tables
    else:
        raise ValueError('this function requires: symbol,strike,calls_or_puts')


def for_vertical(symbol, date, calls_or_puts):
    '''
    
    :param symbol: stock symbol
    :param date: what date for the vertical spread
    :param calls_or_puts: call or put spreads
    :return: quotes for the symbol at time date
    '''
    if date:
        date = str(int(pd.Timestamp(date).timestamp()))
        URL = f'https://finance.yahoo.com/quote/{symbol}/options?&date={date}'
        
        read = requests.get(url=URL, headers=headers)
        tables = pd.read_html(read.text)
        
        if calls_or_puts == 'call':
            calls = tables[0].copy()
            return calls
        elif calls_or_puts == 'put':
            put = tables[1].copy()
            return put
    else:
        raise ValueError('')


if __name__ == '__main__':
    print(get_expiration_dates('spy'))
    print(get_strikes('spy', 'call'))
    print(for_calendar('spy', 300, 'call'))
    print(for_vertical('spy', '2020-12-18', 'call'))