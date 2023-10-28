from rest_framework import serializers
from urlshorten.models import UrlMapper
from django.db import IntegrityError


class UrlMapperSerializer(serializers.ModelSerializer):
    # short_path = serializers.ReadOnlyField()

    class Meta:
        model = UrlMapper
        fields = ["id", "url", "short_path", "hits"]
        read_only_fields = ["id", "hits"]

    def create(self, validated_data):
        ModelClass = self.Meta.model
        instance, created = ModelClass._default_manager.get_or_create(**validated_data)
        if not created:
            raise IntegrityError("object already exists")  # failover.
        return instance


class UrlMapperSerializerRead(serializers.ModelSerializer):
    # short_path = serializers.ReadOnlyField()

    class Meta:
        model = UrlMapper
        fields = ["url", "hits"]
        read_only_fields = ["url", "hits"]
