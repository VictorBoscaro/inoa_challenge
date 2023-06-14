from __future__ import absolute_import, unicode_literals
from .data_treatment import DataUpdater
from celery import shared_task
from .views import RecommendationRule, EmailSender, EmailSelector

@shared_task
def update_data():
    DataUpdater().update_data()

@shared_task
def send_buy_email():

    stocks_to_buy = RecommendationRule().purchase_rule(moving_average=7, var_threshold=-0.05)
    email_list = EmailSelector().purchase_email()
    subject = 'Ações para comprar'
    message = f'Recomendamos a compra das ações {stocks_to_buy} por estarem com o preço abaixo da média móvel abaixo dos últimos 7 dias'
    email = EmailSender(subject, message, email_list)
    email.send_email_to_user()

@shared_task
def send_sell_email():
    stocks_to_sell_by_email = RecommendationRule().sell_rule(0.1)
    emails_to_send = EmailSelector().sell_email(stocks_to_sell_by_email)
    subject = 'Ações para vender'
    for _, row in emails_to_send.iterrows():
        email_list = [row[0]]
        stocks_to_sell = row[1]
        message = f"Recomendamos a venda das ações {stocks_to_sell}. O lucro será de ao menos 10%"
        email = EmailSender(subject, message, email_list)
        email.send_email_to_user()