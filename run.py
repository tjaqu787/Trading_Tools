import dash_frontend.app as app
from os import path
import data.data_series_pull.data_update as data_update

if __name__ == '__main__':
    if not path.exists('data/data.db'):
        print('data.db not found, creating new database')
        data_update.pull_all_data(replace=True)
    app.app.run_server(debug=False)


