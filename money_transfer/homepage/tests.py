__all__ = ()

from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class StaticURLsTests(TestCase):
    def test_index_url(self):
        url = reverse('homepage:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
