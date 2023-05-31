# Create your tests here.

from django.test import TestCase
from datetime import datetime, timedelta
from get_and_update_data.models import AssetPrice
from get_and_update_data.get_data import PriceGetter
import pandas as pd

class PriceGetterTestCase(TestCase):
    def setUp(self):
        # Set up any necessary data or dependencies for the test
        
        # Create some AssetPrice objects for testing
        AssetPrice.objects.create(symbol='PETR4.SA', datetime=datetime.now(), open=100.0, high=105.0, low=99.0, close=102.0, adj_close=101.0, volume=100000, run=datetime.now())
        AssetPrice.objects.create(symbol='CMIG4.SA', datetime=datetime.now(), open=200.0, high=205.0, low=199.0, close=202.0, adj_close=201.0, volume=200000, run=datetime.now() - timedelta(minutes=70))
    
    def test_get_new_data(self):
        # Test the get_new_data method of PriceGetter
        
        # Create an instance of PriceGetter
        price_getter = PriceGetter()
        
        # Call the get_new_data method
        new_data = price_getter.get_new_data()

        # Check if new_data is a pandas DataFrame
        self.assertIsInstance(new_data, pd.DataFrame)
        
        
        # Assert that the new_data DataFrame has the expected columns
        expected_columns = ['datetime', 'open', 'high', 'low', 'close', 'adj_close', 'volume', 'run', 'symbol']
        self.assertCountEqual(new_data.columns, expected_columns)
        
        # Assert that the new_data DataFrame is not empty
        self.assertFalse(new_data.empty)
        
        # Add more specific assertions based on your requirements and expected data
        
        # For example, you can assert that the symbols in new_data are the ones you expect
        expected_symbols = ['PETR4.SA', 'CMIG4.SA']
        symbols = new_data['symbol'].unique().tolist()
        self.assertCountEqual(symbols, expected_symbols)
        
        # You can also assert that the data is properly fetched and updated
        
        # Clean up any created data after the test (if necessary)
        AssetPrice.objects.all().delete()