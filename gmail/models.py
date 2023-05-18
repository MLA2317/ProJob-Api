from django.db import models


# class Email(models.Model):
#     name = models.CharField(max_length=16)
#     position = models.CharField(max_length=16, null=True)
#     email = models.EmailField(max_length=41, null=True)
#     describe = models.TextField()
#
#     class Meta:
#         db_table = 'Email'

class Email(models.Model):
    message = models.TextField()

    def __str__(self):
        return self.message