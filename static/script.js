document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const actionConfirmation = document.getElementById('action-confirmation');
    const actionText = document.getElementById('action-text');
    const confirmButton = document.getElementById('confirm-button');
    const cancelButton = document.getElementById('cancel-button');

    // --- Event Listeners ---
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });
    confirmButton.addEventListener('click', handleActionConfirm);
    cancelButton.addEventListener('click', handleActionCancel);

    // --- Functions ---

    function sendMessage() {
        const messageText = userInput.value.trim();
        if (messageText === '') return;

        appendMessage(messageText, 'user');
        userInput.value = '';
        
        // Send message to backend
        sendToBackend(messageText);
    }

    function appendMessage(text, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);
        
        const p = document.createElement('p');
        p.textContent = text;
        messageElement.appendChild(p);
        
        chatMessages.appendChild(messageElement);
        scrollToBottom();
    }

    async function sendToBackend(userMessage) {
        try {
            const response = await fetch('/api/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userMessage }),
            });
            const data = await response.json();
            appendMessage(data.response, 'bot');
            if (data.action) {
                showActionConfirmation(data.action);
            }
        } catch (error) {
            console.error('Error sending message to backend:', error);
            appendMessage('Извините, произошла ошибка при обработке вашего запроса.', 'bot');
        }
    }

    function showActionConfirmation(action) {
        actionText.textContent = action.text;
        actionConfirmation.dataset.actionType = action.type;
        actionConfirmation.style.display = 'block';
    }

    function hideActionConfirmation() {
        actionConfirmation.style.display = 'none';
    }

    function handleActionConfirm() {
        const actionType = actionConfirmation.dataset.actionType;
        // Send action confirmation to backend
        sendActionToBackend(actionType, true);

        hideActionConfirmation();
    }

    function handleActionCancel() {
        sendActionToBackend(actionConfirmation.dataset.actionType, false);
        hideActionConfirmation();
    }

    async function sendActionToBackend(actionType, confirmed) {
        try {
            const response = await fetch('/api/action/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ actionType, confirmed }),
            });
            const data = await response.json();
            appendMessage(data.response, 'bot');
        } catch (error) {
            console.error('Error sending action to backend:', error);
            appendMessage('Извините, произошла ошибка при обработке вашего действия.', 'bot');
        }
    }

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});