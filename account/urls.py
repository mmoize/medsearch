from django.urls import path, include
from .views import CustomAuthTokenSignup, CustomAuthTokenLogin
from rest_framework import routers

app_name = 'account'

router = routers.DefaultRouter()


urlpatterns = [
    path('signup', CustomAuthTokenSignup.as_view()),
    path('login', CustomAuthTokenLogin.as_view()),
    path('api/', include(router.urls)),
]