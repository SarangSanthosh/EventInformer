// const sendButton = document.querySelector("button");
// const userMessageInput = document.getElementById("user-input");
// const messagesContainer = document.getElementById("messages");

// // Function to display the chat messages
// function displayMessage(message, sender) {
//   const messageElement = document.createElement("div");
//   messageElement.classList.add("message");
//   messageElement.classList.add(sender === "user" ? "user" : "bot");
//   messageElement.textContent = message;
//   messagesContainer.appendChild(messageElement);
//   messagesContainer.scrollTop = messagesContainer.scrollHeight;
// }

// // Function to send the message
// function sendMessage() {
//   const userMessage = userMessageInput.value.trim();
//   if (userMessage) {
//     // Display the user's message
//     displayMessage(userMessage, "user");

//     // Clear the input box
//     userMessageInput.value = "";

//     // Get the CSRF token from the meta tag
//     const csrfToken = document.querySelector('[name="csrf-token"]').content;

//     // Send the request to the backend
//     fetch("/eventchatbot/api/chatbot/", {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//         "X-CSRFToken": csrfToken, // Include the CSRF token here
//       },
//       body: JSON.stringify({
//         message: userMessage,
//       }),
//     })
//       .then((response) => response.json())
//       .then((data) => {
//         // Display the AI's response
//         const aiMessage = data.reply || "Sorry, I couldn't understand that.";
//         displayMessage(aiMessage, "bot");
//       })
//       .catch((error) => {
//         console.error("Error:", error);
//         displayMessage(
//           "Error: Unable to get the response. Please try again later.",
//           "bot"
//         );
//       });
//   }
// }

// // Optional: Allow sending the message by pressing Enter
// function checkEnter(event) {
//   if (event.key === "Enter") {
//     sendMessage();
//   }
// }

// // Add event listener to the send button
// sendButton.addEventListener("click", sendMessage);

const sendButton = document.querySelector("button");
const userMessageInput = document.getElementById("user-input");
const messagesContainer = document.getElementById("messages");

// Function to display the chat messages
function displayMessage(message, sender) {
  const messageElement = document.createElement("div");
  messageElement.classList.add("message");
  messageElement.classList.add(sender === "user" ? "user" : "bot");
  messageElement.textContent = message;
  messagesContainer.appendChild(messageElement);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Function to send the message
function sendMessage() {
  const userMessage = userMessageInput.value.trim();
  if (userMessage) {
    // Display the user's message
    displayMessage(userMessage, "user");

    // Clear the input box
    userMessageInput.value = "";

    // Send the request to the Django backend
    fetch("http://127.0.0.1:8000/eventchatbot", { 
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: userMessage,
      }),
    })
    
    
      .then(response => response.json())
      .then(data => {
        console.log("Bot response:", data);
        displayMessage(data.reply || "Sorry, I couldn't understand that.", "bot");
      })
      .catch(error => {
        console.error("Fetch error:", error);
        displayMessage("Error: Unable to get the response.", "bot");
      });
    
  }
}

// Optional: Allow sending the message by pressing Enter
function checkEnter(event) {
  if (event.key === "Enter") {
    sendMessage();
  }
}

// Add event listener to the send button
sendButton.addEventListener("click", sendMessage);

