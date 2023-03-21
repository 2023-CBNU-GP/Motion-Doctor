from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['userid', 'name', 'id', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }
