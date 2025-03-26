# import json
# import os
# import logging
# import requests
# import google.auth
# from google.auth.transport.requests import Request
# from google.oauth2 import service_account
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import uuid  # For generating unique session IDs

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
# from django.shortcuts import render

# def homepage(request):
#     return render(request, "homepage.html")  # Ensure this template exists

# # Load Google Service Account Credentials
# SERVICE_ACCOUNT_FILE = os.getenv("DIALOGFLOW_KEY_PATH", "/home/sarang/project/EventInformer/ai/dialogflow_key.json")
# try:
#     credentials = service_account.Credentials.from_service_account_file(
#         SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/cloud-platform"]
#     )
# except Exception as e:
#     logger.error(f"Failed to load service account file: {e}")
#     raise

# DIALOGFLOW_PROJECT_ID = "event-project-rekj"
# LANGUAGE_CODE = "en"

# @csrf_exempt
# def dialogflow_webhook(request):
#     if request.method != "POST":
#         return JsonResponse({"error": "Invalid request method"}, status=400)

#     try:
#         data = json.loads(request.body)
#         user_message = data.get("message")
        
#         if not user_message:
#             return JsonResponse({"error": "No message provided"}, status=400)

#         # Generate a unique session ID per user interaction (if a user ID is provided)
#         session_id = data.get("session_id", str(uuid.uuid4()))

#         # Obtain an authenticated token
#         auth_request = Request()
#         credentials.refresh(auth_request)
#         auth_token = credentials.token

#         dialogflow_url = f"https://dialogflow.googleapis.com/v2/projects/{DIALOGFLOW_PROJECT_ID}/agent/sessions/{session_id}:detectIntent"

#         headers = {
#             "Authorization": f"Bearer {auth_token}",
#             "Content-Type": "application/json",
#         }

#         payload = {
#             "queryInput": {
#                 "text": {
#                     "text": user_message,
#                     "languageCode": LANGUAGE_CODE,
#                 }
#             }
#         }

#         response = requests.post(dialogflow_url, headers=headers, json=payload)
#         response_data = response.json()

#         if "queryResult" in response_data:
#             fulfillment_text = response_data["queryResult"].get("fulfillmentText", "Sorry, I couldn't understand that.")
#             return JsonResponse({"reply": fulfillment_text})

#         # Log full response in case of unexpected errors
#         logger.error(f"Unexpected Dialogflow response: {response_data}")
#         return JsonResponse({"error": "Invalid Dialogflow response"}, status=500)

#     except Exception as e:
#         logger.error(f"Error processing request: {str(e)}", exc_info=True)
#         return JsonResponse({"error": str(e)}, status=500)

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
import logging
import requests
import google.auth
from google.auth.transport.requests import Request
from google.oauth2 import service_account
import uuid

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Homepage view
def chat_page(request):
    """Render the chat interface page"""
    return render(request, 'homepage.html')

# Dialogflow integration view
@csrf_exempt
def handle_chat(request):
    """Handle chat messages via Dialogflow"""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        # Load service account credentials
        SERVICE_ACCOUNT_FILE = os.getenv("DIALOGFLOW_KEY_PATH", "/home/sarang/project/EventInformer/ai/dialogflow_key.json")
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, 
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        
        data = json.loads(request.body)
        user_message = data.get("message")
        
        if not user_message:
            return JsonResponse({"error": "No message provided"}, status=400)

        # Generate session ID
        session_id = data.get("session_id", str(uuid.uuid4()))

        # Get authentication token
        auth_request = Request()
        credentials.refresh(auth_request)
        auth_token = credentials.token

        # Call Dialogflow API
        DIALOGFLOW_PROJECT_ID = "proven-serenity-448608-b5"
        dialogflow_url = f"https://dialogflow.googleapis.com/v2/projects/{DIALOGFLOW_PROJECT_ID}/agent/sessions/{session_id}:detectIntent"

        response = requests.post(
            dialogflow_url,
            headers={
                "Authorization": f"Bearer {auth_token}",
                "Content-Type": "application/json",
            },
            json={
                "queryInput": {
                    "text": {
                        "text": user_message,
                        "languageCode": "en",
                    }
                }
            }
        )
        response_data = response.json()

        if "queryResult" in response_data:
            fulfillment_text = response_data["queryResult"].get("fulfillmentText", "Sorry, I couldn't understand that.")
            return JsonResponse({"reply": fulfillment_text})

        logger.error(f"Unexpected Dialogflow response: {response_data}")
        return JsonResponse({"error": "Invalid Dialogflow response"}, status=500)

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return JsonResponse({"error": str(e)}, status=500)

