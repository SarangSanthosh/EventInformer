import firebase_admin
from firebase_admin import credentials, firestore

# Path to your Firebase service account key file
cred = credentials.Certificate('firebase/firebase_service_account.json')

# Initialize the Firebase Admin SDK
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

