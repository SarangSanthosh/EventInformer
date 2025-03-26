# from django.urls import path
# from .views import dialogflow_webhook, homepage

# urlpatterns = [
#     path("", homepage, name="homepage"),  # Homepage at eventchatbot/
#     path("dialogflow/", dialogflow_webhook, name="dialogflow_webhook"),  # Webhook URL
# ]
from django.urls import path
from .views import chat_page, handle_chat

urlpatterns = [
    path('', chat_page, name='chat_page'),          # Handles page view
    path('process/', handle_chat, name='handle_chat'),  # Handles API calls
]