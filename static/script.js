document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const attachButton = document.getElementById('attach-button');
    const fileInput = document.getElementById('file-input');
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

    attachButton.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            // Пока просто выводим имя файла, позже будем его отправлять
            appendMessage(`Прикреплен файл: ${file.name}`, 'system');
        }
    });

    confirmButton.addEventListener('click', handleActionConfirm);
    cancelButton.addEventListener('click', handleActionCancel);

    // --- Functions ---

    function sendMessage() {
        const messageText = userInput.value.trim();
        const file = fileInput.files[0];

        if (messageText === '' && !file) return;

        appendMessage(messageText, 'user');
        userInput.value = '';
        
        // Отправляем на бэкенд
        sendToBackend(messageText, file);

        // Сбрасываем инпут файла после отправки
        fileInput.value = '';
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

    async function sendToBackend(userMessage, file = null) {
        try {
            // Отправляем JSON вместо FormData для соответствия с API
            const response = await fetch('/api/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ "message": userMessage }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

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