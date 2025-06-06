// Enhanced chatbot functionality with progress tracking
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM loaded, initializing Enhanced Chatbot with Progress Tracking...");
    
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
    
    console.log("Enhanced Chatbot with Progress Tracking initialized");
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
    initializeProgressIndicator();
    console.log("Enhanced chatbot initialized");
}

function initializeProgressIndicator() {
    console.log("Initializing progress indicator...");
    
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
    
    // Create progress steps
    progressContainer.innerHTML = `
        <div class="how-it-works">
            <h4>📋 How It Works:</h4>
            <div class="progress-steps">
                <div class="progress-step" data-step="age">
                    <div class="step-number">1</div>
                    <div class="step-info">
                        <div class="step-title">Age</div>
                        <div class="step-subtitle">3-12 years old</div>
                    </div>
                </div>
                <div class="progress-step" data-step="gender">
                    <div class="step-number">2</div>
                    <div class="step-info">
                        <div class="step-title">Gender</div>
                        <div class="step-subtitle">Boy or Girl</div>
                    </div>
                </div>
                <div class="progress-step" data-step="interests">
                    <div class="step-number">3</div>
                    <div class="step-info">
                        <div class="step-title">Interests</div>
                        <div class="step-subtitle">What they love</div>
                    </div>
                </div>
                <div class="progress-step" data-step="budget">
                    <div class="step-number">4</div>
                    <div class="step-info">
                        <div class="step-title">Budget</div>
                        <div class="step-subtitle">Your price range</div>
                    </div>
                </div>
                <div class="progress-step" data-step="confirm">
                    <div class="step-number">✓</div>
                    <div class="step-info">
                        <div class="step-title">Confirm</div>
                        <div class="step-subtitle">Get recommendations</div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Add CSS styles
    addProgressStyles();
}

function addProgressStyles() {
    // Check if styles already added
    if (document.getElementById('progress-styles')) return;
    
    const style = document.createElement('style');
    style.id = 'progress-styles';
    style.textContent = `
        .progress-indicator {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 15px;
            padding: 20px;
            margin: 15px 0;
            border: 2px solid #e6e6e6;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
        }
        
        .how-it-works h4 {
            margin: 0 0 15px 0;
            color: #4a89dc;
            font-size: 1em;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .progress-steps {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
        }
        
        .progress-step {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 10px;
            border-radius: 10px;
            transition: all 0.3s ease;
            min-width: 80px;
            position: relative;
        }
        
        .progress-step:not(:last-child)::after {
            content: '→';
            position: absolute;
            right: -15px;
            top: 50%;
            transform: translateY(-50%);
            color: #ccc;
            font-size: 1.2em;
            z-index: 1;
        }
        
        .step-number {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background: #ddd;
            color: #666;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 0.9em;
            margin-bottom: 8px;
            transition: all 0.3s ease;
        }
        
        .step-info {
            text-align: center;
        }
        
        .step-title {
            font-weight: 600;
            font-size: 0.85em;
            color: #333;
            margin-bottom: 2px;
        }
        
        .step-subtitle {
            font-size: 0.7em;
            color: #666;
            line-height: 1.2;
        }
        
        /* Current step */
        .progress-step.current {
            background: rgba(74, 137, 220, 0.1);
            border: 2px solid #4a89dc;
        }
        
        .progress-step.current .step-number {
            background: #4a89dc;
            color: white;
            animation: pulse 2s infinite;
        }
        
        .progress-step.current .step-title {
            color: #4a89dc;
            font-weight: 700;
        }
        
        /* Completed step */
        .progress-step.completed {
            background: rgba(76, 217, 100, 0.1);
        }
        
        .progress-step.completed .step-number {
            background: #4cd964;
            color: white;
        }
        
        .progress-step.completed .step-title {
            color: #4cd964;
        }
        
        /* Final confirmation step */
        .progress-step.final-completed {
            background: rgba(76, 217, 100, 0.15);
            border: 2px solid #4cd964;
        }
        
        .progress-step.final-completed .step-number {
            background: #4cd964;
            color: white;
            font-size: 1.1em;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .progress-steps {
                flex-direction: column;
                gap: 15px;
            }
            
            .progress-step:not(:last-child)::after {
                content: '↓';
                right: auto;
                bottom: -25px;
                top: auto;
                transform: none;
            }
        }
    `;
    
    document.head.appendChild(style);
}

function updateProgressIndicator(extractedInfo, recommendations) {
    console.log("Updating progress indicator:", extractedInfo, "Has recommendations:", recommendations && recommendations.length > 0);
    
    const steps = document.querySelectorAll('.progress-step');
    
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
            <p><strong>Hello! I'm your Gift Guru! 🎁</strong></p>
            <p>I'll help you find the perfect gift based on 4 key factors:</p>
            <p>👶 <strong>Age</strong> (3-12 years)<br>
               👦👧 <strong>Gender</strong> (male/female)<br>
               📱 <strong>Category</strong> preferences<br>
               💰 <strong>Budget</strong></p>
            <p><strong>Let's start: What's the age of the gift recipient?</strong></p>
        </div>
    `;
    
    if (recContainer) recContainer.style.display = 'none';
    if (suggestions) suggestions.style.display = 'block';
    
    // Reset progress indicator
    const steps = document.querySelectorAll('.progress-step');
    steps.forEach(step => {
        step.classList.remove('current', 'completed', 'final-completed');
    });
    
    // Set first step as current
    const firstStep = document.querySelector('.progress-step[data-step="age"]');
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
        position: absolute; top: 10px; right: 10px;
        padding: 5px 10px; background: #6c757d; color: white;
        border: none; border-radius: 15px; font-size: 0.8em;
        cursor: pointer; z-index: 10;
    `;
    
    resetButton.addEventListener('click', resetConversation);
    chatMessages.style.position = 'relative';
    chatMessages.appendChild(resetButton);
}

function addTypingIndicator() {
    const chatMessages = document.getElementById('chatMessages');
    const typingElement = document.createElement('div');
    typingElement.className = 'bot-message typing-indicator';
    typingElement.innerHTML = `
        <div class="typing-dots">
            <span></span><span></span><span></span>
        </div>
        <p style="margin-left: 10px; color: #666;">Gift Advisor is thinking...</p>
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
    messageElement.innerHTML = `<p>${escapeHtml(message)}</p>`;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
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
    header.style.cssText = 'margin: 0 0 15px 0; color: #4cd964; font-size: 1.2em; font-weight: 700;';
    container.appendChild(header);
    
    const grid = document.createElement('div');
    grid.style.cssText = 'display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px;';
    
    recommendations.forEach(item => {
        const element = document.createElement('div');
        element.style.cssText = `
            background: white; border: 1px solid #e6e6e6; border-radius: 12px;
            overflow: hidden; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
        `;
        
        element.innerHTML = `
            <div style="position: relative;">
                <img src="/static/images/products/${item.image}" alt="${item.name}" 
                     style="width: 100%; height: 180px; object-fit: cover;"
                     onerror="this.src='/static/images/products/placeholder.jpg'">
                <div style="position: absolute; top: 12px; right: 12px; 
                     background: ${item.type === 'combo' ? '#ff6b6b' : '#4cd964'}; 
                     color: white; padding: 4px 10px; border-radius: 20px; font-size: 0.8em;">
                    ${item.type === 'combo' ? 'COMBO' : 'PRODUCT'}
                </div>
            </div>
            <div style="padding: 15px;">
                <h4 style="margin: 0 0 8px 0; color: #333;">${item.name}</h4>
                <p style="color: #ff6b6b; font-weight: bold; margin: 8px 0; font-size: 1.2em;">
                    $${item.price.toFixed(2)}
                </p>
                <div style="background: #f8f9fa; padding: 8px; border-radius: 6px; margin: 10px 0;">
                    <small style="color: #666;">
                        Score: ${item.relevance_scores.match_score || 'N/A'}<br>
                        ${item.relevance_scores.reason || 'Recommended'}
                    </small>
                </div>
                <p style="color: #666; font-size: 0.9em; margin: 10px 0;">
                    ${item.description}
                </p>
                <button class="add-to-cart-rec" data-id="${item.id}" data-type="${item.type}"
                        style="width: 100%; padding: 12px; background: #4cd964; color: white; 
                               border: none; border-radius: 8px; font-weight: 600; cursor: pointer;">
                    Add to Cart
                </button>
            </div>
        `;
        
        grid.appendChild(element);
    });
    
    container.appendChild(grid);
    
    // Add event listeners to add-to-cart buttons
    const addButtons = container.querySelectorAll('.add-to-cart-rec');
    addButtons.forEach(button => {
        button.addEventListener('click', function() {
            const itemId = parseInt(this.dataset.id);
            const itemType = this.dataset.type;
            
            const originalText = this.innerHTML;
            this.innerHTML = 'Adding...';
            this.disabled = true;
            
            addToCart(itemId, itemType).then(() => {
                this.innerHTML = '✓ Added!';
                this.style.background = '#28a745';
                
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.style.background = '#4cd964';
                    this.disabled = false;
                }, 2000);
            }).catch(() => {
                this.innerHTML = 'Error';
                this.style.background = '#dc3545';
                
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.style.background = '#4cd964';
                    this.disabled = false;
                }, 2000);
            });
        });
    });
    
    container.style.display = 'block';
    setTimeout(() => {
        container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 300);
}

// Keep all existing cart functionality (initializeCartFunctionality, addToCart, etc.)
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
    
    // Cart page controls
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
            const price = parseFloat(cartItem.querySelector('.price').textContent.replace('$', ''));
            const subtotal = (price * quantity).toFixed(2);
            
            if (subtotalElement) {
                subtotalElement.textContent = `$${subtotal}`;
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
        cartCountElement.style.transform = 'scale(1.2)';
        setTimeout(() => {
            cartCountElement.style.transform = 'scale(1)';
        }, 200);
    }
}

function updateCartTotals(data) {
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
    let notificationContainer = document.getElementById('notification-container');
    
    if (!notificationContainer) {
        notificationContainer = document.createElement('div');
        notificationContainer.id = 'notification-container';
        notificationContainer.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 1000;';
        document.body.appendChild(notificationContainer);
    }
    
    const notification = document.createElement('div');
    const backgroundColor = type === 'success' ? '#4cd964' : '#dc3545';
    notification.style.cssText = `
        background-color: ${backgroundColor}; color: white; padding: 12px 20px;
        border-radius: 6px; margin-bottom: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transition: all 0.3s ease; transform: translateX(100%); opacity: 0;
    `;
    notification.innerHTML = `
        <div style="display: flex; align-items: center; gap: 8px;">
            <span>${message}</span>
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
        setTimeout(() => notification.remove(), 300);
    }, duration);
}