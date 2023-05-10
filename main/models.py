from django.db import models


class Country(models.Model):
    title = models.CharField(max_length=221)

    def __str__(self):
        return self.title


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.CharField(max_length=221)

    def __str__(self):
        return f"{self.city},{self.country.title}"


class Company(models.Model):
    name = models.CharField(max_length=221)

    def __str__(self):
        return self.name
