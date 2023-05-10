from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=50)
    message = models.TextField()

    def __str__(self):
        return self.name


class Subscribe(models.Model):
    email = models.EmailField()
