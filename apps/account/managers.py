
from typing import Any
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import UserManager, Group


class CustomUserManager(UserManager):
    
    def create_user(self, username, email=None, password=None, **extra_fields):
        user = super(CustomUserManager, self).create_user(username, email, password, **extra_fields)
        guest_group, _ = Group.objects.get_or_create(name='Guest')
        user.groups = guest_group
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        group, _ = Group.objects.get_or_create(name='Superusers')
        extra_fields.setdefault('groups', group)
        super(CustomUserManager, self).create_superuser(username, email, password, **extra_fields)