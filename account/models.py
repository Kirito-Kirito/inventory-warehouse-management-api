from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrator'
        MANAGER = 'MANAGER', 'Warehouse Manager'
        STAFF = 'STAFF', 'Warehouse Staff'

    role = models.CharField(max_length=20, choices=Role.choices,default=Role.STAFF)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'