import pandas as pd
from datetime import timedelta, datetime
from get_and_update_data.models import AssetPrice
import yfinance as yf
from django.db.models import Max
from .aux_classes import UpdateRateFreq, TimeZone

class PriceGetter:
 
    def __init__(self, companies_instance = UpdateRateFreq):

        self.b3_companies = companies_instance().get_last_minute_update()
        
    def companies_to_get_data(self):

        now = datetime.now()
        companies_to_get_data = []
        
        results = AssetPrice.objects.values("symbol").annotate(max_run=Max('run'), max_datetime=Max("datetime"))

        max_datetime_from_db_dict = {}

        for result in results:
            
            symbol = result['symbol']
            max_run = result['max_run']
            max_datetime = result['max_datetime']
            
            # max_run = datetime(2023, 5, 26, 11) #### COMENTAR ESSA LINHA PARA QUANDO O CÓDIGO FOR PARA PRODUÇÃO
            
            if (now - max_run).total_seconds() // 60 >= self.b3_companies[symbol]:
                
                companies_to_get_data.append(symbol)
                max_datetime_from_db_dict[symbol] = max_datetime
            else:
        
                print(f"Company {symbol} was updated less than {self.b3_companies[symbol]} minutes ago.")
 
        return companies_to_get_data, max_datetime_from_db_dict
    
    def call_yahoo_api(self, start_date, end_date, update_freq, run, company):
        
        data = yf.download(company, 
                           start = int(start_date.timestamp()), 
                           end = int(end_date.timestamp()), 
                           interval = update_freq)
    
        data['run'] = run
        data['symbol'] = company
        data['granularity'] = update_freq
        data = data.reset_index()
        print(len(data))
        if not data.empty:
            print('changing columns')
            data.columns = ['datetime', 'open', 'high', 'low', 'close', 'adj_close', 'volume', 'run', 'symbol', 'granularity']
        
        return data
        

    def get_new_data(self):
        
        companies_to_update, max_datetime_dict = self.companies_to_get_data()
        
        final_df = pd.DataFrame()
        run = datetime.now()
        # run = datetime(2023, 5, 26, 11) ######## COMENTAR ESSA LINHA QUANDO O CÓDIGO FOR PARA PRODUÇÃO
        for company in companies_to_update:
            
            last_date_uploaded = max_datetime_dict[company] # This is the last date that was uploaded
            # start_date = datetime(2023, 5, 26, 11) ######## COMENTAR ESSA LINHA QUANDO O CÓDIGO FOR PARA PRODUÇÃO
            end_date = datetime.today() + timedelta(1)
            print(end_date)
            if (run.hour >= 10) & (run.hour <= 18):
                print("Calling yahoo finance API.")
                start_date = last_date_uploaded - timedelta(1) # This is needed because I can't call the API with the start and end date being the same day
                for update_freq in ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d']:
                    data = self.call_yahoo_api(start_date, end_date, update_freq, run, company)
                    final_df = pd.concat([final_df, data], axis = 0)
            else:
                print("The hour is off limit, so the API won't be called.")
        
        return final_df
    
class DataUpdater:

    def __init__(self, data_to_upload = PriceGetter):

        self._data_to_upload = data_to_upload().get_new_data()

    def update_data(self):

        data = self._data_to_upload
        data_uploaded = []
        results_list = []
        for _, row in data.iterrows():
            datetime = row['datetime']
            symbol = row['symbol']
            granularity = row['granularity']
            
            
            results = AssetPrice.objects.values("symbol").filter(symbol=symbol, granularity=granularity).annotate(max_datetime=Max("datetime"))
            if results:
                max_datetime = results[0]['max_datetime']
                max_datetime = TimeZone().to_timezone(max_datetime)
                
                # Check if a record with the same datetime and symbol already exists
                # if not AssetPrice.objects.filter(datetime=datetime, symbol=symbol).exists():
                if not datetime.tzinfo:
                    datetime = TimeZone().to_timezone(datetime)

                if datetime > max_datetime:

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
                    data_uploaded.append([row['datetime'], row['symbol'], row['open'], row['high'], row['close'], row['adj_close'], row['volume'], row['run']])
                else:
                    pass
            else:
                print(f'There is no data for {symbol, datetime, granularity}')
        
        return results_list
    
class DataRetriever:

    def __init__(self, symbol, start_date, end_date, granularity):

        self.symbol = symbol
        self.start_date = start_date
        self.end_date = (pd.to_datetime(end_date) + timedelta(1)).strftime("%Y-%m-%d")
        self.granularity = granularity

    def retrieve_data(self):

        asset_prices = AssetPrice.objects.filter(
            symbol=self.symbol,
            datetime__range=(self.start_date, self.end_date),
            granularity=self.granularity
        ).order_by('datetime')

        prices = [float(asset_price.close) for asset_price in asset_prices]
        dates = [asset_price.datetime for asset_price in asset_prices]
                 
        return dates, prices