from django.urls import path
from .views import JobListApi, JobCreate, JobRUDApi, LikeListCreate, ApplyJobListAdmin, ApplyJobCreate, ApplyJobGetList, CategoryListCreate, \
    TagListCreate, PositionListCreate


urlpatterns = [
    # job
    path('job-create/', JobCreate.as_view()),
    path('job-list/', JobListApi.as_view()),
    path('job-rud/<int:pk>/', JobRUDApi.as_view()),
    # CV
    path('applyjob-admin/', ApplyJobListAdmin.as_view()),
    path('applyjobget-hr/', ApplyJobCreate.as_view()),
    path('applyjob-rud/<int:job_id>/', ApplyJobGetList.as_view()),
    # like
    path('like-create/<int:jobs_id>/', LikeListCreate.as_view()),
    # category
    path('categroy-ls/', CategoryListCreate.as_view()),
    path('tag-ls/', TagListCreate.as_view()),
    path('position-ls/', PositionListCreate.as_view())
]
