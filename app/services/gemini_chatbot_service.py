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
            
            print("✅ Smart GeminiChatbotService initialized successfully")
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
        """Generate a smart context-aware system prompt - SMART UPGRADED"""
        if self._lazy_product_data_load:
            self.update_product_data()
            
        prompt = """You are Gift Guru - a friendly and expert gift consultant with deep product knowledge and smart recommendation capabilities.

Your enhanced capabilities:
- Understand customer needs through natural conversation  
- Ask smart clarifying questions when needed
- Provide specific product recommendations with clear explanations
- Remember context and build on previous conversation
- Consider age, interests, budget, and occasion in recommendations
- Explain WHY you recommend specific items

Our Store Information:"""
        
        # Add enhanced product info with examples
        if self.categories and len(self.categories) > 0:
            prompt += f"\nCategories: {', '.join(self.categories)}"
        
        if self.products and len(self.products) > 0:
            min_price = min(p['price'] for p in self.products)
            max_price = max(p['price'] for p in self.products)
            prompt += f"\nProducts: {len(self.products)} carefully curated items (${min_price:.0f}-${max_price:.0f})"
            
            # Add category examples with sample products
            by_category = {}
            for product in self.products[:15]:  # Sample more products
                category = product.get('category', 'Other')
                if category not in by_category:
                    by_category[category] = []
                if len(by_category[category]) < 4:  # Max 4 examples per category
                    by_category[category].append(f"{product['name']} (${product['price']:.0f})")
            
            prompt += "\nSample products by category:"
            for category, items in by_category.items():
                prompt += f"\n- {category}: {', '.join(items)}"
        
        if self.combos and len(self.combos) > 0:
            prompt += f"\nSpecial gift bundles: {len(self.combos)} curated combinations with savings"
            # Add combo examples
            combo_examples = []
            for combo in self.combos[:3]:
                combo_examples.append(f"{combo['name']} (${combo['price']:.0f})")
            if combo_examples:
                prompt += f"\nExample bundles: {', '.join(combo_examples)}"
            
        prompt += """\n\nSmart conversation guidelines:
- When customer mentions age (like "8-year-old"), prioritize age-appropriate items and explain why they're suitable
- When they mention interests (like "loves art"), focus on matching products and explain the connection
- When they mention budget (like "under $25"), respect their price limit strictly and mention budget compatibility
- When they mention occasions (like "birthday"), suggest occasion-appropriate gifts and explain appropriateness
- When they mention relationships (like "daughter", "friend"), consider relationship-appropriate gifts
- Always explain WHY you're recommending specific items with specific reasons
- Keep responses helpful, friendly, and conversational
- If you need more information, ask 1-2 specific clarifying questions

Smart response examples:
"For an 8-year-old who loves art, I'd recommend our Art Supply Kit ($19.99) - it's perfect for that age group to develop creativity and fine motor skills!"
"Since you mentioned a $25 budget, here are some excellent options that fit perfectly within that range, giving you great value..."
"For a birthday gift, I'm thinking something special and fun that will make the day memorable..."

Remember: Be specific, explain your reasoning, and show enthusiasm for helping find the perfect gift!"""
        
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
        """Prepare enhanced messages with smart context - SMART UPGRADED"""
        contents = []
        
        # Generate enhanced system prompt
        system_prompt = self.generate_system_prompt()
        
        # Add query-specific context intelligence
        query_lower = query.lower()
        context_hints = []
        
        # Smart context detection
        if any(word in query_lower for word in ['year', 'old', 'teen', 'child', 'kid', 'baby', 'toddler']):
            context_hints.append("🎯 FOCUS: Pay special attention to age appropriateness in recommendations.")
        
        if any(word in query_lower for word in ['$', 'budget', 'cheap', 'expensive', 'under', 'around', 'cost', 'price']):
            context_hints.append("💰 FOCUS: Customer has budget constraints - respect their price limits and mention budget compatibility.")
        
        if any(word in query_lower for word in ['love', 'like', 'interest', 'hobby', 'enjoy', 'passion', 'into']):
            context_hints.append("❤️ FOCUS: Customer mentioned specific interests - match products to these interests and explain connections.")
        
        if any(word in query_lower for word in ['birthday', 'christmas', 'graduation', 'wedding', 'anniversary', 'holiday']):
            context_hints.append("🎉 FOCUS: This is for a specific occasion - recommend appropriate gifts and explain why they're perfect for this event.")
        
        if any(word in query_lower for word in ['son', 'daughter', 'mom', 'dad', 'friend', 'boyfriend', 'girlfriend', 'husband', 'wife']):
            context_hints.append("👥 FOCUS: Consider the relationship when recommending - some gifts are more appropriate for certain relationships.")
        
        # Enhanced system content with context intelligence
        system_content = system_prompt
        
        if context_hints:
            system_content += f"\n\n🧠 SMART CONTEXT ALERTS for this specific query:\n" + "\n".join(context_hints)
            system_content += "\n\nUse these alerts to provide more targeted and relevant recommendations with specific explanations."
        
        # Add conversation history context if available
        history = self.conversation_history.get(user_id, [])
        if len(history) >= 2:  # If there's previous conversation
            recent_context = []
            context_summary = []
            
            # Analyze recent conversation for persistent context
            for msg in history[-6:]:  # Last 3 exchanges
                if msg.get('role') == 'user':
                    user_text = msg['parts'][0]['text']
                    recent_context.append(f"Customer previously said: {user_text}")
                    
                    # Extract key context from previous messages
                    if any(word in user_text.lower() for word in ['year', 'old', 'age']):
                        context_summary.append("Age context mentioned previously")
                    if any(word in user_text.lower() for word in ['budget', '$', 'cost', 'price']):
                        context_summary.append("Budget discussed previously")
                    if any(word in user_text.lower() for word in ['love', 'like', 'interest']):
                        context_summary.append("Interests shared previously")
                elif msg.get('role') == 'model':
                    model_text = msg['parts'][0]['text'][:150]  # Truncate for brevity
                    recent_context.append(f"You previously responded: {model_text}...")
            
            if recent_context:
                system_content += f"\n\n💬 CONVERSATION CONTEXT:\n" + "\n".join(recent_context[-4:])  # Last 2 exchanges
                
                if context_summary:
                    system_content += f"\n\n📝 KEY CONTEXT TO REMEMBER: {', '.join(set(context_summary))}"
                
                system_content += "\n\nRemember this context when responding to build on the conversation naturally and avoid asking for information already provided."
        
        # Combine everything for the API call
        combined_message = f"{system_content}\n\n👤 CUSTOMER'S CURRENT QUESTION: {query}"
        
        contents.append({
            "role": "user",
            "parts": [{"text": combined_message}]
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
                "temperature": 0.8,  # Slightly more creative for better conversation
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 400,  # Allow longer responses for better explanations
            }
        }
        
        headers = {"Content-Type": "application/json"}
        
        try:
            print(f"🔄 Calling Smart Gemini API...")
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
            print("✅ Smart Gemini API response received successfully")
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
        """Process a user query with smart context analysis - SMART UPGRADED"""
        # Ensure product data is loaded
        if self._lazy_product_data_load:
            if not self.update_product_data():
                return self._generate_error_response("Failed to load product data")
        
        # Initialize conversation if not exists
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        # Prepare enhanced messages with smart context
        messages = self._prepare_messages(query, user_id)
        
        try:
            # Call Gemini API
            response_data = self._call_gemini_api(messages)
            
            # Extract response text
            if response_data and "candidates" in response_data:
                response_text = response_data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                return self._generate_error_response("Invalid API response")
            
            # Update conversation history with smart management
            self.conversation_history[user_id].append({"role": "user", "parts": [{"text": query}]})
            self.conversation_history[user_id].append({"role": "model", "parts": [{"text": response_text}]})
            
            # Keep conversation history manageable (last 12 messages = 6 exchanges)
            if len(self.conversation_history[user_id]) > 12:
                self.conversation_history[user_id] = self.conversation_history[user_id][-12:]
            
            # Get SMART recommendations using upgraded recommender
            recommendations = []
            if self.recommender:
                try:
                    history = self.conversation_history.get(user_id, [])
                    recommendations = self.recommender.get_recommendations(query, history)
                    
                    # ADD THIS DEBUG SECTION
                    print(f"\n🔍 DEBUG RECOMMENDATIONS for query: '{query}'")
                    print(f"📊 Analysis results:")
                    analysis = self.recommender.analyze_query_smart(query)
                    for key, value in analysis.items():
                        if value:
                            print(f"   {key}: {value}")
                    
                    print(f"\n🎯 Top recommendations:")
                    for i, rec in enumerate(recommendations):
                        print(f"   {i+1}. {rec['name']} (${rec['price']}) - Score: {rec.get('smart_score', 'N/A')}")
                        if 'relevance_scores' in rec:
                            print(f"      Reasons: {rec['relevance_scores']}")
                    print("="*50)
                    # END DEBUG SECTION
                    
                    print(f"🎯 Generated {len(recommendations)} SMART recommendations with explanations")
                    
                    # Debug: Print smart scores for monitoring
                    for rec in recommendations:
                        if 'smart_score' in rec:
                            print(f"   - {rec['name']}: Score {rec['smart_score']}, Reasons: {rec.get('relevance_scores', {}).get('strengths', 'N/A')}")
                            
                except Exception as e:
                    print(f"Error getting smart recommendations: {e}")
                    recommendations = self._get_fallback_recommendations()
            
            return {
                "response": response_text,
                "recommendations": recommendations,
                "smart_features": True,  # Indicate smart features are active
                "conversation_length": len(self.conversation_history[user_id])
            }
            
        except Exception as e:
            print(f"Error in smart process_query: {e}")
            return self._generate_error_response(f"Error processing query: {str(e)}")

    def _get_fallback_recommendations(self):
        """Get basic recommendations when smart recommender fails"""
        try:
            recommendations = []
            # Get mix of products and combos for variety
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
        print(f"Error in smart chatbot: {error_message}")
        
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
    print("✅ Smart Gemini chatbot service singleton created successfully")
except Exception as e:
    print(f"❌ Failed to create Gemini chatbot service: {e}")
    gemini_chatbot_service = None