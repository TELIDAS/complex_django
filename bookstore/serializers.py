from rest_framework import serializers

from bookstore import models


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = ["id", 'name', 'price', 'publisher']
