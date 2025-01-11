from django.urls import path

from apps.country import views

urlpatterns = [
    path("", views.CountryViewSet.as_view({"get": "get_countries"})),
    path(
        "<int:country_id>/",
        views.CountryViewSet.as_view(
            {
                "get": "get_country_by_id",
            }
        ),
    ),
]
