from get_and_update_data.companies_configs import B3Companies
from datetime import datetime
import yfinance as yf
import pandas as pd
from datetime import datetime
from datetime import timedelta
from get_and_update_data.models import AssetPrice
from django.db import models

class UpdateFrequency:
    
    def __init__(self, freq = "60m"):
        self.freq = freq

class PriceGetter:
 
    def __init__(self, companies_instance = B3Companies()):
        self._configs = companies_instance._configs
        
    def companies_to_get_data(self):
        
        now = datetime.today()
        companies_to_get_data = []
        
        results = AssetPrice.objects.values("symbol").annotate(max_run=models.Max('run'), max_datetime=models.Max("datetime"))
        max_datetime_dict = {}

        for result in results:
            
            symbol = result['symbol']
            max_run = result['max_run'].replace(tzinfo=None)
            max_datetime = result['max_datetime']

            max_run = datetime(2023, 5, 26, 11) #### COMENTAR ESSA LINHA PARA QUANDO O CÓDIGO FOR PARA PRODUÇÃO
            
            if (now - max_run).total_seconds() // 60 >= self._configs[symbol]:
                companies_to_get_data.append(symbol)
                max_datetime_dict[symbol] = max_datetime
            else:
                print(f"Company {symbol} was updated less than {self._configs[symbol]} minutes ago.")
                
        return companies_to_get_data, max_datetime_dict
    
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
        run = datetime(2023, 5, 26, 11) ######## COMENTAR ESSA LINHA QUANDO O CÓDIGO FOR PARA PRODUÇÃO
        
        for company in companies_to_update:
            
            start_date = max_datetime_dict[company] 
            start_date = datetime(2023, 5, 26, 11) ######## COMENTAR ESSA LINHA QUANDO O CÓDIGO FOR PARA PRODUÇÃO
            end_date = start_date + timedelta(minutes=60)
                
            if (run.hour >= 10) & (run.hour <= 16):
                print("Calling yahoo finance API.")
                start_date = run
                end_date = run + timedelta(minutes=60)
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

    def __init__(self, price_getter = PriceGetter()):

        self._data_to_upload = price_getter.get_new_data()


    def upload_new_data(self):

        data = self._data_to_upload

        for _, row in data.iterrows():
            datetime = row['datetime']
            symbol = row['symbol']
            
            # Check if a record with the same datetime and symbol already exists
            if not AssetPrice.objects.filter(datetime=datetime, symbol=symbol).exists():
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
            else:
                print("There is not new data to upload")