import os
import json
import requests
import time
from datetime import datetime, timedelta

class GeminiChatbotService:
    def __init__(self, api_key=None):
        try:
            self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
            
            if not self.api_key:
                raise ValueError("Gemini API key is not set or empty")
            
            # Updated to official API endpoint
            self.base_url = "https://generativelanguage.googleapis.com"
            self.api_version = "v1beta"
            self.model = "gemini-2.0-flash"
                
            # Rate limiting
            self.last_api_call = None
            self.min_interval = 2  # Minimum 2 seconds between API calls
            
            # Initialize other attributes
            self.conversation_history = {}
            self.products = []
            self.categories = []
            self.combos = []
            self.recommender = None
            self._lazy_product_data_load = True
            
            # Test API key
            self._test_api_key()
            
            print("✅ GeminiChatbotService initialized successfully")
        except Exception as e:
            print(f"❌ Error initializing GeminiChatbotService: {e}")
            raise

    def _test_api_key(self):
        """Test API key with correct endpoint"""
        try:
            test_url = f"{self.base_url}/{self.api_version}/models/{self.model}:generateContent?key={self.api_key}"
            
            test_payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [
                            {"text": "Hello"}
                        ]
                    }
                ]
            }
            
            response = requests.post(test_url, 
                                   headers={"Content-Type": "application/json"}, 
                                   json=test_payload, 
                                   timeout=5)
            
            if response.status_code != 200:
                print(f"❌ API key test failed with status {response.status_code}")
                print(f"Response: {response.text}")
                raise ValueError(f"Invalid API key (Status: {response.status_code})")
            
            print(f"✅ API key validated successfully. Using model: {self.model}")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ API connection error: {e}")
            raise ValueError(f"API connection error: {e}")

    def update_product_data(self):
        """Update product data - simplified to avoid recursion"""
        try:
            if self._lazy_product_data_load:
                # Import locally to avoid circular imports
                from app.services.product_service import product_service
                
                self.products = product_service.get_all_products()
                self.categories = product_service.get_all_categories()
                self.combos = product_service.get_all_combos()
                
                # Initialize recommender
                if self.recommender is None:
                    from app.services.advanced_recommender import AdvancedRecommender
                    self.recommender = AdvancedRecommender(self.products, self.categories, self.combos)
                else:
                    self.recommender.set_products(self.products, self.categories, self.combos)
                
                self._lazy_product_data_load = False
                print(f"✅ Loaded {len(self.products)} products, {len(self.categories)} categories, {len(self.combos)} combos")
                return True
                
            return True
        except Exception as e:
            print(f"❌ Error updating product data: {e}")
            return False

    def generate_system_prompt(self):
        """Generate a concise system prompt"""
        if self._lazy_product_data_load:
            self.update_product_data()
            
        prompt = """You are Gift Guru - a friendly and knowledgeable gift consultant.

Your role:
- Help customers find perfect gifts from our catalog
- Ask about occasion, recipient, age, interests, budget
- Recommend specific products with clear reasons
- Keep responses conversational and helpful

Our Store:"""
        
        # Add basic product info
        if self.categories and len(self.categories) > 0:
            prompt += f"\nCategories: {', '.join(self.categories[:4])}"
        
        if self.products and len(self.products) > 0:
            min_price = min(p['price'] for p in self.products)
            max_price = max(p['price'] for p in self.products)
            prompt += f"\nProducts: {len(self.products)} items from ${min_price:.0f} to ${max_price:.0f}"
            
            # Add some example products
            prompt += "\nFeatured items:"
            for product in self.products[:3]:
                prompt += f"\n- {product['name']}: ${product['price']:.0f}"
        
        if self.combos and len(self.combos) > 0:
            prompt += f"\nGift combos: {len(self.combos)} special bundles available"
            
        prompt += "\n\nKeep responses friendly, concise, and focused on helping the customer find the right gift."
        
        return prompt

    def _wait_for_rate_limit(self):
        """Wait to avoid rate limit"""
        if self.last_api_call:
            elapsed = time.time() - self.last_api_call
            if elapsed < self.min_interval:
                wait_time = self.min_interval - elapsed
                print(f"⏳ Waiting {wait_time:.1f}s to avoid rate limit...")
                time.sleep(wait_time)

    def _prepare_messages(self, query, user_id):
        """Prepare messages according to Gemini API format"""
        contents = []
        
        # Add system context as first user message
        system_content = f"System context: {self.generate_system_prompt()}\n\nCustomer question: {query}"
        contents.append({
            "role": "user",
            "parts": [{"text": system_content}]
        })
        
        return contents

    def _call_gemini_api(self, messages):
        """Call Gemini API with proper format"""
        if not self.api_key:
            raise ValueError("Gemini API key is not set")
        
        self._wait_for_rate_limit()
        
        url = f"{self.base_url}/{self.api_version}/models/{self.model}:generateContent?key={self.api_key}"
        
        # Format payload according to API standard
        payload = {
            "contents": messages,
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 300,
            }
        }
        
        headers = {"Content-Type": "application/json"}
        
        try:
            print(f"🔄 Calling Gemini API...")
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            
            # Update last API call time
            self.last_api_call = time.time()
            
            if response.status_code == 429:
                print("❌ Gemini API rate limit exceeded")
                raise RuntimeError("API_RATE_LIMIT_EXCEEDED")
            elif response.status_code == 400:
                print(f"❌ Bad request: {response.text}")
                raise RuntimeError("API_BAD_REQUEST")
            elif response.status_code != 200:
                print(f"❌ Gemini API error: Status {response.status_code}")
                print(f"Response: {response.text}")
                raise RuntimeError(f"API_ERROR_{response.status_code}")
            
            data = response.json()
            print("✅ Gemini API response received successfully")
            return data
            
        except requests.exceptions.Timeout:
            print("❌ Gemini API request timed out")
            raise RuntimeError("API_TIMEOUT")
        except requests.exceptions.ConnectionError:
            print("❌ Connection error when calling Gemini API")
            raise RuntimeError("CONNECTION_ERROR")
        except Exception as e:
            print(f"❌ Unexpected error calling Gemini API: {e}")
            raise RuntimeError(f"API_ERROR: {str(e)}")

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
            else:
                return self._generate_error_response("Invalid API response")
            
            # Update conversation history
            self.conversation_history[user_id].append({"role": "user", "parts": [{"text": query}]})
            self.conversation_history[user_id].append({"role": "model", "parts": [{"text": response_text}]})
            
            # Get product recommendations
            recommendations = []
            if self.recommender:
                try:
                    history = self.conversation_history.get(user_id, [])
                    recommendations = self.recommender.get_recommendations(query, history)
                except Exception as e:
                    print(f"Error getting recommendations: {e}")
                    recommendations = self._get_fallback_recommendations()
            
            return {
                "response": response_text,
                "recommendations": recommendations
            }
            
        except Exception as e:
            print(f"Error in process_query: {e}")
            return self._generate_error_response(f"Error processing query: {str(e)}")

    def _get_fallback_recommendations(self):
        """Get basic recommendations when advanced recommender fails"""
        try:
            recommendations = []
            # Get mix of products and combos
            for product in self.products[:2]:
                recommendations.append({
                    "id": product["id"],
                    "name": product["name"],
                    "price": product["price"],
                    "image": product["image"],
                    "description": product["description"],
                    "type": "product",
                    "relevance_scores": {"suggestion": "Popular item"}
                })
            
            for combo in self.combos[:1]:
                recommendations.append({
                    "id": combo["id"],
                    "name": combo["name"],
                    "price": combo["price"],
                    "image": combo["image"],
                    "description": combo["description"],
                    "type": "combo",
                    "relevance_scores": {"suggestion": "Gift bundle"}
                })
            
            return recommendations
        except:
            return []

    def _generate_error_response(self, error_message="An error occurred"):
        """Generate a standardized error response"""
        print(f"Error in chatbot: {error_message}")
        
        # Try to get fallback recommendations
        recommendations = self._get_fallback_recommendations()
            
        return {
            "response": "I'm sorry, I'm having some technical difficulties. Here are some popular products you might like:",
            "recommendations": recommendations,
            "error": error_message
        }

    def reset_conversation(self, user_id="default"):
        """Reset the conversation history for a user"""
        if user_id in self.conversation_history:
            self.conversation_history[user_id] = []
        return {"success": True, "message": "Conversation reset successfully"}

# Create singleton instance with proper error handling
try:
    gemini_chatbot_service = GeminiChatbotService()
    print("✅ Gemini chatbot service singleton created successfully")
except Exception as e:
    print(f"❌ Failed to create Gemini chatbot service: {e}")
    gemini_chatbot_service = None