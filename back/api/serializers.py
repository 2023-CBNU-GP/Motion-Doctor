from rest_framework import serializers
from .models import *


class PatientSerializer(serializers.Serializer):
    uid = serializers.IntegerField()
    name = serializers.CharField(max_length=30)
    id = serializers.CharField(max_length=30)
    email = serializers.CharField(max_length=50)
    type = serializers.CharField(max_length=10)


class DoctorSerializer(serializers.Serializer):
    _id = serializers.IntegerField()
    name = serializers.CharField(max_length=30)
    id = serializers.CharField(max_length=30)
    email = serializers.CharField(max_length=50)
    doctornum = serializers.IntegerField()
    hospitalname = serializers.CharField(max_length=50)
    type = serializers.CharField(max_length=10)
