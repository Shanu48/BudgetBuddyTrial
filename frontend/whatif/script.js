function sendMessage() {
    const userInput = document.getElementById('userInput').value;
  
    if (userInput.trim() === '') {
      return; 
    }
  
    // Create a new message element for the user
    const userMessage = document.createElement('div');
    userMessage.classList.add('user-message');
    userMessage.textContent = userInput;
  
    // Append the user message to the chat messages container
    const chatMessages = document.querySelector('.chat-messages');
    chatMessages.appendChild(userMessage);
  
    // **Simulate a bot response (replace with actual API call)**
    const botResponse = "You said: " + userInput; 
  
    // Create a new message element for the bot
    const botMessage = document.createElement('div');
    botMessage.classList.add('bot-message');
    botMessage.textContent = botResponse;
  
    // Append the bot message to the chat messages container
    chatMessages.appendChild(botMessage);
  
    // Scroll to the bottom of the chat messages
    chatMessages.scrollTop = chatMessages.scrollHeight;
  
    // Clear the input field
    document.getElementById('userInput').value = '';
  }