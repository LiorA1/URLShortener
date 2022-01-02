from rest_framework import serializers
from urlshorten.models import UrlMapper


class UrlMapperSerializer(serializers.ModelSerializer):
    #short_path = serializers.ReadOnlyField()

    class Meta:
        model = UrlMapper
        fields = ['id', 'url', 'short_path', 'hits']
        read_only_fields = ['id', 'short_path', 'hits']
