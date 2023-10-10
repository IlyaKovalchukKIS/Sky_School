from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _

NULLABLE = {'blank': True, 'null': True}


class UserRole(models.TextChoices):
    MEMBER = 'member', _('member')
    MANAGER = 'manager', _('manager')


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    role = models.CharField(max_length=10, choices=UserRole.choices, **NULLABLE)

    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    country = CountryField(verbose_name='страна', **NULLABLE)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
