import json

from django.test import TestCase
from django.urls import reverse

from booksapp.core import upsert_books
from booksapp.models import Book


def make_item(**kwargs):
    item = {
        "id": kwargs.get("id", "ABC213789"),
        "volumeInfo": {
            "title": kwargs.get("title", "Example Title"),
            "publishedDate": kwargs.get("published_date", "2000"),
            "imageLinks": {
                "thumbnail": kwargs.get("thumbnail", "http://example.image.com")
            },
        },
    }
    if "authors" in kwargs:
        item["volumeInfo"]["authors"] = kwargs["authors"]
    if "categories" in kwargs:
        item["volumeInfo"]["categories"] = kwargs["categories"]
    if "average_rating" in kwargs:
        item["volumeInfo"]["averageRating"] = kwargs["average_rating"]
    if "ratings_count" in kwargs:
        item["volumeInfo"]["ratingsCount"] = kwargs["ratings_count"]
    if "thumbnail" in kwargs:
        item["volumeInfo"]["imageLinks"] = {"thumbnail": kwargs["thumbnail"]}
    return item


def make_data(items):
    return {"items": items}


class UpsertBooksTests(TestCase):
    def test_no_data(self):
        upsert_books({})
        self.assertEquals(0, Book.objects.all().count())

    def test_without_items(self):
        upsert_books(make_data([]))
        self.assertEquals(0, Book.objects.all().count())

    def test_create_single_book(self):
        upsert_books(
            make_data(
                [
                    make_item(
                        id="CDF1234",
                        title="t",
                        published_date="2001",
                        average_rating=10,
                        ratings_count=8,
                        authors=["a b", "c d"],
                        categories=["c", "d"],
                        thumbnail="http://image1.com",
                    )
                ]
            )
        )
        self.assertEquals(1, Book.objects.all().count())
        book = Book.objects.get(external_id="CDF1234")
        self.assertEquals(book.title, "t")
        self.assertEquals(book.published_date, "2001")
        self.assertEquals(book.average_rating, 10)
        self.assertEquals(book.ratings_count, 8)
        authors = set(book.authors.values_list("name", flat=True))
        self.assertEquals(authors, {"a b", "c d"})
        categories = set(book.categories.values_list("name", flat=True))
        self.assertEquals(categories, {"c", "d"})
        self.assertEquals(book.thumbnail, "http://image1.com")

    def test_update_single_book(self):
        upsert_books(
            make_data(
                [
                    make_item(
                        id="CDF1234",
                        title="t",
                        published_date="2001",
                        average_rating=10,
                        ratings_count=8,
                        authors=["a b", "c d"],
                        categories=["c", "d"],
                        thumbnail="http://image1.com",
                    )
                ]
            )
        )
        # update
        upsert_books(
            make_data(
                [
                    make_item(
                        id="CDF1234",
                        title="t2",
                        published_date="2002",
                        average_rating=11,
                        ratings_count=9,
                        authors=["c d"],
                        categories=["c"],
                        thumbnail="http://image2.com",
                    )
                ]
            )
        )
        self.assertEquals(1, Book.objects.all().count())
        book = Book.objects.get(external_id="CDF1234")
        self.assertEquals(book.title, "t2")
        self.assertEquals(book.published_date, "2002")
        self.assertEquals(book.average_rating, 11)
        self.assertEquals(book.ratings_count, 9)
        authors = set(book.authors.values_list("name", flat=True))
        self.assertEquals(authors, {"c d"})
        categories = set(book.categories.values_list("name", flat=True))
        self.assertEquals(categories, {"c"})
        self.assertEquals(book.thumbnail, "http://image2.com")

    def test_upsert_more(self):
        upsert_books(make_data([make_item(id="CDF1234"), make_item(id="CDF1235")]))
        ids = set(Book.objects.all().values_list("external_id", flat=True))
        self.assertEquals(ids, {"CDF1234", "CDF1235"})


def extract_data(response):
    return json.loads(response.content.decode())


class BooksAPITest(TestCase):
    path = reverse("book_list")

    def test_no_books(self):
        response = self.client.get(self.path)
        data = extract_data(response)
        self.assertEquals(data, [])

    def test_all_books(self):
        upsert_books(
            make_data(
                [
                    make_item(
                        id="CDF1234",
                        title="t",
                        published_date="2001",
                        average_rating=10,
                        ratings_count=8,
                        authors=["a b"],
                        categories=["c"],
                        thumbnail="http://image1.com",
                    )
                ]
            )
        )
        response = self.client.get(self.path)
        items = extract_data(response)
        self.assertEquals(1, len(items))
        item = items[0]
        self.assertEquals(
            item,
            dict(
                title="t",
                published_date="2001",
                average_rating=10,
                ratings_count=8,
                authors=["a b"],
                categories=["c"],
                thumbnail="http://image1.com",
            ),
        )

    def test_sort_asc(self):
        upsert_books(
            make_data(
                [
                    make_item(id="CDF1234", published_date="2008"),
                    make_item(id="CDF1235", published_date="2005"),
                    make_item(id="CDF1236", published_date="2002"),
                    make_item(id="CDF1237", published_date="2007"),
                ]
            )
        )
        response = self.client.get(self.path, {"sort": "published_date"})
        items = extract_data(response)
        published_dates = [i["published_date"] for i in items]
        self.assertEquals(published_dates, ["2002", "2005", "2007", "2008"])

    def test_sort_desc(self):
        upsert_books(
            make_data(
                [
                    make_item(id="CDF1234", published_date="2008"),
                    make_item(id="CDF1235", published_date="2005"),
                    make_item(id="CDF1236", published_date="2002"),
                    make_item(id="CDF1237", published_date="2007"),
                ]
            )
        )
        response = self.client.get(self.path, {"sort": "-published_date"})
        items = extract_data(response)
        published_dates = [i["published_date"] for i in items]
        self.assertEquals(published_dates, ["2008", "2007", "2005", "2002"])
