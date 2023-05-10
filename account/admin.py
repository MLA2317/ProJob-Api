from django.contrib import admin
from .models import Account, MyHistoryJob
from .forms import AccountChangeForms, AccountFormsCreate


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    add_form = AccountFormsCreate
    form = AccountChangeForms
    list_display = ['id', 'username', 'image_tag', 'first_name', 'last_name', 'email', 'role', 'location', 'is_superuser',
                    'is_staff', 'is_active', 'modified_date', 'created_date']


@admin.register(MyHistoryJob)
class MyHistoryJobAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'worked', 'company', 'city', 'start_date', 'end_date', 'is_current']
