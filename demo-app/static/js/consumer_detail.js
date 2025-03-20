// Trigger-based AI insights
document.addEventListener('DOMContentLoaded', function() {
    console.log('Consumer detail trigger-based AI insights initialized'); // Debug statement

    const app_page_consumerdetail = document.getElementById('app_page_consumerdetail');
    if (!app_page_consumerdetail) {
        console.log('Consumer detail page not found, skipping initialization');
        return;
    }
    
    const appt_quick_actions = document.querySelectorAll('.appt_quick_action');
    
    if (!appt_quick_actions) {
        console.log('No appointment quick actions found, skipping initialization');
        return;
    }
    appt_quick_actions.forEach(quick_action => {
        quick_action.addEventListener('click', async function(e) {
            console.log('Appointment quick action clicked'); // Debug statement
            console.log(quick_action.dataset);
            e.preventDefault();
            const eventTrigger = "appointment disposition change";
            const eventValue = quick_action.dataset.action;
            const appointmentId = quick_action.dataset.appt;
            const consumerId = quick_action.dataset.consumer;
            console.log('Processing action:', eventTrigger, ":", eventValue);
            try {
                console.log('Sending request to backend');
                const response = await fetch('/api/next-best-action', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ 
                        "consumer_id": consumerId,
                        "appointment_id": appointmentId,
                        "event_trigger": eventTrigger,
                        "event_value": eventValue
                    }),
                });
                
                console.log('Response received', response.status);
                
                if (!response.ok) {
                    throw new Error(`Network response was not ok: ${response.status}`);
                }
                
                const data = await response.json();
                console.log('Data received', data);
                
                const div_next_best_action = consumer_detail_next_best_action
                if (div_next_best_action) {
                    div_next_best_action.innerHTML = data.response;
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    });
});
//         appendAIMessage('Thinking...', aiMessageId, true);
        
//         try {
//             console.log('Sending request to backend');
//             // Send request to the backend
//             const response = await fetch('/api/chat', {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                 },
//                 body: JSON.stringify({ user_content: userContent }),
//             });
            
//             console.log('Response received', response.status);
            
//             if (!response.ok) {
//                 throw new Error(`Network response was not ok: ${response.status}`);
//             }
            
//             const data = await response.json();
//             console.log('Data received', data);
            
//             // Update the AI message with the actual response
//             updateAIMessage(aiMessageId, data.response);
            
//         } catch (error) {
//             console.error('Error:', error);
//             updateAIMessage(aiMessageId, 'Sorry, there was an error processing your request.');
//         }
//     });
//     // Function to append an AI message to the chat
//     function appendAIMessage(content, messageId, isLoading = false) {
//         const messageDiv = document.createElement('div');
//         messageDiv.className = 'chat-message ai-message mb-3';
//         messageDiv.id = messageId;
        
//         let messageContent = content;
//         if (isLoading) {
//             messageContent = `<div class="d-flex align-items-center">
//                 <div class="spinner-border spinner-border-sm text-primary me-2" role="status"></div>
//                 <span>${content}</span>
//             </div>`;
//         }
        
//         messageDiv.innerHTML = `
//             <div class="d-flex">
//                 <div class="avatar-circle bg-primary text-white me-2">
//                     <i class="fas fa-robot"></i>
//                 </div>
//                 <div class="message-content p-3 bg-white rounded">
//                     ${messageContent}
//                 </div>
//             </div>
//         `;
        
//         chatContainer.appendChild(messageDiv);
//         chatContainer.scrollTop = chatContainer.scrollHeight;
//     }
    
//     // Function to update an existing AI message
//     function updateAIMessage(messageId, content) {
//         const messageDiv = document.getElementById(messageId);
//         if (messageDiv) {
//             const contentContainer = messageDiv.querySelector('.message-content');
//             if (contentContainer) {
//                 contentContainer.innerHTML = `<p class="mb-0">${content}</p>`;
                
//                 // If the response contains links, make them open in a new tab
//                 contentContainer.querySelectorAll('a').forEach(link => {
//                     if (!link.getAttribute('target')) {
//                         link.setAttribute('target', '_blank');
//                         link.setAttribute('rel', 'noopener noreferrer');
//                     }
//                 });
                
//                 chatContainer.scrollTop = chatContainer.scrollHeight;
//             } else {
//                 console.error('Message content container not found');
//             }
//         } else {
//             console.error(`AI message with ID ${messageId} not found`);
//         }
//     }
    
//     // Initialize modal events to ensure the chat input gets focus
//     const aiAssistantModal = document.getElementById('aiAssistantModal');
//     if (aiAssistantModal) {
//         aiAssistantModal.addEventListener('shown.bs.modal', function() {
//             console.log('Modal shown, focusing input');
//             userInput.focus();
//         });
//     }
// });    