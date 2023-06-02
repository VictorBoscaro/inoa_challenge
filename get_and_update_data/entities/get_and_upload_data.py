from get_and_update_data.configs import B3Companies, UpdateFrequency
from datetime import datetime
import yfinance as yf
import pandas as pd
from datetime import datetime
from datetime import timedelta
from get_and_update_data.models import AssetPrice
from django.db import models
import pytz

class TimeZone:

    def __init__(self, timezone = "America/Sao_Paulo"):
        
        self.timezoned = pytz.timezone(timezone)

    def to_timezone(self, obj):

        return self.timezoned.localize(obj)

class PriceGetter:
 
    def __init__(self, companies_instance = B3Companies()):
        self._configs = companies_instance._configs
        
    def companies_to_get_data(self):
        print("Executing companies to get data")
        now = TimeZone().to_timezone(datetime.today())
        companies_to_get_data = []
        
        results = AssetPrice.objects.values("symbol").annotate(max_run=models.Max('run'), max_datetime=models.Max("datetime"))
        max_datetime_from_db_dict = {}

        for result in results:
            
            symbol = result['symbol']
            max_run = result['max_run']
            max_datetime = result['max_datetime']

            # max_run = datetime(2023, 5, 26, 11) #### COMENTAR ESSA LINHA PARA QUANDO O CÓDIGO FOR PARA PRODUÇÃO
            
            if (now - max_run).total_seconds() // 60 >= self._configs[symbol]:
                
                print((now - max_run).total_seconds() // 60, max_run, now)
                companies_to_get_data.append(symbol)
                max_datetime_from_db_dict[symbol] = max_datetime
            else:
                print((now - max_run).total_seconds() // 60, max_run, now)
                print(f"Company {symbol} was updated less than {self._configs[symbol]} minutes ago.")

        print(companies_to_get_data)    
        return companies_to_get_data, max_datetime_from_db_dict
    
    def call_yahoo_api(self, start_date, end_date, update_freq, run, company):
        
        data = yf.download(company, 
                           start = int(start_date.timestamp()), 
                           end = int(end_date.timestamp()), 
                           interval = update_freq)
        
        data['run'] = run
        data['symbol'] = company
        
        return data.reset_index()

    def get_new_data(self):
        
        update_freq = UpdateFrequency().freq
        
        companies_to_update, max_datetime_dict = self.companies_to_get_data()
        
        
        final_df = pd.DataFrame()
        run = datetime.now()
        # run = datetime(2023, 5, 26, 11) ######## COMENTAR ESSA LINHA QUANDO O CÓDIGO FOR PARA PRODUÇÃO
        print(companies_to_update)
        for company in companies_to_update:
            
            last_date_uploaded = max_datetime_dict[company] # This is the last date that was uplo
            # start_date = datetime(2023, 5, 26, 11) ######## COMENTAR ESSA LINHA QUANDO O CÓDIGO FOR PARA PRODUÇÃO
            end_date = last_date_uploaded + timedelta(minutes=60)
            print(last_date_uploaded, end_date)
            if (run.hour >= 10) & (run.hour <= 16):
                print("Calling yahoo finance API.")
                start_date = last_date_uploaded - timedelta(1) # This is needed because I can't call the API with the start and end date being the same day
                data = self.call_yahoo_api(start_date, end_date, update_freq, run, company)
                final_df = pd.concat([final_df, data], axis = 0)
            else:
                print("The hour is off limit, so the API won't be called.")
                
        
        if len(final_df) > 0:
            final_df.columns = ['datetime', 'open', 'high', 'low', 'close', 'adj_close', 'volume', 'run', 'symbol']
        else:
            pass

        return final_df
    

class UploadData():

    def __init__(self, data_to_upload):

        self._data_to_upload = data_to_upload

    def upload_new_data(self):

        data = self._data_to_upload
        data_uploaded = []
        results_list = []
        for _, row in data.iterrows():
            datetime = row['datetime']
            symbol = row['symbol']

            results = AssetPrice.objects.values("symbol").filter(symbol = symbol).annotate(max_datetime=models.Max("datetime"))
            max_datetime = results[0]['max_datetime']
            print(max_datetime, datetime)
            # Check if a record with the same datetime and symbol already exists
            # if not AssetPrice.objects.filter(datetime=datetime, symbol=symbol).exists():
            if datetime > max_datetime:
                print(datetime - max_datetime)
                print("Data is being uploaded")
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
                data_uploaded.append([row['datetime'], row['symbol'], row['open'], row['high'], row['close'], row['adj_close'], row['volume'], row['run']])
            else:
                print("There is not new data to upload")
        
        return results_list