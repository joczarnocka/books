from huey.contrib.djhuey import task

from booksapp.core import make_books_url, fetch_books, upsert_books


@task()
def fetch_books_from_api(query):
    url = make_books_url(query)
    data = fetch_books(url)
    if data:
        upsert_books(data)
