import re
from transformers import pipeline
import gradio as gr
# Load a question-answering model
qa_model = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# Load a summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
# Sample event context
event_context = """
TechFest 2024 will take place on March 19th at the Kalamassery.
The event starts at 11:00 AM and features keynotes, ML workshops, and a networking session.
"""

# Function to answer FAQs
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
def event_assistant(input_text):
    if "summarize" in input_text.lower():
        return summarize_event(event_context)
    else:
        return answer_question(event_context, input_text)

# Create Gradio Interface
gr.Interface(fn=event_assistant, inputs="text", outputs="text", title="Event AI Assistant").launch()
