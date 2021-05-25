from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']


class Status(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Statuses'

    def __str__(self):
        return self.title


class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user.name} - {self.status.title}'
    
    @property
    def phone_number(self):
        return str(self.phone[:-3] + '***')


class ExportConfiguration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    filename = models.CharField(max_length=100, default='filename')
    field_list = models.CharField(max_length=200, default='id,created_at,description,phone,status')

    def __str__(self):
        return f'{self.user} - {self.filename}'
