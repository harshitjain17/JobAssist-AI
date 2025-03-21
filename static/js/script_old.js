/* filepath: demo-app/static/js/script.js */
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // AI Assistant Chat Functionality
    const chatForm = document.getElementById('aiChatForm');
    if (chatForm) {
        chatForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const input = this.querySelector('input');
            const message = input.value.trim();
            
            if (message) {
                // Add user message to chat
                addMessage('user', message);
                
                // Clear input
                input.value = '';
                
                // Simulate AI response (for demo)
                setTimeout(() => {
                    simulateAIResponse(message);
                }, 1000);
            }
        });
    }
    
    // Handle consumer profile tabs
    const profileTabs = document.querySelectorAll('#consumerProfileTabs .nav-link');
    profileTabs.forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            const target = this.getAttribute('href');
            
            // Hide all tab contents
            document.querySelectorAll('.tab-pane').forEach(pane => {
                pane.classList.remove('show', 'active');
            });
            
            // Show selected tab content
            document.querySelector(target).classList.add('show', 'active');
            
            // Update active tab
            profileTabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
        });
    });
});

// Helper function to add message to chat
function addMessage(sender, content) {
    const chatContainer = document.querySelector('.chat-container');
    if (!chatContainer) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${sender}-message mb-3`;
    
    if (sender === 'user') {
        messageDiv.innerHTML = `
            <div class="d-flex justify-content-end">
                <div class="message-content p-3 bg-primary text-white rounded">
                    <p class="mb-0">${content}</p>
                </div>
            </div>
        `;
    } else {
        messageDiv.innerHTML = `
            <div class="d-flex">
                <div class="avatar-circle bg-primary text-white me-2">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-content p-3 bg-white rounded">
                    <p class="mb-0">${content}</p>
                </div>
            </div>
        `;
    }
    
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Simulate AI response (for demo)
function simulateAIResponse(userMessage) {
    let response = "I'm sorry, I don't have enough information to help with that.";
    
    // Simple pattern matching for demo
    userMessage = userMessage.toLowerCase();
    
    if (userMessage.includes('job') && userMessage.includes('match')) {
        response = "Based on James Wilson's profile, I've found 3 potential job matches:<br><br>1. Data Entry Specialist at Acme Corp (85% match)<br>2. Administrative Assistant at TechSolutions (78% match)<br>3. Customer Service Rep at GlobalSupport (72% match)<br><br>Would you like more details on any of these positions?";
    }
    else if (userMessage.includes('appointment') || userMessage.includes('meeting')) {
        response = "You have a Resume Review appointment with James Wilson tomorrow at 10:00 AM. Based on his profile, I suggest focusing on highlighting his data entry skills and customer service experience. Would you like me to prepare some tailored resume suggestions?";
    }
    else if (userMessage.includes('market') || userMessage.includes('trend')) {
        response = "Current job market trends show increased demand for remote data entry positions (+15% YOY). Companies like Acme Corp and DataPro have recently posted positions with accommodations for mobility challenges. This aligns well with James Wilson's skill set and needs.";
    }
    else if (userMessage.includes('hello') || userMessage.includes('hi')) {
        response = "Hello! I'm JobAssist AI. I can help you find job matches for consumers, prepare for appointments, analyze job market trends, and more. How can I assist you today?";
    }
    
    addMessage('ai', response);
}