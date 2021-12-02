from typing import List, Union

import requests
import pandas as pd
from pandas import DataFrame
from requests_html import HTMLSession

class OptionsChain:
    option_chain: Union[DataFrame, List[DataFrame], List[Union[DataFrame, List[DataFrame]]], None]

    def __init__(self,symbol,calls_or_puts,date_or_strike=None):

        '''
        :param calls_or_puts: Want 'calls' or 'puts'
        :param by_date_or_strike: 'date' for vertical spreads 'strike' for calendar spreads
        :param date: Specicific strike date Y-m-d 2020-12-18
        :param strike: Specific strike, None will iterate over many
        '''
        self.symbol=symbol

        # input catching
        calls_or_puts=calls_or_puts.lower()
        if calls_or_puts==('call' or 'calls'):
            self.calls_or_puts='call'
        elif calls_or_puts==('put' or 'puts'):
            self.calls_or_puts='put'
        elif calls_or_puts =='both':
            self.calls_or_puts='both'
        else:
            raise ValueError('calls or puts?')

        # decide if its a date or number and return accordingly
        try:
            self.strike=int(date_or_strike)
            self.option_chain=self.for_calendar()

        except ValueError:
            self.date=date_or_strike.lower()
            self.option_chain=self.for_vertical()

        except AttributeError:
            pass

    def get_strikes(self):
        URL=f'https://finance.yahoo.com/quote/{self.symbol}/options?straddle=false'
        tables = pd.read_html(URL)

        calls = tables[0].copy()
        puts = tables[1].copy()

        if self.calls_or_puts=='call':
            call_strikes = calls['Strike']
            self.strikes=call_strikes
            return call_strikes

        elif self.calls_or_puts=='put':
            put_strikes = puts['Strike']
            self.strikes=put_strikes
            return put_strikes

    def get_expiration_dates(self,return_dates=False):
        """Scrapes the expiration dates from each option chain for input ticker
           @param: ticker"""
        site = f'https://finance.yahoo.com/quote/{self.symbol}/options?p={self.symbol}'
        resp = requests.get(url=site)
        html = resp.text
        splits = html.split("</option>")
        dates = [elt[elt.rfind(">"):].strip(">") for elt in splits]
        dates = [elt for elt in dates if elt != '']
        self.expiration_dates=dates
        return dates

    def for_calendar(self):
        if self.strike:
            URL = f'https://finance.yahoo.com/quote/{self.symbol}/options?strike={self.strike}&straddle=false'
            tables = pd.read_html(URL)
            if self.calls_or_puts == 'call':
                calls = tables[0].copy()
                return calls
            elif self.calls_or_puts == 'put':
                put = tables[1].copy()
                return put
            elif self.calls_or_puts=='both':
                return tables
        else:
            final = list()
            self.get_strikes()
            for strikes in self.strikes:
                URL = f'https://finance.yahoo.com/quote/{self.symbol}/options?strike={strikes}&straddle=false'
                tables = pd.read_html(URL)

                if self.calls_or_puts == 'call':
                    final = final.append(tables[0].copy())
                elif self.calls_or_puts == 'put':
                    final = final.append(tables[1].copy())
                elif self.calls_or_puts == 'both':
                    final = final.append(tables.copy())

            return final

    def for_vertical(self):
        final=pd.DataFrame()
        if self.date:
            date=str(int(pd.Timestamp(self.date).timestamp()))
            URL=f'https://finance.yahoo.com/quote/{self.symbol}/options?&date={date}'
            tables = pd.read_html(URL)

            if self.calls_or_puts == 'call':
                calls = tables[0].copy()
                return calls
            elif self.calls_or_puts == 'put':
                put=tables[1].copy()
                return put
        else:
            self.get_expiration_dates()
            for days in self.expiration_dates:
                date = str(int(pd.Timestamp(days).timestamp()))
                URL = f'https://finance.yahoo.com/quote/{self.symbol}/options?&date={date}'
                tables = pd.read_html(URL)

                if self.calls_or_puts == 'call':
                    final.index[days].extend(tables[0])
                elif self.calls_or_puts == 'put':
                    try:
                        final = final.append(tables[1])
                    except:
                        final = tables[1]

                elif self.calls_or_puts == 'both':
                    try:
                        final = final.append(tables)
                    except:
                        final = tables
            return final
