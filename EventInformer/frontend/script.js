function sendMessage() {
  const userMessage = document.getElementById("user-input").value;
  if (userMessage.trim()) {
    displayMessage(userMessage, "user");
    document.getElementById("user-input").value = "";

    getBotResponse(userMessage);
  }
}

function displayMessage(message, sender) {
  const messageContainer = document.getElementById("messages");
  const messageElement = document.createElement("div");
  messageElement.classList.add("message", sender);
  messageElement.innerText = message;
  messageContainer.appendChild(messageElement);
  messageContainer.scrollTop = messageContainer.scrollHeight;
}

async function getBotResponse(message) {
  const response = await fetch("http://localhost:8000/api/chatbot/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message: message }),
  });
  const data = await response.json();
  displayMessage(data.reply, "bot");
}

function checkEnter(event) {
  if (event.key === "Enter") {
    sendMessage();
  }
}
