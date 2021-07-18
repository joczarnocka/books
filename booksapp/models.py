from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=200)


class Category(models.Model):
    name = models.CharField(max_length=50)


class Book(models.Model):
    external_id = models.CharField(max_length=15, unique=True)
    title = models.CharField(max_length=300)
    authors = models.ManyToManyField(Author)
    published_date = models.CharField(max_length=4)
    categories = models.ManyToManyField(Category)
    average_rating = models.IntegerField(null=True)
    ratings_count = models.IntegerField(null=True)
    thumbnail = models.CharField(max_length=1000)
