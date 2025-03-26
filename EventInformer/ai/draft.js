//this version aim to return full details of particular event IF ASKED.also give particular event detail
const express = require("express");
const bodyParser = require("body-parser");
const ngrok = require("ngrok");
const { WebhookClient } = require("dialogflow-fulfillment");

const app = express();
const PORT = 5000; // Local port to run the server

app.use(bodyParser.json());

const { createClient } = require("@supabase/supabase-js");

const supabase = createClient(
  "https://sbymlndggpisjpevxtfd.supabase.co",
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNieW1sbmRnZ3Bpc2pwZXZ4dGZkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDE4NzQ5NjIsImV4cCI6MjA1NzQ1MDk2Mn0.N2dpMIqw8zrT1VkRWuEgxltI7_tkXIIn7pPkm-xLLEQ"
);

async function fetchEventData(query, column) {
  const { data, error } = await supabase
    .from("events")
    .select("*")
    .ilike(column, `%${query}%`);

  if (error) throw new Error(error.message);
  return data;
}

// Function to fetch upcoming events
async function fetchUpcomingEvents() {
  const today = new Date().toISOString();
  const { data, error } = await supabase
    .from("events")
    .select("*")
    .gte("event_time", today);

  if (error) throw new Error(error.message);
  return data;
}

// Intent Handler
async function handleEventQuery(agent) {
  let userquery = agent.parameters.name
    ? agent.parameters.name.toLowerCase().trim()
    : "";
  let detailType = agent.parameters.event_detail
    ? agent.parameters.event_detail.toLowerCase().trim()
    : "";

  console.log("User Query:", userquery);
  console.log("Detail Type Detected:", detailType || "None Detected");

  const validDetails = [
    "venue",
    "event_date",
    "event_time",
    "registration_link",
  ];

  try {
    // 📌 Handle "Upcoming Events" Query
    if (userquery.includes("upcoming")) {
      const events = await fetchUpcomingEvents();
      if (events.length === 0) {
        agent.add("No upcoming events found.");
      } else {
        let responseMessage = "📅 **Upcoming Events:**\n\n";
        events.forEach((event) => {
          responseMessage += `🆕 **${event.event_name}**\n`;
        });

        agent.add(responseMessage);
      }
      return;
    }

    // 📌 If no event name is provided
    if (!userquery) {
      agent.add("Please provide an event name.");
      return;
    }

    // 📌 Fetch event details for the specific event
    const events = await fetchEventData(userquery, "event_name");

    if (events.length === 0) {
      agent.add(`❌ No matching events found for **${userquery}**.`);
      return;
    }

    const event = events[0]; // Assume first match

    // 📌 Handle "Specific Event Detail" Query (e.g., venue, time, registration)
    if (detailType) {
      if (!validDetails.includes(detailType)) {
        agent.add(`⚠️ I can only provide: ${validDetails.join(", ")}.`);
        return;
      }

      const detailValue = event[detailType];

      if (!detailValue) {
        agent.add(
          `🚫 No ${detailType} information available for **${event.event_name}**.`
        );
      } else {
        agent.add(`ℹ️ **${event.event_name}** → ${detailType}: ${detailValue}`);
      }

      return; // ✅ Ensure function exits after responding with the requested detail
    }

    // 📌 If the user simply asks about an event, return full details
    let responseMessage = `📌 **Details for ${event.event_name}:**\n\n`;
    responseMessage += `   📍 *Venue:* ${event.venue || "TBA"}\n`;
    responseMessage += `   🕒 *Time:* ${event.event_time || "TBA"}\n`;
    responseMessage += `   📅 *Date:* ${event.event_date || "TBA"}\n`;
    responseMessage += `   🔗 *Register:* [Click Here](${
      event.registration_link || "#"
    })\n`;

    agent.add(responseMessage);
  } catch (error) {
    agent.add("⚠️ An error occurred while processing your request.");
    console.error(error);
  }
}

// Webhook endpoint for Dialogflow
app.post("/", (req, res) => {
  const agent = new WebhookClient({ request: req, response: res });

  let intentMap = new Map();
  intentMap.set("FetchEventdetails", handleEventQuery);

  agent.handleRequest(intentMap);
});

// Start Express Server
app.listen(PORT, async () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);

  // Expose the local server to the internet using Ngrok
  const url = await ngrok.connect(PORT);
  console.log(`🌍 Ngrok tunnel created: ${url}`);
  console.log(`⚡ Set this URL in Dialogflow Fulfillment: ${url}/`);
});
