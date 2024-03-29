# Create your tests here.

from django.test import TestCase
from datetime import datetime, timedelta
from get_and_update_data.models import AssetPrice, StockPortfolio
from .views import EmailSelector, RecommendationRule, EmailSender
import pandas as pd
from get_and_update_data.aux_classes import UpdateRateFreq
from .data_treatment import DataRetriever, PriceGetter, DataUpdater
from datetime import datetime
from django.contrib.auth.models import User
from .models import AssetPrice
import datetime
from decimal import Decimal
import os

if "DJANGO_SETTINGS_MODULE" in os.environ:
    print("Django settings is in the enviroment")
else:
    print("Django is not in the project")

class PriceGetterTestCase(TestCase):
    def setUp(self):
        # Set up any necessary data or dependencies for the test
        
        
        # Create some AssetPrice objects for testing
        AssetPrice.objects.create(symbol='PETR4.SA', datetime=datetime.now() - timedelta(minutes=120), open=100.0, high=105.0, low=99.0, close=102.0, adj_close=101.0, volume=100000, run=datetime.now() - timedelta(minutes=120))
        AssetPrice.objects.create(symbol='CMIG4.SA', datetime=datetime.now() - timedelta(minutes=60), open=200.0, high=205.0, low=199.0, close=202.0, adj_close=201.0, volume=200000, run=datetime.now() - timedelta(minutes=70))
        AssetPrice.objects.create(symbol='PETR4.SA', datetime=datetime.now() - timedelta(minutes=120), open=100.0, high=105.0, low=99.0, close=102.0, adj_close=101.0, volume=100000, run=datetime.now() - timedelta(minutes=120))
    
    def test_get_new_data(self):
        # Test the get_new_data method of PriceGetter
        
        # Create an instance of PriceGetter
        price_getter = PriceGetter()
        
        # Call the get_new_data method
        new_data = price_getter.get_new_data()
        print("Printing new data:")
        print(new_data)
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

class DataUploadTestCase(TestCase):

    def setUp(self):

        AssetPrice.objects.create(symbol='PETR4.SA', datetime=datetime.now() - timedelta(minutes=120), open=100.0, high=105.0, low=99.0, close=102.0, adj_close=101.0, volume=100000, run=datetime.now() - timedelta(minutes=120))
        AssetPrice.objects.create(symbol='CMIG4.SA', datetime=datetime.now() - timedelta(minutes=60), open=200.0, high=205.0, low=199.0, close=202.0, adj_close=201.0, volume=200000, run=datetime.now() - timedelta(minutes=70))
        AssetPrice.objects.create(symbol='PETR4.SA', datetime=datetime.now() - timedelta(minutes=120), open=100.0, high=105.0, low=99.0, close=102.0, adj_close=101.0, volume=100000, run=datetime.now() - timedelta(minutes=120))
    
    def test_upload_new_data(self):
        
        price_getter = PriceGetter()
        data_to_upload = price_getter.get_new_data()
        
        print("Printing data to upload:")
        print(type(data_to_upload))
        data_uploader = DataUpdater(data_to_upload)
        print(f'Data uploader is type: {type(data_uploader)}')
        print("Getting data from API:")
        data_uploaded = data_uploader.upload_new_data()
        # df_uploaded = pd.DataFrame(data_uploaded, columns = ['datetime', 'open', 'high', 'low', 'close', 'adj_close', 'volume', 'run', 'symbol'])
        print(len(data_uploaded))
        print("Printing uploaded data:")
        
        # The test will be: the unique companies to get_data needs to be the same as the unique companies in data_to_upload
        
        uploaded_data = AssetPrice.objects.all()
        print(type(uploaded_data))
        # self.assertEqual(len(uploaded_data), len(data_to_upload))
        self.assertGreater(len(uploaded_data), 0)

        for _, data in data_to_upload.iterrows():
            self.assertEqual(AssetPrice.objects.filter(datetime=data['datetime'], symbol=data['symbol']).count(), 1)


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

def email_selector_purchase_test():
    # print('email selector test')
    purchase_users = EmailSelector().purchase_email()
    # print(purchase_users)
    all_email = User.objects.values_list('email', flat=True).distinct()
    all_email = [email for email in all_email]

    if all_email == purchase_users:
        print('Os emails são iguais')
    else:
        print('Os emails não são iguais')

def email_select_sell_test(symbol):
    sell_email = EmailSelector(symbol).sell_email()
    print("sell email")
    print(sell_email)
    symbol_email = StockPortfolio.objects.filter(symbol=symbol, sold_date__isnull=True).values_list('email', flat=True).distinct()
    symbol_email = [email for email in symbol_email]
    print('symbol email')
    print(symbol_email)
    if sell_email == symbol_email:
        print('Os emails são iguais')
    else:
        print('Os emails não são iguais')

class TestPurchaseRecommendationRule(TestCase):

    @classmethod
    def setUpTestData(cls):
        now = datetime.datetime.now()
        base_price = Decimal('100.0')
        for i in range(60):
            date = now - datetime.timedelta(days=60-i)
            if i >= 55:
                base_price = base_price * Decimal('0.97') # 1% decrease each day for last 5 days
            AssetPrice.objects.create(datetime=date, open=base_price, high=base_price, low=base_price,
                                      close=base_price, adj_close=base_price, volume=Decimal('10000'),
                                      run=now, symbol='AAPL', granularity='1d')
    
    def test_purchase_rule(self):
        print('Testing purchase rule')
        rule = RecommendationRule(asset_model=AssetPrice)
        result = rule.purchase_rule(moving_average=5, var_threshold=-0.05)  # using negative var_threshold as the price is lower than the moving average
        self.assertIn('AAPL', result)

class TestSellRecommendationRule(TestCase):

    @classmethod
    def setUpTestData(cls):
        now = datetime.datetime.now()
        base_price = Decimal('100.0')
        for i in range(60):
            date = now - datetime.timedelta(days=60-i)
            AssetPrice.objects.create(datetime=date, open=base_price, high=base_price, low=base_price,
                                      close=base_price, adj_close=base_price, volume=Decimal('10000'),
                                      run=now, symbol='AAPL', granularity='1d')

        # Assuming users bought the stock 60 days ago
        StockPortfolio.objects.create(symbol='AAPL', price=Decimal('90.0'), date=now-datetime.timedelta(days=60),
                                      email='test_user@example.com', username='test_user')

        # The stock price has increased by more than 10% (from 90 to 100)
    
    def test_sell_rule(self):
        print('Testing sell rule')
        rule = RecommendationRule()
        result = rule.sell_rule(sell_threshold=0.1)  
        self.assertEqual(len(result), 1)  # Expecting 1 stock to be sold
        self.assertEqual(result.iloc[0]['email'], 'test_user@example.com')
        self.assertEqual(result.iloc[0]['symbol'], 'AAPL')


a = RecommendationRule().sell_rule(0.1)
email_list = EmailSelector().sell_email(a)

# print(email_list)
# subject = 'Ações para comprar'
# message = f'Recomendamos a compra das ações {a} por estarem com o preço abaixo da média móvel dos últimos 7 dias'
# print('instantiating email sender')
# email = EmailSender(subject, message, email_list)
# print('sending email')
# email.send_email_to_user()

