from django.db import models


class News(models.Model):
    """ News model """

    link = models.TextField()

    class Meta:
        db_table = 'news'
        verbose_name = "News-Link"
        verbose_name_plural = "News-Links"
