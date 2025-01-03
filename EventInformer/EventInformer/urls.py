from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.homepage, name="homepage"),  # Main homepage route
    path('eventchatbot/', include('eventchatbot.urls')),  # Includes urls from the eventchatbot app
]
