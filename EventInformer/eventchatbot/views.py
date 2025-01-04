from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from transformers import pipeline
import json
import firebase_admin
from firebase_admin import credentials, firestore
from firebase.fire import format_event_response  # Import the function from firebase.py

# Initialize Firebase (Ensure firebase_service_account.json is correctly configured)
cred = credentials.Certificate("firebase/firebase_service_account.json")
#firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

# Initialize AI models
qa_model = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


# Homepage View
def homepage(request):
    return render(request, 'homepage.html')


# Event AI API View
class EventAIAPIView(View):
    def post(self, request):
        try:
            # Parse JSON body
            body = json.loads(request.body)
            user_message = body.get("message", "").lower()

            if not user_message:
                return JsonResponse({"error": "Message is required."}, status=400)

            # Fetch events from Firestore
            events_ref = db.collection("events")
            events = events_ref.stream()
            event_list = [event.to_dict() for event in events]

            if event_list:
                # Format Firestore data into dynamic context using the helper function
                event_context = "Here are the details of upcoming events:\n"
                for event in event_list:
                    formatted_event = format_event_response(event)  # Use the function to format the event data
                    event_context += formatted_event + "\n\n"
            else:
                event_context = "No events are currently available."

            # Summarization Request
            if "summarize" in user_message:
                summary = summarizer(event_context, max_length=50, min_length=25, do_sample=False)
                reply = summary[0]["summary_text"]

            # Question-Answering Request
            else:
                result = qa_model({"context": event_context, "question": user_message})
                reply = result.get("answer", "Sorry, I couldn't understand that.")

            return JsonResponse({"reply": reply})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
