from django.contrib import admin
from .models import Blog, Body, ImageBody, Comment


class BodyInline(admin.TabularInline):
    model = Body
    extra = 1


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    inlines = (BodyInline,)
    list_display = ('id', 'author', 'title', 'created_date')
    search_fields = ('title',)
    date_hierarchy = 'created_date'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'parent_comment', 'mini_comment_id')
    search_fields = ('author__first_name', 'author__last_name', 'author__username', 'blog__title',
                     'mini_comment_id',)
    date_hierarchy = 'created_date'


admin.site.register(ImageBody)
