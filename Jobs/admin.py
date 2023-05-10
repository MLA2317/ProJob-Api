from django.contrib import admin
from .models import Job, ApplyJob, Category, Tag, Like, Position

# admin.site.register(Job)
# admin.site.register(ApplyJob)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Like)
admin.site.register(Position)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'title', 'category', 'city', 'price', 'position', 'day', 'created_date']


@admin.register(ApplyJob)
class ApplyJobAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'job', 'resume', 'created_date']
