import re
from transformers import pipeline
import gradio as gr

# Load a question-answering model
qa_model = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# Load a summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Sample event context
event_context = """
TechFest 2024 will take place on March 19th at Kalamassery.
The event starts at 11:00 AM and features keynotes, ML workshops, and a networking session.
"""

# Function to extract date and time
def extract_date_time(context):
    date_time_pattern = r"\b(?:\d{1,2}(?:st|nd|rd|th)?\s(?:[A-Za-z]+)\s(?:\d{4}))\b.*?(\d{1,2}:\d{2}\s?[APap][Mm])"
    match = re.search(date_time_pattern, context)
    if match:
        return f"Event Date and Time: {match.group()}"
    else:
        return "Date and time not found in the context."

# Function to answer FAQs
def answer_question(context, question):
    if "date and time" in question.lower():
        return extract_date_time(context)
    
    result = qa_model({"context": context, "question": question})
    
    # Check if an answer is found
    answer = result.get("answer", "Sorry, I couldn't find an answer.")
    return answer

# Function to summarize event details
def summarize_event(details):
    summary = summarizer(details, max_length=100, min_length=25, do_sample=False)
    return summary[0]["summary_text"]

# Event Assistant function
def event_assistant(input_text):
    if "summarize" in input_text.lower():
        return summarize_event(event_context)
    else:
        return answer_question(event_context, input_text)

# Create Gradio Interface
gr.Interface(fn=event_assistant, inputs="text", outputs="text", title="Event AI Assistant").launch()
