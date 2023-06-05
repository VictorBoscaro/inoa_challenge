from django.core.management.base import BaseCommand
from get_and_update_data.models import B3Companie, AssetPrice
from get_and_update_data.entities.get_and_upload_data import UploadData
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
import os

if "DJANGO_SETTINGS_MODULE" in os.environ:
    print("Django settings is in the enviroment")
else:
    print("Django is not in the project")


class Command(BaseCommand):

    help = "Command to retrieve data from the API"
    
    def __init__(self):
        super().__init__()

        self.b3_companies = {
            'RADL3.SA': 60,
            'BBDC4.SA': 60,
            'CMIG4.SA': 60,
            'BBDC3.SA': 60,
            'JBSS3.SA': 60,
            'EQTL3.SA': 60,
            'BBSE3.SA': 60,
            'CCRO3.SA': 60,
            'BRKM5.SA': 60,
            'USIM5.SA': 60,
            'MULT3.SA': 60,
            'ITSA4.SA': 60,
            'BBAS3.SA': 60,
            'ENBR3.SA': 60,
            'OIBR4.SA': 60,
            'ECOR3.SA': 60,
            'UGPA3.SA': 60,
            'KLBN11.SA': 60,
            'PETR3.SA': 60,
            'SBSP3.SA': 60,
            'LREN3.SA': 60,
            'PETR4.SA': 60
        }

        self.final_df = None

    def handle(self, *args, **options):

        b3_companies = self.b3_companies
        start_date = pd.to_datetime("2023-04-01")
        end_date = pd.to_datetime("2023-06-05")

        final_df = self.get_new_data(start_date, end_date, b3_companies)

        if not final_df.empty:
            final_df.columns = ['datetime', 'open', 'high', 'low', 'close', 'adj_close', 'volume', 'run', 'symbol']
            self.final_df = final_df
        else:
            print("Data frame is empty")

    def call_yahoo_api(self, start_date, end_date, update_freq, run, company):
        print(int(start_date.timestamp()), int(end_date.timestamp()))

        data = yf.download(company, 
                            start = int(start_date.timestamp()), 
                            end = int(end_date.timestamp()), 
                            interval = update_freq)

        data['run'] = run
        data['symbol'] = company

        return data.reset_index()

    def get_new_data(self, start_date, end_date, companies_to_update):
    

        final_dfs = []
        run = datetime.now()

        for company, update_freq in companies_to_update.items():
                
            update_freq = f"{update_freq}m"
            data = self.call_yahoo_api(start_date, end_date, update_freq, run, company)
            #print(data)
            final_dfs.append(data)     

        if final_dfs:
            final_df = pd.concat(final_dfs, axis = 0)
            return final_df
        else:
            return pd.DataFrame()


class UploadData:

    def __init__(self, data_to_upload):

        self._data_to_upload = data_to_upload

    def handle(self):

        self.upload_new_data()


    def upload_new_data(self):

        data = self._data_to_upload
        data_uploaded = []

        for _, row in data.iterrows():
            datetime = row['datetime']
            symbol = row['symbol']
            
            # Check if a record with the same datetime and symbol already exists
            if not AssetPrice.objects.filter(datetime=datetime, symbol=symbol).exists():
                
                # Create a new instance of AssetPrice and save it to the database
                asset_price = AssetPrice(
                    datetime=datetime,
                    symbol=symbol,
                    open=row['open'],
                    high=row['high'],
                    low=row['low'],
                    close=row['close'],
                    adj_close=row['adj_close'],
                    volume=row['volume'],
                    run=row['run']
                )
                asset_price.save()
                #data_uploaded.append([row['datetime'], row['symbol'], row['open'], row['high'], row['close'], row['adj_close'], row['volume'], row['run']])
            else:
                print("There is not new data to upload")
        
        return data_uploaded
    
class UpdateCompanies:

    def __init__(self):
        self.b3_companies = {
                'RADL3.SA': 60,
                'BBDC4.SA': 60,
                'CMIG4.SA': 60,
                'BBDC3.SA': 60,
                'JBSS3.SA': 60,
                'EQTL3.SA': 60,
                'BBSE3.SA': 60,
                'CCRO3.SA': 60,
                'BRKM5.SA': 60,
                'USIM5.SA': 60,
                'MULT3.SA': 60,
                'ITSA4.SA': 60,
                'BBAS3.SA': 60,
                'ENBR3.SA': 60,
                'OIBR4.SA': 60,
                'ECOR3.SA': 60,
                'UGPA3.SA': 60,
                'KLBN11.SA': 60,
                'PETR3.SA': 60,
                'SBSP3.SA': 60,
                'LREN3.SA': 60,
                'PETR4.SA': 60
            }
    
    def handle(self):
        for key, value in self.b3_companies.items():

            if not B3Companie.objects.filter(symbol=key, minutes_update_rate=value).exists():
                    
                    # Create a new instance of AssetPrice and save it to the database
                    companies = B3Companie(
                        symbol = key,
                        minutes_update_rate = value
                    )

                    companies.save()

# command = Command()
# command.handle()
# final_df = command.final_df
# upload_data = UploadData(final_df)
# upload_data.upload_new_data()


# companies_update = UpdateCompanies()
# companies_update.handle()


granularity = """1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d"""
granularities = list(map(lambda x: x.strip(), granularity.split(',')))


start_date = (datetime.today() - timedelta(30)).strftime("%Y-%m-%d")
end_date = datetime.today().strftime('%Y-%m-%d')
run = datetime.now()

b3_companies = Command().b3_companies.keys()

final_df = pd.DataFrame()

for company in b3_companies:
    
    print(company)
    for granularity in granularities:
        print(granularity)
        if granularity == '1m':
            date_range = pd.date_range(datetime.today() - timedelta(29), end_date, freq = '7D')
            for date in date_range:
                
                from_date = (date).strftime("%Y-%m-%d")
                to_date = (date + timedelta(7)).strftime("%Y-%m-%d")
                
                print(f"start_date: {from_date}, end_date: {to_date}")
                data = yf.download(company, start = from_date, end = to_date, interval = granularity)
                data['run'] = run
                data['symbol'] = company
                data['granularity'] = granularity
                final_df = pd.concat([final_df, data], axis = 0)
                
        if granularity in ['60m', '90m', '1h', '1d']:
            data = yf.download(company, start = start_date, end = end_date, interval = granularity)
            data['run'] = run
            data['symbol'] = company
            data['granularity'] = granularity
            final_df = pd.concat([final_df, data], axis = 0)
        
        else:
            date_range = pd.date_range(datetime.today() - timedelta(59), end_date, freq = '60D')
            for date in date_range:
                from_date = (date).strftime("%Y-%m-%d")
                to_date = (date + timedelta(60)).strftime("%Y-%m-%d")
                
                if (date + timedelta(60)) > datetime.today():
                    to_date = datetime.today()
                
                data = yf.download(company, start = from_date, end = to_date, interval = granularity)
                data['run'] = run
                data['symbol'] = company
                data['granularity'] = granularity
                final_df = pd.concat([final_df, data], axis = 0)


final_df = final_df.reset_index()
final_df.columns = ['datetime', 'open', 'high', 'low', 'close', 'adj_close', 'volume', 'run', 'symbol', 'granularity']
final_df['open'] = final_df.open.round(4)
final_df['high'] = final_df.high.round(4)
final_df['low'] = final_df.low.round(4)
final_df['close'] = final_df.close.round(4)
final_df['adj_close'] = final_df.adj_close.round(4)
final_df['volume'] = final_df.volume.round(4)
print(final_df.info())

for _, row in final_df.iterrows():
    datetime = row['datetime']
    granularity = row['granularity']
    symbol = row['symbol']
    print(datetime, symbol, granularity, row['open'], row['close'], row['low'], row['high'], row['adj_close'], row['volume'], row['run'])
    
    if not AssetPrice.objects.filter(datetime=datetime, symbol=symbol, granularity=granularity).exists():
                
                # Create a new instance of AssetPrice and save it to the database
                asset_price = AssetPrice(
                    datetime=datetime,
                    symbol=symbol,
                    open=row['open'],
                    high=row['high'],
                    low=row['low'],
                    close=row['close'],
                    adj_close=row['adj_close'],
                    volume=row['volume'],
                    run=row['run'],
                    granularity=granularity
                )
                asset_price.save()