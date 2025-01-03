from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from transformers import pipeline
import json

# Define your AI model pipelines (ensure they are correctly initialized)
qa_model = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Event context
event_context = """
TechFest 2024 will take place on March 19th at Kalamassery.
The event starts at 11:00 AM and features keynotes, ML workshops, and a networking session.
Notable speakers include Ars, SSK, SRK, and LJP.
"""

def homepage(request):
    return render(request, 'homepage.html')

class EventAIAPIView(View):
    def post(self, request):
        try:
            # Parse JSON body
            body = json.loads(request.body)
            user_message = body.get("message", "")

            if not user_message:
                return JsonResponse({"error": "Message is required."}, status=400)

            # Handle summarization requests
            if "summarize" in user_message.lower():
                summary = summarizer(event_context, max_length=50, min_length=25, do_sample=False)
                reply = summary[0]["summary_text"]
            else:
                # Handle Q&A
                result = qa_model({"context": event_context, "question": user_message})
                reply = result.get("answer", "Sorry, I couldn't understand that.")

            return JsonResponse({"reply": reply})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
