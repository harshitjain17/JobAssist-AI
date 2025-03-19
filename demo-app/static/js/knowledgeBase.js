// Knowledge Base functionality for JobAssist AI

document.addEventListener('DOMContentLoaded', function() {
    console.log('Knowledge Base script initialized from external file'); // Debug statement
    
    // Only initialize if we're on a page with the Knowledge Base UI
    const knowledgeBaseForm = document.getElementById('knowledgeBaseForm');
    const searchQuery = document.getElementById('searchQuery');
    const knowledgeBaseContainer = document.getElementById('knowledgeBaseContainer');
    
    if (!knowledgeBaseForm || !searchQuery || !knowledgeBaseContainer) {
        console.log('Knowledge Base UI not found on this page, skipping initialization');
        return;
    }
    
    console.log('Knowledge Base UI found, initializing');
    
    // Handle form submission
    knowledgeBaseForm.addEventListener('submit', async function(e) {
        console.log('Knowledge Base Form submitted'); // Debug statement
        e.preventDefault();
        
        const searchQueryContent = searchQuery.value.trim();
        if (!searchQueryContent) {
            console.log('Empty search query, ignoring submission');
            return;
        }
        
        console.log('Processing search query:', searchQueryContent);
        
        // Add search query to chat
        appendSearchQuery(searchQueryContent);
        
        // Clear input
        searchQuery.value = '';
        
        // Add a loading message for the AI response
        const searchQueryId = `ai-${Date.now()}`;
        appendSearchResult('Thinking...', searchQueryId, true);
        
        try {
            console.log('Sending request to backend');
            // Send request to the backend
            const response = await fetch('/api/search-knowledge-base', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ search_query: searchQueryContent }),
            });
            
            console.log('Response received', response.status);
            
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.status}`);
            }
            
            const search_results = await response.json();
            console.log('search results received', search_results);
            
            // Update the Search Result with the actual response
            updateSearchResult(searchQueryId, search_results.response);
            
        } catch (error) {
            console.error('Error:', error);
            updateSearchResult(searchQueryId, 'No relevant data found.');
        }
    });
    
    // Handle suggestion clicks
    document.querySelectorAll('.suggestion').forEach(link => {
        link.addEventListener('click', function(e) {
            console.log('Suggestion clicked:', this.textContent);
            e.preventDefault();
            searchQuery.value = this.textContent;
            // Use a proper click or submit event instead of a synthetic event
            knowledgeBaseForm.querySelector('button[type="submit"]').click();
        });
    });
    
    // Function to append a user message to the chat
    function appendSearchQuery(content) {
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
        knowledgeBaseContainer.appendChild(messageDiv);
        knowledgeBaseContainer.scrollTop = knowledgeBaseContainer.scrollHeight;
    }
    
    // Function to append an AI message to the chat
    function appendSearchResult(content, searchQueryId, isLoading = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'chat-message ai-message mb-3';
        messageDiv.id = searchQueryId;
        
        let searchResultContent = content;
        if (isLoading) {
            searchResultContent = `<div class="d-flex align-items-center">
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
                    ${searchResultContent}
                </div>
            </div>
        `;
        
        knowledgeBaseContainer.appendChild(messageDiv);
        knowledgeBaseContainer.scrollTop = knowledgeBaseContainer.scrollHeight;
    }
    
    // Function to update an existing AI message
    function updateSearchResult(searchQueryId, content) {
        const messageDiv = document.getElementById(searchQueryId);
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
                
                knowledgeBaseContainer.scrollTop = knowledgeBaseContainer.scrollHeight;
            } else {
                console.error('Knowledge Base container not found');
            }
        } else {
            console.error(`Search Result with ID ${searchQueryId} not found`);
        }
    }
    
    // Initialize modal events to ensure the knowledge base input gets focus
    const knowledgeBaseModal = document.getElementById('knowledgeBaseModal');
    if (knowledgeBaseModal) {
        knowledgeBaseModal.addEventListener('shown.bs.modal', function() {
            console.log('Modal shown, focusing input');
            searchQuery.focus();
        });
    }

    document.getElementById("toggleAddInsight").addEventListener("click", function() {
        document.getElementById("addInsightFormContainer").classList.toggle("d-none");
    });
    
    document.getElementById("cancelAddInsight").addEventListener("click", function() {
        document.getElementById("addInsightFormContainer").classList.add("d-none");
        document.getElementById("addInsightSuccessMessage").classList.add("d-none");
        document.getElementById("addInsightErrorMessage").classList.add("d-none");

        // Clear the form fields
        document.getElementById("category").value = '';  // Clear category input
        document.getElementById("details").value = '';   // Clear details input
    });
    
    document.getElementById("addInsightForm").addEventListener("submit", async function(event) {
        event.preventDefault();
        
        // Get form values
        const category = document.getElementById("category").value;
        const details = document.getElementById("details").value;
    
        // Simulate saving to DB (Replace with actual API call)
        console.log("Saving Insight:", { category, details });
        try {
            console.log('Sending request to backend');
            // Send request to the backend
            const response = await fetch('/api/save-knowledge-base', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ category: category, details: details }),
            });
            
            console.log('Response received', response.status);
            
            if (!response.ok) {
                document.getElementById("addInsightErrorMessage").classList.remove("d-none");
            } else {
                // Show success message
                document.getElementById("addInsightSuccessMessage").classList.remove("d-none");

                // Clear input fields but keep form open
                document.getElementById("category").value = "";
                document.getElementById("details").value = "";
            }
        } catch (error) {
            document.getElementById("addInsightErrorMessage").classList.remove("d-none");
        }
    
    });
});
