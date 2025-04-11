document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const messageForm = document.getElementById('messageForm');
    const userInput = document.getElementById('userInput');
    const chatMessages = document.getElementById('chatMessages');
    const sendButton = document.getElementById('sendButton');
    const presetPromptsContainer = document.getElementById('presetPrompts');
    const clearChatButton = document.getElementById('clearChat');
    const loadingTemplate = document.getElementById('loadingTemplate');
    
    // Bootstrap Modal for crisis alerts
    const crisisModal = new bootstrap.Modal(document.getElementById('crisisModal'));
    
    // Load chat history when page loads
    loadChatHistory();
    
    // Load preset prompts
    loadPresetPrompts();
    
    // Event listeners
    messageForm.addEventListener('submit', handleMessageSubmit);
    clearChatButton.addEventListener('click', clearChatHistory);
    
    // Scroll to bottom of chat container
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Load chat history
    function loadChatHistory() {
        fetch('/api/get_history')
            .then(response => response.json())
            .then(history => {
                // Clear current messages
                chatMessages.innerHTML = '';
                
                if (history.length === 0) {
                    // Add welcome message if no history
                    addMessage('assistant', 'Welcome to EmpathAI! I\'m here to provide a judgment-free zone where you can express your thoughts and feelings. How are you doing today?');
                } else {
                    // Add messages from history
                    history.forEach(msg => {
                        addMessage(msg.role, msg.content);
                    });
                }
                
                // Scroll to bottom after loading history
                scrollToBottom();
            })
            .catch(error => {
                console.error('Error loading chat history:', error);
            });
    }
    
    // Load preset prompts
    function loadPresetPrompts() {
        fetch('/api/preset_prompts')
            .then(response => response.json())
            .then(prompts => {
                presetPromptsContainer.innerHTML = '';
                
                prompts.forEach(prompt => {
                    const btn = document.createElement('button');
                    btn.className = 'btn btn-sm btn-outline-secondary preset-prompt-btn';
                    btn.textContent = prompt.text;
                    btn.dataset.prompt = prompt.text;
                    
                    btn.addEventListener('click', function() {
                        userInput.value = this.dataset.prompt;
                        userInput.focus();
                    });
                    
                    presetPromptsContainer.appendChild(btn);
                });
            })
            .catch(error => {
                console.error('Error loading preset prompts:', error);
            });
    }
    
    // Handle message submit
    async function handleMessageSubmit(e) {
        e.preventDefault();
        
        const userMessage = userInput.value.trim();
        if (!userMessage) return;
        
        // Clear input field
        userInput.value = '';
        
        // Add user message to chat
        addMessage('user', userMessage);
        
        // Show loading indicator
        const loadingElement = addLoadingIndicator();
        
        // Disable send button while processing
        sendButton.disabled = true;
        
        try {
            // Send message to server
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: userMessage })
            });
            
            const data = await response.json();
            
            // Remove loading indicator
            if (loadingElement) {
                loadingElement.remove();
            }
            
            // Add AI response to chat
            addMessage('assistant', data.response);
            
            // If crisis detected, show modal
            if (data.crisis_detected) {
                setTimeout(() => {
                    crisisModal.show();
                }, 1000);
            }
        } catch (error) {
            console.error('Error sending message:', error);
            
            // Remove loading indicator
            if (loadingElement) {
                loadingElement.remove();
            }
            
            // Add error message
            addMessage('assistant', 'Sorry, there was an error processing your message. Please try again.');
        } finally {
            // Re-enable send button
            sendButton.disabled = false;
            
            // Scroll to bottom
            scrollToBottom();
        }
    }
    
    // Add message to chat
    function addMessage(role, content) {
        const messageRow = document.createElement('div');
        messageRow.className = `message-row ${role}`;
        
        const messageBubble = document.createElement('div');
        messageBubble.className = 'message-bubble';
        
        // Format content with line breaks
        const formattedContent = content.replace(/\n/g, '<br>');
        
        // Create paragraph for message content
        const paragraph = document.createElement('p');
        paragraph.innerHTML = formattedContent;
        
        messageBubble.appendChild(paragraph);
        messageRow.appendChild(messageBubble);
        chatMessages.appendChild(messageRow);
        
        // Scroll to the new message
        scrollToBottom();
        
        return messageRow;
    }
    
    // Add loading indicator
    function addLoadingIndicator() {
        const loadingNode = document.importNode(loadingTemplate.content, true);
        chatMessages.appendChild(loadingNode);
        scrollToBottom();
        
        return chatMessages.lastElementChild;
    }
    
    // Clear chat history
    function clearChatHistory() {
        fetch('/api/clear_history', {
            method: 'POST'
        })
            .then(response => response.json())
            .then(data => {
                // Reload chat history (which will show welcome message)
                loadChatHistory();
            })
            .catch(error => {
                console.error('Error clearing chat history:', error);
            });
    }
});
