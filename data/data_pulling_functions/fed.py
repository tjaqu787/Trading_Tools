import pandas as pd
import requests
from time import sleep
from functools import cache


@cache
def data_from_fed(indicator, name_of_series=None, start_date='2015-01-01', end_date=None,
                  file_type='json', freq=None, aggregation_method=None, remove_na=True,exception_call=False):
    '''
    https://fred.stlouisfed.org/docs/api/fred/series.htmlParameters
api_key
Read API Keys for more information. 32 character alpha-numeric lowercase string, required

file_type
A key or file extension that indicates the type of file to send.
    string, optional, default: xml
    One of the following values: 'xml', 'json'

    xml = Extensible Markup Language. The HTTP Content-Type is text/xml.
    json = JavaScript Object Notation. The HTTP Content-Type is application/json.

series_id
The id for a series.
    string, required

realtime_start
The start of the real-time period. For more information, see Real-Time Periods.
    YYYY-MM-DD formatted string, optional, default: today's date
realtime_end
The end of the real-time period. For more information, see Real-Time Periods.
    YYYY-MM-DD formatted string, optional, default: today's date
    frequency

An optional parameter that indicates a lower frequency to aggregate values to. The FRED frequency aggregation feature converts higher frequency data series into lower frequency data series (e.g. converts a monthly data series into an annual data series). In FRED, the highest frequency data is daily, and the lowest frequency data is annual. There are 3 aggregation methods available- average, sum, and end of period. See the aggregation_method parameter.

    string, optional, default: no value for no frequency aggregation
    One of the following values: 'd', 'w', 'bw', 'm', 'q', 'sa', 'a', 'wef', 'weth', 'wew', 'wetu', 'wem', 'wesu', 'wesa', 'bwew', 'bwem'


    Note that an error will be returned if a frequency is specified that is higher than the native frequency of the series. For instance if a series has the native frequency 'Monthly' (as returned by the fred/series request), it is not possible to aggregate the series to the higher 'Daily' frequency using the frequency parameter value 'd'.
    No frequency aggregation will occur if the frequency specified by the frequency parameter matches the native frequency of the series. For instance if the value of the frequency parameter is 'm' and the native frequency of the series is 'Monthly' (as returned by the fred/series request), observations will be returned, but they will not be aggregated to a lower frequency.
    For most cases, it will be sufficient to specify a lower frequency without a period description (e.g. 'd', 'w', 'bw', 'm', 'q', 'sa', 'a') as opposed to frequencies with period descriptions (e.g. 'wef', 'weth', 'wew', 'wetu', 'wem', 'wesu', 'wesa', 'bwew', 'bwem') which only exist for the weekly and biweekly frequencies.
        The weekly and biweekly frequencies with periods exist to offer more options and override the default periods implied by values 'w' and 'bw'.
        The value 'w' defaults to frequency and period 'Weekly, Ending Friday' when aggregating daily series.
        The value 'bw' defaults to frequency and period 'Biweekly, Ending Wednesday' when aggregating daily and weekly series.
        Consider the difference between values 'w' for 'Weekly' and 'wef' for 'Weekly, Ending Friday'. When aggregating observations from daily to weekly, the value 'w' defaults to frequency and period 'Weekly, Ending Friday' which is the same as 'wef'. Here, the difference is that the period 'Ending Friday' is implicit for value 'w' but explicit for value 'wef'. However, if a series has native frequency 'Weekly, Ending Monday', an error will be returned for value 'wef' but not value 'w'.
    Note that frequency aggregation is currently only available for file_type equal to xml or json due to time constraints.
    Read the 'Frequency Aggregation' section of the FRED FAQs for implementation details.

aggregation_method
A key that indicates the aggregation method used for frequency aggregation. This parameter has no affect if the frequency parameter is not set.
    string, optional, default: avg
    One of the following values: 'avg', 'sum', 'eop'

    avg = Average
    sum = Sum
    eop = End of Period

output_type
An integer that indicates an output type.

    integer, optional, default: 1
    One of the following values: '1', '2', '3', '4'
    1 = Observations by Real-Time Period
    2 = Observations by Vintage Date, All Observations
    3 = Observations by Vintage Date, New and Revised Observations Only
    4 = Observations, Initial Release Only
    For output types '2' and '3', some XML attribute names start with the series ID which may have a first character that is a number (i.e. 0 through 9). In this case only, the XML attribute name starts with an underscore then the series ID in order to avoid invalid XML. If the series ID starts with a letter (i.e. A through Z) then an underscore is not prepended.
    For more information, read: https://alfred.stlouisfed.org/help/downloaddata#outputformats

    '''
    '''    Frequencies without period descriptions:
    d = Daily
    w = Weekly
    bw = Biweekly
    m = Monthly
    q = Quarterly
    sa = Semiannual
    a = Annual
    Frequencies with period descriptions:
    wef = Weekly, Ending Friday
    weth = Weekly, Ending Thursday
    wew = Weekly, Ending Wednesday
    wetu = Weekly, Ending Tuesday
    wem = Weekly, Ending Monday
    wesu = Weekly, Ending Sunday
    wesa = Weekly, Ending Saturday
    bwew = Biweekly, Ending Wednesday
    bwem = Biweekly, Ending Monday
'''

    api_key = 'cc886be1d4badb25435d5d4032d25cfc'
    url = f'https://api.stlouisfed.org/fred/series/observations?series_id={indicator}'
    if start_date:
        url = url + f'&observation_start={start_date}'
    if end_date:
        url = url + f'&observation_end={end_date}'
    url = url + f'&api_key={api_key}'

    if freq:
        if aggregation_method:
            # avg = Average,sum = Sum,eop = End of Period
            url = url + f'&frequency={freq}&aggregation_method={aggregation_method}'
        else:
            print('Must specify aggregation_method("avg" = Average,"sum" = Sum,"eop"=End of Period) with a change in freq')
            return

    url = url + f'&file_type={file_type}'
    try:
        response = requests.get(url)
        dictr = response.json()
        recs = dictr['observations']
        data = pd.json_normalize(recs)

    except:
        print('oops something went wrong, check input')
        if not exception_call:
            sleep(6.0)
            data_from_fed(indicator, name_of_series=None, start_date='2015-01-01', end_date=None,
                  file_type='json', freq=None, aggregation_method=None, remove_na=True,exception_call=True)
        print(indicator, name_of_series, start_date, end_date, freq, aggregation_method, file_type)
        print(url)
        raise ValueError

    if remove_na:
        data = data[data['value'] != '.']
        data.dropna()
    data = data[['date', 'value']]
    print(name_of_series)
    if name_of_series is None:
        data.rename(columns={'value': indicator}, inplace=True)
    else:
        data.rename(columns={'value': name_of_series}, inplace=True)
    return data
