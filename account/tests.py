from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from account.models import Account


class AccountTests(APITestCase):

    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        username = 'test'

        url = reverse('account-list')
        data = {
            'username': username,
            'email': 'test@mail.com',
            'password': 'verysecretpassword'
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.first().username, 'test')

    def test_list_accounts(self):
        url = reverse('account-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], Account.objects.count())
