from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogViewSet, BodyRUD, CommentListCreate

router = DefaultRouter()
router.register('post', BlogViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('blog_rud/<int:pk>', BodyRUD.as_view()),
    path('<int:post_id>/coment-create/', CommentListCreate.as_view())
]
