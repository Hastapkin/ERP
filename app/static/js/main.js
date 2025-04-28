// Cart functionality
document.addEventListener('DOMContentLoaded', function() {
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
    
    // Chatbot functionality
    const chatInput = document.getElementById('chatInput');
    const sendButton = document.getElementById('sendButton');
    const chatMessages = document.getElementById('chatMessages');
    const recommendationsContainer = document.getElementById('recommendations');
    
    if (sendButton && chatInput) {
        sendButton.addEventListener('click', function() {
            sendChatMessage();
        });
        
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendChatMessage();
            }
        });
    }
    
    // Filter functionality
    const categoryLinks = document.querySelectorAll('.category-link');
    categoryLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const category = this.dataset.category;
            window.location.href = `/products?category=${category}`;
        });
    });
});

// Cart API functions
function addToCart(productId, productType) {
    fetch('/api/cart/add', {
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
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update cart count
            updateCartCount(data.cart_count);
            
            // Show success message
            showNotification('Item added to cart');
        }
    })
    .catch(error => {
        console.error('Error adding to cart:', error);
    });
}

function updateCartItem(cartItem, quantity) {
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
    .then(response => response.json())
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
    });
}

function removeFromCart(cartItem) {
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
    .then(response => response.json())
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
                document.getElementById('cartItems').style.display = 'none';
                document.getElementById('cartSummary').style.display = 'none';
                document.getElementById('cartEmpty').style.display = 'block';
            }
        }
    })
    .catch(error => {
        console.error('Error removing cart item:', error);
    });
}

function updateCartCount(count) {
    const cartCountElement = document.querySelector('.cart-count');
    if (cartCountElement) {
        cartCountElement.textContent = count;
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

// Chatbot functions
function sendChatMessage() {
    const chatInput = document.getElementById('chatInput');
    const message = chatInput.value.trim();
    
    if (message === '') return;
    
    // Add user message to chat
    addUserMessage(message);
    
    // Clear input
    chatInput.value = '';
    
    // Send to API
    fetch('/api/chatbot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            query: message
        }),
    })
    .then(response => response.json())
    .then(data => {
        // Add bot response
        addBotMessage(data.response);
        
        // Show recommendations
        showRecommendations(data.recommendations);
    })
    .catch(error => {
        console.error('Error sending message:', error);
        addBotMessage('Sorry, I couldn\'t process your request at the moment.');
    });
}

function addUserMessage(message) {
    const chatMessages = document.getElementById('chatMessages');
    
    if (chatMessages) {
        const messageElement = document.createElement('div');
        messageElement.className = 'user-message';
        messageElement.innerHTML = `<p>${message}</p>`;
        
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

function addBotMessage(message) {
    const chatMessages = document.getElementById('chatMessages');
    
    if (chatMessages) {
        const messageElement = document.createElement('div');
        messageElement.className = 'bot-message';
        messageElement.innerHTML = `<p>${message}</p>`;
        
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

function showRecommendations(recommendations) {
    const container = document.getElementById('recommendations');
    
    if (container) {
        // Clear previous recommendations
        container.innerHTML = '';
        
        if (recommendations.length === 0) {
            container.style.display = 'none';
            return;
        }
        
        // Add each recommendation
        recommendations.forEach(item => {
            const element = document.createElement('div');
            element.className = 'recommendation-item';
            element.innerHTML = `
                <img src="/static/images/products/${item.image}" alt="${item.name}">
                <div class="recommendation-details">
                    <h4>${item.name}</h4>
                    <p class="price">$${item.price.toFixed(2)}</p>
                    <p>${item.description}</p>
                    <button class="add-to-cart-rec" data-id="${item.id}" data-type="${item.type}">Add to Cart</button>
                </div>
            `;
            
            container.appendChild(element);
        });
        
        // Add event listeners to the new buttons
        const addButtons = container.querySelectorAll('.add-to-cart-rec');
        addButtons.forEach(button => {
            button.addEventListener('click', function() {
                const itemId = parseInt(this.dataset.id);
                const itemType = this.dataset.type;
                
                addToCart(itemId, itemType);
            });
        });
        
        // Show recommendations
        container.style.display = 'block';
    }
}

// Helper functions
function showNotification(message) {
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
    notification.style.backgroundColor = '#4cd964';
    notification.style.color = 'white';
    notification.style.padding = '10px 20px';
    notification.style.borderRadius = '6px';
    notification.style.marginBottom = '10px';
    notification.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
    notification.style.transition = 'all 0.3s ease';
    notification.innerHTML = message;
    
    // Add to container
    notificationContainer.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}