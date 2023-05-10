from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from .models import Category, Tag, Job, Like, ApplyJob, Position
from main.serializer import CompanySerializer, CitySerializer
from account.serializer import MyProfileSerializer, AccountUpdateSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title']


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'title']


class JobListSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    city = CitySerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    author = MyProfileSerializer(read_only=True)
    position = PositionSerializer(read_only=True)

    class Meta:
        model = Job
        fields = ['id', 'author', 'title', 'company', 'city', 'tags', 'price', 'position']


class JobDetailSerializer(serializers.ModelSerializer):
    author = AccountUpdateSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)

    # tags = PositionSerializer(read_only=True, many=True)

    class Meta:
        model = Job
        fields = ['id', 'author', 'title', 'category', 'company', 'tags', 'city', 'price', 'position',
                  'description', 'created_date']


class JobPostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    # '''
    # {
    #     id: 1
    #    country title: "nimadir shahar"
    #     city: {            # read_only=True holatda ishledi
    #         id: 2
    #         title: "nimadir Davlat"
    #         }
    #     tags: {             # many=True holatda ishledi
    #         1: {
    #             id: 1
    #             title: 'tag1'
    #             }
    #         }
    #         2: {
    #             id: 3
    #             title: 'tag3'
    #             }
    #         }
    # }
    # '''

    class Meta:
        model = Job
        fields = ['id', 'author', 'title', 'category', 'tags', 'company', 'city', 'price', 'position', 'day',
                  'description']
        extra_kwargs = {
            'author': {'required': False}
        }

    def validate(self, attrs):
        request = self.context['request']
        author = request.user
        print(author)
        if author.role == 1:
            raise ValidationError({
                'message': "You don't create job!"
            })
        print(attrs)
        return attrs

    def create(self, validated_data):
        requests = self.context['request']
        author = requests.user
        instance = super().create(validated_data)
        instance.author = author
        print(instance.author)
        instance.save()
        return instance


class LikeGetSerializer(serializers.ModelSerializer):
    author = MyProfileSerializer(read_only=True)
    jobs = JobListSerializer(read_only=True, many=True)

    class Meta:
        model = Like
        fields = ['id', 'author', 'jobs']


class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'author', 'jobs']


class ApplyJobGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyJob
        fields = ['job', 'author', 'resume', 'created_date']


class ApplyJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyJob
        fields = ['id', 'job', 'author', 'resume', 'created_date']
        extra_kwargs = ({
            "author": {"read_only": False}
        })

    def validate(self, attrs):
        author = attrs.get('author')
        if author.role == 0:
            raise ValidationError({
                'message': "You don't send CV, because you are HR!"
            })
        return attrs

    def create(self, validated_data):
        request = self.context['request']
        author = request.user
        instance = super().create(validated_data)
        instance.author = author
        return instance



