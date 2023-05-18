import requests
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from contact.models import Subscribe
from .models import Email
from account.utils import SendEmail


#dynamic method
class EmailSendAPI(APIView):
    def post(self, request):
        message = request.data.get('message')
        print(message)
        send_mail(
            'This is JobPro',
            message,
            'settings.EMAIL_HOST_USER',
            [i.email for i in Subscribe.objects.all()],
            fail_silently=False
        )
        instance = Email.objects.create(message=message)
        return Response('Message sent Successfully')


#  static method
# class EmailView(views.APIView):
#     def post(self, request, *args, **kwargs):
#         for i in self.request.data['email']:
#             data = {
#                 'email': i,
#                 'subject': 'Python Job',
#                 'body': 'Hi, I need strong Python'
#             }
#             SendEmail.sen_email(data)
#         return response.Response('as')
