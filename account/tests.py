from django.urls import reverse
from rest_framework import status

from account.models import Account
from core.tests import CoreTestCase


class AccountTests(CoreTestCase):

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

    def test_update_account_by_owner(self):
        username = 'test'
        password = 'password'
        email = 'user@email.com'

        Account.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        access_token = self.login_user(username, password)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        url = reverse('account-detail', kwargs={'pk': username})

        response = self.client.patch(url, {'bio': 'Some bio'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['bio'], Account.objects.get(username=username).bio)

    def test_update_account_by_non_owner(self):
        account = Account.objects.create_user(
            username='test',
            password='password',
            email='user@email.com'
        )

        username = 'username'
        password = 'password'
        email = 'email@email.com'
        Account.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        access_token = self.login_user(username, password)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        url = reverse('account-detail', kwargs={'pk': account.username})

        response = self.client.patch(url, {'bio': 'Some bio'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_with_wrong_credentials(self):
        username = 'username'
        password = 'password'
        wrong_password = 'wrong_password'
        email = 'email@email.com'
        Account.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        url = reverse('token_obtain_pair')
        login_response = self.client.post(url, data={'username': username, 'password': wrong_password})
        self.assertEqual(login_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_register_with_wrong_body(self):
        username = 'username'
        password = 'password'
        email = 'email@email.com'

        url = reverse('account-list')
        
        data = {
            'username': username,
            'password': password
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'username': username,
            'email': email
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'email': email,
            'password': password
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_exising_username(self):
        username = 'username'
        password = 'password'
        email = 'email@email.com'
        Account.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        url = reverse('account-list')
        data = {
            'username': username,
            'password': 'new_password',
            'email': 'new_email@email.com'
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_inactive_user(self):
        username = 'username'
        password = 'password'
        email = 'email@email.com'
        account = Account.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        account.is_active = False
        account.save()

        url = reverse('token_obtain_pair')
        login_response = self.client.post(url, data={'username': username, 'password': password})
        self.assertEqual(login_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_username(self):
        username = 'username'
        password = 'password'
        new_username = 'new_username'
        email = 'email@email.com'
        account = Account.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        access_token = self.login_user(username, password)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        url = reverse('account-detail', kwargs={'pk': account.username})
        data = {'username': new_username}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['username'], Account.objects.get(username=new_username).username)

    def test_update_to_existing_username(self):
        existing_username = 'existing_username'
        existing_password = 'password'
        existing_email = 'existing_email@email.com'
        Account.objects.create_user(
            username=existing_username,
            email=existing_email,
            password=existing_password,
        )

        username = 'username'
        password = 'password'
        email = 'email@email.com'

        Account.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        access_token = self.login_user(username, password)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        url = reverse('account-detail', kwargs={'pk': username})
        data = {'username': existing_username}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_account(self):
        username = 'username'
        password = 'password'
        email = 'email@email.com'

        Account.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        access_token = self.login_user(username, password)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        url = reverse('account-detail', kwargs={'pk': username})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_another_persons_account(self):
        existing_username = 'existing_username'
        existing_password = 'password'
        existing_email = 'existing_email@email.com'
        Account.objects.create_user(
            username=existing_username,
            email=existing_email,
            password=existing_password,
        )

        username = 'username'
        password = 'password'
        email = 'email@email.com'

        Account.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        access_token = self.login_user(username, password)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        url = reverse('account-detail', kwargs={'pk': existing_username})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
