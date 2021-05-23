"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

from merge.views import *

router = routers.DefaultRouter()
router.register(r'todos', TodoView, 'todo')
router.register(r'user', UserView, 'user')
router.register(r'profile', ProfileView, 'profile')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', Home.as_view(), name='home'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/', get_oauthtoken, name='token'),
    path('user/', get_user, name='user'),
    path('api/', include(router.urls)),
    path('repo/', include('merge.urls')),
    path('chat/', include('chats.api.urls', namespace='chat')),
    path('chpw/', change_password, name='change password'),
]
