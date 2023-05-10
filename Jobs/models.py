from django.db import models
from account.models import Account
from main.models import Country, City, Company


class Category(models.Model):
    title = models.CharField(max_length=221)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=221)

    def __str__(self):
        return self.title


class Position(models.Model):
    title = models.CharField(max_length=221)

    def __str__(self):
        return self.title


class Job(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=221)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='companies')
    tag = models.ManyToManyField(Tag)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='cities')
    price = models.DecimalField(decimal_places=3, max_digits=5)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True)
    day = models.IntegerField(null=True, blank=True)
    description = models.TextField()

    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Like(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='author')
    jobs = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='jobs')

    def __str__(self):
        return f"{self.author}'s like"


class ApplyJob(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"resume of {self.author} in {self.job}"
