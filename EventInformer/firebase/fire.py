import firebase_admin
from firebase_admin import credentials, firestore
from django.http import JsonResponse
# Path to your Firebase service account key file


# Initialize the Firebase Admin SDK
if not firebase_admin._apps:
  cred = credentials.Certificate('firebase/firebase_service_account.json')
  firebase_admin.initialize_app(cred)

# Firestore client initialization
db = firestore.client()

def store_event_in_firebase(event_data):
    events_ref = db.collection('events')  # Reference to Firestore 'events' collection
    events_ref.add(event_data)  # Add event data to the Firestore collection

def get_events_from_firebase():
    events_ref = db.collection('events')
    events = events_ref.stream()

    # Convert Firestore documents to a list of dictionaries
    event_list = []
    for event in events:
        event_dict = event.to_dict()
        event_list.append(event_dict)

    return event_list

def format_event_response(event_data):
    name = event_data.get('Name', 'Unknown')
    description = event_data.get('Description', 'Not Available')
    venue = event_data.get('Venue', 'Not Available')
    speakers = event_data.get('Speakers', 'Not Available')
    
    # Firestore timestamps are usually stored as native datetime objects
    timestamp = event_data.get('Date and time')
    if timestamp:
        formatted_date = timestamp.strftime("%d %B %Y at %I:%M %p")  # Format the date
    else:
        formatted_date = "Not Available"
    
    return (
        f"Event Name: {name}\n"
        f"Date: {formatted_date}\n"
        f"Venue: {venue}\n"
        f"Description: {description}\n"
        f"Speakers: {speakers}"
    )
