import plotly.express as px
from .models import AssetPrice
import pandas as pd
from datetime import timedelta
import numpy as np

class LineChart:

    def __init__(self, x_values, y_values, moving_average, title, x_label, y_label):
        self.x_values = x_values
        self.y_values = y_values
        self.ma = moving_average
        self.title = title
        self.x_label = x_label
        self.y_label = y_label

    def moving_average(self, data, window_size):

        padded_data = np.pad(data, (window_size - 1, 0), mode = 'edge')
        weights = np.ones(window_size)/window_size
        moving_avg = np.convolve(padded_data, weights, mode = 'valid')

        return moving_avg

    def make_plot(self):
        
        if self.ma != 1:
                       
            self.y_values = self.moving_average(self.y_values, self.ma)

        fig = px.line(x=self.x_values, y = self.y_values)

        fig.update_layout(
            title = self.title,
            xaxis_title = self.x_label,
            yaxis_title = self.y_label  
        )

        return fig
    
    def plot_to_json(self):

        fig = self.make_plot()
        json_fig = fig.to_json()
        return json_fig
    
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
