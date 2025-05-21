// Enhanced cart and chatbot functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded, initializing application...");
    
    // Initialize chatbot state
    window.chatbotState = {
        isTyping: false,
        conversationStarted: false,
        suggestions: [
            "I'm looking for a birthday gift for my 8-year-old daughter",
            "What do you recommend for teenagers?",
            "I need something under $25",
            "Show me educational toys",
            "Gift ideas for boys who love art"
        ]
    };

    // Cart functionality
    initializeCartFunctionality();
    
    // Chatbot functionality
    initializeChatbot();
    
    // Filter functionality
    initializeFilters();
    
    // Log initialization success
    console.log("Application initialized successfully");
});

// Cart Functions
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

// Chatbot Functions
function initializeChatbot() {
    console.log("Initializing chatbot...");
    
    const chatInput = document.getElementById('chatInput');
    const sendButton = document.getElementById('sendButton');
    const chatMessages = document.getElementById('chatMessages');
    const recommendationsContainer = document.getElementById('recommendations');
    
    if (!chatInput || !sendButton || !chatMessages) {
        console.error("Critical chatbot elements missing from the DOM!");
        console.log({
            chatInput: chatInput ? "Found" : "Missing",
            sendButton: sendButton ? "Found" : "Missing",
            chatMessages: chatMessages ? "Found" : "Missing"
        });
        return;
    }
    
    console.log("All required chatbot elements found in DOM");
    
    // Add event listeners
    sendButton.addEventListener('click', function() {
        console.log("Send button clicked");
        sendChatMessage();
    });
    
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            console.log("Enter key pressed in chat input");
            e.preventDefault();
            sendChatMessage();
        }
    });
    
    // Add input suggestions
    addInputSuggestions();
    
    // Add reset button
    addResetButton();
    
    console.log("Chatbot initialized successfully");
}

function addInputSuggestions() {
    console.log("Adding input suggestions...");
    const chatInput = document.getElementById('chatInput');
    if (!chatInput || window.chatbotState.conversationStarted) {
        console.log("Skipping suggestions: input not found or conversation already started");
        return;
    }
    
    const suggestionsContainer = document.createElement('div');
    suggestionsContainer.className = 'chat-suggestions';
    suggestionsContainer.style.cssText = `
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 10px;
        padding: 10px;
        background: #f8f9fa;
        border-radius: 8px;
        border: 1px solid #e6e6e6;
    `;
    
    window.chatbotState.suggestions.forEach(suggestion => {
        const suggestionButton = document.createElement('button');
        suggestionButton.className = 'suggestion-btn';
        suggestionButton.textContent = suggestion;
        suggestionButton.style.cssText = `
            padding: 8px 12px;
            background: white;
            border: 1px solid #ddd;
            border-radius: 20px;
            font-size: 0.9em;
            cursor: pointer;
            transition: all 0.3s;
            white-space: nowrap;
        `;
        
        suggestionButton.addEventListener('click', function() {
            chatInput.value = suggestion;
            sendChatMessage();
            suggestionsContainer.remove();
        });
        
        suggestionButton.addEventListener('mouseenter', function() {
            this.style.background = '#f0f0f0';
            this.style.borderColor = '#4a89dc';
        });
        
        suggestionButton.addEventListener('mouseleave', function() {
            this.style.background = 'white';
            this.style.borderColor = '#ddd';
        });
        
        suggestionsContainer.appendChild(suggestionButton);
    });
    
    chatInput.parentNode.insertBefore(suggestionsContainer, chatInput.nextSibling);
    console.log("Chat suggestions added");
}

function addResetButton() {
    console.log("Adding reset button...");
    const chatMessages = document.getElementById('chatMessages');
    if (!chatMessages) {
        console.error("Cannot add reset button: chat messages container not found");
        return;
    }
    
    const resetButton = document.createElement('button');
    resetButton.className = 'chat-reset-btn';
    resetButton.innerHTML = '🔄 New Conversation';
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
        console.log("Reset button clicked");
        resetConversation();
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
    console.log("Reset button added");
}

function resetConversation() {
    console.log("Resetting conversation...");
    const chatMessages = document.getElementById('chatMessages');
    const recommendationsContainer = document.getElementById('recommendations');
    
    if (!chatMessages) {
        console.error("Cannot reset conversation: chat messages container not found");
        return;
    }
    
    // Clear chat messages except welcome message
    const welcomeMessage = chatMessages.querySelector('.bot-message');
    chatMessages.innerHTML = '';
    if (welcomeMessage) {
        chatMessages.appendChild(welcomeMessage);
    } else {
        // If welcome message was removed, add a new one
        const newWelcome = document.createElement('div');
        newWelcome.className = 'bot-message';
        newWelcome.innerHTML = '<p>Hello! I can help you find the perfect gift. What occasion are you shopping for?</p>';
        chatMessages.appendChild(newWelcome);
    }
    
    // Clear recommendations
    if (recommendationsContainer) {
        recommendationsContainer.style.display = 'none';
        recommendationsContainer.innerHTML = '';
    }
    
    // Reset chatbot state
    window.chatbotState.conversationStarted = false;
    window.chatbotState.isTyping = false;
    
    // Call API to reset server-side context
    fetch('/api/chatbot/reset', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    }).then(response => response.json())
      .then(data => {
          console.log('Conversation reset:', data);
          // Re-add suggestions
          setTimeout(() => {
              addInputSuggestions();
          }, 100);
      })
      .catch(error => {
          console.error("Error resetting conversation:", error);
          showNotification("Error resetting conversation", "error");
      });
    
    // Re-add reset button
    addResetButton();
    console.log("Conversation reset complete");
}

function sendChatMessage() {
    console.log("sendChatMessage called");
    const chatInput = document.getElementById('chatInput');
    const message = chatInput.value.trim();
    
    console.log(`Message: "${message}", isTyping: ${window.chatbotState.isTyping}`);
    
    if (message === '' || window.chatbotState.isTyping) {
        console.log("Empty message or already typing, returning");
        return;
    }
    
    // Remove suggestions after first message
    if (!window.chatbotState.conversationStarted) {
        const suggestions = document.querySelector('.chat-suggestions');
        if (suggestions) {
            console.log("Removing suggestions");
            suggestions.remove();
        }
        window.chatbotState.conversationStarted = true;
    }
    
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
    console.log("Sending request to /api/chatbot");
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
        console.log(`Response status: ${response.status}`);
        
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log("Response received:", data);
        
        // Remove typing indicator
        removeTypingIndicator();
        window.chatbotState.isTyping = false;
        
        // Add bot response with delay for natural feel
        setTimeout(() => {
            addBotMessage(data.response);
            
            // Show recommendations if any
            if (data.recommendations && data.recommendations.length > 0) {
                console.log(`Showing ${data.recommendations.length} recommendations`);
                setTimeout(() => {
                    showRecommendations(data.recommendations);
                }, 500);
            } else {
                console.log("No recommendations to show");
            }
        }, 500);
    })
    .catch(error => {
        clearTimeout(timeoutId);
        console.error('Error sending message:', error);
        removeTypingIndicator();
        window.chatbotState.isTyping = false;
        
        addBotMessage('Sorry, I couldn\'t process your request at the moment. Please try again.');
        showNotification('Gift advisor service unavailable. Please try again later.', 'error', 6000);
    });
}

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
        `;
        
        // Add CSS for typing animation if not exists
        if (!document.getElementById('typing-style')) {
            const dotsStyle = document.createElement('style');
            dotsStyle.id = 'typing-style';
            dotsStyle.textContent = `
                .typing-dots {
                    display: inline-flex;
                    align-items: center;
                    gap: 4px;
                }
                .typing-dots span {
                    width: 8px;
                    height: 8px;
                    background: #666;
                    border-radius: 50%;
                    animation: typing 1.4s infinite;
                }
                .typing-dots span:nth-child(2) {
                    animation-delay: 0.2s;
                }
                .typing-dots span:nth-child(3) {
                    animation-delay: 0.4s;
                }
                @keyframes typing {
                    0%, 60%, 100% {
                        transform: translateY(0);
                        opacity: 0.4;
                    }
                    30% {
                        transform: translateY(-10px);
                        opacity: 1;
                    }
                }
            `;
            document.head.appendChild(dotsStyle);
        }
        
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

// Enhanced recommendation display
function showRecommendations(recommendations) {
    console.log("Showing recommendations");
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
    
    // Add header
    const header = document.createElement('h3');
    header.textContent = 'Recommended for you';
    header.style.cssText = `
        margin: 0 0 15px 0;
        color: #4a89dc;
        font-size: 1.1em;
        display: flex;
        align-items: center;
        gap: 8px;
    `;
    
    // Add icon to header
    header.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#4a89dc" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg> Recommended Just For You';
    
    container.appendChild(header);
    
    // Create recommendations grid
    const recommendationsGrid = document.createElement('div');
    recommendationsGrid.className = 'recommendations-grid';
    recommendationsGrid.style.cssText = `
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 20px;
        margin-top: 15px;
    `;
    
    // Add slideUp animation CSS if not exists
    if (!document.getElementById('slide-animation')) {
        const slideStyle = document.createElement('style');
        slideStyle.id = 'slide-animation';
        slideStyle.textContent = `
            @keyframes slideUp {
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            .recommendation-item:hover {
                transform: translateY(-8px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);
                border-color: #4a89dc;
            }
            .add-to-cart-rec:hover {
                background: linear-gradient(135deg, #37b54a 0%, #28a745 100%);
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(76, 217, 100, 0.4);
            }
            .relevance-tag {
                display: inline-block;
                padding: 3px 8px;
                border-radius: 12px;
                font-size: 0.7em;
                font-weight: 600;
                margin-right: 5px;
                margin-bottom: 5px;
                background: #f0f5ff;
                color: #4a89dc;
                border: 1px solid #d0e0ff;
            }
            .relevance-tags {
                display: flex;
                flex-wrap: wrap;
                gap: 5px;
                margin-top: 8px;
                margin-bottom: 8px;
            }
        `;
        document.head.appendChild(slideStyle);
    }
    
    // Add each recommendation
    recommendations.forEach((item, index) => {
        console.log(`Building recommendation ${index+1}: ${item.name}`);
        
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
        
        // Start building HTML content
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
        
        // Add relevance tags if available
        if (item.relevance_scores && Object.keys(item.relevance_scores).length > 0) {
            itemHTML += `<div class="relevance-tags">`;
            
            for (const [key, value] of Object.entries(item.relevance_scores)) {
                itemHTML += `<span class="relevance-tag">${value}</span>`;
            }
            
            itemHTML += `</div>`;
        }
        
        // Add description and button
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
    
    // Add event listeners to the new buttons
    const addButtons = container.querySelectorAll('.add-to-cart-rec');
    addButtons.forEach(button => {
        button.addEventListener('click', function() {
            const itemId = parseInt(this.dataset.id);
            const itemType = this.dataset.type;
            
            console.log(`Add to cart clicked: ${itemType} #${itemId}`);
            
            // Change button state
            const originalText = this.innerHTML;
            this.innerHTML = `
                <svg class="spinner" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="animation: spin 1s linear infinite;">
                    <circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-dashoffset="16"></circle>
                </svg>
                Adding...
            `;
            this.disabled = true;
            
            // Add style for the spinner
            if (!document.getElementById('spinner-style')) {
                const spinnerStyle = document.createElement('style');
                spinnerStyle.id = 'spinner-style';
                spinnerStyle.textContent = `
                    @keyframes spin {
                        0% { transform: rotate(0deg); }
                        100% { transform: rotate(360deg); }
                    }
                `;
                document.head.appendChild(spinnerStyle);
            }
            
            addToCart(itemId, itemType).then(() => {
                this.innerHTML = `
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
    
    console.log("Recommendations displayed successfully");
}

// Filter Functions
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

// Cart API Functions
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

// Helper Functions
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