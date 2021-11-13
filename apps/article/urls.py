from django.urls import path

from rest_framework.routers import SimpleRouter
from apps.article import views


router = SimpleRouter()
router.register('', views.ArticleViewSet)

urlpatterns = [] + router.get_urls()
