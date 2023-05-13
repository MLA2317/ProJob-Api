from django.shortcuts import render
from rest_framework import response, generics, views
from account.utils import SendEmail


class EmailView(views.APIView):
    def post(self, request, *args, **kwargs):
        for i in self.request.data['email']:
            data = {
                'email': i,
                'subject': 'Python Job',
                'body': 'Hi, I need strong Python'
            }
            SendEmail.sen_email(data)
        return response.Response('as')
