from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.conf import settings
from django.utils.safestring import mark_safe
from rest_framework_simplejwt.tokens import RefreshToken
from main.models import Company, Country, City

from django.db.models.signals import pre_save


class AccountManager(BaseUserManager): # manager - bu user model un yordamchi class, user model create qilish un qonun qoidalarini toplami
    def create_user(self, username, password=None, **extra_fields):
        if username is None:
            raise TypeError('User should have a username')

        user = self.model(username=username, **extra_fields) # user yasavolamiz
        user.set_password(password)
        user.save(using=self._db) # db - bu settingdagi defoult database dan foydalansin
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        if password is None:
            raise TypeError("Password should not be None")

        user = self.create_user(
            username=username,
            password=password,
            **extra_fields
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.role = 2
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    ROLE = (
        (0, 'HR'),  # ish beruvchi
        (1, 'Candidate'),
        (2, 'is_staff'),
    )
    username = models.CharField(max_length=50, unique=True, verbose_name='Username', db_index=True)
    avatar = models.ImageField(upload_to='profile/', null=True)
    email = models.EmailField(max_length=50, unique=True, verbose_name='Email', db_index=True)
    first_name = models.CharField(max_length=50, verbose_name='first_name', null=True)
    last_name = models.CharField(max_length=50, verbose_name='last_name', null=True)
    role = models.IntegerField(choices=ROLE, default=0)
    location = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    is_superuser = models.BooleanField(default=False, verbose_name='Super user')
    is_staff = models.BooleanField(default=False, verbose_name='Staff user')
    is_active = models.BooleanField(default=True, verbose_name='Active user')
    bio = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Created Date')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Modified Date')

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def image_tag(self):
        if self.avatar:
            return mark_safe(f"<a href='{self.avatar.url}'><img src='{self.avatar.url}' style='height:43px;'/></a>")
        else:
            return 'Image not found'

    @property
    def avatar_url(self):
        if self.avatar:
            if settings.DEBUG:
                return f"{settings.LOCALE_BASE_URL}{self.avatar.url}"
            return f"{settings.PROD_BASE_URL}{self.avatar.url}"
        return None

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return data


class MyHistoryJob(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    worked = models.CharField(max_length=50)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(auto_now_add=True)
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return f"Candidate's job of {self.company} company"


def account_post_save(instance, sender, *args, **kwargs):
    if instance.role == 2:
        instance.is_staff = True
    else:
        instance.is_staff = False
    return instance


pre_save.connect(account_post_save, sender=Account)


