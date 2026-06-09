from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, nickname, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model(email=email, nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    nickname = models.CharField(max_length=10, blank=False, null=False)
    profile = models.TextField(blank=False, null=False)
    affiliation = models.CharField(max_length=100, blank=False, null=False)
    position = models.CharField(max_length=100, blank=False, null=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']
    objects = CustomUserManager()