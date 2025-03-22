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
    const loadingSpinner = document.getElementById("loadingSpinner");
    const taskStepsList = document.getElementById('taskSteps');
    const taskNoteToJobCoachList = document.getElementById('taskNoteToJobCoach');
    const taskAdditionalResourcesList = document.getElementById('taskAdditionalResources');
    const generateAudioButton = document.getElementById('generateAudioButton');
    const audioLoadingSpinner = document.getElementById('audioLoadingSpinner');
    const saveTaskBtn = document.getElementById('saveTaskBreakdown');
    
    if (generateTaskBtn) {
        generateTaskBtn.addEventListener('click', async function() {
            // Show loading spinner and hide the result container
            loadingSpinner.classList.remove('d-none');  // Show the spinner
            taskResultDiv.classList.add('d-none');

            // Clear the previous audio and hide the audio player
            const audioPlayer = document.getElementById('audioPlayer');
            audioPlayer.src = '';  
            audioPlayer.classList.add('d-none');  

            // Hide the audio loading spinner
            audioLoadingSpinner.classList.add('d-none');

            const taskName = document.getElementById('taskName').value;
            const taskDetails = document.getElementById('taskDetails').value;
            // const needsVisual = document.getElementById('needsVisual').checked;
            // const needsSimplified = document.getElementById('needsSimplified').checked;

            if (!taskName || !taskDetails) {
                alert('Please enter a task name and details.');
                return;
            }

            try {
                const response = await fetch('/api/task-breakdown', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        task_name: taskName,
                        task_details: taskDetails,
                        // accommodations: {
                        //     needsVisual: needsVisual,
                        //     needsSimplified: needsSimplified
                        // },
                        consumer_id: window.consumerId || 'c001' // Fallback to 'c001' if not set
                    })
                });

                const result = await response.json();

                if (response.ok) {
                    // Populate the steps list
                    taskStepsList.innerHTML = '';
                    const stepsArray = result.steps_for_employee.split(' | ');
                    stepsArray.forEach(step => {
                        const li = document.createElement('li');
                        li.className = 'mb-2';
                        li.textContent = step.replace(/^\d+\.\s*/, ""); ;
                        taskStepsList.appendChild(li);
                    });

                    // Populate the note to job coach list
                    taskNoteToJobCoachList.innerHTML = '';
                    const notesArray = result.note_to_job_coach.split(' | ');
                    notesArray.forEach(note => {
                        const li = document.createElement('li');
                        li.className = 'mb-2';
                        li.textContent = note;
                        taskNoteToJobCoachList.appendChild(li);
                    });

                    // Populate the additional resources list
                    taskAdditionalResourcesList.innerHTML = '';
                    const resourcesArray = result.additional_training_resources.split(' | '); 
                    resourcesArray.forEach(resource => {
                        const [resourceName, resourceLink] = resource.split(': '); 

                        const li = document.createElement('li');
                        li.className = 'mb-2';

                        const a = document.createElement('a'); 
                        a.href = resourceLink.trim(); 
                        a.textContent = resourceName.trim(); 
                        a.target = "_blank"; 

                        li.appendChild(a); 
                        taskAdditionalResourcesList.appendChild(li); 
                    });

                    // Show the save button, hide the spinner, and display the result
                    saveTaskBtn.classList.remove('d-none');
                    loadingSpinner.classList.add('d-none');  
                    taskResultDiv.classList.remove('d-none');
                } else {
                    taskStepsList.innerHTML = `<p class="text-danger">Error: ${result.error}</p>`;
                    loadingSpinner.classList.add('d-none');  
                    // taskNoteToJobCoachList.innerHTML = '';
                    // taskAdditionalResourcesList.innerHTML = '';
                }
            } catch (error) {
                console.error('Task breakdown error:', error);
                taskStepsList.innerHTML = '<p class="text-danger">An error occurred while generating the breakdown.</p>';
                loadingSpinner.classList.add('d-none');  
                // taskNoteToJobCoachList.innerHTML = '';
                // taskAdditionalResourcesList.innerHTML = '';
            } finally {
                generateTaskBtn.disabled = false;
            }
        });
        generateAudioButton.addEventListener('click', async function() {
            console.log('Generate audio button clicked');
            const audioLoadingSpinner = document.getElementById('audioLoadingSpinner');
            audioLoadingSpinner.classList.remove('d-none');
            const taskSteps = [];  // Replace with the array containing notes to be converted to audio
            taskStepsList.querySelectorAll('li').forEach(li => {
                taskSteps.push(li.textContent);
            });

            const textToConvert = taskSteps.join(' '); // Combine notes into a single text string

            try {
                // Call the backend to generate audio
                const response = await fetch('/api/generateAudio', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: textToConvert })
                });

                if (response.ok) {
                    // Parse the JSON response
                    const data = await response.json();

                    // Get the base64-encoded audio data
                    const audioBase64 = data.audio;

                    // Convert base64 string to binary data (audio)
                    const audioBlob = new Blob([new Uint8Array(atob(audioBase64).split("").map(c => c.charCodeAt(0)))], { type: "audio/mpeg" });

                    // Create an audio URL from the blob
                    const audioUrl = URL.createObjectURL(audioBlob);

                    // Get the audio player element
                    const audioPlayer = document.getElementById('audioPlayer');
                    
                    // Set the audio player source to the blob URL
                    audioPlayer.src = audioUrl;

                    // Make the audio player visible and remove spinner
                    audioPlayer.classList.remove('d-none');
                    audioLoadingSpinner.classList.add('d-none');
                    // audioPlayer.play();
                } else {
                    console.error('Error generating audio:', response.statusText);
                    audioLoadingSpinner.classList.add('d-none');
                }
            } catch (error) {
                console.error('Error:', error);
                audioLoadingSpinner.classList.add('d-none');
            }
        });
        saveTaskBtn.addEventListener('click', async function() {
            try {
                const response = await fetch('/upload_note', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        category: 'Task Breakdown',
                        content: `Task: ${document.getElementById('taskName').value}\nSteps:\n${Array.from(taskStepsList.children).map(li => li.textContent).join('\n')}\nNote to Job COach:\n${Array.from(taskNoteToJobCoachList.children).map(li => li.textContent).join('\n')}\nAdditional Resources:\n${Array.from(taskAdditionalResourcesList.children).map(li => li.textContent).join('\n')}`,
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
    
    // Listen for when the modal is hidden (closed)
    $('#taskBreakdownModal').on('hidden.bs.modal', function () {
        // Reset form fields
        document.getElementById('taskBreakdownForm').reset();
        
        // Reset steps, notes, and resources
        document.getElementById('taskSteps').innerHTML = '';
        document.getElementById('taskNoteToJobCoach').innerHTML = '';
        document.getElementById('taskAdditionalResources').innerHTML = '';
        
        // Hide the audio player
        const audioPlayer = document.getElementById('audioPlayer');
        audioPlayer.classList.add('d-none');
        audioPlayer.pause();
        audioPlayer.src = '';  // Reset the audio source
        
        // Hide the loading spinner
        document.getElementById('loadingSpinner').classList.add('d-none');
        
        // Hide the result section
        document.getElementById('taskBreakdownResult').classList.add('d-none');
        
        // Reset any other UI elements
        document.getElementById('saveTaskBreakdown').classList.add('d-none');
    });


    // Add functionality to the AI chat form
    // const aiChatForm = document.getElementById('aiChatForm');
    // if (aiChatForm) {
    //     aiChatForm.addEventListener('submit', function(e) {
    //         e.preventDefault();
    //         const input = this.querySelector('input');
    //         const message = input.value.trim();
            
    //         if (message) {
    //             // Add user message to chat
    //             addMessage('user', message);
                
    //             // Clear input
    //             input.value = '';
                
    //             // Show typing indicator
    //             const chatContainer = document.querySelector('.chat-container');
    //             const typingDiv = document.createElement('div');
    //             typingDiv.className = 'chat-message ai-message mb-3 typing-indicator';
    //             typingDiv.innerHTML = `
    //                 <div class="d-flex">
    //                     <div class="avatar-circle bg-primary text-white me-2">
    //                         <i class="fas fa-robot"></i>
    //                     </div>
    //                     <div class="message-content p-3 bg-white rounded">
    //                         <div class="typing-dots">
    //                             <span></span>
    //                             <span></span>
    //                             <span></span>
    //                         </div>
    //                     </div>
    //                 </div>
    //             `;
    //             chatContainer.appendChild(typingDiv);
    //             chatContainer.scrollTop = chatContainer.scrollHeight;
                
    //             // Simulate AI response (for demo)
    //             setTimeout(() => {
    //                 // Remove typing indicator
    //                 chatContainer.removeChild(typingDiv);
                    
    //                 // Add AI response
    //                 simulateAIResponse(message);
    //             }, 1500);
    //         }
    //     });
    // }
    
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

    // Add functionality to the Knowledge Base form
    const aiKnowledgeBaseForm = document.getElementById('aiKnowledgeBaseForm');
    if (aiKnowledgeBaseForm) {
        aiKnowledgeBaseForm.addEventListener('submit', function(e) {
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
    // Don't reinitialize the chat functionality if it's implemented inline
    // in dashboard.html. Let's make sure we're not causing a conflict.
    const aiKnowledgeBaseFormInScript = document.getElementById('aiKnowledgeBaseForm');
    if (aiKnowledgeBaseFormInScript && !window.chatInitialized) {
        console.log('Initializing chat from script.js - this could cause conflicts');
        // Implementation would go here but we'll skip it to avoid conflicts
    }

    // Helper function to add message to chat
function addMessage(sender, content) {
    const knowledgeBaseContainer = document.querySelector('#knowledgeBaseContainer');
    if (!knowledgeBaseContainer) return;
    
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
});