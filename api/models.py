from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin
from .manager import UserManager


class CustomUser(AbstractUser,PermissionsMixin):
    first_name = models.CharField(max_length=50,null=True,blank=True)
    last_name = models.CharField(max_length=50,null=True,blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50) 
    otp = models.IntegerField(null=True,blank=True)

    object = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    
