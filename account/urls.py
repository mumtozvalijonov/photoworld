from django.urls import path
from rest_framework_simplejwt import views as jwt_views


from rest_framework.routers import SimpleRouter
from account import views


router = SimpleRouter()
router.register('', views.AccountViewSet)

urlpatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh')
] + router.get_urls()
