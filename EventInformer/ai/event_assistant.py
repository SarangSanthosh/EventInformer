import re
from transformers import pipeline
import gradio as gr

# Load models
qa_model = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Event context
event_context = """
TechFest 2024 will take place on March 19th at the Kalamassery.
The event starts at 11:00 AM and features keynotes, ML workshops, and a networking session.
Notable speakers are ars, ssk, srk, ljp.
"""

# Function to extract date and time
def extract_date_time(context):
    date_pattern = r"\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s\d{1,2}(?:st|nd|rd|th)?,?\s\d{4}\b"
    time_pattern = r"\b\d{1,2}:\d{2}\s(?:AM|PM)\b"

    date_match = re.search(date_pattern, context)
    time_match = re.search(time_pattern, context)

    date = date_match.group(0) if date_match else "No date found"
    time = time_match.group(0) if time_match else "No time found"

    return f"{date} at {time}"

# Function to answer questions
def answer_question(context, question):
    # If the question explicitly asks for date and time, extract both
    if "date and time" in question.lower():
        return extract_date_time(context)
    
    # Default QA model response
    result = qa_model({"context": context, "question": question})
    return result["answer"]

# Function to summarize event details
def summarize_event(details):
    summary = summarizer(details, max_length=50, min_length=25, do_sample=False)
    return summary[0]["summary_text"]

# Event assistant logic
def event_assistant(input_text):
    if "summarize" in input_text.lower():
        return summarize_event(event_context)
    else:
        return answer_question(event_context, input_text)

# Gradio Interface
gr.Interface(fn=event_assistant, inputs="text", outputs="text", title="Event AI Assistant").launch()
