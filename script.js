const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

// Function to send a message to the backend
async function sendMessage(message) {
  try {
    const response = await fetch('http://localhost:5000/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    });
    const data = await response.json();
    displayMessage('bot', data.reply);
  } catch (error) {
    console.error('Error:', error);
    displayMessage('bot', 'Something went wrong. Please try again.');
  }
}

// Function to display messages in the chat box
function displayMessage(sender, message) {
  const messageElement = document.createElement('div');
  messageElement.className = sender === 'user' ? 'user-message' : 'bot-message';
  messageElement.textContent = message;
  chatBox.appendChild(messageElement);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Event listener for the send button
sendBtn.addEventListener('click', () => {
  const message = userInput.value.trim();
  if (message) {
    displayMessage('user', message);
    sendMessage(message);
    userInput.value = '';
  }
});

// Optional: Handle "Enter" key press
userInput.addEventListener('keypress', (event) => {
  if (event.key === 'Enter') {
    sendBtn.click();
  }
});
