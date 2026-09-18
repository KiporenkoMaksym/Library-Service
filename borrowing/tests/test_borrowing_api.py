from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase

from django.urls import reverse

from book.models import Book
from book.tests.test_book import sample_book
from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingDetailSerializer,
    BorrowingSerializer
)
from user.tests.test_user_api import create_user

BORROWING_API_URL = reverse("borrowing:borrowing-list")

def sample_borrowing(**params):
    book = Book.objects.create(
        title="Test Book",
        author="Test Author",
        inventory=5,
        daily_free=2.00
    )

    defaults = {
        "borrow_date": "2021-01-01",
        "expected_return_date": "2021-01-03",
        "book": book,
    }
    defaults.update(params)

    return Borrowing.objects.create(**defaults)

def detail_url(borrowing_id):
    return reverse(
        "borrowing:borrowing-detail",
        args=[borrowing_id]
    )


class PublicBorrowingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(BORROWING_API_URL)

        self.assertEqual(
            res.status_code,
            status.HTTP_401_UNAUTHORIZED
        )


class PrivateBorrowingApiTests(TestCase):
    def setUp(self):
        self.user = create_user(
            email="test@test.com",
            first_name="Test",
            last_name="User",
            password="testpassword",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.book = sample_book()


    def test_get_borrowing(self):
        borrowing = sample_borrowing(user=self.user)

        res = self.client.get(BORROWING_API_URL)
        serializer = BorrowingSerializer([borrowing], many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_borrowing(self):
        borrowing = sample_borrowing(user=self.user)

        url = detail_url(borrowing.id)
        res = self.client.get(url)

        serializer = BorrowingDetailSerializer(borrowing)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_post_borrowing(self):
        payload = {
            "borrow_date": "2021-01-01",
            "expected_return_date": "2021-01-03",
            "book": self.book.id
        }

        res = self.client.post(BORROWING_API_URL, payload)

        self.assertEqual(
            res.status_code,
            status.HTTP_201_CREATED
        )


class AdminBorrowingApiTest(TestCase):
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
        self.book = sample_book()

    def test_post_borrowing_admin(self):
        payload = {
            "borrow_date": "2021-01-01",
            "expected_return_date": "2021-01-03",
            "book": self.book.id
        }

        res = self.client.post(BORROWING_API_URL, payload)

        self.assertEqual(
            res.status_code,
            status.HTTP_201_CREATED
        )

    def test_put_borrowing_admin(self):
        borrowing = sample_borrowing(user=self.user)

        payload = {
            "borrow_date": "2021-01-01",
            "expected_return_date": "2021-01-03",
            "book": self.book.id
        }

        url = detail_url(borrowing.id)
        res = self.client.put(url, payload)

        borrowing.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            str(borrowing.borrow_date),
            payload["borrow_date"]
        )
        self.assertEqual(
            str(borrowing.expected_return_date),
            payload["expected_return_date"]
        )

    def test_delete_borrowing_admin(self):
        borrowing = sample_borrowing(user=self.user)

        url = detail_url(borrowing.id)
        res = self.client.delete(url)

        self.assertEqual(
            res.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertFalse(
            Borrowing.objects.filter(id=borrowing.id).exists()
        )
