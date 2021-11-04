from django.urls import path

from rest_framework.routers import SimpleRouter
from account import views


router = SimpleRouter()
router.register('', views.AccountViewSet)


urlpatterns = [] + router.get_urls()
