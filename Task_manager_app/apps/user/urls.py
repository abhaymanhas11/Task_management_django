from django.urls import path
from apps.user import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path("", views.LoginUser.as_view(), name="loginuser"),
    path("logout", views.Userlogout, name="logout"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", views.RegisterAPIView.as_view(), name="register"),
]
    