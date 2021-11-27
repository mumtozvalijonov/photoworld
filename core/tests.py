from rest_framework.test import APITestCase

from django.urls import reverse


class CoreTestCase(APITestCase):
    def login_user(self, username, password):
        url = reverse('token_obtain_pair')
        login_response = self.client.post(url, data={'username': username, 'password': password})
        access_token = login_response.json()['access']
        return access_token