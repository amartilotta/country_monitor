from django.urls import path, include
from rest_framework import routers
from country_monitor.apps.country import views

router = routers.DefaultRouter()
router.register(r'countries', views.CountryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]