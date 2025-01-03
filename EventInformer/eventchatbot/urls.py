from django.urls import path
from . import views

urlpatterns = [
    path('api/chatbot/', views.EventAIAPIView.as_view(), name='chatbot_api'),
]
