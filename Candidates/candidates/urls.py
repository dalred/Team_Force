from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from users import views

urlpatterns = [
    path('', views.root),
    path("admin/", admin.site.urls),
    path("", include("users.urls")),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
router = routers.SimpleRouter()
urlpatterns += router.urls