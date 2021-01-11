from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=50)
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
