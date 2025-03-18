// Chat functionality for JobAssist AI

document.addEventListener('DOMContentLoaded', function() {
    console.log('Chat script initialized from external file'); // Debug statement
    
    // Only initialize if we're on a page with the chat UI
    const chatForm = document.getElementById('aiChatForm');
    const userInput = document.getElementById('userInput');
    const chatContainer = document.getElementById('chatContainer');
    
    if (!chatForm || !userInput || !chatContainer) {
        console.log('Chat UI not found on this page, skipping initialization');
        return;
    }
    
    console.log('Chat UI found, initializing');
    
    // Handle form submission
    chatForm.addEventListener('submit', async function(e) {
        console.log('Form submitted'); // Debug statement
        e.preventDefault();
        
        const userContent = userInput.value.trim();
        if (!userContent) {
            console.log('Empty input, ignoring submission');
            return;
        }
        
        console.log('Processing message:', userContent);
        
        // Add user message to chat
        appendUserMessage(userContent);
        
        // Clear input
        userInput.value = '';
        
        // Add a loading message for the AI response
        const aiMessageId = `ai-${Date.now()}`;
        appendAIMessage('Thinking...', aiMessageId, true);
        
        try {
            console.log('Sending request to backend');
            // Send request to the backend
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ user_content: userContent }),
            });
            
            console.log('Response received', response.status);
            
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('Data received', data);
            
            // Update the AI message with the actual response
            updateAIMessage(aiMessageId, data.response);
            
        } catch (error) {
            console.error('Error:', error);
            updateAIMessage(aiMessageId, 'Sorry, there was an error processing your request.');
        }
    });
    
    // Handle suggestion clicks
    document.querySelectorAll('.suggestion').forEach(link => {
        link.addEventListener('click', function(e) {
            console.log('Suggestion clicked:', this.textContent);
            e.preventDefault();
            userInput.value = this.textContent;
            // Use a proper click or submit event instead of a synthetic event
            chatForm.querySelector('button[type="submit"]').click();
        });
    });
    
    // Function to append a user message to the chat
    function appendUserMessage(content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'chat-message user-message mb-3';
        messageDiv.innerHTML = `
            <div class="d-flex justify-content-end">
                <div class="message-content p-3 bg-primary text-white rounded">
                    <p class="mb-0">${content}</p>
                </div>
                <div class="avatar-circle bg-secondary text-white ms-2">
                    <i class="fas fa-user"></i>
                </div>
            </div>
        `;
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    
    // Function to append an AI message to the chat
    function appendAIMessage(content, messageId, isLoading = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'chat-message ai-message mb-3';
        messageDiv.id = messageId;
        
        let messageContent = content;
        if (isLoading) {
            messageContent = `<div class="d-flex align-items-center">
                <div class="spinner-border spinner-border-sm text-primary me-2" role="status"></div>
                <span>${content}</span>
            </div>`;
        }
        
        messageDiv.innerHTML = `
            <div class="d-flex">
                <div class="avatar-circle bg-primary text-white me-2">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content p-3 bg-white rounded">
                    ${messageContent}
                </div>
            </div>
        `;
        
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    
    // Function to update an existing AI message
    function updateAIMessage(messageId, content) {
        const messageDiv = document.getElementById(messageId);
        if (messageDiv) {
            const contentContainer = messageDiv.querySelector('.message-content');
            if (contentContainer) {
                contentContainer.innerHTML = `<p class="mb-0">${content}</p>`;
                
                // If the response contains links, make them open in a new tab
                contentContainer.querySelectorAll('a').forEach(link => {
                    if (!link.getAttribute('target')) {
                        link.setAttribute('target', '_blank');
                        link.setAttribute('rel', 'noopener noreferrer');
                    }
                });
                
                chatContainer.scrollTop = chatContainer.scrollHeight;
            } else {
                console.error('Message content container not found');
            }
        } else {
            console.error(`AI message with ID ${messageId} not found`);
        }
    }
    
    // Initialize modal events to ensure the chat input gets focus
    const aiAssistantModal = document.getElementById('aiAssistantModal');
    if (aiAssistantModal) {
        aiAssistantModal.addEventListener('shown.bs.modal', function() {
            console.log('Modal shown, focusing input');
            userInput.focus();
        });
    }
});
