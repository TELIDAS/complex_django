from rest_framework import generics

from bookstore import serializers, models


class SelectBookListAPIView(generics.ListAPIView):
    serializer_class = serializers.BookSerializer

    def get_queryset(self):
        select_related_tables = ['publisher']
        queryset = models.Book.objects.prefetch_related(*select_related_tables).all().order_by("id")
        return queryset
