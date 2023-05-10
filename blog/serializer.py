from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Comment, Blog, Body
from account.serializer import MyProfileSerializer


class MiniBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = Body
        fields = ('id', 'body', 'is_script')


class BlogDetailSerializer(serializers.ModelSerializer):
    post_body = MiniBodySerializer(read_only=True)
    author = MyProfileSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'author', 'title', 'image', 'description', 'created_date']


class BlogPostSerializer(serializers.ModelSerializer):
    post_body = MiniBodySerializer(read_only=True, many=True)

    class Meta:
        model = Blog
        fields = ('id', 'title', 'author', 'image', 'post_body', 'created_date')
        extra_kwargs = {
            'author': {"read_only": True},
            'image': {'required': False}
        }

    def validate(self, attrs):
        author = attrs.get('author')
        if author.role == 1:
            raise ValidationError('You are not HR')
        return attrs

    def create(self, validated_data):
        post_body = validated_data.pop('post_body', None)
        request = self.context['request']
        author = request.user
        instance = Blog.objects.filter(author=author, **validated_data)
        if post_body:
            for body in post_body:
                Body.objects.create(post_id=instance.id, body=body['body'], is_script=body['is_script'])
        return instance


class BodySerializer(serializers.ModelSerializer):
    class Meta:
        model = Body
        fields = ['id', 'post', 'body', 'blog_image', 'is_script']


class MiniCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "author", "blog", "comments", "body", "mini_comment_id", "created_date")


class CommentSerializer(serializers.ModelSerializer):
    author = MyProfileSerializer(read_only=True)
    children = serializers.SerializerMethodField(read_only=True)

    def get_children(self, obj): # obj bu commentni otasi
        children = Comment.objects.filter(parent_comment_id=obj.id)
        serializer = MiniCommentSerializer(children, many=True)
        return serializer.data

    class Meta:
        model = Comment
        fields = ("id", "author", "blog", "comments", "body", "mini_comment_id", "children", "created_date")
        extra_kwargs = {
            "author": {"read_only": True},
            "mini_comment_id": {"read_only": True},
            "blog": {"read_only": True}
        }

    def create(self, validated_data):
        request = self.context['request']
        blog_id = self.context['blog_id']
        user_id = request.user.id
        instance = Comment.objects.create(author_id=user_id, blog_id=blog_id, **validated_data) # **validation - malumotlani dictinary qilib beradi, fields dagi barcha malumotlani beradi
        return instance
