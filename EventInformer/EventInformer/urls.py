from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("eventchatbot/", include("eventchatbot.urls")),  # Include app URLs
]