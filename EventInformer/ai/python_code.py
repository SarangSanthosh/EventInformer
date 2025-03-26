import re
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ConversationHandler
from supabase import create_client, Client

SUPABASE_URL = "https://sbymlndggpisjpevxtfd.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNieW1sbmRnZ3Bpc2pwZXZ4dGZkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDE4NzQ5NjIsImV4cCI6MjA1NzQ1MDk2Mn0.N2dpMIqw8zrT1VkRWuEgxltI7_tkXIIn7pPkm-xLLEQ"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

ASK_CONFIRMATION = 1

def extract_event_details(text):
    event_details = {}

    lines = text.split("\n")
    for line in lines:
        cleaned_line = re.sub(r'^"\s*|\s*"$', '', line).strip()  
        if cleaned_line:
            event_details['event_name'] = cleaned_line
            break
    else:
        event_details['event_name'] = "Not specified"

    date_match = re.search(r"[📅🗓]\s*([^\n📍]+)", text)
    if date_match:
        event_details['event_date'] = date_match.group(1).strip()
    else:
        alt_date_match = re.search(r"\b(\w{3,9}\s+\d{1,2},?\s+\d{4})\b", text, re.IGNORECASE)
        if not alt_date_match:
            alt_date_match = re.search(r"\b(?:Date|Dates):\s*(\d{1,2}\s*\w{3,9})\b", text, re.IGNORECASE)
        event_details['event_date'] = alt_date_match.group(1).strip() if alt_date_match else "Not specified"

    time_match = re.search(r"\b(\d{1,2}:\d{2}|\d{1,2})\s?[APap][Mm]\b", text)
    event_details['event_time'] = time_match.group(0) if time_match else "Not specified"

    venue_match = re.search(r"📍\s*([^📅\n]+)", text)
    if venue_match:
        event_details['venue'] = venue_match.group(1).strip()
    else:
        venue_keywords = r"\b(?:auditorium|hall|center|centre|arena|stadium|complex|conference room)\b"
        venue_match_alt = re.search(venue_keywords, text, re.IGNORECASE)
        event_details['venue'] = venue_match_alt.group(0).strip() if venue_match_alt else "Not specified"

    registration_link_match = re.search(r"(https?://[^\s]+)", text)
    event_details['registration_link'] = registration_link_match.group(1) if registration_link_match else "Not specified"

    contact_numbers = re.findall(r"\b\d{10}\b", text)
    event_details['contact'] = ", ".join(contact_numbers) if contact_numbers else "Not specified"

    return event_details

async def send_event_details(update: Update, context):
    if update.message.text:
        user_message = update.message.text
        event_data = extract_event_details(user_message)

        formatted_message = (
            f"✅ Event Details Extracted:\n"
            f"📌 Event Name: {event_data['event_name']}\n"
            f"📅 Date: {event_data['event_date']}\n"
            f"⏰ Time: {event_data['event_time']}\n"
            f"📍 Venue: {event_data['venue']}\n"
            f"🔗 Registration: {event_data['registration_link']}\n"
            f"📞 Contact: {event_data['contact']}"
        )

        context.user_data["event_data"] = event_data

        await update.message.reply_text(formatted_message)
        await update.message.reply_text("Do you want to save this event in the database? (yes/no)")

        return ASK_CONFIRMATION  

async def store_event_in_supabase(event_data):
    data_to_insert = {
        "event_name": event_data['event_name'],
        "event_date": event_data['event_date'],
        "event_time": event_data['event_time'],
        "venue": event_data['venue'],
        "registration_link": event_data['registration_link'],
        "contact": event_data['contact'],
    }

    response = supabase.table("events").insert(data_to_insert).execute()

    if response.data:
        return "✅ Event saved successfully!"
    else:
        return f"❌ Failed to save event: {response.error}"

async def handle_confirmation(update: Update, context):
    user_response = update.message.text.strip().lower()

    if user_response == "yes":
        event_data = context.user_data.get("event_data", {})
        if event_data:
            message = await store_event_in_supabase(event_data)
            await update.message.reply_text(message)
        else:
            await update.message.reply_text("❌ No event data found.")
    else:
        await update.message.reply_text("❌ Event was not saved.")

    return ConversationHandler.END  

async def handle_message(update: Update, context):
    return await send_event_details(update, context)

def main():
    bot_token = "7744285499:AAGeYi80mX1d2y-xGQQ-fJ0a-sYHfyIjYP8"  #
    application = Application.builder().token(bot_token).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)],
        states={ASK_CONFIRMATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_confirmation)]},
        fallbacks=[],
    )

    application.add_handler(conv_handler)

    application.run_polling()

if __name__ == '__main__':
    main()
