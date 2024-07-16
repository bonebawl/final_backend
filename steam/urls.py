from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path("bruh/", views.search_games),
    path("api/nearby/", views.get_places, name="view"),
    path("api/reset/", views.reset_api_requests, name="reset"),
    path("api/search/", views.wikipedia_handler, name="wiki")
]


