from django.db.models import Q
from rest_framework.response import Response
from rest_framework import generics, status, permissions, serializers
from .serializer import JobListSerializer, JobDetailSerializer, JobPostSerializer, ApplyJobSerializer, \
    ApplyJobGetSerializer, CategorySerializer, TagSerializer, PositionSerializer, LikePostSerializer, LikeGetSerializer
from .models import Job, ApplyJob, Position, Category, Tag, Like


class TagListCreate(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAdminUser]


class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


class PositionListCreate(generics.ListCreateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [permissions.IsAuthenticated]


class ApplyJobCreate(generics.CreateAPIView):
    queryset = ApplyJob.objects.all()
    serializer_class = ApplyJobSerializer
    permission_classes = [permissions.IsAuthenticated]


class ApplyJobListAdmin(generics.ListAPIView):
    queryset = ApplyJob.objects.all()
    serializer_class = ApplyJobSerializer
    permission_classes = [permissions.IsAdminUser]


class ApplyJobGetList(generics.ListAPIView):
    queryset = ApplyJob.objects.all()
    serializer_class = ApplyJobGetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset() # obyketni hammasini oladi
        job_id = self.kwargs.get('job_id') # joblani id sini oladi
        author = self.request.user # userni oladi
        if author.role == '1': # validatsiya qiladi
            raise serializers.ValidationError("You aren't HR")
        # qs = qs.filter(job__author_id=author.id)
        # qs = qs.filter(job_id = job_id)
        return qs.filter(job_id=job_id) # job_id ga tegishli resumelani chiqarib beradi


class JobListApi(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get('search')
        cat = self.request.GET.get('cat')
        city = self.request.GET.get('city')
        search_conditions = Q()
        cat_conditions = Q()
        city_conditions = Q()
        if search:
            search_conditions = Q(title_icontains=search)
        if cat:
            cat_conditions = Q(category__title__exact=cat)
        if city:
            city_conditions =Q(city__title__exact=city)
        qs = qs.filter(search_conditions, cat_conditions, city_conditions)
        return qs


class JobRUDApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class JobCreate(generics.CreateAPIView):
    queryset = Job.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return JobPostSerializer
        return JobListSerializer


class LikeListCreate(generics.ListCreateAPIView):
    # http://127.0.0.1:8000/Jobs/like-create/1/
    queryset = Like.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return LikePostSerializer
        return LikeGetSerializer

    def create(self, request, *args, **kwargs):
        author_id = request.user.id
        jobs_id = self.kwargs.get('jobs_id')
        likes = Like.objects.filter(author_id=author_id, jobs_id=jobs_id)
        if likes:
            likes.delete()
            return Response({'message': 'Like deleted'})
        likes = Like.objects.create(author_id=author_id, jobs_id=jobs_id)
        serializer = LikePostSerializer(likes)
        return Response(serializer.data)





