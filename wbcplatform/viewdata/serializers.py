from rest_framework import serializers
from django.contrib.auth.models import User

class DataFileSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        super(DataFileSerializer, self).__init__(*args, **kwargs)

