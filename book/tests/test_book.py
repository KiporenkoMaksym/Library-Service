from django.test import TestCase

from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from book.models import Book
from book.serializers import BookSerializer
from user.tests.test_user_api import create_user

BOOK_URL = reverse("book:book-list")

def sample_book(**params):
    defaults = {
        "title": "Sample Book",
        "author": "Sample Author",
        "cover": "HARD",
        "inventory": 10,
        "daily_fee": 5,
    }
    defaults.update(params)

    return Book.objects.create(**defaults)


class PublicBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_books(self):
        sample_book()

        res = self.client.get(BOOK_URL)
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_post_books(self):
        payload = {
            "title": "Test Book",
            "author": "Test Author",
            "cover": "HARD",
            "inventory": 10,
            "daily_fee": 5,
        }

        res = self.client.post(BOOK_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBookApiTests(TestCase):
    def setUp(self):
        self.user = create_user(
            email="test@test.com",
            first_name="Test",
            last_name="User",
            password="testpassword",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_books_auth(self):
        sample_book()

        res = self.client.get(BOOK_URL)

        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_post_books_auth(self):
        payload = {
            "title": "Test Book",
            "author": "Test Author",
            "cover": "HARD",
            "inventory": 10,
            "daily_fee": 5,
        }

        res = self.client.post(BOOK_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminBookApiTest(TestCase):
    def setUp(self):
        self.user = create_user(
            email="test@test.com",
            first_name="Test",
            last_name="User",
            password="testpassword",
            is_staff=True,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_post_books_admin(self):
        payload = {
            "title": "Test Book",
            "author": "Test Author",
            "cover": "HARD",
            "inventory": 10,
            "daily_fee": 5,
        }

        res = self.client.post(BOOK_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_retrieve_books_admin(self):
        sample_book()

        res = self.client.get(f"{BOOK_URL}20/")

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_books_admin(self):
        sample_book()

        res = self.client.put(f"{BOOK_URL}20/", {})

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_books_admin(self):
        sample_book()

        res = self.client.delete(f"{BOOK_URL}20/")

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
