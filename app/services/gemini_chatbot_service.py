import os
import json
import requests
from pathlib import Path

# Import required classes at the top
from app.services.context_analyzer import ContextAnalyzer
from app.services.advanced_recommender import AdvancedRecommender

class GeminiChatbotService:
    def __init__(self, api_key=None):
        try:
            # Gemini API configuration
            self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
            
            if not self.api_key:
                raise ValueError("Gemini API key is not set or empty")
            
            # Update these to match current Gemini API structure   
            self.base_url = "https://generativelanguage.googleapis.com"
            self.api_version = "v1"  # Changed from v1beta to v1
            self.model = "gemini-1.5-pro"  # Changed from gemini-pro to gemini-1.5-pro
                
            # Test the API key immediately
            self._test_api_key()
                
            # History for chat context
            self.conversation_history = {}
            
            # Product data will be loaded when needed
            self.products = []
            self.categories = []
            self.combos = []
            
            # Initialize the advanced components
            self.context_analyzer = ContextAnalyzer()
            self.recommender = AdvancedRecommender()
            
            # Load initial product data (wait to avoid circular imports)
            self._lazy_product_data_load = True
            
            print("✅ GeminiChatbotService initialized successfully")
        except Exception as e:
            print(f"❌ Error initializing GeminiChatbotService: {e}")
            # Re-raise to be caught by the outer try/except
            raise
            
    def _test_api_key(self):
        """Test if the API key is valid by making a simple request"""
        try:
            # Use the listModels endpoint to check API key validity
            test_url = f"{self.base_url}/{self.api_version}/models?key={self.api_key}"
            print(f"Testing API with URL: {test_url}")
            
            response = requests.get(test_url, timeout=5)
            
            if response.status_code != 200:
                print(f"❌ API key test failed with status {response.status_code}")
                print(f"Response: {response.text}")
                raise ValueError(f"Invalid API key (Status: {response.status_code})")
            
            # Check available models
            models = response.json().get('models', [])
            available_models = [model.get('name', '').split('/')[-1] for model in models]
            print(f"Available models: {available_models}")
            
            # Check if our model is available
            if self.model not in available_models:
                # Try to find an alternative model
                alternatives = ['gemini-1.0-pro', 'gemini-pro']
                for alt_model in alternatives:
                    if alt_model in available_models:
                        self.model = alt_model
                        print(f"✅ Model changed to available model: {self.model}")
                        break
                else:
                    if available_models:
                        self.model = available_models[0]
                        print(f"⚠️ Model {self.model} not found, using first available model: {self.model}")
                    else:
                        raise ValueError("No Gemini models available for this API key")
            
            print(f"✅ API key validated successfully. Using model: {self.model}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ API connection error: {e}")
            raise ValueError(f"API connection error: {e}")
    
    def update_product_data(self):
        """Update product data for recommendations"""
        try:
            # Avoid circular import by importing locally
            if self._lazy_product_data_load:
                from app.services.product_service import product_service
                
                # Get products directly
                self.products = product_service.get_all_products()
                self.categories = product_service.get_all_categories()
                self.combos = product_service.get_all_combos()
                
                # Cập nhật recommender
                if self.products and self.categories:
                    self.recommender.set_products(self.products, self.categories, self.combos)
                    
                    # Generate context only if products exist
                    self.product_context = self._generate_enhanced_product_context()
                    self._lazy_product_data_load = False
                    return True
                
            return False
        except Exception as e:
            print(f"❌ Error updating product data: {e}")
            return False
    
    def generate_system_prompt(self):
        """Generate the enhanced system prompt with product information"""
        # Ensure product data is loaded
        if self._lazy_product_data_load:
            self.update_product_data()
            
        system_prompt = """You are an experienced Gift Shop Consultant named "Gift Guru" with expertise in helping customers find personalized gifts. You possess detailed knowledge about our product catalog and provide expert recommendations.

YOUR MAIN GOALS:
1. Understand customer needs through thoughtful conversation
2. Provide personalized gift recommendations from our catalog
3. Create an engaging and helpful shopping experience

CONVERSATION APPROACH:
- Be warm, friendly, and conversational but professional
- Ask thoughtful follow-up questions to understand needs better
- Focus on understanding: occasion, recipient, relationship, age, interests, budget
- Proactively suggest specific products from our inventory, not generic gift ideas
- Explain WHY a product would be a good match for their needs
- Suggest complementary items when appropriate (gift combos)

RESPONSE STRUCTURE:
1. Acknowledge the customer's request/question
2. Provide helpful insights or ask clarifying questions
3. Make specific product recommendations with brief explanations
4. Invite further questions or refinement

PRODUCT RECOMMENDATION GUIDELINES:
- For children (0-12): Prioritize toys, educational items, arts & crafts
- For teenagers (13-19): Consider electronics, trendy items, hobby-related gifts
- For adults: Suggest practical, sophisticated, or experience-based gifts
- For special occasions (birthdays, anniversaries): Recommend gift combos or premium items
- For tight budgets: Focus on quality items under $25
- When unsure: Ask more questions rather than making assumptions

Here's information about our products:
"""
        # Add product context with improved formatting
        system_prompt += self.product_context
        
        return system_prompt
    
    def _generate_enhanced_product_context(self):
        """Generate an enhanced context string about available products"""
        # Ensure product data is loaded
        if self._lazy_product_data_load:
            self.update_product_data()
            
        context = "PRODUCT CATALOG INFORMATION:\n\n"
        
        # Add categories with descriptions
        context += "PRODUCT CATEGORIES:\n"
        category_descriptions = {
            "Arts & Crafts": "Creative supplies for artistic expression",
            "Toys": "Fun and engaging playthings for various ages",
            "Electronics": "Modern gadgets and digital devices",
            "Books": "Reading materials for education and entertainment",
            "Clothes": "Apparel items for various ages and styles",
            "Sports": "Equipment and accessories for active lifestyles"
        }
        
        for category in self.categories:
            description = category_descriptions.get(category, "Quality items for gifting")
            context += f"- {category}: {description}\n"
        
        # Add price ranges
        context += "\nPRICE RANGES:\n"
        context += "- Budget-friendly: Items under $20\n"
        context += "- Mid-range: Items between $20-$50\n"
        context += "- Premium: Items over $50\n"
        
        # Add products with more details
        context += "\nFEATURED PRODUCTS:\n"
        for product in self.products[:15]:  # Limited to 15 for context size
            context += f"- {product['name']} ({product['category']}): ${product['price']:.2f} - {product['description']}\n"
        
        # Add combo information
        context += "\nGIFT COMBOS (Bundles with 10% discount):\n"
        for combo in self.combos[:5]:
            combo_products_str = ', '.join(combo.get('products', []))
            context += f"- {combo['name']}: ${combo['price']:.2f} - Includes: {combo_products_str}\n"
        
        # Add special recommendations
        context += "\nSPECIAL OCCASION RECOMMENDATIONS:\n"
        context += "- For Birthdays: Birthday Special Gift Set, Personalized items, Age-appropriate toys\n"
        context += "- For Anniversaries: Romantic gift sets, Premium items, Personalized keepsakes\n"
        context += "- For Children: Educational toys, Arts & Crafts supplies, Interactive games\n"
        context += "- For Teenagers: Electronics, Trendy accessories, Books, Sports equipment\n"
        
        return context
    
    def process_query(self, query, user_id="default"):
        """Process a user query and generate a response with recommendations"""
        # Ensure product data is loaded
        if self._lazy_product_data_load:
            if not self.update_product_data():
                return self._generate_error_response("Failed to load product data")
        
        # Initialize conversation if not exists
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        # Prepare messages
        messages = self._prepare_messages(query, user_id)
        
        try:
            # Call Gemini API
            response_data = self._call_gemini_api(messages)
            
            # Extract response text
            if response_data and "candidates" in response_data:
                response_text = response_data["candidates"][0]["content"]["parts"][0]["text"]
            elif response_data and "contents" in response_data:
                # Alternative response format
                response_text = response_data["contents"][0]["parts"][0]["text"]
            else:
                return self._generate_error_response("Received invalid response from Gemini API")
            
            # Update conversation history
            self.conversation_history[user_id].append({"role": "user", "parts": [{"text": query}]})
            self.conversation_history[user_id].append({"role": "model", "parts": [{"text": response_text}]})
            
            # Get product recommendations using the advanced recommender
            history = self.conversation_history.get(user_id, [])
            recommendations = self.recommender.get_recommendations(query, history)
            
            return {
                "response": response_text,
                "recommendations": recommendations
            }
            
        except Exception as e:
            print(f"Error in process_query: {e}")
            return self._generate_error_response(f"Error processing query: {str(e)}")
    
    def _prepare_messages(self, query, user_id):
        """Prepare messages for Gemini API call"""
        # Always include system prompt as first message
        messages = [
            {"role": "user", "parts": [{"text": "System: " + self.generate_system_prompt()}]},
            {"role": "model", "parts": [{"text": "I understand my role as Gift Guru, your gift shop consultant. I'll help customers find perfect gifts by asking thoughtful questions, making personalized recommendations from your inventory, and suggesting gift combos for special occasions. I'll keep my responses friendly, conversational, and provide specific product suggestions with explanations of why they're a good match."}]}
        ]
        
        # Add conversation history (limited to last 5 exchanges)
        history = self.conversation_history.get(user_id, [])[-(10):]  # Just the last 5 exchanges (10 messages)
        messages.extend(history)
        
        # Add current query
        if not history or history[-1]["role"] != "user":
            messages.append({"role": "user", "parts": [{"text": query}]})
        
        return messages
    
    def _call_gemini_api(self, messages):
        """Call Gemini API with prepared messages"""
        if not self.api_key:
            raise ValueError("Gemini API key is not set")
        
        url = f"{self.base_url}/{self.api_version}/models/{self.model}:generateContent?key={self.api_key}"
        
        payload = {
            "contents": messages,
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 800,
            }
        }
        
        headers = {"Content-Type": "application/json"}
        
        try:
            print(f"Calling Gemini API with URL: {url}")
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            
            if response.status_code != 200:
                print(f"Gemini API error: Status {response.status_code}")
                print(f"Response text: {response.text}")
                return None
            
            data = response.json()
            print(f"Gemini API response received successfully")
            return data
            
        except requests.exceptions.Timeout:
            print("Gemini API request timed out")
            raise RuntimeError("API request timed out")
        except requests.exceptions.ConnectionError:
            print("Connection error when calling Gemini API")
            raise RuntimeError("Connection error")
        except Exception as e:
            print(f"Unexpected error calling Gemini API: {e}")
            raise RuntimeError(f"API call failed: {str(e)}")
    
    def _generate_error_response(self, error_message="An error occurred"):
        """Generate a standardized error response"""
        print(f"Error in chatbot: {error_message}")
        
        # Try to get top products for recommendations instead of empty list
        try:
            if self.products and len(self.products) > 0:
                recommendations = [
                    {
                        "id": product["id"],
                        "name": product["name"],
                        "price": product["price"],
                        "image": product["image"],
                        "description": product["description"],
                        "type": "product",
                        "relevance_scores": {"suggestion": "Popular item"}
                    }
                    for product in self.products[:3]
                ]
            else:
                recommendations = []
        except:
            recommendations = []
            
        return {
            "response": "I'm sorry, I couldn't process your request at the moment. Please try again.",
            "recommendations": recommendations,
            "error": error_message
        }
    
    def reset_conversation(self, user_id="default"):
        """Reset the conversation history for a user"""
        if user_id in self.conversation_history:
            self.conversation_history[user_id] = []
        return {"success": True, "message": "Conversation reset successfully"}


# Create singleton instance - with proper error handling
try:
    gemini_chatbot_service = GeminiChatbotService()
    print("✅ Gemini chatbot service singleton created successfully")
except Exception as e:
    print(f"❌ Failed to create Gemini chatbot service: {e}")
    gemini_chatbot_service = None