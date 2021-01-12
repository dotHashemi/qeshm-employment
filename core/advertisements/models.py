from django.db import models
from django.contrib.auth.models import User

from cities.models import City
from categories.models import Category


class Advertisement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    description = models.TextField()
    isFullTime = models.BooleanField(default=False)
    isRemote = models.BooleanField(default=False)
    isInternship = models.BooleanField(default=False)
    isMilitary = models.BooleanField(default=False)
    salary = models.PositiveIntegerField(default=None, null=True, blank=True)
    isActive = models.BooleanField(default=True)
    isVerified = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title
