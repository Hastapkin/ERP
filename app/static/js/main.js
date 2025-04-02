document.addEventListener('DOMContentLoaded', function() {
    // Simulate chatbot functionality for the static site
    const chatInput = document.getElementById('chatInput');
    const sendButton = document.getElementById('sendButton');
    const chatMessages = document.getElementById('chatMessages');
    const recommendationsContainer = document.getElementById('recommendations');
    
    // Sample recommendations data
    const sampleRecommendations = {
        birthday: [
            { id: 1, type: 'product', name: 'Birthday Card', price: 4.99, image: 'birthday_card.jpg' },
            { id: 3, type: 'product', name: 'Teddy Bear', price: 14.99, image: 'teddy_bear.jpg' },
            { id: 1, type: 'combo', name: 'Birthday Special', price: 29.99, image: 'birthday_combo.jpg' }
        ],
        anniversary: [
            { id: 2, type: 'product', name: 'Chocolate Box', price: 19.99, image: 'chocolate_box.jpg' },
            { id: 4, type: 'product', name: 'Wine Bottle', price: 24.99, image: 'wine.jpg' },
            { id: 2, type: 'combo', name: 'Anniversary Delight', price: 39.99, image: 'anniversary_combo.jpg' }
        ],
        default: [
            { id: 2, type: 'product', name: 'Chocolate Box', price: 19.99, image: 'chocolate_box.jpg' },
            { id: 3, type: 'product', name: 'Teddy Bear', price: 14.99, image: 'teddy_bear.jpg' }
        ]
    };
    
    // Send message when button is clicked
    sendButton.addEventListener('click', sendMessage);
    
    // Send message when Enter key is pressed
    chatInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });
    
    function sendMessage() {
        const message = chatInput.value.trim();
        if (message === '') return;
        
        // Add user message to chat
        addMessageToChat('user', message);
        
        // Clear input field
        chatInput.value = '';
        
        // Show typing indicator
        const typingIndicator = document.createElement('div');
        typingIndicator.className = 'bot-message typing';
        typingIndicator.innerHTML = '<p>Thinking...</p>';
        chatMessages.appendChild(typingIndicator);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Simulate bot response after a delay
        setTimeout(() => {
            // Remove typing indicator
            chatMessages.removeChild(typingIndicator);
            
            // Generate bot response based on user message
            let botResponse;
            let recommendations;
            
            const messageLower = message.toLowerCase();
            
            if (messageLower.includes('birthday')) {
                botResponse = "For birthdays, I recommend our Birthday Special combo or our Teddy Bear - both are very popular birthday gifts!";
                recommendations = sampleRecommendations.birthday;
            } else if (messageLower.includes('anniversary') || messageLower.includes('wedding')) {
                botResponse = "For anniversaries, our chocolate boxes and wine make excellent gifts to celebrate the special occasion.";
                recommendations = sampleRecommendations.anniversary;
            } else if (messageLower.includes('child') || messageLower.includes('kid')) {
                botResponse = "For children, our Teddy Bear is a wonderful gift that brings joy and comfort.";
                recommendations = [sampleRecommendations.birthday[1]]; // Teddy bear
            } else {
                botResponse = "I'd be happy to help you find the perfect gift! What occasion are you shopping for, and who will receive the gift?";
                recommendations = sampleRecommendations.default;
            }
            
            // Add bot response to chat
            addMessageToChat('bot', botResponse);
            
            // Display recommendations
            showRecommendations(recommendations);
            
        }, 1000); // 1 second delay to simulate thinking
    }
    
    function addMessageToChat(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.className = sender === 'user' ? 'user-message' : 'bot-message';
        messageElement.innerHTML = `<p>${message}</p>`;
        chatMessages.appendChild(messageElement);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function showRecommendations(items) {
        recommendationsContainer.innerHTML = '';
        
        if (!items || items.length === 0) {
            return;
        }
        
        const heading = document.createElement('h3');
        heading.textContent = 'Recommended for you:';
        recommendationsContainer.appendChild(heading);
        
        // Create product recommendations
        items.forEach(item => {
            const element = document.createElement('div');
            element.className = 'recommendation-item';
            element.style.display = 'flex';
            element.style.alignItems = 'center';
            element.style.marginBottom = '1rem';
            element.style.padding = '0.5rem';
            element.style.borderBottom = '1px solid #eee';
            
            element.innerHTML = `
                <img src="static/images/products/${item.image}" alt="${item.name}" 
                     style="width: 60px; height: 60px; object-fit: cover; margin-right: 1rem; border-radius: 4px;">
                <div style="flex: 1;">
                    <h4 style="margin: 0 0 0.5rem 0;">${item.name}</h4>
                    <p style="margin: 0; color: #ff6b6b; font-weight: bold;">$${item.price}</p>
                </div>
                <button class="add-recommended" 
                        style="background-color: #4cd964; padding: 0.3rem 0.8rem; font-size: 0.8rem;">
                    Add to Cart
                </button>
            `;
            
            recommendationsContainer.appendChild(element);
        });
        
        // Add event listeners to the "Add to Cart" buttons
        const addButtons = recommendationsContainer.querySelectorAll('.add-recommended');
        addButtons.forEach(button => {
            button.addEventListener('click', function() {
                const cartCount = document.querySelector('.cart-count');
                cartCount.textContent = parseInt(cartCount.textContent) + 1;
                
                // Show alert
                alert('Item added to cart!');
            });
        });
    }
    
    // Add to cart functionality for product cards
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const cartCount = document.querySelector('.cart-count');
            cartCount.textContent = parseInt(cartCount.textContent) + 1;
            
            // Show alert
            alert('Item added to cart!');
        });
    });
    
    // Cart button
    const cartButton = document.getElementById('cartButton');
    cartButton.addEventListener('click', function() {
        alert('Cart functionality will be implemented in the next phase!');
    });
});