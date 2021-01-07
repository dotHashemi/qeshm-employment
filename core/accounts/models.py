from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def size(value,length=5):
    if len(str(value))!=length:
        raise ValidationError("%s is not the correct length." % value)


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    type = models.CharField(max_length=10, default=None)
    phone = models.CharField(max_length=11, unique=True)
    isVerified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)


class Verify(models.Model) :
    phone = models.CharField(unique=True, max_length=11)
    type = models.CharField(max_length=10)
    code = models.CharField(max_length=5, default=None)
    created = models.DateTimeField(auto_now=True)