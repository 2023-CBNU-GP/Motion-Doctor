from rest_framework import serializers
from .models import Userinfo


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userinfo
        fields = ['userid', 'name', 'id', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }
