from rest_framework import serializers
from urlshorten.models import UrlMapper, UrlMapper2
from django.db import IntegrityError



class UrlMapperSerializer(serializers.ModelSerializer):
    # short_path = serializers.ReadOnlyField()

    class Meta:
        model = UrlMapper
        fields = ["id", "url", "short_path", "hits"]
        read_only_fields = ["id", "short_path", "hits"]


class UrlMapperSerializer2(serializers.ModelSerializer):
    # short_path = serializers.ReadOnlyField()

    class Meta:
        model = UrlMapper2
        fields = ["id", "url", "short_path", "hits"]
        read_only_fields = ["id", "hits"]

    def create(self, validated_data):
        ModelClass = self.Meta.model
        instance, created = ModelClass._default_manager.get_or_create(**validated_data)
        if not created:
            raise IntegrityError("object already exists")  # failover.
        return instance


# {
#     "url": "https://www.geeksforgeeks.org/turn-off-the-rightmost-set-bit/2/"
# }

class UrlMapperSerializerRead(serializers.ModelSerializer):
    # short_path = serializers.ReadOnlyField()

    class Meta:
        model = UrlMapper2
        fields = ["url", "hits"]
        read_only_fields = ["url", "hits"]