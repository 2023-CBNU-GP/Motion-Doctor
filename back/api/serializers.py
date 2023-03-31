from rest_framework import serializers
from .models import *


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['uid', 'name', 'id', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['uid', 'name', 'id', 'password', 'email', 'doctornum', 'hospitalname']
        extra_kwargs = {
            'password': {'write_only': True}
        }
