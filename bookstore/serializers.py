from rest_framework import serializers

from bookstore import models


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Publisher
        fields = ["id", 'name']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = ["id", 'name', 'price', 'publisher']


class StoreSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True, many=True)

    class Meta:
        model = models.Store
        fields = ["id", 'name', 'books', "book"]
