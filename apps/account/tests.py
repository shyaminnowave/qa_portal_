from typing import Any
from django.test import TestCase
import pytest
from django.contrib.auth import get_user_model
from pkg_resources import DistributionNotFound, get_distribution
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import Group
# Create your tests here.

User = get_user_model()


@pytest.mark.django_db
class TestUser:

    def setup_method(self):
        self.group = Group.objects.create(name='Guest')

    def test_create_user(self):
        user = User.objects.create_user(
            username="test_name",
            email="test@innowave.tech",
            password="password@123"
        )
        assert user.email == 'test@innowave.tech'
        assert user.username == 'test_name'
        assert self.group in user.groups.all()
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser

    def test_super_user(self):
        admin_user = User.objects.create_superuser(
                    username='admin',
                    email='test@innowave.tech',
                    password='admin123'
                )
        assert admin_user.email == 'test@innowave.tech'
        assert admin_user.username == 'admin'
        assert admin_user.is_staff
        assert admin_user.is_active
        assert admin_user.is_superuser


class TestLoginView(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'test1@innowave.tech ',
            'fullname': 'shyamkumar',
            'password': 'shyamkumar',
            'confirm_password': 'shyamkumar'
        }
        self.url = reverse('accounts.create-user')

    def test_create_user(self):
        response = self.client.post(self.url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_wrong_user(self):
        _data = {
            'email': 'test1@gmail.in ',
            'fullname': 'shyamkumar',
            'password': 'shyamkumar',
            'confirm_password': 'shyamkumar'
        }
        response = self.client.post(self.url, _data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user(self):
        user = User.objects.create_user(email='tets@gmail.com',
                                        username='test',
                                        password='shyamkumar')
        self.data = {
            'email': 'tets@gmail.com',
            'password': 'shyamkumar'
        }
        self._url = reverse('login')
        response = self.client.post(self._url, self.data)
        self.assertContains(response, 'access', status_code=status.HTTP_200_OK)

    def test_wrong_user(self):
        user = User.objects.create_user(email='tets@gmail.com',
                                        username='test',
                                        password='shyamkumar')

        self._url = reverse('login')
        self.data = {
            'email': 'tets@gmail.com',
            'password': 'shyamumar'
        }
        response = self.client.post(self._url, self.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)