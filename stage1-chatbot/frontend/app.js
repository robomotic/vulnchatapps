document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const clearButton = document.getElementById('clear-button');

    function addMessage(content, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user' : 'assistant'}`;
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = content;
        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to send message to backend
    async function sendMessage(message) {
        try {
            const response = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message }),
            });

            if (!response.ok) {
                const data = await response.json().catch(() => ({}));
                // Show error dialog with backend error detail if available
                showErrorDialog(data.detail || 'Sorry, there was an error processing your request. Please try again.');
                return null;
            }

            const data = await response.json();
            return data.response;
        } catch (error) {
            showErrorDialog('Sorry, there was an error connecting to the server. Please try again.');
            return null;
        }
    }

    // Function to show error dialog
    function showErrorDialog(message) {
        // Remove any existing dialog
        const existing = document.getElementById('chatbot-error-dialog');
        if (existing) existing.remove();

        const dialog = document.createElement('div');
        dialog.id = 'chatbot-error-dialog';
        dialog.style.position = 'fixed';
        dialog.style.zIndex = 2000;
        dialog.style.left = '0';
        dialog.style.top = '0';
        dialog.style.width = '100vw';
        dialog.style.height = '100vh';
        dialog.style.background = 'rgba(0,0,0,0.3)';
        dialog.style.display = 'flex';
        dialog.style.alignItems = 'center';
        dialog.style.justifyContent = 'center';

        const box = document.createElement('div');
        box.style.background = '#fff';
        box.style.padding = '32px 24px';
        box.style.borderRadius = '12px';
        box.style.boxShadow = '0 2px 16px rgba(0,0,0,0.18)';
        box.style.maxWidth = '90vw';
        box.style.maxHeight = '60vh';
        box.style.overflowY = 'auto';
        box.style.textAlign = 'center';

        const title = document.createElement('h4');
        title.textContent = 'Chatbot Error';
        title.style.color = '#c00';
        title.style.marginBottom = '16px';
        box.appendChild(title);

        const msg = document.createElement('div');
        msg.textContent = message;
        msg.style.marginBottom = '20px';
        box.appendChild(msg);

        const closeBtn = document.createElement('button');
        closeBtn.textContent = 'Close';
        closeBtn.className = 'btn btn-danger';
        closeBtn.onclick = () => dialog.remove();
        box.appendChild(closeBtn);

        dialog.appendChild(box);
        document.body.appendChild(dialog);
    }

    sendButton.addEventListener('click', async () => {
        const message = userInput.value.trim();
        if (!message) return;

        // Add user message to chat
        addMessage(message, true);
        userInput.value = '';

        // Add loading indicator
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message assistant';
        loadingDiv.innerHTML = '<div class="message-content">Typing...</div>';
        chatMessages.appendChild(loadingDiv);

        // Get response from backend
        const response = await sendMessage(message);

        // Remove loading indicator
        chatMessages.removeChild(loadingDiv);
        if (response) {
            addMessage(response, false);
        }
    });

    clearButton.addEventListener('click', () => {
        chatMessages.innerHTML = '';
        // Optionally, add the assistant's welcome message again
        addMessage("Hello! I'm PharmaCare's virtual assistant. How can I help you today?", false);
    });

    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendButton.click();
        }
    });
});
