from rest_framework import serializers
from .models import Email


class EmailSerializer(serializers.ModelSerializer):
    model = Email
    fields = '__all__'
