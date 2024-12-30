from transformers import pipeline

# Load the question-answering model from Hugging Face
qa_model = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# Load the summarization model for event details
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Sample event context (you should replace this with dynamic event data from your database)
event_context = """
TechFest 2024 will take place on March 19th at the Kalamassery.
The event starts at 11:00 AM and features keynotes, ML workshops, and a networking session.
Registration link: https://example.com/register
"""

# Function to answer questions based on the event context
def answer_question(context, question):
    result = qa_model({"context": context, "question": question})
    return result["answer"]

# Function to summarize the event details
def summarize_event(details):
    summary = summarizer(details, max_length=50, min_length=25, do_sample=False)
    return summary[0]["summary_text"]

# Main function to handle user input
def event_assistant(input_text):
    # Check if the user asked to summarize the event details
    if "summarize" in input_text.lower():
        return summarize_event(event_context)
    else:
        # Otherwise, assume the user is asking a question about the event
        return answer_question(event_context, input_text)
