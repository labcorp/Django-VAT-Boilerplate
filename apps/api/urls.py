from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()
app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),

    path('auth/basic/', views.obtain_auth_token),
    path('auth/jwt/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
