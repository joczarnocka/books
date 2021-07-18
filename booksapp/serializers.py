from rest_framework import serializers

from booksapp.models import Book, Author, Category


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ["name"]

    def to_representation(self, instance):
        return instance.name


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]

    def to_representation(self, instance):
        return instance.name


class BookSerializer(serializers.HyperlinkedModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = [
            "title",
            "authors",
            "published_date",
            "average_rating",
            "categories",
            "ratings_count",
            "thumbnail",
        ]


class BookUpdateSerializer(serializers.Serializer):
    q = serializers.CharField(max_length=50)
