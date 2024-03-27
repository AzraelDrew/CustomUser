import uuid
from django.utils.timezone import now
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("邮箱地址无效")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.save()
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get("is_staff") is not True:
            return ValueError("超级用户的is_staff属性必须为True")

        if extra_fields.get("is_superuser") is not True:
            return ValueError("超级用户的is_superuser属性必须为True")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, blank=True, default='unknown')
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    phone = models.CharField(max_length=11, blank=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True,)
    last_login = models.DateTimeField(auto_now_add=True,)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        self.set_password(self.password)
        return super().save(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.last_login = now()
        return super().save(update_fields=['last_login'])

    def __str__(self):
        return self.email
