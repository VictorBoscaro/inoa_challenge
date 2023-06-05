# Create your tests here.

from django.test import TestCase
from datetime import datetime, timedelta
from get_and_update_data.models import AssetPrice
from get_and_update_data.entities.get_and_upload_data import PriceGetter, UploadData
import pandas as pd
from get_and_update_data.see_there_it_goes import DataRetriever
from datetime import datetime

import os

if "DJANGO_SETTINGS_MODULE" in os.environ:
    print("Django settings is in the enviroment")
else:
    print("Django is not in the project")

# class PriceGetterTestCase(TestCase):
#     def setUp(self):
#         # Set up any necessary data or dependencies for the test
        
        
#         # Create some AssetPrice objects for testing
#         AssetPrice.objects.create(symbol='PETR4.SA', datetime=datetime.now() - timedelta(minutes=120), open=100.0, high=105.0, low=99.0, close=102.0, adj_close=101.0, volume=100000, run=datetime.now() - timedelta(minutes=120))
#         AssetPrice.objects.create(symbol='CMIG4.SA', datetime=datetime.now() - timedelta(minutes=60), open=200.0, high=205.0, low=199.0, close=202.0, adj_close=201.0, volume=200000, run=datetime.now() - timedelta(minutes=70))
#         AssetPrice.objects.create(symbol='PETR4.SA', datetime=datetime.now() - timedelta(minutes=120), open=100.0, high=105.0, low=99.0, close=102.0, adj_close=101.0, volume=100000, run=datetime.now() - timedelta(minutes=120))
    
#     def test_get_new_data(self):
#         # Test the get_new_data method of PriceGetter
        
#         # Create an instance of PriceGetter
#         price_getter = PriceGetter()
        
#         # Call the get_new_data method
#         new_data = price_getter.get_new_data()
#         print("Printing new data:")
#         print(new_data)
#         # Check if new_data is a pandas DataFrame
#         self.assertIsInstance(new_data, pd.DataFrame)
        
#         # Assert that the new_data DataFrame has the expected columns
#         expected_columns = ['datetime', 'open', 'high', 'low', 'close', 'adj_close', 'volume', 'run', 'symbol']
#         self.assertCountEqual(new_data.columns, expected_columns)
        
#         # Assert that the new_data DataFrame is not empty
#         self.assertFalse(new_data.empty)
        
#         # Add more specific assertions based on your requirements and expected data
        
#         # For example, you can assert that the symbols in new_data are the ones you expect
#         expected_symbols = ['PETR4.SA', 'CMIG4.SA']
#         symbols = new_data['symbol'].unique().tolist()
#         self.assertCountEqual(symbols, expected_symbols)
        
#         # You can also assert that the data is properly fetched and updated
        
#         # Clean up any created data after the test (if necessary)
#         AssetPrice.objects.all().delete()  

# class DataUploadTestCase(TestCase):

#     def setUp(self):

#         AssetPrice.objects.create(symbol='PETR4.SA', datetime=datetime.now() - timedelta(minutes=120), open=100.0, high=105.0, low=99.0, close=102.0, adj_close=101.0, volume=100000, run=datetime.now() - timedelta(minutes=120))
#         AssetPrice.objects.create(symbol='CMIG4.SA', datetime=datetime.now() - timedelta(minutes=60), open=200.0, high=205.0, low=199.0, close=202.0, adj_close=201.0, volume=200000, run=datetime.now() - timedelta(minutes=70))
#         AssetPrice.objects.create(symbol='PETR4.SA', datetime=datetime.now() - timedelta(minutes=120), open=100.0, high=105.0, low=99.0, close=102.0, adj_close=101.0, volume=100000, run=datetime.now() - timedelta(minutes=120))
    
#     def test_upload_new_data(self):
        
#         price_getter = PriceGetter()
#         data_to_upload = price_getter.get_new_data()
        
#         print("Printing data to upload:")
#         print(type(data_to_upload))
#         data_uploader = UploadData(data_to_upload)
#         print(f'Data uploader is type: {type(data_uploader)}')
#         print("Getting data from API:")
#         data_uploaded = data_uploader.upload_new_data()
#         # df_uploaded = pd.DataFrame(data_uploaded, columns = ['datetime', 'open', 'high', 'low', 'close', 'adj_close', 'volume', 'run', 'symbol'])
#         print(len(data_uploaded))
#         print("Printing uploaded data:")
        
#         # The test will be: the unique companies to get_data needs to be the same as the unique companies in data_to_upload
        
#         uploaded_data = AssetPrice.objects.all()
#         print(type(uploaded_data))
#         # self.assertEqual(len(uploaded_data), len(data_to_upload))
#         self.assertGreater(len(uploaded_data), 0)

#         for _, data in data_to_upload.iterrows():
#             self.assertEqual(AssetPrice.objects.filter(datetime=data['datetime'], symbol=data['symbol']).count(), 1)


class DataRetrieverTestCase:

    def __init__(self, symbol, start_date, end_date, granularity):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.granularity = granularity

    def test_retrieve_data(self):

        # Define the date range and symbol for testing
  
        data_retriever = DataRetriever(self.symbol, self.start_date, self.end_date, self.granularity)

        # Retrieve the data using the DataRetriever class
        dates, prices = data_retriever.retrieve_data()
        dates = [date.strftime("%Y-%m-%d") for date in dates]
        print("Printing prices and dates:")
        print(dates, prices)
        # Assert that the data is correct
        expected_prices = [120, 130, 140]
        expected_dates = ["2023-01-03", "2023-01-04", "2023-01-05"]

        print('Asserting prices:')
        self.assertEqual(prices, expected_prices)
        print('Asserting dates:')
        self.assertEqual(dates, expected_dates)


data_retriever_test = DataRetrieverTestCase("PETR4.SA", '2023-05-01', '2023-06-01', '60m')
data_retriever_test.test_retrieve_data()
