import citizen_debt_savings
import cpi
import delinquency_rates
import ppi
import quarterly_statements
import rate


# this is a function pulls all data from the FRED API and saves it to the db
# It will be replaced with code that downloads the fred release calendar and runs the code at release
# also could make this run asynchronously to speed up the process


def pull_all_data(start_date='1995-01-01', replace=True):
    ppi.download_PPI_data(start_date, replace)
    quarterly_statements.download_quarterly_data(start_date, replace)
    citizen_debt_savings.download_data(start_date, replace)
    rate.download_rate_data(start_date, replace)
    delinquency_rates.download_delinquency_data(start_date, replace)
    cpi.download_cpi_data(start_date, replace)

if __name__ == '__main__':
    pull_all_data(replace=True )
