from rest_framework.decorators import api_view
from rest_framework.response import Response

from booksapp.serializers import BookSerializer
from booksapp.models import Book
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from booksapp.tasks import fetch_books_from_api
from booksapp.serializers import BookUpdateSerializer
from booksapp.filters import BookFilter


@api_view(["GET"])
def book_list(request: HttpRequest):
    bf = BookFilter(request.GET, Book.objects.all())
    results = BookSerializer(bf.qs, many=True).data
    return Response(results)


@api_view(["GET"])
def book_details(request: HttpRequest, bookId):
    book = get_object_or_404(Book, id=bookId)
    result = BookSerializer(book).data
    return Response(result)


@api_view(["POST"])
def upsert_books(request: HttpRequest):
    bus = BookUpdateSerializer(data=request.data)
    if bus.is_valid():
        fetch_books_from_api(bus.data["q"])
        return Response(status=202)
    return Response(bus.errors)
