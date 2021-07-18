import requests

from django.db import transaction

from booksapp.models import Book, Category, Author

BOOKS_API_URL_TEMPLATE = "https://www.googleapis.com/books/v1/volumes?q={}"


def make_books_url(q):
    return BOOKS_API_URL_TEMPLATE.format(q)


def fetch_books(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()


REQUIRED_BOOK_FIELDS = ["title", "publishedDate"]
OPTIONAL_BOOK_FIELDS = [
    "authors",
    "categories",
    "averageRating",
    "ratingsCount",
    "thumbnail",
]


def _select(d, keys, all_required):
    selected = {}
    for key in keys:
        value = d.get(key)
        if value is None:
            if all_required:
                return None
        else:
            selected[key] = value
    return selected


def _upsert_book_authors(book, authors_names):
    book.authors.remove(*book.authors.all())
    for author_name in authors_names:
        author = Author.objects.filter(name=author_name).first()
        if author is None:
            author = Author.objects.create(name=author_name)
        book.authors.add(author)


def _upsert_book_categories(book, categories_names):
    book.categories.remove(*book.categories.all())
    for category_name in categories_names:
        category = Category.objects.filter(name=category_name).first()
        if category is None:
            category = Category.objects.create(name=category_name)
        book.categories.add(category)


@transaction.atomic()
def _upsert_book(
    external_id,
    title,
    published_date,
    average_rating,
    ratings_count,
    thumbnail,
    authors=(),
    categories=(),
):
    book = Book.objects.filter(external_id=external_id).first()
    if book is None:
        book = Book.objects.create(
            external_id=external_id,
            title=title,
            published_date=published_date,
            average_rating=average_rating,
            ratings_count=ratings_count,
            thumbnail=thumbnail,
        )
    else:
        book.title = title
        book.published_date = published_date
        book.average_rating = average_rating
        book.ratings_count = ratings_count
        book.thumbnail = thumbnail
        book.save()
    if authors:
        _upsert_book_authors(book, authors)
    if categories:
        _upsert_book_categories(book, categories)


def upsert_books(data):
    for item in data.get("items", []):
        external_id = item.get("id")
        if not external_id:
            continue
        info = item.get("volumeInfo")
        if not info:
            continue
        required = _select(info, REQUIRED_BOOK_FIELDS, all_required=True)
        if not required:
            continue
        optional = _select(info, OPTIONAL_BOOK_FIELDS, all_required=False)
        thumbnail = info.get("imageLinks", {}).get("thumbnail", "")
        _upsert_book(
            external_id=external_id,
            title=required["title"],
            published_date=required["publishedDate"],
            average_rating=optional.get("averageRating"),
            ratings_count=optional.get("ratingsCount"),
            authors=optional.get("authors", []),
            categories=optional.get("categories", []),
            thumbnail=thumbnail,
        )
