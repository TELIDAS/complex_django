from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=300)

    class Meta:
        db_table = 'publisher'
        verbose_name = "Publisher"
        verbose_name_plural = "Publishers"

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=300)
    price = models.IntegerField(default=0)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'books'
        db_table = 'book'
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=300)
    books = models.ManyToManyField(Book)

    class Meta:
        default_related_name = 'stores'
        db_table = 'store'
        verbose_name = "Store"
        verbose_name_plural = "Stores"

    def __str__(self):
        return self.name
