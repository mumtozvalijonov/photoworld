from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from PIL import Image
from io import BytesIO

from account.models import Account
from apps.photo.models import Photo


class PhotoTests(APITestCase):

    def test_list_photo(self):
        url = reverse('photo-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], Photo.objects.count())

    def test_create_photo(self):
        username = 'test'
        password = 'secretpassword'
        Account.objects.create_user(
            username=username,
            email='test@test.com',
            password=password
        )

        url = reverse('token_obtain_pair')
        login_response = self.client.post(url, data={'username': username, 'password': password})
        access_token = login_response.json()['access']

        # headers = {'Authorization': f'Bearer {access_token}'}
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        photo_file = self.generate_photo_file()
        data = {
            'image': photo_file
        }
        url = reverse('photo-list')
        response = self.client.post(url, data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def generate_photo_file(self):
        file_obj = BytesIO()
        with Image.new("RGBA", size=(50, 50), color=(255, 0, 0)) as image:
            image.save(file_obj, "png")
            file_obj.seek(0)
            file_obj.name = "testasdas.png"
            file_obj.size = 1000
        return file_obj

