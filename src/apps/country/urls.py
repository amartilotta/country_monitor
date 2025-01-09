from django.urls import include, path
from rest_framework import routers

from apps.country import views

router = routers.DefaultRouter()
router.register(r"countries", views.CountryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
