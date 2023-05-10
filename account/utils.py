from django.core.mail import EmailMessage


class SendEmail:
    @staticmethod
    def sen_email(data):
        email = EmailMessage(to=[data['email']], subject=data['subject'], body=data['body'])
        email.send()