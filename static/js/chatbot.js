// Chatbot functionality
document.addEventListener('DOMContentLoaded', function() {
    const chatbotToggle = document.getElementById('chatbotToggle');
    const chatbotWindow = document.getElementById('chatbotWindow');
    const chatbotClose = document.getElementById('chatbotClose');
    const chatbotMessages = document.getElementById('chatbotMessages');
    const chatbotInput = document.getElementById('chatbotInput');
    const chatbotSend = document.getElementById('chatbotSend');

    if (!chatbotToggle) return; // Exit if chatbot elements don't exist

    // Toggle chatbot window
    chatbotToggle.addEventListener('click', function() {
        if (chatbotWindow.style.display === 'none' || !chatbotWindow.style.display) {
            chatbotWindow.style.display = 'block';
            addMessage('bot', 'Hello! I\'m here to help you with any questions about AI-Solution. What would you like to know?');
        } else {
            chatbotWindow.style.display = 'none';
        }
    });

    // Close chatbot window
    if (chatbotClose) {
        chatbotClose.addEventListener('click', function() {
            chatbotWindow.style.display = 'none';
        });
    }

    // Send message
    function sendMessage() {
        const message = chatbotInput.value.trim();
        if (!message) return;

        addMessage('user', message);
        chatbotInput.value = '';

        // Show typing indicator
        addTypingIndicator();

        // Send to backend
        fetch('/api/chatbot/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            removeTypingIndicator();
            if (data.success) {
                addMessage('bot', data.response);
            } else {
                addMessage('bot', 'Sorry, I encountered an error. Please try again or contact our support team.');
            }
        })
        .catch(error => {
            removeTypingIndicator();
            addMessage('bot', 'Sorry, I\'m having trouble connecting. Please try again later.');
        });
    }

    // Send button click
    if (chatbotSend) {
        chatbotSend.addEventListener('click', sendMessage);
    }

    // Enter key to send
    if (chatbotInput) {
        chatbotInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }

    // Add message to chat
    function addMessage(sender, message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `mb-3 ${sender === 'user' ? 'text-end' : ''}`;
        
        const messageContent = document.createElement('div');
        messageContent.className = `d-inline-block p-2 rounded ${
            sender === 'user' 
                ? 'bg-primary text-white' 
                : 'bg-light text-dark'
        }`;
        messageContent.style.maxWidth = '80%';
        messageContent.textContent = message;
        
        messageDiv.appendChild(messageContent);
        chatbotMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    // Add typing indicator
    function addTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.id = 'typing-indicator';
        typingDiv.className = 'mb-3';
        typingDiv.innerHTML = `
            <div class="d-inline-block p-2 rounded bg-light text-muted">
                <span class="typing-dots">
                    <span>.</span><span>.</span><span>.</span>
                </span>
                Typing...
            </div>
        `;
        chatbotMessages.appendChild(typingDiv);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    // Remove typing indicator
    function removeTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    // Get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});