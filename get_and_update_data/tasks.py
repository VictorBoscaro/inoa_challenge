from __future__ import absolute_import, unicode_literals
from .see_there_it_goes import DataUpdater, PriceGetter, TimeZone, UpdateRateFreq
from celery import shared_task
from .models import MyModel

@shared_task
def update_data():
    DataUpdater().update_data()

# @shared_task
# def send_email():
#     # your code to send email goes here