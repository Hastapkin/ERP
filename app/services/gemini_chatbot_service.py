import os
import json
import requests
import time
import re

class GeminiChatbotService:
    def __init__(self, api_key=None):
        try:
            self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
            
            if not self.api_key:
                raise ValueError("Gemini API key is not set")
            
            # Gemini API settings
            self.base_url = "https://generativelanguage.googleapis.com"
            self.api_version = "v1beta"
            self.model = "gemini-2.0-flash"
                
            # Rate limiting
            self.last_api_call = None
            self.min_interval = 2
            
            # Conversation history and state
            self.conversation_history = {}
            self.conversation_state = {}  # Store extracted info per user
            self.products = []
            self.categories = []
            self.combos = []
            
            # Enhanced patterns for information extraction
            self.init_extraction_patterns()
            
            # Test API key
            self._test_api_key()
            
            print("✅ Enhanced Gemini Chatbot Service with No Products Handling initialized")
        except Exception as e:
            print(f"❌ Error initializing Gemini service: {e}")
            raise

    def init_extraction_patterns(self):
        """Initialize comprehensive extraction patterns"""
        
        # AGE PATTERNS - More comprehensive
        self.age_patterns = [
            # Direct age mentions
            r'(\d+)\s*(?:years?\s*old|year-old|yr-old|yrs?\s*old)',
            r'(?:age|aged)\s*(?:is\s*)?(\d+)',
            r'(\d+)\s*(?:years?|yrs?)\s*(?:of\s*age)?',
            r'my\s*(\d+)[-\s]*year[-\s]*old',
            r'for\s*(?:a|an)?\s*(\d+)[-\s]*year[-\s]*old',
            r'(\d+)[-\s]*year[-\s]*old\s*(?:boy|girl|child|kid)',
            r'(?:boy|girl|child|kid)\s*(?:is\s*)?(\d+)',
            r'(\d+)\s*(?:th)?\s*birthday',
            r'turning\s*(\d+)',
            # Single digits with context
            r'\b([3-9]|1[0-2])\b(?=\s*(?:years?|yr|old|birthday))',
            # Just numbers in range (last resort)
            r'\b([3-9]|1[0-2])\b'
        ]
        
        # GENDER PATTERNS - More precise
        self.gender_patterns = {
            'male': [
                r'\b(?:boy|son|male|he|his|him|man|gentleman|lad|dude|guy)\b',
                r'\b(?:for\s*)?(?:a\s*)?boy\b',
                r'\bmy\s*son\b',
                r'\b(?:little\s*)?boy\b',
                r'\bmale\s*child\b'
            ],
            'female': [
                r'\b(?:girl|daughter|female|she|her|woman|lady|gal|lass)\b',
                r'\b(?:for\s*)?(?:a\s*)?girl\b',
                r'\bmy\s*daughter\b',
                r'\b(?:little\s*)?girl\b',
                r'\bfemale\s*child\b'
            ]
        }
        
        # CATEGORY PATTERNS - More specific and comprehensive
        self.category_patterns = {
            'Arts & Crafts': [
                r'\b(?:arts?\s*(?:and|&)?\s*crafts?|art\s*supplies?|creative\s*(?:play|activities?|stuff)?)\b',
                r'\b(?:drawing|painting|coloring|sketching|crafting|creating)\b',
                r'\b(?:crayons?|markers?|paints?|brushes?|canvas|paper)\b',
                r'\b(?:diy|handmade|artistic|creative|imagination)\b',
                r'\bloves?\s*(?:to\s*)?(?:draw|paint|color|create|craft)\b'
            ],
            'Toys': [
                r'\b(?:toys?|games?|playthings?|play\s*(?:time|things?)?)\b',
                r'\b(?:building|blocks?|lego|construction|puzzles?)\b',
                r'\b(?:action\s*figures?|dolls?|stuffed\s*animals?|plushies?)\b',
                r'\b(?:cars?|trucks?|vehicles?|trains?|robots?)\b',
                r'\b(?:board\s*games?|card\s*games?|video\s*games?)\b',
                r'\bloves?\s*(?:to\s*)?play\b',
                r'\b(?:imaginative|pretend)\s*play\b'
            ],
            'Books': [
                r'\b(?:books?|reading|stories|literature|novels?)\b',
                r'\b(?:educational|learning|study|knowledge)\b',
                r'\b(?:picture\s*books?|story\s*books?|chapter\s*books?)\b',
                r'\bloves?\s*(?:to\s*)?read\b',
                r'\b(?:bookworm|reader|studious)\b'
            ],
            'Electronics': [
                r'\b(?:electronics?|tech|technology|gadgets?|devices?)\b',
                r'\b(?:tablets?|computers?|phones?|digital)\b',
                r'\b(?:gaming|video\s*games?|consoles?)\b',
                r'\b(?:smart|bluetooth|wireless|electronic)\b',
                r'\bloves?\s*technology\b'
            ],
            'Clothes': [
                r'\b(?:clothes|clothing|fashion|outfits?|apparel)\b',
                r'\b(?:shirts?|pants?|dresses?|shoes?|accessories)\b',
                r'\b(?:style|stylish|fashionable|trendy)\b',
                r'\bloves?\s*(?:fashion|dressing\s*up)\b'
            ],
            'Sports': [
                r'\b(?:sports?|athletic|exercise|fitness|active|outdoor)\b',
                r'\b(?:balls?|soccer|football|basketball|baseball|tennis)\b',
                r'\b(?:running|swimming|cycling|skating|dancing)\b',
                r'\b(?:physical\s*activity|active\s*play|outdoor\s*play)\b',
                r'\bloves?\s*(?:sports?|being\s*active|outdoor\s*activities?)\b'
            ]
        }
        
        # BUDGET PATTERNS - More comprehensive
        self.budget_patterns = [
            # Range patterns
            r'between\s*\$?(\d+)[-\s]*(?:and|to|&)\s*\$?(\d+)',
            r'from\s*\$?(\d+)[-\s]*(?:to|up\s*to)\s*\$?(\d+)',
            r'\$?(\d+)[-\s]*(?:to|and|-)\s*\$?(\d+)',
            r'(\d+)[-\s]*(?:to|and|-)\s*(\d+)\s*dollars?',
            # Under/below patterns
            r'(?:under|below|less\s*than|max|maximum|up\s*to)\s*\$?(\d+)',
            r'no\s*more\s*than\s*\$?(\d+)',
            r'budget\s*(?:of|is)?\s*\$?(\d+)',
            # Around/about patterns
            r'(?:around|about|approximately|roughly)\s*\$?(\d+)',
            r'close\s*to\s*\$?(\d+)',
            # Over/above patterns  
            r'(?:over|above|more\s*than|at\s*least)\s*\$?(\d+)',
            # Direct amount patterns
            r'\$(\d+)(?!\d)',
            r'(\d+)\s*dollars?',
            r'(\d+)\s*bucks?',
            # Budget categories
            r'\b(?:cheap|budget|affordable|inexpensive|low\s*cost)\b',
            r'\b(?:expensive|premium|high[-\s]*end|luxury|pricey)\b'
        ]

    def _test_api_key(self):
        """Test API key"""
        try:
            test_url = f"{self.base_url}/{self.api_version}/models/{self.model}:generateContent?key={self.api_key}"
            test_payload = {"contents": [{"role": "user", "parts": [{"text": "Hello"}]}]}
            
            response = requests.post(test_url, 
                                   headers={"Content-Type": "application/json"}, 
                                   json=test_payload, timeout=5)
            
            if response.status_code != 200:
                raise ValueError(f"Invalid API key (Status: {response.status_code})")
            
            print(f"✅ Gemini API key validated")
            return True
            
        except requests.exceptions.RequestException as e:
            raise ValueError(f"API connection error: {e}")

    def update_product_data(self):
        """Load product data"""
        try:
            from app.services.product_service import product_service
            self.products = product_service.get_all_products()
            self.categories = product_service.get_all_categories()
            self.combos = product_service.get_all_combos()
            print(f"📦 Loaded: {len(self.products)} products")
            return True
        except Exception as e:
            print(f"❌ Error loading products: {e}")
            return False

    def extract_age(self, text):
        """Enhanced age extraction"""
        text_lower = text.lower().strip()
        
        print(f"🔍 Analyzing text for age: '{text}'")
        
        # Try each pattern in order of specificity
        for i, pattern in enumerate(self.age_patterns):
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                try:
                    age = int(match.group(1))
                    if 3 <= age <= 12:
                        print(f"✅ Age extracted: {age} (pattern {i+1})")
                        return age
                    else:
                        print(f"❌ Age {age} out of range 3-12")
                except (ValueError, IndexError):
                    continue
        
        print(f"❌ No valid age found")
        return None

    def extract_gender(self, text):
        """Enhanced gender extraction"""
        text_lower = text.lower().strip()
        
        print(f"🔍 Analyzing text for gender: '{text}'")
        
        # Check male patterns first
        for pattern in self.gender_patterns['male']:
            if re.search(pattern, text_lower):
                print(f"✅ Gender extracted: male (pattern: {pattern})")
                return 'male'
        
        # Then check female patterns
        for pattern in self.gender_patterns['female']:
            if re.search(pattern, text_lower):
                print(f"✅ Gender extracted: female (pattern: {pattern})")
                return 'female'
        
        print(f"❌ No gender found")
        return None

    def extract_category(self, text):
        """Enhanced category extraction"""
        text_lower = text.lower().strip()
        
        print(f"🔍 Analyzing text for category: '{text}'")
        
        # Score each category based on pattern matches
        category_scores = {}
        
        for category, patterns in self.category_patterns.items():
            score = 0
            matched_patterns = []
            
            for pattern in patterns:
                matches = re.finditer(pattern, text_lower)
                for match in matches:
                    score += 1
                    matched_patterns.append(pattern)
            
            if score > 0:
                category_scores[category] = (score, matched_patterns)
                print(f"📊 {category}: score {score}, patterns: {matched_patterns[:2]}")
        
        if category_scores:
            # Return category with highest score
            best_category = max(category_scores.keys(), key=lambda x: category_scores[x][0])
            print(f"✅ Category extracted: {best_category} (score: {category_scores[best_category][0]})")
            return best_category
        
        print(f"❌ No category found")
        return None

    def extract_budget(self, text):
        """Enhanced budget extraction"""
        text_lower = text.lower().strip()
        
        print(f"🔍 Analyzing text for budget: '{text}'")
        
        # Handle budget categories first
        if re.search(r'\b(?:cheap|budget|affordable|inexpensive|low\s*cost)\b', text_lower):
            print(f"✅ Budget extracted: Under $25 (budget category)")
            return "Under $25"
        
        if re.search(r'\b(?:expensive|premium|high[-\s]*end|luxury|pricey)\b', text_lower):
            print(f"✅ Budget extracted: Over $60 (premium category)")
            return "Over $60"
        
        # Try each budget pattern
        for pattern in self.budget_patterns:
            match = re.search(pattern, text_lower)
            if match:
                try:
                    groups = match.groups()
                    
                    # Range budget (two numbers)
                    if len(groups) >= 2 and groups[1] and groups[1].isdigit():
                        min_amount = int(groups[0])
                        max_amount = int(groups[1])
                        if min_amount > max_amount:
                            min_amount, max_amount = max_amount, min_amount
                        result = f"${min_amount}-{max_amount}"
                        print(f"✅ Budget extracted: {result} (range)")
                        return result
                    
                    # Single amount
                    elif groups[0] and groups[0].isdigit():
                        amount = int(groups[0])
                        
                        # Determine type based on keywords in the match
                        full_match = match.group(0)
                        if any(word in full_match for word in ['under', 'below', 'less', 'max', 'up to']):
                            result = f"Under ${amount}"
                        elif any(word in full_match for word in ['over', 'above', 'more', 'at least']):
                            result = f"Over ${amount}"
                        elif any(word in full_match for word in ['around', 'about', 'approximately', 'close']):
                            result = f"Around ${amount}"
                        else:
                            result = f"Around ${amount}"
                        
                        print(f"✅ Budget extracted: {result}")
                        return result
                        
                except (ValueError, IndexError):
                    continue
        
        print(f"❌ No budget found")
        return None

    def analyze_message_comprehensively(self, text):
        """Comprehensive analysis of a single message"""
        print(f"\n🔍 COMPREHENSIVE ANALYSIS: '{text}'")
        
        # Extract all possible information
        extracted = {
            'age': self.extract_age(text),
            'gender': self.extract_gender(text),
            'category': self.extract_category(text),
            'budget': self.extract_budget(text)
        }
        
        # Also check for multi-info messages
        # Example: "8 year old boy who loves toys"
        if extracted['age'] and extracted['gender'] and not extracted['category']:
            # Look for category hints in the same sentence
            words = text.lower().split()
            for i, word in enumerate(words):
                if word in ['loves', 'likes', 'enjoys', 'into']:
                    # Look at next few words
                    next_words = ' '.join(words[i+1:i+4])
                    category = self.extract_category(next_words)
                    if category:
                        extracted['category'] = category
                        print(f"🔗 Linked category from same message: {category}")
                        break
        
        print(f"📊 EXTRACTION RESULTS: {extracted}")
        return extracted

    def get_conversation_state(self, user_id):
        """Get current conversation state for user"""
        if user_id not in self.conversation_state:
            self.conversation_state[user_id] = {
                'age': None,
                'gender': None,
                'category': None,
                'budget': None,
                'confidence': {
                    'age': 0,
                    'gender': 0,
                    'category': 0,
                    'budget': 0
                }
            }
        return self.conversation_state[user_id]

    def update_conversation_state(self, user_id, new_info):
        """Update conversation state with new information"""
        state = self.get_conversation_state(user_id)
        
        print(f"📝 UPDATING STATE for user {user_id}")
        print(f"   Previous: {state}")
        print(f"   New info: {new_info}")
        
        # Update with new information (only if not None)
        for key, value in new_info.items():
            if value is not None and key in state:
                old_value = state[key]
                state[key] = value
                state['confidence'][key] = 1.0  # High confidence for direct extraction
                
                if old_value != value:
                    print(f"   ✅ Updated {key}: {old_value} → {value}")
                else:
                    print(f"   ♻️ Confirmed {key}: {value}")
        
        print(f"   Final state: {state}")
        return state

    def extract_info_from_full_conversation(self, user_id):
        """Extract info from entire conversation history as backup"""
        if user_id not in self.conversation_history:
            return {'age': None, 'gender': None, 'category': None, 'budget': None}
        
        # Combine all user messages
        all_user_text = ""
        for msg in self.conversation_history[user_id]:
            if msg.get('role') == 'user':
                all_user_text += " " + msg['parts'][0]['text']
        
        if all_user_text.strip():
            print(f"🔄 BACKUP EXTRACTION from full conversation: '{all_user_text.strip()}'")
            return self.analyze_message_comprehensively(all_user_text)
        
        return {'age': None, 'gender': None, 'category': None, 'budget': None}

    def generate_system_prompt(self):
        """Generate system prompt"""
        if not self.products:
            self.update_product_data()
            
        category_list = ", ".join(self.categories) if self.categories else "Arts & Crafts, Toys, Books, Electronics, Clothes, Sports"
        
        return f"""You are Gift Guru - an expert gift consultant who helps customers find perfect gifts.

🎯 YOUR MISSION: Collect exactly 4 pieces of information in order:

1. **AGE** (3-12 years old)
2. **GENDER** (male/female) 
3. **CATEGORY** from: {category_list}
4. **BUDGET** (amount or range)

📊 OUR STORE: {len(self.products)} products, Ages 3-12, Price range $8-$100

🤖 CONVERSATION RULES:

**If missing AGE:** "What's the age of the gift recipient? (We specialize in ages 3-12)"
**If missing GENDER:** "Great! A [age]-year-old. Is this for a boy or a girl?"
**If missing CATEGORY:** "Perfect! A [age]-year-old [boy/girl]. What does this child enjoy? Choose from: {category_list}"
**If missing BUDGET:** "Excellent! What's your budget range? Examples: 'under $30', 'around $50', 'between $20-40'"
**If have ALL 4:** "Perfect! I'm finding the best matching products from our catalog..."

🎯 STYLE: Be enthusiastic, ask ONE question at a time, keep responses short and focused."""

    def _wait_for_rate_limit(self):
        """Wait for rate limit"""
        if self.last_api_call:
            elapsed = time.time() - self.last_api_call
            if elapsed < self.min_interval:
                wait_time = self.min_interval - elapsed
                print(f"⏳ Waiting {wait_time:.1f}s...")
                time.sleep(wait_time)

    def _call_gemini_api(self, messages):
        """Call Gemini API"""
        if not self.api_key:
            raise ValueError("Gemini API key is not set")
        
        self._wait_for_rate_limit()
        
        url = f"{self.base_url}/{self.api_version}/models/{self.model}:generateContent?key={self.api_key}"
        
        payload = {
            "contents": messages,
            "generationConfig": {
                "temperature": 0.3,
                "topK": 20,
                "topP": 0.8,
                "maxOutputTokens": 200,
            }
        }
        
        try:
            print(f"🔄 Calling Gemini API...")
            response = requests.post(url, headers={"Content-Type": "application/json"}, 
                                   json=payload, timeout=15)
            
            self.last_api_call = time.time()
            
            if response.status_code == 429:
                raise RuntimeError("API_RATE_LIMIT_EXCEEDED")
            elif response.status_code != 200:
                raise RuntimeError(f"API_ERROR_{response.status_code}")
            
            data = response.json()
            print("✅ Gemini API response received")
            return data
            
        except requests.exceptions.Timeout:
            raise RuntimeError("API_TIMEOUT")
        except Exception as e:
            raise RuntimeError(f"API_ERROR: {str(e)}")

    def get_recommendations(self, state):
        """Get recommendations with strict filtering and no-products handling"""
        if not self.products:
            self.update_product_data()
        
        age, gender, category, budget = state['age'], state['gender'], state['category'], state['budget']
        print(f"🎯 Getting recommendations: {age}y {gender}, {category}, {budget}")
        
        # STEP 1: Filter products by category FIRST (strict filtering)
        if category:
            category_products = [p for p in self.products if p.get('category') == category]
            category_combos = [c for c in self.combos if c.get('category') == category]
            print(f"📊 Found {len(category_products)} products and {len(category_combos)} combos in {category}")
        else:
            category_products = self.products
            category_combos = self.combos
            print(f"📊 No category filter, using all {len(category_products)} products")
        
        # STEP 2: Apply budget filter if specified
        budget_filtered_products = []
        budget_filtered_combos = []
        
        if budget:
            print(f"💰 Applying budget filter: {budget}")
            
            for product in category_products:
                price = product.get('price', 0)
                if self._price_fits_budget(price, budget):
                    budget_filtered_products.append(product)
                    print(f"   ✅ {product['name']} (${price}) fits budget")
                else:
                    print(f"   ❌ {product['name']} (${price}) outside budget")
            
            for combo in category_combos:
                price = combo.get('price', 0)
                if self._price_fits_budget(price, budget):
                    budget_filtered_combos.append(combo)
                    print(f"   ✅ {combo['name']} (${price}) fits budget")
                else:
                    print(f"   ❌ {combo['name']} (${price}) outside budget")
                    
            print(f"💰 After budget filter: {len(budget_filtered_products)} products, {len(budget_filtered_combos)} combos")
        else:
            budget_filtered_products = category_products
            budget_filtered_combos = category_combos
        
        # STEP 3: Check if we have any products after filtering
        total_available = len(budget_filtered_products) + len(budget_filtered_combos)
        
        if total_available == 0:
            print("❌ NO PRODUCTS FOUND after filtering!")
            return self._handle_no_products_case(age, gender, category, budget)
        
        # STEP 4: Score remaining products
        scored_items = []
        
        for product in budget_filtered_products:
            score = self._score_product_strict(product, age, gender, category, budget)
            scored_items.append((product, score, 'product'))
            print(f"📊 {product['name']}: score {score:.1f}")
        
        for combo in budget_filtered_combos:
            score = self._score_product_strict(combo, age, gender, category, budget)
            combo_score = score * 1.1  # Small bonus for combos
            scored_items.append((combo, combo_score, 'combo'))
            print(f"📊 {combo['name']}: score {combo_score:.1f}")
        
        # STEP 5: Sort and take top results
        scored_items.sort(key=lambda x: x[1], reverse=True)
        
        # Take top 3, but ensure we have decent scores
        good_items = [(item, score, item_type) for item, score, item_type in scored_items if score >= 3.0]
        
        if not good_items:
            print("❌ NO GOOD MATCHES found (all scores < 3.0)!")
            return self._handle_no_products_case(age, gender, category, budget)
        
        top_items = good_items[:3]
        
        # STEP 6: Format recommendations
        recommendations = []
        for item, score, item_type in top_items:
            recommendations.append({
                "id": item["id"],
                "name": item["name"],
                "price": item["price"],
                "image": item["image"],
                "description": item["description"],
                "type": item_type,
                "relevance_scores": {
                    "match_score": f"{score:.1f}/10",
                    "reason": self._get_reason(item, age, gender, category, budget)
                }
            })
        
        print(f"✅ Generated {len(recommendations)} quality recommendations")
        return recommendations

    def _handle_no_products_case(self, age, gender, category, budget):
        """Handle case when no products are found matching criteria"""
        print(f"🚫 NO PRODUCTS CASE: age={age}, gender={gender}, category={category}, budget={budget}")
        
        # Analyze what's causing the issue
        reasons = []
        suggestions = []
        
        if category and budget:
            # Check if category has products at all
            category_products = [p for p in self.products if p.get('category') == category]
            if not category_products:
                reasons.append(f"We don't have any {category} products in our current inventory")
                suggestions.append("Try a different category like Arts & Crafts or Toys")
            else:
                # Check budget range for this category
                category_prices = [p.get('price', 0) for p in category_products]
                min_price = min(category_prices)
                max_price = max(category_prices)
                
                reasons.append(f"No {category} products found within your budget")
                reasons.append(f"{category} products range from ${min_price:.0f} to ${max_price:.0f}")
                
                # Suggest budget adjustment
                if 'under' in budget.lower():
                    budget_limit = int(re.search(r'\$?(\d+)', budget).group(1))
                    if min_price > budget_limit:
                        suggestions.append(f"Try increasing your budget to at least ${min_price:.0f}")
                
                # Suggest similar products in budget
                if budget:
                    budget_products = []
                    for product in self.products:
                        if self._price_fits_budget(product.get('price', 0), budget):
                            budget_products.append(product)
                    
                    if budget_products:
                        other_categories = set(p.get('category') for p in budget_products)
                        other_categories.discard(category)
                        if other_categories:
                            suggestions.append(f"Consider {' or '.join(list(other_categories)[:2])} which have options in your budget")

        elif category and not budget:
            category_products = [p for p in self.products if p.get('category') == category]
            if not category_products:
                reasons.append(f"We don't currently have any {category} products")
                suggestions.append("Try Arts & Crafts, Toys, or Books instead")

        elif budget and not category:
            reasons.append("No specific category selected")
            suggestions.append("Please specify what type of products you're interested in")

        # Build response message
        response_parts = []
        
        if reasons:
            response_parts.append("I'm sorry, but " + ". ".join(reasons) + ".")
        else:
            response_parts.append("I'm sorry, but I couldn't find any products matching your specific criteria.")
        
        if suggestions:
            response_parts.append("\n🤔 **Here are some suggestions:**")
            for suggestion in suggestions:
                response_parts.append(f"• {suggestion}")
        
        response_parts.append("\n💡 **You can also:**")
        response_parts.append("• Adjust your budget range")
        response_parts.append("• Try a different category")
        response_parts.append("• Ask me to show popular products for this age group")
        
        final_response = "\n".join(response_parts)
        
        print(f"📝 No products response: {final_response}")
        
        return []  # Return empty list, no recommendations

    def _score_product_strict(self, product, age, gender, category, budget):
        """Strict scoring - only for products that should actually match"""
        score = 5.0  # Base score
        
        # Age appropriateness (more conservative)
        if age:
            if age <= 5 and product.get('category') in ['Arts & Crafts', 'Toys']:
                score += 1.5
            elif age <= 8 and product.get('category') in ['Toys', 'Arts & Crafts', 'Books']:
                score += 1.5
            elif age >= 9 and product.get('category') in ['Electronics', 'Sports', 'Books']:
                score += 1.5
            else:
                score -= 0.5  # Penalty for age mismatch
        
        # Category match (STRICT - this should already be filtered)
        if category and category == product.get('category'):
            score += 2.0  # High bonus for exact category match
        elif category and category != product.get('category'):
            score -= 3.0  # Heavy penalty for wrong category (shouldn't happen)
        
        # Budget match (STRICT - this should already be filtered)
        if budget:
            price = product.get('price', 0)
            if self._price_fits_budget(price, budget):
                score += 1.5  # Bonus for exact budget match
            elif self._price_close_budget(price, budget):
                score += 0.5  # Small bonus for close match
            else:
                score -= 2.0  # Penalty for budget mismatch (shouldn't happen)
        
        # Gender preference (light touch)
        if gender:
            name = product.get('name', '').lower()
            if gender == 'male' and any(word in name for word in ['car', 'truck', 'robot', 'action', 'superhero']):
                score += 0.5
            elif gender == 'female' and any(word in name for word in ['doll', 'princess', 'unicorn', 'jewelry']):
                score += 0.5
        
        return max(0, score)

    def _price_fits_budget(self, price, budget_str):
        """Enhanced budget matching"""
        if not budget_str:
            return True
            
        try:
            if 'under' in budget_str.lower() or 'below' in budget_str.lower():
                limit = int(re.search(r'\$?(\d+)', budget_str).group(1))
                return price <= limit
            elif 'over' in budget_str.lower() or 'above' in budget_str.lower():
                limit = int(re.search(r'\$?(\d+)', budget_str).group(1))
                return price >= limit
            elif 'around' in budget_str.lower() or 'about' in budget_str.lower():
                target = int(re.search(r'\$?(\d+)', budget_str).group(1))
                return abs(price - target) <= target * 0.25  # 25% tolerance
            elif '-' in budget_str:
                matches = re.findall(r'\$?(\d+)', budget_str)
                if len(matches) == 2:
                    min_val, max_val = int(matches[0]), int(matches[1])
                    return min_val <= price <= max_val
        except (ValueError, AttributeError):
            pass
            
        return True

    def _price_close_budget(self, price, budget_str):
        """Check if price is close to budget (for scoring)"""
        if not budget_str:
            return True
            
        try:
            if 'under' in budget_str.lower():
                limit = int(re.search(r'\$?(\d+)', budget_str).group(1))
                return price <= limit * 1.15  # 15% over tolerance
            elif 'around' in budget_str.lower():
                target = int(re.search(r'\$?(\d+)', budget_str).group(1))
                return abs(price - target) <= target * 0.4  # 40% tolerance
        except (ValueError, AttributeError):
            pass
            
        return False

    def _get_reason(self, product, age, gender, category, budget):
        """Get reason for recommendation"""
        reasons = []
        if category and category == product.get('category'):
            reasons.append(f"Perfect for {category}")
        if budget and self._price_fits_budget(product.get('price', 0), budget):
            reasons.append("Within budget")
        if age and age <= 8 and product.get('category') in ['Toys', 'Arts & Crafts']:
            reasons.append(f"Great for {age}-year-olds")
        return ", ".join(reasons) if reasons else "Popular choice"

    def process_query(self, query, user_id="default"):
        """Enhanced process_query with no-products handling"""
        print(f"\n🔄 PROCESSING QUERY: '{query}' for user {user_id}")
        print("="*60)
        
        # Ensure product data is loaded
        if not self.products:
            self.update_product_data()
        
        # Initialize conversation if not exists
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        # Handle greeting
        if len(query.strip()) < 3 or query.lower().strip() in ['hi', 'hello', 'hey', 'start']:
            greeting_response = """Hello! I'm your Gift Guru! 🎁

I'll help you find the perfect gift based on 4 key factors:
👶 **Age** (3-12 years - our specialty!)
👦👧 **Gender** (male/female)
📱 **Category** preferences
💰 **Budget**

Let's start: **What's the age of the gift recipient?**"""
            
            return {
                "response": greeting_response,
                "recommendations": [],
                "conversation_stage": "greeting"
            }
        
        # STEP 1: Extract info from current message
        new_info = self.analyze_message_comprehensively(query)
        
        # STEP 2: Update conversation state
        state = self.update_conversation_state(user_id, new_info)
        
        # STEP 3: If still missing info, try extracting from full conversation
        missing_info = [key for key, value in state.items() 
                       if key != 'confidence' and value is None]
        
        if missing_info:
            print(f"🔄 Still missing: {missing_info}. Trying full conversation extraction...")
            backup_info = self.extract_info_from_full_conversation(user_id)
            
            # Update with backup info (only for missing pieces)
            for key in missing_info:
                if backup_info.get(key):
                    state[key] = backup_info[key]
                    state['confidence'][key] = 0.8  # Lower confidence for backup extraction
                    print(f"🔄 Backup extracted {key}: {backup_info[key]}")
        
        # STEP 4: Add current query to conversation history
        self.conversation_history[user_id].append({"role": "user", "parts": [{"text": query}]})
        
        # STEP 5: Check if we have all info for recommendations
        complete_info = all([
            state['age'] is not None,
            state['gender'] is not None,
            state['category'] is not None,
            state['budget'] is not None
        ])
        
        if complete_info:
            print("🎯 ALL INFO COLLECTED! Getting recommendations...")
            recommendations = self.get_recommendations(state)
            
            if not recommendations:
                # No products found - let Gemini know to give a "no products" response
                context_str = f"No products found for: Age {state['age']}, Gender {state['gender']}, Category {state['category']}, Budget {state['budget']}"
                system_prompt = f"""The user has provided all needed information but we found NO products matching their criteria.

{context_str}

Respond with empathy and suggest they try:
1. A different category 
2. Adjusting their budget
3. Asking for popular products for their age group

Be helpful and understanding. Do NOT mention specific products since none were found."""
                
                messages = [{
                    "role": "user",
                    "parts": [{"text": f"{system_prompt}\n\nUSER: {query}\n\nExplain that no products were found and give helpful suggestions."}]
                }]
                
                try:
                    response_data = self._call_gemini_api(messages)
                    if response_data and "candidates" in response_data:
                        response_text = response_data["candidates"][0]["content"]["parts"][0]["text"]
                    else:
                        response_text = "I'm sorry, but I couldn't find any products matching your specific criteria. Would you like to try a different category or adjust your budget?"
                except:
                    response_text = "I'm sorry, but I couldn't find any products matching your specific criteria. Would you like to try a different category or adjust your budget?"
                
                self.conversation_history[user_id].append({"role": "model", "parts": [{"text": response_text}]})
                
                return {
                    "response": response_text,
                    "recommendations": [],
                    "conversation_stage": "no_products_found",
                    "extracted_info": {k: v for k, v in state.items() if k != 'confidence'},
                    "no_products_reason": "No products match the specified criteria"
                }
            else:
                # Products found - normal flow
                system_prompt = self.generate_system_prompt()
                context_str = f"All info collected: Age {state['age']}, Gender {state['gender']}, Category {state['category']}, Budget {state['budget']}"
                
                messages = [{
                    "role": "user", 
                    "parts": [{"text": f"{system_prompt}\n\n{context_str}\n\nUSER: {query}\n\nSay that you found perfect matches and are showing recommendations."}]
                }]
        else:
            # Still collecting info - normal Gemini flow
            system_prompt = self.generate_system_prompt()
            
            # Build context about current state
            context_info = []
            for key, value in state.items():
                if key != 'confidence' and value is not None:
                    context_info.append(f"{key.title()}: {value}")
            
            context_str = "Current info: " + ", ".join(context_info) if context_info else "No info collected yet"
            
            messages = [{
                "role": "user",
                "parts": [{"text": f"{system_prompt}\n\n{context_str}\n\nUSER: {query}\n\nRespond according to the conversation rules."}]
            }]
            
            recommendations = []
        
        try:
            # STEP 6: Call Gemini API
            response_data = self._call_gemini_api(messages)
            
            # Extract response
            if response_data and "candidates" in response_data:
                response_text = response_data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                return self._generate_error_response("Invalid API response")
            
            # Update conversation history
            self.conversation_history[user_id].append({"role": "model", "parts": [{"text": response_text}]})
            
            # Keep conversation manageable
            if len(self.conversation_history[user_id]) > 12:
                self.conversation_history[user_id] = self.conversation_history[user_id][-12:]
            
            # STEP 7: Return result
            result = {
                "response": response_text,
                "recommendations": recommendations,
                "conversation_stage": "recommendations" if complete_info and recommendations else "collecting_info",
                "extracted_info": {k: v for k, v in state.items() if k != 'confidence'},
                "missing_info": [key for key, value in state.items() 
                               if key != 'confidence' and value is None]
            }
            
            print("="*60)
            print(f"✅ PROCESSING COMPLETE")
            print(f"   Response length: {len(response_text)} chars")
            print(f"   Recommendations: {len(recommendations)}")
            print(f"   Missing info: {result['missing_info']}")
            print("="*60)
            
            return result
            
        except Exception as e:
            print(f"❌ Error in process_query: {e}")
            return self._generate_error_response(f"Error processing query: {str(e)}")

    def _generate_error_response(self, error_message="An error occurred"):
        """Generate error response with fallback"""
        print(f"❌ Error in Gemini chatbot: {error_message}")
        
        # Simple fallback recommendations
        recommendations = []
        try:
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
        except:
            pass
            
        return {
            "response": "I'm sorry, I'm having some technical difficulties. Here are some popular products:",
            "recommendations": recommendations,
            "error": error_message,
            "conversation_stage": "error"
        }

    def reset_conversation(self, user_id="default"):
        """Reset conversation for a user"""
        if user_id in self.conversation_history:
            self.conversation_history[user_id] = []
        if user_id in self.conversation_state:
            self.conversation_state[user_id] = {
                'age': None, 'gender': None, 'category': None, 'budget': None,
                'confidence': {'age': 0, 'gender': 0, 'category': 0, 'budget': 0}
            }
        print(f"🔄 Reset conversation and state for user {user_id}")
        return {"success": True, "message": "Conversation reset successfully"}

    def get_conversation_debug_info(self, user_id="default"):
        """Get debug information about conversation state"""
        state = self.get_conversation_state(user_id)
        history_length = len(self.conversation_history.get(user_id, []))
        
        return {
            "current_state": state,
            "history_length": history_length,
            "missing_info": [key for key, value in state.items() 
                           if key != 'confidence' and value is None],
            "confidence_scores": state.get('confidence', {}),
            "ready_for_recommendations": all([
                state['age'] is not None,
                state['gender'] is not None,
                state['category'] is not None,
                state['budget'] is not None
            ])
        }

# Create singleton instance
try:
    gemini_chatbot_service = GeminiChatbotService()
    print("✅ Enhanced Gemini Chatbot Service with No Products Handling created successfully")
except Exception as e:
    print(f"❌ Failed to create Enhanced Gemini Chatbot Service: {e}")
    gemini_chatbot_service = None