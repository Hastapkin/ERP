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
            
            print("✅ GUIDED CONVERSATION GeminiChatbotService initialized successfully")
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
        """Update product data with ENHANCED recommender"""
        try:
            if self._lazy_product_data_load:
                # Import locally to avoid circular imports
                from app.services.product_service import product_service
                
                self.products = product_service.get_all_products()
                self.categories = product_service.get_all_categories()
                self.combos = product_service.get_all_combos()
                
                # Initialize ENHANCED recommender
                if self.recommender is None:
                    from app.services.advanced_recommender import AdvancedRecommender
                    self.recommender = AdvancedRecommender(self.products, self.categories, self.combos)
                    print("🧠 GUIDED AdvancedRecommender initialized")
                else:
                    self.recommender.set_products(self.products, self.categories, self.combos)
                
                self._lazy_product_data_load = False
                print(f"✅ Loaded {len(self.products)} products, {len(self.categories)} categories, {len(self.combos)} combos with GUIDED intelligence")
                return True
                
            return True
        except Exception as e:
            print(f"❌ Error updating product data: {e}")
            return False

    def generate_system_prompt(self):
        """Generate GUIDED CONVERSATION system prompt"""
        if self._lazy_product_data_load:
            self.update_product_data()
            
        # Get category info for guided questions
        category_list = ", ".join(self.categories) if self.categories else "Arts & Crafts, Toys, Books, Electronics, Clothes, Sports"
        
        prompt = f"""You are Gift Guru - a FRIENDLY and SYSTEMATIC gift consultant who helps customers find perfect gifts through guided conversation.

🎯 YOUR MISSION: Guide customers through 4 KEY QUESTIONS to recommend the perfect gift based on our data.

📊 OUR STORE PROFILE:
- Age Range: 3-12 years old (our specialty!)  
- Gender Options: Male/Female
- Categories: {category_list}
- Price Range: $8-$100 for individual items, $40-$150 for gift bundles
- Based on REAL purchase data from happy customers

🤖 GUIDED CONVERSATION FLOW:

📝 STEP 1 - WARM GREETING & AGE:
If this is the start of conversation, always greet warmly and ask about AGE first:
"Hello! I'm your Gift Guru, and I'm here to help you find the perfect gift! 🎁

To give you the best recommendations based on our customer data, I'd love to know:

**What's the age of the lucky gift recipient?** (We specialize in gifts for ages 3-12)"

📝 STEP 2 - GENDER (if not provided):
"Great! And is this gift for a **boy or a girl**? This helps me suggest items that have been most popular with that gender based on our purchase history."

📝 STEP 3 - INTERESTS/CATEGORY (if not provided):
"Perfect! Now, what kind of things do they enjoy? Are they into:
- 🎨 **Arts & Crafts** (drawing, coloring, creating)
- 🧸 **Toys** (games, building, imaginative play)  
- 📚 **Books** (reading, stories, learning)
- 📱 **Electronics** (gadgets, tech toys)
- 👕 **Clothes** (fashion, accessories) 
- ⚽ **Sports** (active play, outdoor activities)

Or feel free to tell me about their hobbies and interests!"

📝 STEP 4 - BUDGET (if not provided):
"Excellent! Last question - **what's your budget range?**
- 💚 **Budget-friendly**: $8-$25 (great individual items)
- 💙 **Mid-range**: $25-$60 (popular choices) 
- 💜 **Premium**: $60-$100 (special individual items)
- 🎁 **Gift Bundle**: $40-$150 (curated combinations)

This helps me focus on options that give you the best value!"

🎯 INFORMATION GATHERING RULES:

✅ **ALWAYS ASK FOR MISSING INFO**: If customer hasn't provided age, gender, interests, or budget - ask for it!

✅ **ONE QUESTION AT A TIME**: Don't overwhelm - ask for one missing piece of info per response.

✅ **BE ENCOURAGING**: "Great choice!" "Perfect!" "Excellent!" - keep it positive.

✅ **EXPLAIN WHY YOU'RE ASKING**: "This helps me suggest items that have been most popular..." 

✅ **OFFER OPTIONS**: Give specific choices when asking about interests/categories.

🎯 RECOMMENDATION PHASE (when you have enough info):

When you have AT LEAST age + gender + (interests OR budget), then provide recommendations:

"Based on our customer data, here are some fantastic options that have been super popular with [age]-year-old [gender]s who love [interest/category]:

[Explain why these work well with specific data insights]

Would you like to know more about any of these, or would you prefer to see options in a different category or price range?"

🎯 CONVERSATION STYLE:

✅ **Friendly & Enthusiastic**: Use emojis, exclamation points, positive language
✅ **Data-Driven**: "Based on our customer data..." "This has been popular with..."
✅ **Helpful**: Always explain WHY you're asking questions  
✅ **Patient**: Guide them step by step, don't rush
✅ **Personal**: "I'd love to help you find..." "Let me suggest..."

❌ **NEVER**:
- Overwhelm with too many questions at once
- Mention specific product names (let recommendations handle that)
- Skip the information gathering process
- Give recommendations without enough info

🎯 EXAMPLES:

**New Customer:**
"Hello! I'm your Gift Guru, and I'm excited to help you find the perfect gift! 🎁 To give you the best recommendations, what's the age of the gift recipient? We specialize in ages 3-12!"

**Missing Gender:**
"Wonderful! A 8-year-old - that's a fun age! Is this gift for a boy or a girl? This helps me suggest items that have been most popular based on our purchase history."

**Missing Interests:**
"Perfect! Now, what kind of activities does this 8-year-old boy enjoy? Is he into arts & crafts, toys & games, books, electronics, sports, or something else? Tell me about his hobbies!"

**Missing Budget:**
"Excellent! He sounds creative! What's your budget range? This helps me focus on the best value options: budget-friendly ($8-25), mid-range ($25-60), premium ($60-100), or a special gift bundle ($40-150)?"

**Ready to Recommend:**
"Perfect! Based on our data, 8-year-old boys who love arts & crafts have given excellent ratings to several items in your budget range. Here's what I'd recommend..."

Remember: Your goal is to gather the 4 key pieces of info (age, gender, interests, budget) through friendly conversation, then provide data-driven recommendations!"""
        
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
        """Prepare messages with GUIDED CONVERSATION context"""
        contents = []
        
        # Generate GUIDED system prompt
        system_prompt = self.generate_system_prompt()
        
        # Analyze conversation state
        conversation_state = self._analyze_conversation_state(user_id, query)
        
        # Add conversation state guidance
        query_lower = query.lower()
        context_hints = []
        
        # Determine what information we still need
        missing_info = []
        if not conversation_state.get('has_age'):
            missing_info.append("age")
        if not conversation_state.get('has_gender'):
            missing_info.append("gender") 
        if not conversation_state.get('has_interests'):
            missing_info.append("interests/category")
        if not conversation_state.get('has_budget'):
            missing_info.append("budget")
        
        if missing_info:
            context_hints.append(f"🎯 MISSING INFO: Customer hasn't provided {', '.join(missing_info)}. Ask for the MOST IMPORTANT missing piece first.")
        
        # Check if we can recommend
        if conversation_state.get('can_recommend'):
            context_hints.append("✅ ENOUGH INFO: You have enough information to provide recommendations! Proceed with data-driven suggestions.")
        
        # Check conversation stage
        if conversation_state.get('is_greeting'):
            context_hints.append("👋 GREETING: This appears to be a new conversation. Start with warm greeting and ask for age.")
        
        # Add context from conversation history
        history = self.conversation_history.get(user_id, [])
        if len(history) >= 2:
            recent_context = []
            for msg in history[-4:]:  # Last 2 exchanges
                if msg.get('role') == 'user':
                    user_text = msg['parts'][0]['text']
                    recent_context.append(f"Customer said: {user_text}")
                elif msg.get('role') == 'model':
                    model_text = msg['parts'][0]['text'][:100]
                    recent_context.append(f"You said: {model_text}...")
            
            if recent_context:
                context_hints.append(f"📜 CONVERSATION HISTORY:\n" + "\n".join(recent_context[-4:]))
        
        # Enhanced system content
        system_content = system_prompt
        
        if context_hints:
            system_content += f"\n\n🧠 CONVERSATION GUIDANCE for this interaction:\n" + "\n".join(context_hints)
        
        # Add current query context
        combined_message = f"{system_content}\n\n👤 CUSTOMER'S MESSAGE: {query}\n\n🎯 YOUR RESPONSE STRATEGY: Follow the guided conversation flow. Ask for missing information step by step, or provide recommendations if you have enough info!"
        
        contents.append({
            "role": "user",
            "parts": [{"text": combined_message}]
        })
        
        return contents

    def _analyze_conversation_state(self, user_id, current_query):
        """Analyze what information we have collected so far"""
        state = {
            'has_age': False,
            'has_gender': False, 
            'has_interests': False,
            'has_budget': False,
            'can_recommend': False,
            'is_greeting': False
        }
        
        # Get conversation history
        history = self.conversation_history.get(user_id, [])
        
        # Check if this is a greeting (new conversation or simple hello)
        if len(history) == 0 or current_query.lower().strip() in ['hi', 'hello', 'hey', 'help', 'start']:
            state['is_greeting'] = True
            return state
        
        # Combine all user messages to analyze
        all_user_text = current_query.lower()
        for msg in history:
            if msg.get('role') == 'user':
                all_user_text += " " + msg['parts'][0]['text'].lower()
        
        # Check for age information
        import re
        age_patterns = [
            r'(\d+)\s*(?:year|yr)s?\s*old',
            r'age\s*(\d+)',
            r'(\d+)[- ]year[- ]old',
            r'\b([3-9]|1[0-2])\b'  # Ages 3-12
        ]
        
        for pattern in age_patterns:
            if re.search(pattern, all_user_text):
                age_match = re.search(pattern, all_user_text)
                if age_match:
                    age = int(age_match.group(1))
                    if 3 <= age <= 12:
                        state['has_age'] = True
                        break
        
        # Check for gender information  
        gender_keywords = ['boy', 'girl', 'male', 'female', 'son', 'daughter', 'he', 'she', 'his', 'her']
        if any(keyword in all_user_text for keyword in gender_keywords):
            state['has_gender'] = True
        
        # Check for interests/category information
        interest_keywords = [
            'art', 'craft', 'drawing', 'painting', 'creative',
            'toy', 'game', 'play', 'building', 
            'book', 'read', 'story', 'learning',
            'electronic', 'tech', 'gadget', 'device',
            'clothes', 'fashion', 'dress', 'wear',
            'sport', 'active', 'outdoor', 'exercise',
            'love', 'like', 'enjoy', 'into', 'hobby', 'interest'
        ]
        if any(keyword in all_user_text for keyword in interest_keywords):
            state['has_interests'] = True
        
        # Check for budget information
        budget_patterns = [
            r'\$\d+',
            r'\d+\s*dollar',
            r'budget', 'cheap', 'expensive', 'price', 'cost',
            r'under', 'below', 'around', 'between', 'within'
        ]
        if any(re.search(pattern, all_user_text) for pattern in budget_patterns):
            state['has_budget'] = True
        
        # Determine if we can recommend
        # Need at least: age + gender + (interests OR budget)
        if state['has_age'] and state['has_gender'] and (state['has_interests'] or state['has_budget']):
            state['can_recommend'] = True
        
        print(f"🔍 CONVERSATION STATE: {state}")
        return state

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
                "temperature": 0.8,  # Friendly and engaging
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 350,  # Enough for guided questions
            }
        }
        
        headers = {"Content-Type": "application/json"}
        
        try:
            print(f"🔄 Calling GUIDED Gemini API...")
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
            print("✅ GUIDED Gemini API response received successfully")
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
        """Process query with GUIDED CONVERSATION intelligence"""
        # Ensure product data is loaded
        if self._lazy_product_data_load:
            if not self.update_product_data():
                return self._generate_error_response("Failed to load product data")
        
        # Initialize conversation if not exists
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        # Analyze conversation state
        conversation_state = self._analyze_conversation_state(user_id, query)
        
        # Prepare enhanced messages with GUIDED context
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
            
            # Keep conversation history manageable
            if len(self.conversation_history[user_id]) > 12:
                self.conversation_history[user_id] = self.conversation_history[user_id][-12:]
            
            # Get recommendations ONLY if we have enough information
            recommendations = []
            if conversation_state.get('can_recommend') and self.recommender:
                try:
                    history = self.conversation_history.get(user_id, [])
                    recommendations = self.recommender.get_recommendations(query, history)
                    
                    print(f"🎯 Generated {len(recommendations)} GUIDED recommendations")
                    
                except Exception as e:
                    print(f"Error getting GUIDED recommendations: {e}")
                    recommendations = []
            
            return {
                "response": response_text,
                "recommendations": recommendations,
                "conversation_state": conversation_state,
                "guided_conversation": True,
                "conversation_length": len(self.conversation_history[user_id]),
                "intelligence_level": "GUIDED_CONVERSATION"
            }
            
        except Exception as e:
            print(f"Error in GUIDED process_query: {e}")
            return self._generate_error_response(f"Error processing query: {str(e)}")

    def _get_fallback_recommendations(self):
        """Get basic recommendations when enhanced recommender fails"""
        try:
            recommendations = []
            # Prioritize individual products for fallback
            for product in self.products[:3]:
                recommendations.append({
                    "id": product["id"],
                    "name": product["name"],
                    "price": product["price"],
                    "image": product["image"],
                    "description": product["description"],
                    "type": "product",
                    "relevance_scores": {"suggestion": "Popular choice"}
                })
            
            return recommendations
        except:
            return []

    def _generate_error_response(self, error_message="An error occurred"):
        """Generate enhanced error response"""
        print(f"Error in GUIDED chatbot: {error_message}")
        
        recommendations = self._get_fallback_recommendations()
            
        return {
            "response": "I'm sorry, I'm having some technical difficulties. Here are some popular products from our catalog:",
            "recommendations": recommendations,
            "error": error_message,
            "guided_conversation": True
        }

    def reset_conversation(self, user_id="default"):
        """Reset the conversation history for a user"""
        if user_id in self.conversation_history:
            self.conversation_history[user_id] = []
        return {"success": True, "message": "Conversation reset successfully", "guided_conversation": True}

# Create singleton instance with enhanced error handling
try:
    gemini_chatbot_service = GeminiChatbotService()
    print("✅ GUIDED CONVERSATION Gemini chatbot service singleton created successfully")
except Exception as e:
    print(f"❌ Failed to create GUIDED Gemini chatbot service: {e}")
    gemini_chatbot_service = None