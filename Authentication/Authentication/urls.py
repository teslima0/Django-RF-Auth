"""Authentication URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path,include
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers
from UserAuth.views import UserViewSet,LoginAPIView,LogoutAPIView
from rest_framework_simplejwt.views import (TokenRefreshView,)
schema_view = get_schema_view(
   openapi.Info(
      title="SpaceYaTech Blog API",
      default_version='v1',
      description="Blog website for developer",
      terms_of_service="https://www.ourapp.com/policies/terms/",
      contact=openapi.Contact(email="contact@expense.local"),
      license=openapi.License(name="Test License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()
router.register(r'UserAuth', UserViewSet, 'user')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ApiAuth/', include(router.urls)),
    path ('login/',LoginAPIView.as_view(), name = 'login'),
    path ('logout/',LogoutAPIView.as_view(), name = 'logout'),
    path ('token/refresh',TokenRefreshView.as_view(), name = 'token_refresh'),
    path ('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path ('api/api.json', schema_view.without_ui( cache_timeout=0), name='schema-swagger-ui'),
    path ('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


