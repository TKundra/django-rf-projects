from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
"""
AbstractUser        - django default fields + your own custom fields
AbstractBaseUser    - no default fields, start from scratch ny creating your own, completely new user model
BaseUserManager     - 
"""
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields): # (self, first_field, password, others)
        if not email:
            raise ValueError("Email is required")
        
        email = self.normalize_email(email)             # from Abc@gma.com to abc@gmail.com
        user = self.model(email=email, **extra_fields)
        user.set_password(password)                     # encrypt password
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_staff being True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser being True")

        return self.create_user(email=email, password=password, **extra_fields)

class User(AbstractUser):
    email = models.CharField(max_length=80, unique=True)
    username = models.CharField(max_length=45, unique=True)
    date_of_birth = models.DateField(null=True)
    bio = models.CharField(max_length=50)

    objects = CustomUserManager()   # will help to provide custom fields to django
    USERNAME_FIELD = "email"        # will change default django login field i.e by default username-password. From now email-password
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
