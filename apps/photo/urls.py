from django.urls import path

from rest_framework.routers import SimpleRouter

from apps.photo import views


router = SimpleRouter()
router.register('', views.PhotoViewSet)


urlpatterns = [] + router.get_urls()
