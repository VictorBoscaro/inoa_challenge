import plotly.express as px
import numpy as np
from get_and_update_data.models import B3Companie
import pytz
from django.db.models import Max

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

class UpdateRateFreq:

    def __init__(self, b3_companies = B3Companie):

        self.b3_companies = b3_companies
    
    def get_last_minute_update(self):

        latest_runs = self.b3_companies.objects.values('symbol').annotate(latest_run=Max('run'))

        # Get the B3Companie objects matching the latest 'run' for each 'symbol'
        latest_records = self.b3_companies.objects.filter(run__in=[item['latest_run'] for item in latest_runs])

        # Create a dictionary where the key is the symbol and the value is the minutes_update_rate of the last run for each symbol
        symbol_rate_dict = {record.symbol: record.minutes_update_rate for record in latest_records}

        # Now, symbol_rate_dict is a dictionary with each 'symbol' as the key and 'minutes_update_rate' as the value
        return symbol_rate_dict

class TimeZone:

    def __init__(self, timezone = "America/Sao_Paulo"):
        
        self.timezoned = pytz.timezone(timezone)

    def to_timezone(self, obj):

        return self.timezoned.localize(obj)