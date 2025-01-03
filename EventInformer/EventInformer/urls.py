from django.urls import path, include
from . import views
from django.contrib import admin


urlpatterns = [
    path("", views.homepage, name="homepage"),  # Main homepage route
     path('admin/', admin.site.urls),
    path('eventchatbot/', include('eventchatbot.urls')),  # Includes urls from the eventchatbot app
]
