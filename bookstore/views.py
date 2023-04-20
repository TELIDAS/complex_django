from rest_framework import generics

from bookstore import serializers, models


class BookListAPIView(generics.ListAPIView):
    serializer_class = serializers.BookSerializer

    def get_queryset(self):
        select_related_tables = ['publisher']
        queryset = models.Book.objects.prefetch_related(*select_related_tables).all().order_by("id")
        return queryset


class StoreListAPIView(generics.ListAPIView):
    serializer_class = serializers.StoreSerializer

    def get_queryset(self):
        prefetch_related_tables = ["books"]
        queryset = models.Store.objects.prefetch_related(*prefetch_related_tables).all()
        return queryset
