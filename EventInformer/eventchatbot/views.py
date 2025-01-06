from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from transformers import pipeline
import json
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from firebase.fire import format_event_response
from difflib import get_close_matches  # Import the function from firebase.py

cred = credentials.Certificate("firebase/firebase_service_account.json")


# Get Firestore client
db = firestore.client()

def homepage(request):
    return render(request, 'homepage.html')

def get_closest_event_name(input_name, event_list):
    input_name = input_name.lower()
    all_event_names = [event.get('Name', '').lower() for event in event_list]
    matches = get_close_matches(input_name, all_event_names, n=1, cutoff=0.6)  # Adjust cutoff for flexibility
    return matches[0] if matches else None

def extract_event_details(user_message, event_name, event_data):
    if not event_data:
        return f"Sorry, I couldn't find any details for '{event_name}'. Please check the event name and try again."
    
    user_message = user_message.lower()

    if "time" in user_message or "starts" in user_message or "schedule" in user_message:
        return f"The event '{event_name}' starts at {event_data.get('Date and time', 'not specified')}."
    elif "date" in user_message:
        return f"The event '{event_name}' is scheduled for {event_data.get('Date and time', 'not specified')}."
    elif "speakers" in user_message:
        return f"The speakers for the event '{event_name}' are {event_data.get('Speakers', 'not specified')}."
    elif "venue" in user_message:
        return f"The venue for the event '{event_name}' is {event_data.get('Venue', 'not specified')}."
    elif "about" in user_message or "info" in user_message or "description" in user_message:
        return f"The event '{event_name}' is about: {event_data.get('Description', 'No description available')}."
    else:
        return "I'm not sure how to help with that. Could you clarify?"



def fetch_event_details(event_name):
    events_ref = db.collection("events")
    events = [event.to_dict() for event in events_ref.stream()]
    
    closest_name = get_closest_event_name(event_name, events)
    if closest_name:
        for event in events:
            if event.get('Name', '').lower() == closest_name:
                return event
    return None



# Function to handle vague or non-event related queries
def handle_vague_queries(user_message):
    vague_keywords = [
        "hi", "hello", "how are you", "how's it going", "what's up", "joke", "meme", "funny", "tell me something",
        "good morning", "good evening", "how do you do", "random", "love", "life", "mom", "dad", "what's your name"
    ]
    for keyword in vague_keywords:
        if keyword in user_message:
            return True
    return False

class EventAIAPIView(View):
    def post(self, request):
        try:
            # Parse JSON body
            body = json.loads(request.body)
            user_message = body.get("message", "").lower()

            if not user_message:
                return JsonResponse({"error": "Message is required."}, status=400)

            # Handle vague queries
            if handle_vague_queries(user_message):
                if "hi" in user_message or "hello" in user_message:
                    return JsonResponse({"reply": "Hello! How can I assist you with upcoming events today?"})
                elif "how are you" in user_message or "how's it going" in user_message:
                    return JsonResponse({"reply": "I'm doing great! How about you? Let's talk about some upcoming events!"})
                elif "joke" in user_message or "meme" in user_message:
                    return JsonResponse({"reply": "I can only assist with events! Ask me about upcoming events."})
                else:
                    return JsonResponse({"reply": "I'm here to help with event details. Can you ask about upcoming events?"})

            # Handle event-specific queries
            if any(keyword in user_message for keyword in ["speakers", "venue", "time", "schedule", "about"]):
                event_name = user_message.split("of")[-1].strip()
                event_data = fetch_event_details(event_name)
                if event_data:
                    reply = extract_event_details(user_message, event_name, event_data)
                else:
                    reply = f"Sorry, I couldn't find any event named '{event_name}'. Please check the name and try again."
                return JsonResponse({"reply": reply})

            # Handle general event details
            if any(keyword in user_message for keyword in ["tell me about", "what is", "details of", "info about"]):
                event_name = user_message.split("about")[-1].strip()
                if not event_name:
                    return JsonResponse({"reply": "Please specify an event name."})

                event_data = fetch_event_details(event_name)
                if event_data:
                    reply = extract_event_details(user_message, event_name, event_data)
                else:
                    reply = f"Sorry, I couldn't find any event named '{event_name}'. Please check the name and try again."
                return JsonResponse({"reply": reply})

            # Fetch all events if no specific query matches
            events_ref = db.collection("events")
            events = events_ref.stream()
            event_list = [event.to_dict() for event in events]

            if event_list:
                # Format Firestore data into dynamic context using the helper function
                event_context = "Here are the details of upcoming events:\n"
                for event in event_list:
                    formatted_event = format_event_response(event)
                    event_context += formatted_event + "\n\n"
            else:
                event_context = "No events are currently available."

            return JsonResponse({"reply": event_context})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
