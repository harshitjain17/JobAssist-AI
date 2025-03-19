// Main JavaScript for JobAssist AI demo application

document.addEventListener('DOMContentLoaded', function() {
    console.log('script.js loaded'); // Debug statement
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    const popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // AI Search functionality (demo)
    const aiSearchForm = document.getElementById('aiSearchForm');
    if (aiSearchForm) {
        aiSearchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const searchField = this.querySelector('input');
            const searchTerm = searchField.value.trim();
            
            if (searchTerm) {
                const resultsContainer = document.getElementById('aiSearchResults');
                resultsContainer.innerHTML = '<div class="text-center py-5"><div class="spinner-border text-primary" role="status"></div><p class="mt-3">Searching for jobs matching criteria...</p></div>';
                
                // Simulate API call
                setTimeout(function() {
                    // Demo results
                    resultsContainer.innerHTML = `
                        <h5 class="mb-4">Jobs matching "${searchTerm}"</h5>
                        <div class="card mb-3">
                            <div class="card-body">
                                <div class="d-flex justify-content-between align-items-start">
                                    <div>
                                        <h5 class="card-title">Data Entry Specialist</h5>
                                        <h6 class="card-subtitle text-muted mb-2">Acme Corp • Remote</h6>
                                        <p class="card-text">Looking for a detail-oriented data entry specialist to work remotely. Flexible hours, accessible work environment.</p>
                                        <div class="mb-2">
                                            <span class="badge bg-success me-1">97% Match</span>
                                            <span class="badge bg-secondary me-1">Part-time</span>
                                            <span class="badge bg-info">Remote</span>
                                        </div>
                                    </div>
                                    <button class="btn btn-outline-primary">Apply</button>
                                </div>
                            </div>
                        </div>
                        <div class="card mb-3">
                            <div class="card-body">
                                <div class="d-flex justify-content-between align-items-start">
                                    <div>
                                        <h5 class="card-title">Administrative Assistant</h5>
                                        <h6 class="card-subtitle text-muted mb-2">Tech Solutions Inc • Portland, OR</h6>
                                        <p class="card-text">Administrative role supporting office operations. Candidate will manage emails, scheduling, and basic office tasks.</p>
                                        <div class="mb-2">
                                            <span class="badge bg-warning me-1">82% Match</span>
                                            <span class="badge bg-secondary me-1">Full-time</span>
                                            <span class="badge bg-secondary">Hybrid</span>
                                        </div>
                                    </div>
                                    <button class="btn btn-outline-primary">Apply</button>
                                </div>
                            </div>
                        </div>
                        <div class="card">
                            <div class="card-body">
                                <div class="d-flex justify-content-between align-items-start">
                                    <div>
                                        <h5 class="card-title">Customer Service Representative</h5>
                                        <h6 class="card-subtitle text-muted mb-2">Support Services LLC • Remote</h6>
                                        <p class="card-text">Provide customer support via phone and email. Training provided, focus on problem-solving skills.</p>
                                        <div class="mb-2">
                                            <span class="badge bg-warning me-1">75% Match</span>
                                            <span class="badge bg-secondary me-1">Full-time</span>
                                            <span class="badge bg-info">Remote</span>
                                        </div>
                                    </div>
                                    <button class="btn btn-outline-primary">Apply</button>
                                </div>
                            </div>
                        </div>
                    `;
                }, 1500);
            }
        });
    }
    
    // Add Case Note functionality (demo)
    const addNoteBtn = document.querySelector('.modal-footer .btn-primary');
    if (addNoteBtn) {
        addNoteBtn.addEventListener('click', function() {
            const noteCategory = document.getElementById('noteCategory').value;
            const noteContent = document.getElementById('noteContent').value;
            
            if (noteContent.trim()) {
                // In a real app, this would save to the database
                // For demo purposes, just close the modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('addNoteModal'));
                modal.hide();
                
                // Show success notification
                const toastContainer = document.createElement('div');
                toastContainer.className = 'position-fixed bottom-0 end-0 p-3';
                toastContainer.style.zIndex = '11';
                toastContainer.innerHTML = `
                    <div class="toast align-items-center text-white bg-success border-0" role="alert" aria-live="assertive" aria-atomic="true">
                        <div class="d-flex">
                            <div class="toast-body">
                                <i class="fas fa-check-circle me-2"></i> Case note added successfully!
                            </div>
                            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                        </div>
                    </div>
                `;
                
                document.body.appendChild(toastContainer);
                const toastEl = toastContainer.querySelector('.toast');
                const toast = new bootstrap.Toast(toastEl, { autohide: true, delay: 3000 });
                toast.show();
                
                setTimeout(() => {
                    document.body.removeChild(toastContainer);
                }, 3500);
            }
        });
    }
    
    // Task Breakdown Generator
    const generateTaskBtn = document.getElementById('generateTaskBreakdown');
    const taskResultDiv = document.getElementById('taskBreakdownResult');
    const taskStepsList = document.getElementById('taskSteps');
    const taskAccommodationsList = document.getElementById('taskAccommodations');
    const saveTaskBtn = document.getElementById('saveTaskBreakdown');
    
    if (generateTaskBtn) {
        generateTaskBtn.addEventListener('click', async function() {
            const taskName = document.getElementById('taskName').value;
            const taskDetails = document.getElementById('taskDetails').value;
            const needsVisual = document.getElementById('needsVisual').checked;
            const needsSimplified = document.getElementById('needsSimplified').checked;

            if (!taskName || !taskDetails) {
                alert('Please enter a task name and details.');
                return;
            }

            // Show loading indicator
            taskStepsList.innerHTML = '<div class="text-center py-3"><div class="spinner-border text-primary" role="status"></div><p class="mt-2">Generating task breakdown...</p></div>';
            taskAccommodationsList.innerHTML = '';
            taskResultDiv.classList.remove('d-none');
            generateTaskBtn.disabled = true;

            try {
                const response = await fetch('/ai/task-breakdown', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        task_name: taskName,
                        task_details: taskDetails,
                        accommodations: {
                            needsVisual: needsVisual,
                            needsSimplified: needsSimplified
                        },
                        consumer_id: window.consumerId || 'c001' // Fallback to 'c001' if not set
                    })
                });

                const result = await response.json();

                if (response.ok) {
                    // Populate the steps list
                    taskStepsList.innerHTML = '';
                    result.steps.forEach(step => {
                        const li = document.createElement('li');
                        li.className = 'mb-2';
                        li.textContent = step;
                        taskStepsList.appendChild(li);
                    });

                    // Populate the accommodations list
                    taskAccommodationsList.innerHTML = '';
                    result.accommodations.forEach(accommodation => {
                        const li = document.createElement('li');
                        li.className = 'mb-2';
                        li.textContent = accommodation;
                        taskAccommodationsList.appendChild(li);
                    });

                    // Show the save button
                    saveTaskBtn.classList.remove('d-none');
                } else {
                    taskStepsList.innerHTML = `<p class="text-danger">Error: ${result.error}</p>`;
                    taskAccommodationsList.innerHTML = '';
                }
            } catch (error) {
                console.error('Task breakdown error:', error);
                taskStepsList.innerHTML = '<p class="text-danger">An error occurred while generating the breakdown.</p>';
                taskAccommodationsList.innerHTML = '';
            } finally {
                generateTaskBtn.disabled = false;
            }
        });

        saveTaskBtn.addEventListener('click', async function() {
            try {
                const response = await fetch('/upload_note', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        category: 'Task Breakdown',
                        content: `Task: ${document.getElementById('taskName').value}\nSteps:\n${Array.from(taskStepsList.children).map(li => li.textContent).join('\n')}\nAccommodations:\n${Array.from(taskAccommodationsList.children).map(li => li.textContent).join('\n')}`,
                        consumer_id: window.consumerId || 'c001'
                    })
                });

                if (response.ok) {
                    const modal = bootstrap.Modal.getInstance(document.getElementById('taskBreakdownModal'));
                    modal.hide();
                    alert('Task breakdown saved to consumer profile.');
                } else {
                    alert('Error saving task breakdown.');
                }
            } catch (error) {
                console.error('Save error:', error);
                alert('An error occurred while saving.');
            }
        });
    }
    
    // Add functionality to the AI chat form
    const aiChatForm = document.getElementById('aiChatForm');
    if (aiChatForm) {
        aiChatForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const input = this.querySelector('input');
            const message = input.value.trim();
            
            if (message) {
                // Add user message to chat
                addMessage('user', message);
                
                // Clear input
                input.value = '';
                
                // Show typing indicator
                const chatContainer = document.querySelector('.chat-container');
                const typingDiv = document.createElement('div');
                typingDiv.className = 'chat-message ai-message mb-3 typing-indicator';
                typingDiv.innerHTML = `
                    <div class="d-flex">
                        <div class="avatar-circle bg-primary text-white me-2">
                            <i class="fas fa-robot"></i>
                        </div>
                        <div class="message-content p-3 bg-white rounded">
                            <div class="typing-dots">
                                <span></span>
                                <span></span>
                                <span></span>
                            </div>
                        </div>
                    </div>
                `;
                chatContainer.appendChild(typingDiv);
                chatContainer.scrollTop = chatContainer.scrollHeight;
                
                // Simulate AI response (for demo)
                setTimeout(() => {
                    // Remove typing indicator
                    chatContainer.removeChild(typingDiv);
                    
                    // Add AI response
                    simulateAIResponse(message);
                }, 1500);
            }
        });
    }
    
    // Add functionality to job search in consumer profile
    const jobSearchForm = document.querySelector('#jobSearchModal form');
    if (jobSearchForm) {
        jobSearchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const input = this.querySelector('input');
            const searchTerm = input.value.trim();
            
            if (searchTerm) {
                // Show loading state
                const resultsContainer = document.querySelector('#jobSearchModal .list-group');
                resultsContainer.innerHTML = '<div class="text-center py-4"><div class="spinner-border text-primary" role="status"></div><p class="mt-2">Searching for matching jobs...</p></div>';
                
                // Simulate API call delay
                setTimeout(function() {
                    // In a real implementation, this would be fetch('/ai/job-match', {...})
                    
                    // Restore job listings (these are already in the HTML)
                    resultsContainer.innerHTML = `
                        <a href="#" class="list-group-item list-group-item-action">
                            <div class="d-flex w-100 justify-content-between align-items-center">
                                <h6 class="mb-1">Administrative Assistant</h6>
                                <span class="badge bg-success">90% Match</span>
                            </div>
                            <p class="mb-1">FastTrack Solutions • Portland, OR (Hybrid)</p>
                            <small class="text-muted">Entry-level position with accommodations available. Posted 2 days ago.</small>
                        </a>
                        <a href="#" class="list-group-item list-group-item-action">
                            <div class="d-flex w-100 justify-content-between align-items-center">
                                <h6 class="mb-1">Virtual Customer Support Agent</h6>
                                <span class="badge bg-success">88% Match</span>
                            </div>
                            <p class="mb-1">Global Connect • Remote (Full-time)</p>
                            <small class="text-muted">Work-from-home position with flexible scheduling. Posted 5 days ago.</small>
                        </a>
                        <a href="#" class="list-group-item list-group-item-action">
                            <div class="d-flex w-100 justify-content-between align-items-center">
                                <h6 class="mb-1">Data Entry Clerk</h6>
                                <span class="badge bg-success">85% Match</span>
                            </div>
                            <p class="mb-1">CityCare Health • Portland, OR (Remote)</p>
                            <small class="text-muted">Healthcare data entry with accommodation support. Posted 1 week ago.</small>
                        </a>
                    `;
                }, 1500);
            }
        });
    }
    
    // Don't reinitialize the chat functionality if it's implemented inline
    // in dashboard.html. Let's make sure we're not causing a conflict.
    const aiChatFormInScript = document.getElementById('aiChatForm');
    if (aiChatFormInScript && !window.chatInitialized) {
        console.log('Initializing chat from script.js - this could cause conflicts');
        // Implementation would go here but we'll skip it to avoid conflicts
    }
});