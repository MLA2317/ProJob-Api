from django.db import models
from django.conf import settings
from django.db.models.signals import post_save


class Blog(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=221)
    image = models.ImageField(upload_to='blog/')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Body(models.Model):
    post = models.OneToOneField(Blog, on_delete=models.CASCADE, related_name='post_body')
    body = models.TextField()

    def __str__(self):
        return self.body


class ImageBody(models.Model):
    body_text = models.ForeignKey(Body, on_delete=models.CASCADE, null=True, blank=True)
    blog_image = models.ImageField(upload_to='blog/image/', null=True, blank=True)
    is_script = models.BooleanField(default=False)


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='comments')
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    mini_comment_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"comment of {self.author} ({self.id})"

    @property
    def get_related_comments(self):
        qs = Comment.objects.filter(mini_comment_id=self.id).exclude(id=self.id)
        if qs:
            return qs
        return None


def comment_post_save(instance, sender, created, *args, **kwargs):
    if created:
        mini_comment = instance
        while mini_comment.parent_comment:
            mini_comment = mini_comment.parent_comment
        instance.mini_comment_id = mini_comment.id
        instance.save()


post_save.connect(comment_post_save, sender=Comment)
