from django.core.mail import send_mail, EmailMessage
from django.core.management.base import BaseCommand
import smtplib
from get_and_update_data.views import EmailSender

print('Sending email')

class Command(BaseCommand):

    def send_email1(self):
        print('sending_email1')
        send_mail(subject='Sim', 
                message='This email is using send_email1 method', 
                recipient_list=['victorboscaro@gmail.com'], 
                from_email='inoachallengetest@outlook.com', 
                fail_silently=False)
        
    def send_email2(self):
        print('class that sends email')
        EmailSender('Test', 'This is an email from django', ['victorboscaro@gmail.com', 'victorboscaro@outlook.com']).send_email_to_user()

    

    def handle(self, *args, **options):
        self.send_email1()
        self.send_email2()
        #self.send_email3()