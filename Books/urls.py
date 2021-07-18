from django.contrib import admin
from django.urls import path

from booksapp.api import book_list, book_details, upsert_books

urlpatterns = [
    path("admin/", admin.site.urls),
    path("books", book_list, name="book_list"),
    path("books/<int:bookId>", book_details, name="book_details"),
    path("db", upsert_books, name="upsert_books"),
]
