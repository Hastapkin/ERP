// Enhanced chatbot functionality with improved UI and message formatting
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM loaded, initializing Enhanced Chatbot with Improved UI...");
    
    window.chatbotState = {
        isTyping: false,
        conversationStarted: false,
        collectedInfo: {
            age: null,
            gender: null,
            category: null,
            budget: null
        },
        progressSteps: ['age', 'gender', 'interests', 'budget', 'confirm']
    };

    initializeCartFunctionality();
    initializeEnhancedChatbot();
    initializeFilters();
    
    console.log("Enhanced Chatbot with Improved UI initialized");
});

function initializeEnhancedChatbot() {
    console.log("Initializing Enhanced chatbot...");
    
    const chatInput = document.getElementById('chatInput');
    const sendButton = document.getElementById('sendButton');
    const chatMessages = document.getElementById('chatMessages');
    
    if (!chatInput || !sendButton || !chatMessages) {
        console.error("Chatbot elements missing!");
        return;
    }
    
    sendButton.addEventListener('click', () => sendChatMessage());
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendChatMessage();
        }
    });
    
    addResetButton();
    initializeImprovedProgressIndicator();
    console.log("Enhanced chatbot initialized");
}

function initializeImprovedProgressIndicator() {
    console.log("Initializing improved progress indicator...");
    
    // Create progress indicator if it doesn't exist
    let progressContainer = document.getElementById('progress-indicator');
    if (!progressContainer) {
        progressContainer = document.createElement('div');
        progressContainer.id = 'progress-indicator';
        progressContainer.className = 'progress-indicator';
        
        // Insert after chatbot title
        const chatbotSection = document.querySelector('.chatbot-section h2');
        if (chatbotSection) {
            chatbotSection.insertAdjacentElement('afterend', progressContainer);
        }
    }
    
    // Create improved progress steps
    progressContainer.innerHTML = `
        <div class="how-it-works-improved">
            <div class="progress-header">
                <span class="progress-icon">📋</span>
                <span class="progress-title">How It Works</span>
            </div>
            <div class="progress-steps-improved">
                <div class="progress-step-improved" data-step="age">
                    <div class="step-circle">
                        <span class="step-number">1</span>
                        <div class="step-checkmark">✓</div>
                    </div>
                    <div class="step-content">
                        <div class="step-label">Age</div>
                        <div class="step-desc">3-12 years old</div>
                    </div>
                </div>
                
                <div class="progress-connector"></div>
                
                <div class="progress-step-improved" data-step="gender">
                    <div class="step-circle">
                        <span class="step-number">2</span>
                        <div class="step-checkmark">✓</div>
                    </div>
                    <div class="step-content">
                        <div class="step-label">Gender</div>
                        <div class="step-desc">Boy or Girl</div>
                    </div>
                </div>
                
                <div class="progress-connector"></div>
                
                <div class="progress-step-improved" data-step="interests">
                    <div class="step-circle">
                        <span class="step-number">3</span>
                        <div class="step-checkmark">✓</div>
                    </div>
                    <div class="step-content">
                        <div class="step-label">Interests</div>
                        <div class="step-desc">What they love</div>
                    </div>
                </div>
                
                <div class="progress-connector"></div>
                
                <div class="progress-step-improved" data-step="budget">
                    <div class="step-circle">
                        <span class="step-number">4</span>
                        <div class="step-checkmark">✓</div>
                    </div>
                    <div class="step-content">
                        <div class="step-label">Budget</div>
                        <div class="step-desc">Your price range</div>
                    </div>
                </div>
                
                <div class="progress-connector"></div>
                
                <div class="progress-step-improved" data-step="confirm">
                    <div class="step-circle">
                        <span class="step-number">✓</span>
                        <div class="step-checkmark">✓</div>
                    </div>
                    <div class="step-content">
                        <div class="step-label">Recommendations</div>
                        <div class="step-desc">Perfect matches</div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Add improved CSS styles
    addImprovedProgressStyles();
}

function addImprovedProgressStyles() {
    // Check if styles already added
    if (document.getElementById('improved-progress-styles')) return;
    
    const style = document.createElement('style');
    style.id = 'improved-progress-styles';
    style.textContent = `
        .progress-indicator {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            border-radius: 16px;
            padding: 24px;
            margin: 20px 0;
            border: 1px solid rgba(74, 137, 220, 0.15);
            box-shadow: 0 4px 20px rgba(74, 137, 220, 0.08);
        }
        
        .how-it-works-improved {
            width: 100%;
        }
        
        .progress-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid rgba(74, 137, 220, 0.1);
        }
        
        .progress-icon {
            font-size: 1.2em;
        }
        
        .progress-title {
            color: #4a89dc;
            font-size: 1.1em;
            font-weight: 600;
        }
        
        .progress-steps-improved {
            display: flex;
            align-items: center;
            justify-content: space-between;
            width: 100%;
            position: relative;
        }
        
        .progress-step-improved {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            position: relative;
            z-index: 2;
            background: white;
            padding: 8px;
            border-radius: 12px;
            transition: all 0.3s ease;
            min-width: 80px;
        }
        
        .step-circle {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: #e9ecef;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 12px;
            position: relative;
            transition: all 0.3s ease;
            border: 3px solid transparent;
        }
        
        .step-number {
            font-size: 1.1em;
            font-weight: 700;
            color: #6c757d;
            transition: all 0.3s ease;
        }
        
        .step-checkmark {
            position: absolute;
            font-size: 1.4em;
            color: white;
            opacity: 0;
            transform: scale(0);
            transition: all 0.3s ease;
        }
        
        .step-content {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        
        .step-label {
            font-size: 0.9em;
            font-weight: 600;
            color: #495057;
            transition: color 0.3s ease;
        }
        
        .step-desc {
            font-size: 0.75em;
            color: #6c757d;
            line-height: 1.3;
        }
        
        .progress-connector {
            flex: 1;
            height: 3px;
            background: linear-gradient(90deg, #e9ecef 0%, #dee2e6 100%);
            margin: 0 -8px;
            border-radius: 2px;
            position: relative;
            z-index: 1;
            transition: all 0.3s ease;
        }
        
        /* Current step styles */
        .progress-step-improved.current .step-circle {
            background: #4a89dc;
            border-color: rgba(74, 137, 220, 0.3);
            box-shadow: 0 0 0 4px rgba(74, 137, 220, 0.15);
            animation: pulse-current 2s infinite;
        }
        
        .progress-step-improved.current .step-number {
            color: white;
        }
        
        .progress-step-improved.current .step-label {
            color: #4a89dc;
            font-weight: 700;
        }
        
        /* Completed step styles */
        .progress-step-improved.completed .step-circle {
            background: #28a745;
            border-color: rgba(40, 167, 69, 0.3);
        }
        
        .progress-step-improved.completed .step-number {
            opacity: 0;
            transform: scale(0);
        }
        
        .progress-step-improved.completed .step-checkmark {
            opacity: 1;
            transform: scale(1);
        }
        
        .progress-step-improved.completed .step-label {
            color: #28a745;
        }
        
        .progress-step-improved.completed + .progress-connector {
            background: linear-gradient(90deg, #28a745 0%, #20c997 100%);
        }
        
        /* Final completed step styles */
        .progress-step-improved.final-completed .step-circle {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            border-color: rgba(40, 167, 69, 0.4);
            box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
        }
        
        .progress-step-improved.final-completed .step-label {
            color: #28a745;
            font-weight: 700;
        }
        
        @keyframes pulse-current {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .progress-steps-improved {
                flex-direction: column;
                gap: 16px;
            }
            
            .progress-connector {
                height: 40px;
                width: 3px;
                margin: -8px 0;
            }
            
            .progress-step-improved {
                flex-direction: row;
                text-align: left;
                width: 100%;
                max-width: 280px;
                padding: 12px;
                background: rgba(255, 255, 255, 0.8);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(74, 137, 220, 0.1);
            }
            
            .step-circle {
                margin-bottom: 0;
                margin-right: 16px;
                flex-shrink: 0;
            }
            
            .step-content {
                text-align: left;
            }
        }
        
        /* Enhanced chatbot message styles */
        .bot-message {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            border: 1px solid rgba(74, 137, 220, 0.1);
            border-radius: 20px 20px 20px 6px;
            padding: 20px;
            margin: 16px 0;
            box-shadow: 0 4px 15px rgba(74, 137, 220, 0.08);
            position: relative;
        }
        
        .bot-message::before {
            content: '🤖';
            position: absolute;
            top: 12px;
            left: 12px;
            font-size: 1.2em;
            opacity: 0.7;
        }
        
        .bot-message p {
            margin: 0 0 12px 32px;
            line-height: 1.6;
            color: #495057;
        }
        
        .bot-message p:last-child {
            margin-bottom: 0;
        }
        
        .bot-message .message-highlight {
            background: linear-gradient(135deg, rgba(74, 137, 220, 0.1) 0%, rgba(74, 137, 220, 0.05) 100%);
            padding: 8px 12px;
            border-radius: 8px;
            border-left: 3px solid #4a89dc;
            margin: 12px 0;
        }
        
        .user-message {
            background: linear-gradient(135deg, #4a89dc 0%, #5b9be0 100%);
            border-radius: 20px 20px 6px 20px;
            padding: 16px 20px;
            margin: 16px 0;
            box-shadow: 0 4px 15px rgba(74, 137, 220, 0.25);
            position: relative;
        }
        
        .user-message p {
            margin: 0;
            color: white;
            font-weight: 500;
        }
    `;
    
    document.head.appendChild(style);
}

function updateProgressIndicator(extractedInfo, recommendations) {
    console.log("Updating improved progress indicator:", extractedInfo, "Has recommendations:", recommendations && recommendations.length > 0);
    
    const steps = document.querySelectorAll('.progress-step-improved');
    
    // Map extracted info to progress steps
    const infoMapping = {
        'age': extractedInfo?.age,
        'gender': extractedInfo?.gender,
        'interests': extractedInfo?.category,  // category maps to interests
        'budget': extractedInfo?.budget
    };
    
    // Update chatbot state
    if (extractedInfo) {
        window.chatbotState.collectedInfo = {
            age: extractedInfo.age,
            gender: extractedInfo.gender,
            category: extractedInfo.category,
            budget: extractedInfo.budget
        };
    }
    
    // Update each step
    steps.forEach(step => {
        const stepType = step.dataset.step;
        
        // Remove all status classes
        step.classList.remove('current', 'completed', 'final-completed');
        
        if (stepType === 'confirm') {
            // Final step - completed only if we have recommendations
            if (recommendations && recommendations.length > 0) {
                step.classList.add('final-completed');
                console.log("✅ Final step completed - recommendations available");
            }
        } else {
            // Regular steps
            const hasInfo = infoMapping[stepType] !== null && infoMapping[stepType] !== undefined;
            
            if (hasInfo) {
                step.classList.add('completed');
                console.log(`✅ Step ${stepType} completed:`, infoMapping[stepType]);
            }
        }
    });
    
    // Set current step (first incomplete step)
    const incompleteStep = Array.from(steps).find(step => {
        const stepType = step.dataset.step;
        if (stepType === 'confirm') {
            return !(recommendations && recommendations.length > 0);
        }
        return !infoMapping[stepType];
    });
    
    if (incompleteStep && !incompleteStep.classList.contains('completed') && !incompleteStep.classList.contains('final-completed')) {
        incompleteStep.classList.add('current');
        console.log(`→ Current step: ${incompleteStep.dataset.step}`);
    }
}

function formatBotMessage(message) {
    "Format bot message to clean up markdown and improve readability"
    
    // Remove excessive asterisks and clean up formatting
    let formattedMessage = message
        // Remove double asterisks (bold markdown)
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        // Remove single asterisks (italic markdown) 
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        // Clean up any remaining asterisks
        .replace(/\*/g, '')
        // Convert numbered lists to proper formatting
        .replace(/(\d+\.\s)/g, '<br>$1')
        // Convert bullet points
        .replace(/^•\s/gm, '<br>• ')
        // Clean up multiple line breaks
        .replace(/\n{3,}/g, '\n\n')
        // Convert line breaks to proper spacing
        .replace(/\n/g, '<br>')
        // Clean up extra spaces
        .replace(/\s{2,}/g, ' ')
        // Fix spacing around HTML tags
        .replace(/<br>\s*<br>/g, '<br>')
        .replace(/^<br>/, '');
    
    return formattedMessage;
}

function sendChatMessage() {
    const chatInput = document.getElementById('chatInput');
    const message = chatInput.value.trim();
    
    if (message === '' || window.chatbotState.isTyping) return;
    
    // Hide suggestions after first message
    if (!window.chatbotState.conversationStarted) {
        const suggestions = document.querySelector('#chatSuggestions');
        if (suggestions) suggestions.style.display = 'none';
        window.chatbotState.conversationStarted = true;
    }
    
    addUserMessage(message);
    chatInput.value = '';
    addTypingIndicator();
    window.chatbotState.isTyping = true;
    
    fetch('/api/chatbot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: message })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Chatbot response:", data);
        removeTypingIndicator();
        window.chatbotState.isTyping = false;
        
        setTimeout(() => {
            addBotMessage(data.response);
            
            // Update progress indicator with extracted info and recommendations
            updateProgressIndicator(data.extracted_info, data.recommendations);
            
            if (data.recommendations && data.recommendations.length > 0) {
                setTimeout(() => showRecommendations(data.recommendations), 500);
            } else {
                const recContainer = document.getElementById('recommendations');
                if (recContainer) recContainer.style.display = 'none';
            }
        }, 500);
    })
    .catch(error => {
        console.error('Error:', error);
        removeTypingIndicator();
        window.chatbotState.isTyping = false;
        addBotMessage('Sorry, I encountered an error. Please try again.');
    });
}

function resetConversation() {
    console.log("Resetting conversation...");
    const chatMessages = document.getElementById('chatMessages');
    const recContainer = document.getElementById('recommendations');
    const suggestions = document.getElementById('chatSuggestions');
    
    // Reset chatbot state
    window.chatbotState = {
        isTyping: false,
        conversationStarted: false,
        collectedInfo: {
            age: null,
            gender: null,
            category: null,
            budget: null
        },
        progressSteps: ['age', 'gender', 'interests', 'budget', 'confirm']
    };
    
    chatMessages.innerHTML = `
        <div class="bot-message">
            <p><strong>Hello! I'm your Gift Guru!</strong></p>
            <p>I'll help you find the perfect gift based on 4 key factors:</p>
            <div class="message-highlight">
                <p><strong>Age:</strong> 3-12 years (our specialty!)<br>
                <strong>Gender:</strong> Boy or Girl<br>
                <strong>Interests:</strong> What they love<br>
                <strong>Budget:</strong> Your price range</p>
            </div>
            <p><strong>Let's start: What's the age of the gift recipient?</strong></p>
        </div>
    `;
    
    if (recContainer) recContainer.style.display = 'none';
    if (suggestions) suggestions.style.display = 'block';
    
    // Reset progress indicator
    const steps = document.querySelectorAll('.progress-step-improved');
    steps.forEach(step => {
        step.classList.remove('current', 'completed', 'final-completed');
    });
    
    // Set first step as current
    const firstStep = document.querySelector('.progress-step-improved[data-step="age"]');
    if (firstStep) {
        firstStep.classList.add('current');
    }
    
    fetch('/api/chatbot/reset', { method: 'POST' })
        .then(response => response.json())
        .then(data => console.log('Reset:', data))
        .catch(error => console.error("Reset error:", error));
    
    addResetButton();
}

function addResetButton() {
    const chatMessages = document.getElementById('chatMessages');
    if (!chatMessages) return;
    
    const resetButton = document.createElement('button');
    resetButton.innerHTML = '🔄 Start Over';
    resetButton.style.cssText = `
        position: absolute; top: 12px; right: 12px;
        padding: 8px 14px; background: rgba(108, 117, 125, 0.9);
        color: white; border: none; border-radius: 20px; 
        font-size: 0.8em; font-weight: 500; cursor: pointer; 
        z-index: 10; backdrop-filter: blur(10px);
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
    `;
    
    resetButton.addEventListener('click', resetConversation);
    resetButton.addEventListener('mouseenter', function() {
        this.style.background = 'rgba(90, 98, 104, 0.9)';
        this.style.transform = 'scale(1.05)';
    });
    resetButton.addEventListener('mouseleave', function() {
        this.style.background = 'rgba(108, 117, 125, 0.9)';
        this.style.transform = 'scale(1)';
    });
    
    chatMessages.style.position = 'relative';
    chatMessages.appendChild(resetButton);
}

function addTypingIndicator() {
    const chatMessages = document.getElementById('chatMessages');
    const typingElement = document.createElement('div');
    typingElement.className = 'bot-message typing-indicator';
    typingElement.innerHTML = `
        <div style="display: flex; align-items: center; gap: 12px; margin-left: 32px;">
            <div class="typing-dots">
                <span></span><span></span><span></span>
            </div>
            <p style="margin: 0; color: #6c757d; font-style: italic;">Gift Advisor is thinking...</p>
        </div>
    `;
    chatMessages.appendChild(typingElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTypingIndicator() {
    const typingIndicator = document.querySelector('.typing-indicator');
    if (typingIndicator) typingIndicator.remove();
}

function addUserMessage(message) {
    const chatMessages = document.getElementById('chatMessages');
    const messageElement = document.createElement('div');
    messageElement.className = 'user-message';
    messageElement.innerHTML = `<p>${escapeHtml(message)}</p>`;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addBotMessage(message) {
    const chatMessages = document.getElementById('chatMessages');
    const messageElement = document.createElement('div');
    messageElement.className = 'bot-message';
    
    // Format the message to clean up markdown
    const formattedMessage = formatBotMessage(message);
    messageElement.innerHTML = `<div style="margin-left: 32px;">${formattedMessage}</div>`;
    
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Keep existing cart functionality and other functions...
function initializeCartFunctionality() {
    console.log("Initializing cart functionality...");
    
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productCard = this.closest('.product-card');
            const productId = parseInt(productCard.dataset.id);
            const productType = productCard.dataset.type;
            addToCart(productId, productType);
        });
    });
    
    // Cart page controls (existing code)
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
}

function initializeFilters() {
    const categoryLinks = document.querySelectorAll('.category-link');
    categoryLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const category = this.dataset.category;
            window.location.href = `/products?category=${category}`;
        });
    });
}

function addToCart(productId, productType) {
    return fetch('/api/cart/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: productId, type: productType, quantity: 1 }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateCartCount(data.cart_count);
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

function showRecommendations(recommendations) {
    console.log("Showing recommendations");
    const container = document.getElementById('recommendations');
    
    if (!container || !recommendations || recommendations.length === 0) {
        if (container) container.style.display = 'none';
        return;
    }
    
    container.innerHTML = '';
    
    const header = document.createElement('h3');
    header.innerHTML = '🎯 Perfect Matches Found!';
    header.style.cssText = `
        margin: 0 0 20px 0; 
        color: #28a745; 
        font-size: 1.3em; 
        font-weight: 700;
        text-align: center;
        padding: 16px;
        background: linear-gradient(135deg, rgba(40, 167, 69, 0.1) 0%, rgba(40, 167, 69, 0.05) 100%);
        border-radius: 12px;
        border: 1px solid rgba(40, 167, 69, 0.2);
    `;
    container.appendChild(header);
    
    const grid = document.createElement('div');
    grid.style.cssText = 'display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px;';
    
    recommendations.forEach((item, index) => {
        const element = document.createElement('div');
        element.style.cssText = `
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            border: 1px solid rgba(74, 137, 220, 0.15);
            border-radius: 16px;
            overflow: hidden; 
            box-shadow: 0 8px 32px rgba(74, 137, 220, 0.12);
            transition: all 0.3s ease;
            animation: slideInUp 0.6s ease-out forwards;
            animation-delay: ${index * 0.1}s;
            opacity: 0;
            transform: translateY(20px);
        `;
        
        element.innerHTML = `
            <div style="position: relative; overflow: hidden;">
                <img src="/static/images/products/${item.image}" alt="${item.name}" 
                     style="width: 100%; height: 200px; object-fit: cover; transition: transform 0.3s ease;"
                     onerror="this.src='/static/images/products/placeholder.jpg'">
                <div style="position: absolute; top: 16px; right: 16px; 
                     background: ${item.type === 'combo' ? 'linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%)' : 'linear-gradient(135deg, #4a89dc 0%, #3742fa 100%)'}; 
                     color: white; padding: 6px 14px; border-radius: 20px; font-size: 0.8em;
                     font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;
                     box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                    ${item.type === 'combo' ? 'COMBO' : 'PRODUCT'}
                </div>
            </div>
            <div style="padding: 24px;">
                <h4 style="margin: 0 0 12px 0; font-size: 1.2em; color: #2c3e50; font-weight: 600; line-height: 1.3;">
                    ${item.name}
                </h4>
                <div style="display: flex; justify-content: space-between; align-items: center; margin: 12px 0;">
                    <span style="color: #e74c3c; font-weight: 700; font-size: 1.4em;">
                        ${item.price.toFixed(2)}
                    </span>
                    <div style="background: rgba(40, 167, 69, 0.1); padding: 4px 10px; border-radius: 12px; font-size: 0.8em; color: #27ae60; font-weight: 600;">
                        Score: ${item.relevance_scores.match_score || 'N/A'}
                    </div>
                </div>
                <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 12px; border-radius: 12px; margin: 16px 0; border-left: 4px solid #4a89dc;">
                    <div style="font-size: 0.85em; color: #495057; font-weight: 500;">
                        ✨ ${item.relevance_scores.reason || 'Recommended for you'}
                    </div>
                </div>
                <p style="color: #6c757d; font-size: 0.9em; margin: 16px 0; line-height: 1.5;">
                    ${item.description}
                </p>
                <button class="add-to-cart-rec" data-id="${item.id}" data-type="${item.type}"
                        style="width: 100%; padding: 14px; 
                               background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
                               color: white; border: none; border-radius: 12px; 
                               font-weight: 600; cursor: pointer; font-size: 0.95em;
                               transition: all 0.3s ease; display: flex; justify-content: center; 
                               align-items: center; gap: 10px;
                               box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);">
                    <span style="font-size: 1.1em;">🛒</span>
                    Add to Cart
                </button>
            </div>
        `;
        
        // Add hover effects
        element.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
            this.style.boxShadow = '0 12px 40px rgba(74, 137, 220, 0.18)';
            const img = this.querySelector('img');
            img.style.transform = 'scale(1.05)';
        });
        
        element.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 8px 32px rgba(74, 137, 220, 0.12)';
            const img = this.querySelector('img');
            img.style.transform = 'scale(1)';
        });
        
        grid.appendChild(element);
    });
    
    container.appendChild(grid);
    
    // Add keyframe animation
    if (!document.getElementById('slideInUp-keyframes')) {
        const keyframes = document.createElement('style');
        keyframes.id = 'slideInUp-keyframes';
        keyframes.textContent = `
            @keyframes slideInUp {
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
        `;
        document.head.appendChild(keyframes);
    }
    
    // Add event listeners to add-to-cart buttons
    const addButtons = container.querySelectorAll('.add-to-cart-rec');
    addButtons.forEach(button => {
        button.addEventListener('click', function() {
            const itemId = parseInt(this.dataset.id);
            const itemType = this.dataset.type;
            
            const originalText = this.innerHTML;
            this.innerHTML = '<span style="font-size: 1.1em;">⏳</span> Adding...';
            this.disabled = true;
            this.style.background = 'linear-gradient(135deg, #6c757d 0%, #495057 100%)';
            
            addToCart(itemId, itemType).then(() => {
                this.innerHTML = '<span style="font-size: 1.1em;">✅</span> Added to Cart!';
                this.style.background = 'linear-gradient(135deg, #20c997 0%, #17a2b8 100%)';
                
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.style.background = 'linear-gradient(135deg, #28a745 0%, #20c997 100%)';
                    this.disabled = false;
                }, 2500);
            }).catch(() => {
                this.innerHTML = '<span style="font-size: 1.1em;">❌</span> Error';
                this.style.background = 'linear-gradient(135deg, #dc3545 0%, #c82333 100%)';
                
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.style.background = 'linear-gradient(135deg, #28a745 0%, #20c997 100%)';
                    this.disabled = false;
                }, 2500);
            });
        });
        
        // Add button hover effects
        button.addEventListener('mouseenter', function() {
            if (!this.disabled) {
                this.style.background = 'linear-gradient(135deg, #20c997 0%, #17a2b8 100%)';
                this.style.transform = 'translateY(-2px)';
                this.style.boxShadow = '0 6px 20px rgba(40, 167, 69, 0.4)';
            }
        });
        
        button.addEventListener('mouseleave', function() {
            if (!this.disabled) {
                this.style.background = 'linear-gradient(135deg, #28a745 0%, #20c997 100%)';
                this.style.transform = 'translateY(0)';
                this.style.boxShadow = '0 4px 15px rgba(40, 167, 69, 0.3)';
            }
        });
    });
    
    container.style.display = 'block';
    container.style.background = 'linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%)';
    container.style.borderRadius = '20px';
    container.style.padding = '32px';
    container.style.marginTop = '24px';
    container.style.border = '1px solid rgba(74, 137, 220, 0.1)';
    container.style.boxShadow = '0 8px 32px rgba(74, 137, 220, 0.08)';
    
    setTimeout(() => {
        container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 400);
}

// Helper functions (keeping existing implementation)
function updateCartItem(cartItem, quantity) {
    const itemId = parseInt(cartItem.dataset.id);
    const itemType = cartItem.dataset.type;
    
    fetch('/api/cart/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: itemId, type: itemType, quantity: quantity }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const subtotalElement = cartItem.querySelector('.cart-item-subtotal p');
            const price = parseFloat(cartItem.querySelector('.price').textContent.replace(' , '));
            const subtotal = (price * quantity).toFixed(2);
            
            if (subtotalElement) {
                subtotalElement.textContent = `${subtotal}`;
            }
            
            updateCartTotals(data);
            updateCartCount(data.cart_count);
        }
    })
    .catch(error => {
        console.error('Error updating cart:', error);
        showNotification('Error updating cart', 'error');
    });
}

function removeFromCart(cartItem) {
    const itemId = parseInt(cartItem.dataset.id);
    const itemType = cartItem.dataset.type;
    
    fetch('/api/cart/remove', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: itemId, type: itemType }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            cartItem.remove();
            updateCartTotals(data);
            updateCartCount(data.cart_count);
            
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
    const cartCountElement = document.querySelector('.cart-count');
    if (cartCountElement) {
        cartCountElement.textContent = count;
        cartCountElement.style.transform = 'scale(1.3)';
        cartCountElement.style.transition = 'transform 0.3s ease';
        setTimeout(() => {
            cartCountElement.style.transform = 'scale(1)';
        }, 300);
    }
}

function updateCartTotals(data) {
    const subtotalElement = document.querySelector('.summary-row:nth-child(1) span:last-child');
    const shippingElement = document.querySelector('.summary-row:nth-child(2) span:last-child');
    const taxElement = document.querySelector('.summary-row:nth-child(3) span:last-child');
    const totalElement = document.querySelector('.summary-row.total span:last-child');
    
    if (subtotalElement && data.cart_subtotal !== undefined) {
        subtotalElement.textContent = `${data.cart_subtotal.toFixed(2)}`;
    }
    if (shippingElement && data.shipping !== undefined) {
        shippingElement.textContent = `${data.shipping.toFixed(2)}`;
    }
    if (taxElement && data.tax !== undefined) {
        taxElement.textContent = `${data.tax.toFixed(2)}`;
    }
    if (totalElement && data.total !== undefined) {
        totalElement.textContent = `${data.total.toFixed(2)}`;
    }
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showNotification(message, type = 'success', duration = 4000) {
    let notificationContainer = document.getElementById('notification-container');
    
    if (!notificationContainer) {
        notificationContainer = document.createElement('div');
        notificationContainer.id = 'notification-container';
        notificationContainer.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 1000;';
        document.body.appendChild(notificationContainer);
    }
    
    const notification = document.createElement('div');
    const backgroundColor = type === 'success' ? 
        'linear-gradient(135deg, #28a745 0%, #20c997 100%)' : 
        'linear-gradient(135deg, #dc3545 0%, #c82333 100%)';
    
    notification.style.cssText = `
        background: ${backgroundColor}; 
        color: white; padding: 14px 20px;
        border-radius: 12px; margin-bottom: 12px; 
        box-shadow: 0 8px 32px rgba(0,0,0,0.15);
        transition: all 0.4s ease; transform: translateX(100%); 
        opacity: 0; backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    `;
    notification.innerHTML = `
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 1.2em;">${type === 'success' ? '✅' : '❌'}</span>
            <span style="font-weight: 500;">${message}</span>
        </div>
    `;
    
    notificationContainer.appendChild(notification);
    
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
        notification.style.opacity = '1';
    }, 10);
    
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        notification.style.opacity = '0';
        setTimeout(() => notification.remove(), 400);
    }, duration);
}