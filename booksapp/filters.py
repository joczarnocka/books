from django import forms
from django_filters import rest_framework as filters

from booksapp.models import Book


class NameField(forms.CharField):
    def to_python(self, value):
        if value:
            return value.replace('"', "").replace("'", "")
        return value


class NameFilter(filters.CharFilter):
    field_class = NameField


class BookFilter(filters.FilterSet):
    author = NameFilter(field_name="authors__name", lookup_expr="contains")
    category = NameFilter(field_name="categories__name", lookup_expr="contains")
    sort = filters.OrderingFilter(
        fields=[
            ("published_date", "published_date"),
            ("ratings_count", "ratings_count"),
        ]
    )

    class Meta:
        model = Book
        fields = ("title", "published_date", "average_rating", "ratings_count")
