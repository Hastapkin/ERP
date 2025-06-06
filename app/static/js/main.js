// Enhanced cart and chatbot functionality with GUIDED CONVERSATION
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded, initializing GUIDED CONVERSATION application...");
    
    // Initialize chatbot state with guided conversation tracking
    window.chatbotState = {
        isTyping: false,
        conversationStarted: false,
        conversationStage: 'greeting', // greeting, age, gender, interests, budget, recommendations
        collectedInfo: {
            age: null,
            gender: null,
            interests: [],
            budget: null
        },
        suggestions: [
            "I need a gift for my 8-year-old daughter",
            "Gift for a 6-year-old boy who loves building toys", 
            "Looking for something under $30 for a 10-year-old",
            "My 5-year-old loves art and crafts",
            "Birthday gift for 9-year-old girl, around $25"
        ]
    };

    // Cart functionality
    initializeCartFunctionality();
    
    // Enhanced chatbot functionality
    initializeGuidedChatbot();
    
    // Filter functionality
    initializeFilters();
    
    // Log initialization success
    console.log("GUIDED CONVERSATION application initialized successfully");
});

// Enhanced Guided Chatbot Functions
function initializeGuidedChatbot() {
    console.log("Initializing GUIDED chatbot...");
    
    const chatInput = document.getElementById('chatInput');
    const sendButton = document.getElementById('sendButton');
    const chatMessages = document.getElementById('chatMessages');
    const recommendationsContainer = document.getElementById('recommendations');
    
    if (!chatInput || !sendButton || !chatMessages) {
        console.error("Critical chatbot elements missing from the DOM!");
        return;
    }
    
    console.log("All required chatbot elements found in DOM");
    
    // Add event listeners
    sendButton.addEventListener('click', function() {
        console.log("Send button clicked - GUIDED mode");
        sendGuidedChatMessage();
    });
    
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            console.log("Enter key pressed in GUIDED chat input");
            e.preventDefault();
            sendGuidedChatMessage();
        }
    });
    
    // Add suggestion button handlers
    initializeSuggestionButtons();
    
    // Add reset button
    addGuidedResetButton();
    
    // Update placeholder based on conversation stage
    updateChatPlaceholder();
    
    console.log("GUIDED chatbot initialized successfully");
}

function initializeSuggestionButtons() {
    console.log("Initializing suggestion buttons...");
    
    // Handle suggestion clicks
    window.sendSuggestion = function(text) {
        const chatInput = document.getElementById('chatInput');
        const suggestions = document.getElementById('chatSuggestions');
        
        if (chatInput) {
            chatInput.value = text;
        }
        
        // Hide suggestions after first use
        if (suggestions) {
            suggestions.style.display = 'none';
        }
        
        // Mark conversation as started
        window.chatbotState.conversationStarted = true;
        
        // Send the message
        sendGuidedChatMessage();
    };
    
    // Hide suggestions when user starts typing
    const chatInput = document.getElementById('chatInput');
    const suggestions = document.getElementById('chatSuggestions');
    
    if (chatInput && suggestions) {
        chatInput.addEventListener('input', function() {
            if (this.value.length > 0 && !window.chatbotState.conversationStarted) {
                suggestions.style.display = 'none';
                window.chatbotState.conversationStarted = true;
            }
        });
        
        chatInput.addEventListener('focus', function() {
            if (this.value.length > 0 && !window.chatbotState.conversationStarted) {
                suggestions.style.display = 'none';
                window.chatbotState.conversationStarted = true;
            }
        });
    }
    
    console.log("Suggestion buttons initialized");
}

function updateChatPlaceholder() {
    const chatInput = document.getElementById('chatInput');
    if (!chatInput) return;
    
    const placeholders = {
        'greeting': 'Tell me the age of the gift recipient...',
        'age': 'What age are we shopping for?',
        'gender': 'Is this for a boy or girl?',
        'interests': 'What do they like to do? (art, toys, books, etc.)',
        'budget': 'What\'s your budget range?',
        'recommendations': 'Ask for gift recommendations...'
    };
    
    chatInput.placeholder = placeholders[window.chatbotState.conversationStage] || 'Ask for gift recommendations...';
}

function sendGuidedChatMessage() {
    console.log("sendGuidedChatMessage called");
    const chatInput = document.getElementById('chatInput');
    const message = chatInput.value.trim();
    
    console.log(`Message: "${message}", isTyping: ${window.chatbotState.isTyping}`);
    
    if (message === '' || window.chatbotState.isTyping) {
        console.log("Empty message or already typing, returning");
        return;
    }
    
    // Remove suggestions after first message
    if (!window.chatbotState.conversationStarted) {
        const suggestions = document.querySelector('#chatSuggestions');
        if (suggestions) {
            console.log("Removing suggestions");
            suggestions.style.display = 'none';
        }
        window.chatbotState.conversationStarted = true;
    }
    
    // Analyze message for information extraction
    analyzeUserMessage(message);
    
    // Add user message to chat
    addUserMessage(message);
    
    // Clear input
    chatInput.value = '';
    
    // Show typing indicator
    addTypingIndicator();
    window.chatbotState.isTyping = true;
    
    // Create abort controller for timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => {
        controller.abort();
        console.log("Request timed out");
    }, 30000);
    
    // Send to API
    console.log("Sending GUIDED request to /api/chatbot");
    fetch('/api/chatbot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            query: message
        }),
        signal: controller.signal
    })
    .then(response => {
        clearTimeout(timeoutId);
        console.log(`GUIDED response status: ${response.status}`);
        
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log("GUIDED response received:", data);
        
        // Remove typing indicator
        removeTypingIndicator();
        window.chatbotState.isTyping = false;
        
        // Update conversation stage if provided
        if (data.conversation_state) {
            updateConversationStage(data.conversation_state);
        }
        
        // Add bot response with delay for natural feel
        setTimeout(() => {
            addBotMessage(data.response);
            
            // Show recommendations if any
            if (data.recommendations && data.recommendations.length > 0) {
                console.log(`Showing ${data.recommendations.length} GUIDED recommendations`);
                setTimeout(() => {
                    showRecommendations(data.recommendations);
                }, 500);
            } else {
                console.log("No recommendations to show (information gathering phase)");
                // Hide recommendations during information gathering
                const recommendationsContainer = document.getElementById('recommendations');
                if (recommendationsContainer) {
                    recommendationsContainer.style.display = 'none';
                }
            }
            
            // Update placeholder for next stage
            updateChatPlaceholder();
            
        }, 500);
    })
    .catch(error => {
        clearTimeout(timeoutId);
        console.error('Error sending GUIDED message:', error);
        removeTypingIndicator();
        window.chatbotState.isTyping = false;
        
        addBotMessage('Sorry, I couldn\'t process your request at the moment. Please try again.');
        showNotification('Gift advisor service unavailable. Please try again later.', 'error', 6000);
    });
}

function analyzeUserMessage(message) {
    const messageLower = message.toLowerCase();
    
    // Extract age information
    const agePatterns = [
        /(\d+)\s*(?:year|yr)s?\s*old/,
        /age\s*(\d+)/,
        /(\d+)[- ]year[- ]old/,
        /\b([3-9]|1[0-2])\b/
    ];
    
    for (const pattern of agePatterns) {
        const match = messageLower.match(pattern);
        if (match) {
            const age = parseInt(match[1]);
            if (age >= 3 && age <= 12) {
                window.chatbotState.collectedInfo.age = age;
                console.log(`Extracted age: ${age}`);
                break;
            }
        }
    }
    
    // Extract gender information
    const genderKeywords = {
        'male': ['boy', 'son', 'male', 'he', 'his', 'him'],
        'female': ['girl', 'daughter', 'female', 'she', 'her']
    };
    
    for (const [gender, keywords] of Object.entries(genderKeywords)) {
        if (keywords.some(keyword => messageLower.includes(keyword))) {
            window.chatbotState.collectedInfo.gender = gender;
            console.log(`Extracted gender: ${gender}`);
            break;
        }
    }
    
    // Extract interests
    const interestKeywords = {
        'art': ['art', 'craft', 'drawing', 'painting', 'creative', 'coloring'],
        'toys': ['toy', 'game', 'play', 'building', 'blocks'],
        'books': ['book', 'read', 'story', 'learning'],
        'electronics': ['electronic', 'tech', 'gadget', 'device'],
        'clothes': ['clothes', 'fashion', 'dress', 'wear'],
        'sports': ['sport', 'active', 'outdoor', 'exercise', 'ball']
    };
    
    for (const [interest, keywords] of Object.entries(interestKeywords)) {
        if (keywords.some(keyword => messageLower.includes(keyword))) {
            if (!window.chatbotState.collectedInfo.interests.includes(interest)) {
                window.chatbotState.collectedInfo.interests.push(interest);
                console.log(`Extracted interest: ${interest}`);
            }
        }
    }
    
    // Extract budget information
    const budgetPatterns = [
        /\$(\d+)/,
        /(\d+)\s*dollar/,
        /under\s*\$?(\d+)/,
        /below\s*\$?(\d+)/,
        /around\s*\$?(\d+)/,
        /budget.*?\$?(\d+)/
    ];
    
    for (const pattern of budgetPatterns) {
        const match = messageLower.match(pattern);
        if (match) {
            window.chatbotState.collectedInfo.budget = parseInt(match[1]);
            console.log(`Extracted budget: $${match[1]}`);
            break;
        }
    }
    
    console.log("Current collected info:", window.chatbotState.collectedInfo);
}

function updateConversationStage(conversationState) {
    console.log("Updating conversation stage:", conversationState);
    
    // Update our local state
    if (conversationState.has_age) window.chatbotState.conversationStage = 'gender';
    if (conversationState.has_gender) window.chatbotState.conversationStage = 'interests';
    if (conversationState.has_interests) window.chatbotState.conversationStage = 'budget';
    if (conversationState.can_recommend) window.chatbotState.conversationStage = 'recommendations';
    
    console.log("New conversation stage:", window.chatbotState.conversationStage);
}

function addGuidedResetButton() {
    console.log("Adding GUIDED reset button...");
    const chatMessages = document.getElementById('chatMessages');
    if (!chatMessages) {
        console.error("Cannot add reset button: chat messages container not found");
        return;
    }
    
    const resetButton = document.createElement('button');
    resetButton.className = 'chat-reset-btn';
    resetButton.innerHTML = '🔄 Start Over';
    resetButton.style.cssText = `
        position: absolute;
        top: 10px;
        right: 10px;
        padding: 5px 10px;
        background: #6c757d;
        color: white;
        border: none;
        border-radius: 15px;
        font-size: 0.8em;
        cursor: pointer;
        transition: all 0.3s;
        z-index: 10;
    `;
    
    resetButton.addEventListener('click', function() {
        console.log("GUIDED reset button clicked");
        resetGuidedConversation();
    });
    
    resetButton.addEventListener('mouseenter', function() {
        this.style.background = '#5a6268';
    });
    
    resetButton.addEventListener('mouseleave', function() {
        this.style.background = '#6c757d';
    });
    
    // Make chat messages container relative positioned
    chatMessages.style.position = 'relative';
    chatMessages.appendChild(resetButton);
    console.log("GUIDED reset button added");
}

function resetGuidedConversation() {
    console.log("Resetting GUIDED conversation...");
    const chatMessages = document.getElementById('chatMessages');
    const recommendationsContainer = document.getElementById('recommendations');
    const suggestions = document.getElementById('chatSuggestions');
    
    if (!chatMessages) {
        console.error("Cannot reset conversation: chat messages container not found");
        return;
    }
    
    // Reset chatbot state
    window.chatbotState = {
        isTyping: false,
        conversationStarted: false,
        conversationStage: 'greeting',
        collectedInfo: {
            age: null,
            gender: null,
            interests: [],
            budget: null
        },
        suggestions: [
            "I need a gift for my 8-year-old daughter",
            "Gift for a 6-year-old boy who loves building toys",
            "Looking for something under $30 for a 10-year-old", 
            "My 5-year-old loves art and crafts",
            "Birthday gift for 9-year-old girl, around $25"
        ]
    };
    
    // Clear chat messages except welcome message
    chatMessages.innerHTML = `
        <div class="bot-message">
            <p><strong>Hello! I'm your Gift Guru! 🎁</strong></p>
            <p>I'm here to help you find the perfect gift using our customer data and purchase insights!</p>
            <p><strong>To get started, just tell me:</strong></p>
            <p>👶 <strong>What's the age</strong> of the gift recipient? (We specialize in ages 3-12)</p>
            <div class="conversation-hints">
                <p><em>I'll also ask about gender, interests, and budget to give you the best recommendations based on what other customers loved!</em></p>
            </div>
        </div>
    `;
    
    // Clear recommendations
    if (recommendationsContainer) {
        recommendationsContainer.style.display = 'none';
        recommendationsContainer.innerHTML = '';
    }
    
    // Show suggestions again
    if (suggestions) {
        suggestions.style.display = 'block';
    }
    
    // Reset placeholder
    updateChatPlaceholder();
    
    // Call API to reset server-side context
    fetch('/api/chatbot/reset', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    }).then(response => response.json())
      .then(data => {
          console.log('GUIDED conversation reset:', data);
      })
      .catch(error => {
          console.error("Error resetting GUIDED conversation:", error);
          showNotification("Error resetting conversation", "error");
      });
    
    // Re-add reset button
    addGuidedResetButton();
    console.log("GUIDED conversation reset complete");
}

// Keep all the existing functions but enhance them for guided conversation
function addTypingIndicator() {
    console.log("Adding typing indicator");
    const chatMessages = document.getElementById('chatMessages');
    
    if (chatMessages) {
        const typingElement = document.createElement('div');
        typingElement.className = 'bot-message typing-indicator';
        typingElement.innerHTML = `
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
            <p style="margin-left: 10px; font-size: 0.9em; color: #666;">Gift Guru is thinking...</p>
        `;
        
        chatMessages.appendChild(typingElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

function removeTypingIndicator() {
    console.log("Removing typing indicator");
    const typingIndicator = document.querySelector('.typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

function addUserMessage(message) {
    console.log("Adding user message");
    const chatMessages = document.getElementById('chatMessages');
    
    if (chatMessages) {
        const messageElement = document.createElement('div');
        messageElement.className = 'user-message';
        messageElement.innerHTML = `<p>${escapeHtml(message)}</p>`;
        
        // Add timestamp
        const timestamp = document.createElement('div');
        timestamp.className = 'message-timestamp';
        timestamp.textContent = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        timestamp.style.cssText = `
            font-size: 0.7em;
            color: rgba(255,255,255,0.7);
            margin-top: 5px;
            text-align: right;
        `;
        messageElement.appendChild(timestamp);
        
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Add animation
        messageElement.style.opacity = '0';
        messageElement.style.transform = 'translateY(20px)';
        setTimeout(() => {
            messageElement.style.transition = 'all 0.3s ease';
            messageElement.style.opacity = '1';
            messageElement.style.transform = 'translateY(0)';
        }, 10);
    }
}

function addBotMessage(message) {
    console.log("Adding bot message");
    const chatMessages = document.getElementById('chatMessages');
    
    if (chatMessages) {
        const messageElement = document.createElement('div');
        messageElement.className = 'bot-message';
        messageElement.innerHTML = `<p>${escapeHtml(message)}</p>`;
        
        // Add timestamp
        const timestamp = document.createElement('div');
        timestamp.className = 'message-timestamp';
        timestamp.textContent = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        timestamp.style.cssText = `
            font-size: 0.7em;
            color: #999;
            margin-top: 5px;
        `;
        messageElement.appendChild(timestamp);
        
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Add animation
        messageElement.style.opacity = '0';
        messageElement.style.transform = 'translateY(20px)';
        setTimeout(() => {
            messageElement.style.transition = 'all 0.3s ease';
            messageElement.style.opacity = '1';
            messageElement.style.transform = 'translateY(0)';
        }, 10);
    }
}

// Enhanced recommendation display for guided conversation
function showRecommendations(recommendations) {
    console.log("Showing GUIDED recommendations");
    const container = document.getElementById('recommendations');
    
    if (!container) {
        console.error("Recommendations container not found");
        return;
    }
    
    // Clear previous recommendations
    container.innerHTML = '';
    
    if (!recommendations || recommendations.length === 0) {
        console.log("No recommendations to display");
        container.style.display = 'none';
        return;
    }
    
    // Add enhanced header for guided conversation
    const header = document.createElement('h3');
    header.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#4cd964" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>
        </svg> 
        Perfect Matches Based on Your Preferences! 🎯
    `;
    header.style.cssText = `
        margin: 0 0 15px 0;
        color: #4cd964;
        font-size: 1.2em;
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 700;
    `;
    
    container.appendChild(header);
    
    // Add info summary based on collected information
    const infoSummary = document.createElement('div');
    infoSummary.className = 'conversation-stage';
    
    let summaryText = "Based on what you told me: ";
    const info = window.chatbotState.collectedInfo;
    const summaryParts = [];
    
    if (info.age) summaryParts.push(`${info.age}-year-old`);
    if (info.gender) summaryParts.push(info.gender === 'male' ? 'boy' : 'girl');
    if (info.interests.length > 0) summaryParts.push(`loves ${info.interests.join(' & ')}`);
    if (info.budget) summaryParts.push(`$${info.budget} budget`);
    
    if (summaryParts.length > 0) {
        summaryText += summaryParts.join(', ');
    } else {
        summaryText = "Here are some great options for you:";
    }
    
    infoSummary.innerHTML = `<span class="stage-icon">📝</span> ${summaryText}`;
    container.appendChild(infoSummary);
    
    // Create recommendations grid (reuse existing function but enhance it)
    const recommendationsGrid = document.createElement('div');
    recommendationsGrid.className = 'recommendations-grid';
    recommendationsGrid.style.cssText = `
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 20px;
        margin-top: 15px;
    `;
    
    // Add each recommendation (reuse existing code)
    recommendations.forEach((item, index) => {
        const element = document.createElement('div');
        element.className = 'recommendation-item';
        element.style.cssText = `
            background: white;
            border: 1px solid #e6e6e6;
            border-radius: 12px;
            overflow: hidden;
            transition: all 0.3s ease;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
            animation: slideUp 0.5s ease forwards;
            animation-delay: ${index * 0.1}s;
            opacity: 0;
            transform: translateY(20px);
            position: relative;
        `;
        
        let itemHTML = `
            <div class="rec-image" style="position: relative; overflow: hidden;">
                <img src="/static/images/products/${item.image}" alt="${item.name}" 
                     style="width: 100%; height: 180px; object-fit: cover; transition: transform 0.3s ease;"
                     onerror="this.src='/static/images/products/placeholder.jpg'">
                <div class="rec-type-badge" style="position: absolute; top: 12px; right: 12px; 
                     background: ${item.type === 'combo' ? '#ff6b6b' : '#4cd964'}; 
                     color: white; padding: 4px 10px; border-radius: 20px; font-size: 0.8em;
                     font-weight: 600; letter-spacing: 0.5px; box-shadow: 0 2px 8px rgba(0,0,0,0.2);">
                    ${item.type === 'combo' ? 'GIFT SET' : 'PRODUCT'}
                </div>
            </div>
            <div class="rec-details" style="padding: 15px;">
                <h4 style="margin: 0 0 8px 0; font-size: 1.1em; color: #333;">${item.name}</h4>
                <p class="price" style="color: #ff6b6b; font-weight: bold; margin: 8px 0; font-size: 1.2em;">
                    $${item.price.toFixed(2)}
                </p>
        `;
        
        // Add relevance tags
        if (item.relevance_scores && Object.keys(item.relevance_scores).length > 0) {
            itemHTML += `<div class="relevance-tags">`;
            for (const [key, value] of Object.entries(item.relevance_scores)) {
                itemHTML += `<span class="relevance-tag">${value}</span>`;
            }
            itemHTML += `</div>`;
        }
        
        itemHTML += `
                <p style="color: #666; font-size: 0.9em; margin: 10px 0; line-height: 1.5;">
                    ${item.description}
                </p>
                <button class="add-to-cart-rec" data-id="${item.id}" data-type="${item.type}"
                        style="width: 100%; padding: 12px; background: linear-gradient(135deg, #4cd964 0%, #37b54a 100%); color: white; 
                               border: none; border-radius: 8px; font-weight: 600; cursor: pointer;
                               transition: all 0.3s; margin-top: 15px; display: flex; justify-content: center; align-items: center; gap: 8px;">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="9" cy="21" r="1"></circle>
                        <circle cx="20" cy="21" r="1"></circle>
                        <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
                    </svg>
                    Add to Cart
                </button>
            </div>
        `;
        
        element.innerHTML = itemHTML;
        recommendationsGrid.appendChild(element);
    });
    
    container.appendChild(recommendationsGrid);
    
    // Add event listeners to buttons (reuse existing logic)
    const addButtons = container.querySelectorAll('.add-to-cart-rec');
    addButtons.forEach(button => {
        button.addEventListener('click', function() {
            const itemId = parseInt(this.dataset.id);
            const itemType = this.dataset.type;
            
            console.log(`Add to cart clicked: ${itemType} #${itemId}`);
            
            const originalText = this.innerHTML;
            this.innerHTML = `
                <svg class="spinner" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-dashoffset="16"></circle>
                </svg>
                Adding...
            `;
            this.disabled = true;
            
            addToCart(itemId, itemType).then(() => {
                this.innerHTML = `
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M20 6L9 17l-5-5"/>
                    </svg>
                    Added to Cart
                `;
                this.style.background = 'linear-gradient(135deg, #28a745 0%, #218838 100%)';
                
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.style.background = 'linear-gradient(135deg, #4cd964 0%, #37b54a 100%)';
                    this.disabled = false;
                }, 2000);
            }).catch((error) => {
                console.error("Error adding to cart:", error);
                this.innerHTML = `
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <line x1="18" y1="6" x2="6" y2="18"></line>
                        <line x1="6" y1="6" x2="18" y2="18"></line>
                    </svg>
                    Error
                `;
                this.style.background = '#dc3545';
                
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.style.background = 'linear-gradient(135deg, #4cd964 0%, #37b54a 100%)';
                    this.disabled = false;
                }, 2000);
            });
        });
    });
    
    // Show recommendations with animation
    container.style.display = 'block';
    setTimeout(() => {
        container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 300);
    
    console.log("GUIDED recommendations displayed successfully");
}

// ===== REST OF THE EXISTING FUNCTIONS =====
// Cart functionality, filters, etc. remain the same...

function initializeCartFunctionality() {
    console.log("Initializing cart functionality...");
    
    // Add to cart buttons
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productCard = this.closest('.product-card');
            const productId = parseInt(productCard.dataset.id);
            const productType = productCard.dataset.type;
            
            addToCart(productId, productType);
        });
    });
    
    // Cart quantity buttons
    const decreaseButtons = document.querySelectorAll('.quantity-btn.decrease');
    const increaseButtons = document.querySelectorAll('.quantity-btn.increase');
    const quantityInputs = document.querySelectorAll('.quantity-input');
    const removeButtons = document.querySelectorAll('.remove-item');
    
    decreaseButtons.forEach(button => {
        button.addEventListener('click', function() {
            const cartItem = this.closest('.cart-item');
            const input = cartItem.querySelector('.quantity-input');
            let quantity = parseInt(input.value);
            
            if (quantity > 1) {
                quantity -= 1;
                input.value = quantity;
                updateCartItem(cartItem, quantity);
            }
        });
    });
    
    increaseButtons.forEach(button => {
        button.addEventListener('click', function() {
            const cartItem = this.closest('.cart-item');
            const input = cartItem.querySelector('.quantity-input');
            let quantity = parseInt(input.value);
            
            quantity += 1;
            input.value = quantity;
            updateCartItem(cartItem, quantity);
        });
    });
    
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            const cartItem = this.closest('.cart-item');
            let quantity = parseInt(this.value);
            
            if (quantity < 1) {
                quantity = 1;
                this.value = quantity;
            }
            
            updateCartItem(cartItem, quantity);
        });
    });
    
    removeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const cartItem = this.closest('.cart-item');
            removeFromCart(cartItem);
        });
    });
    
    console.log("Cart functionality initialized");
}

function initializeFilters() {
    console.log("Initializing filters...");
    const categoryLinks = document.querySelectorAll('.category-link');
    categoryLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const category = this.dataset.category;
            window.location.href = `/products?category=${category}`;
        });
    });
    console.log("Filters initialized");
}

function addToCart(productId, productType) {
    console.log(`Adding to cart: ${productType} #${productId}`);
    return fetch('/api/cart/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            id: productId,
            type: productType,
            quantity: 1
        }),
    })
    .then(response => {
        console.log(`Add to cart response status: ${response.status}`);
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Update cart count
            updateCartCount(data.cart_count);
            
            // Show success notification
            showNotification('Item added to cart successfully!');
            
            return data;
        } else {
            throw new Error('Failed to add item to cart');
        }
    })
    .catch(error => {
        console.error('Error adding to cart:', error);
        showNotification('Error adding item to cart', 'error');
        throw error;
    });
}

function updateCartItem(cartItem, quantity) {
    console.log(`Updating cart item quantity to ${quantity}`);
    const itemId = parseInt(cartItem.dataset.id);
    const itemType = cartItem.dataset.type;
    
    fetch('/api/cart/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            id: itemId,
            type: itemType,
            quantity: quantity
        }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Update subtotal
            const subtotalElement = cartItem.querySelector('.cart-item-subtotal p');
            const price = parseFloat(cartItem.querySelector('.price').textContent.replace('$', ''));
            const subtotal = (price * quantity).toFixed(2);
            
            if (subtotalElement) {
                subtotalElement.textContent = `$${subtotal}`;
            }
            
            // Update cart totals
            updateCartTotals(data);
            
            // Update cart count
            updateCartCount(data.cart_count);
        }
    })
    .catch(error => {
        console.error('Error updating cart item:', error);
        showNotification('Error updating cart', 'error');
    });
}

function removeFromCart(cartItem) {
    console.log("Removing item from cart");
    const itemId = parseInt(cartItem.dataset.id);
    const itemType = cartItem.dataset.type;
    
    fetch('/api/cart/remove', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            id: itemId,
            type: itemType
        }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Remove item from DOM
            cartItem.remove();
            
            // Update cart totals
            updateCartTotals(data);
            
            // Update cart count
            updateCartCount(data.cart_count);
            
            // Show empty cart message if needed
            if (data.cart_count === 0) {
                const cartItemsContainer = document.getElementById('cartItems');
                const cartSummary = document.getElementById('cartSummary');
                const cartEmpty = document.getElementById('cartEmpty');
                
                if (cartItemsContainer) cartItemsContainer.style.display = 'none';
                if (cartSummary) cartSummary.style.display = 'none';
                if (cartEmpty) cartEmpty.style.display = 'block';
            }
        }
    })
    .catch(error => {
        console.error('Error removing cart item:', error);
        showNotification('Error removing item from cart', 'error');
    });
}

function updateCartCount(count) {
    console.log(`Updating cart count to ${count}`);
    const cartCountElement = document.querySelector('.cart-count');
    if (cartCountElement) {
        cartCountElement.textContent = count;
        
        // Add animation for cart count update
        cartCountElement.style.transform = 'scale(1.2)';
        cartCountElement.style.transition = 'transform 0.2s ease';
        setTimeout(() => {
            cartCountElement.style.transform = 'scale(1)';
        }, 200);
    }
}

function updateCartTotals(data) {
    console.log("Updating cart totals");
    const subtotalElement = document.querySelector('.summary-row:nth-child(1) span:last-child');
    const shippingElement = document.querySelector('.summary-row:nth-child(2) span:last-child');
    const taxElement = document.querySelector('.summary-row:nth-child(3) span:last-child');
    const totalElement = document.querySelector('.summary-row.total span:last-child');
    
    if (subtotalElement && data.cart_subtotal !== undefined) {
        subtotalElement.textContent = `$${data.cart_subtotal.toFixed(2)}`;
    }
    
    if (shippingElement && data.shipping !== undefined) {
        shippingElement.textContent = `$${data.shipping.toFixed(2)}`;
    }
    
    if (taxElement && data.tax !== undefined) {
        taxElement.textContent = `$${data.tax.toFixed(2)}`;
    }
    
    if (totalElement && data.total !== undefined) {
        totalElement.textContent = `$${data.total.toFixed(2)}`;
    }
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showNotification(message, type = 'success', duration = 4000) {
    console.log(`Showing notification: ${message} (${type})`);
    
    // Check if notification container exists
    let notificationContainer = document.getElementById('notification-container');
    
    if (!notificationContainer) {
        // Create container if it doesn't exist
        notificationContainer = document.createElement('div');
        notificationContainer.id = 'notification-container';
        notificationContainer.style.position = 'fixed';
        notificationContainer.style.top = '20px';
        notificationContainer.style.right = '20px';
        notificationContainer.style.zIndex = '1000';
        document.body.appendChild(notificationContainer);
    }
    
    // Create notification
    const notification = document.createElement('div');
    notification.className = 'notification';
    const backgroundColor = type === 'success' ? '#4cd964' : '#dc3545';
    notification.style.backgroundColor = backgroundColor;
    notification.style.color = 'white';
    notification.style.padding = '12px 20px';
    notification.style.borderRadius = '6px';
    notification.style.marginBottom = '10px';
    notification.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
    notification.style.transition = 'all 0.3s ease';
    notification.style.transform = 'translateX(100%)';
    notification.style.opacity = '0';
    notification.innerHTML = `
        <div style="display: flex; align-items: center; gap: 8px;">
            <span>${type === 'success' ? '✓' : '✗'}</span>
            <span>${message}</span>
        </div>
    `;
    
    // Add to container
    notificationContainer.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
        notification.style.opacity = '1';
    }, 10);
    
    // Remove after specified duration
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        notification.style.opacity = '0';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, duration);
}