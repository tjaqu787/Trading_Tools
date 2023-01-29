import pandas as pd

def real_treasury_yields(all_year_current_month='current'):
    '''
    :param all_year_current_month: can download full years current month or all
    :return: ['Date', '5 YR', '7 YR', '10 YR', '20 YR', '30 YR']
    '''

    'http://www.treasurydirect.gov/TA_WS/securities/auctioned?format=html&type=FRN'
    url=""
    try:
        all_year_current_month=int(all_year_current_month)
        year = f'Year&year={all_year_current_month}'
    except AttributeError:

        if all_year_current_month.lower()=='all':
            year="All"
        else:
            year=''

    url=f'https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=realyield{year}'

    df = pd.read_html(url)[1]
    df.rename(columns={'DATE':'Date'},inplace=True)
    df.set_index('Date',inplace=True)

    return df


def nominal_treasury_yields(all_year_current_month='current'):
    '''
    :param all_year_current_month: can download full years current month or all
    :return: [ 'Date',  '1 mo',  '2 mo',  '3 mo',  '6 mo',  '1 yr',  '2 yr',  '3 yr',
  '5 yr',  '7 yr', '10 yr', '20 yr', '30 yr']
    '''

    'http://www.treasurydirect.gov/TA_WS/securities/auctioned?format=html&type=FRN'
    url=""
    try:
        all_year_current_month=int(all_year_current_month)
        year = f'Year&year={all_year_current_month}'
    except AttributeError:

        if all_year_current_month.lower()=='all':
            year="All"
        else:
            year=''
    url=f'https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield{year}'
    df = pd.read_html(url)[1]
    df.set_index('Date',inplace=True)

    return df
