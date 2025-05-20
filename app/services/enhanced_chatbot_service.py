import re
import json
from collections import defaultdict
from .product_service import product_service

class EnhancedChatbotService:
    def __init__(self):
        # Load and analyze Excel data
        self.analyzed_data = None
        self.recommendation_rules = {}
        self.conversation_context = {}
        self.analyze_excel_data()
        
        # Enhanced keyword detection
        self.age_keywords = {
            'toddler': ['baby', 'toddler', 'little one', '2', '3', '4', '5'],
            'child': ['child', 'kid', 'young', '6', '7', '8', '9', '10'],
            'teen': ['teen', 'teenager', 'adolescent', '11', '12', '13', '14', '15'],
            'adult': ['adult', 'grown up', 'man', 'woman', '16', '17', '18', '20+']
        }
        
        self.occasion_keywords = {
            'birthday': ['birthday', 'bday', 'born', 'celebration'],
            'christmas': ['christmas', 'xmas', 'holiday', 'santa'],
            'education': ['school', 'learning', 'educational', 'teach', 'study'],
            'play': ['fun', 'play', 'entertainment', 'game'],
            'creative': ['creative', 'art', 'craft', 'drawing', 'painting'],
            'development': ['development', 'growth', 'skill', 'ability']
        }
        
        self.gender_keywords = {
            'male': ['boy', 'son', 'brother', 'father', 'dad', 'grandfather', 'he', 'him', 'his'],
            'female': ['girl', 'daughter', 'sister', 'mother', 'mom', 'grandmother', 'she', 'her']
        }
        
        self.price_keywords = {
            'budget': ['cheap', 'affordable', 'budget', 'inexpensive', 'low cost', 'under 20'],
            'moderate': ['reasonable', 'medium', 'moderate', '20-40', 'mid-range'],
            'premium': ['expensive', 'premium', 'high quality', 'luxury', 'over 40', 'best']
        }
        
        self.relationship_keywords = {
            'family': ['son', 'daughter', 'child', 'kid', 'brother', 'sister', 'family'],
            'friend': ['friend', 'buddy', 'pal', 'classmate'],
            'relative': ['cousin', 'nephew', 'niece', 'grandchild']
        }
    
    def analyze_excel_data(self):
        """Analyze Excel data to create recommendation rules"""
        # Get raw product data from product service
        products = product_service.get_all_products()
        
        # Initialize analysis structure
        self.analyzed_data = {
            'age_preferences': defaultdict(lambda: defaultdict(int)),
            'gender_preferences': defaultdict(lambda: defaultdict(int)),
            'category_popularity': defaultdict(int),
            'price_ranges': {
                'budget': {'min': 0, 'max': 20, 'items': []},
                'moderate': {'min': 20, 'max': 40, 'items': []},
                'premium': {'min': 40, 'max': 1000, 'items': []}
            },
            'item_metadata': {}
        }
        
        # Analyze products (simulated based on real Excel structure)
        for product in products:
            category = product['category']
            price = product['price']
            
            # Category popularity
            self.analyzed_data['category_popularity'][category] += 1
            
            # Price range classification
            if price < 20:
                self.analyzed_data['price_ranges']['budget']['items'].append(product)
            elif price <= 40:
                self.analyzed_data['price_ranges']['moderate']['items'].append(product)
            else:
                self.analyzed_data['price_ranges']['premium']['items'].append(product)
            
            # Simulated age and gender preferences based on category
            self._simulate_preferences(product)
        
        # Build recommendation rules
        self._build_recommendation_rules()
    
    def _simulate_preferences(self, product):
        """Simulate age and gender preferences based on product category"""
        category = product['category']
        
        # Age preferences based on category (simulated logic)
        if category in ['Toys', 'Role Play']:
            self.analyzed_data['age_preferences']['child'][category] += 2
            self.analyzed_data['age_preferences']['toddler'][category] += 1
        elif category in ['Arts & Crafts']:
            self.analyzed_data['age_preferences']['child'][category] += 1
            self.analyzed_data['age_preferences']['teen'][category] += 2
        elif category in ['Educational']:
            self.analyzed_data['age_preferences']['teen'][category] += 2
            self.analyzed_data['age_preferences']['child'][category] += 1
        elif category in ['Electronics']:
            self.analyzed_data['age_preferences']['teen'][category] += 2
            self.analyzed_data['age_preferences']['adult'][category] += 1
        
        # Gender preferences (simulated)
        if category in ['Arts & Crafts', 'Role Play']:
            self.analyzed_data['gender_preferences']['female'][category] += 2
            self.analyzed_data['gender_preferences']['male'][category] += 1
        elif category in ['Toys', 'Electronics']:
            self.analyzed_data['gender_preferences']['male'][category] += 2
            self.analyzed_data['gender_preferences']['female'][category] += 1
        else:
            self.analyzed_data['gender_preferences']['male'][category] += 1
            self.analyzed_data['gender_preferences']['female'][category] += 1
    
    def _build_recommendation_rules(self):
        """Build recommendation rules from analyzed data"""
        self.recommendation_rules = {
            'age_based': {},
            'gender_based': {},
            'price_based': {},
            'category_combinations': {}
        }
        
        # Age-based rules
        for age_group, categories in self.analyzed_data['age_preferences'].items():
            sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
            self.recommendation_rules['age_based'][age_group] = [cat for cat, _ in sorted_categories[:3]]
        
        # Gender-based rules
        for gender, categories in self.analyzed_data['gender_preferences'].items():
            sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
            self.recommendation_rules['gender_based'][gender] = [cat for cat, _ in sorted_categories[:3]]
        
        # Price-based rules
        for price_range, data in self.analyzed_data['price_ranges'].items():
            if data['items']:
                # Get most popular category in this price range
                category_counts = defaultdict(int)
                for item in data['items']:
                    category_counts[item['category']] += 1
                
                top_category = max(category_counts.items(), key=lambda x: x[1])[0] if category_counts else None
                self.recommendation_rules['price_based'][price_range] = {
                    'top_category': top_category,
                    'avg_price': sum(item['price'] for item in data['items']) / len(data['items']),
                    'count': len(data['items'])
                }
    
    def process_query(self, query, user_id='default'):
        """Enhanced query processing with context awareness"""
        query = query.lower().strip()
        
        # Initialize user context if not exists
        if user_id not in self.conversation_context:
            self.conversation_context[user_id] = {
                'preferences': {},
                'conversation_flow': [],
                'last_recommendation_type': None
            }
        
        context = self.conversation_context[user_id]
        context['conversation_flow'].append(query)
        
        # Extract information from query
        extracted_info = self._extract_comprehensive_info(query)
        
        # Update context with new information
        context['preferences'].update(extracted_info)
        
        # Determine response strategy
        if self._is_greeting(query):
            return self._handle_greeting(context)
        elif self._is_follow_up_question(query):
            return self._handle_follow_up(query, context)
        elif self._is_specific_request(query):
            return self._handle_specific_request(extracted_info, context)
        else:
            return self._handle_general_inquiry(extracted_info, context)
    
    def _extract_comprehensive_info(self, query):
        """Extract all possible information from query"""
        info = {}
        
        # Age detection
        for age_group, keywords in self.age_keywords.items():
            if any(keyword in query for keyword in keywords):
                info['age_group'] = age_group
                break
        
        # Numeric age detection
        age_match = re.search(r'(\d+)\s*(?:year|yr)s?\s*old', query)
        if age_match:
            age = int(age_match.group(1))
            if age <= 5:
                info['age_group'] = 'toddler'
            elif age <= 10:
                info['age_group'] = 'child'
            elif age <= 15:
                info['age_group'] = 'teen'
            else:
                info['age_group'] = 'adult'
            info['specific_age'] = age
        
        # Gender detection
        for gender, keywords in self.gender_keywords.items():
            if any(keyword in query for keyword in keywords):
                info['gender'] = gender
                break
        
        # Occasion detection
        for occasion, keywords in self.occasion_keywords.items():
            if any(keyword in query for keyword in keywords):
                info['occasion'] = occasion
                break
        
        # Price detection
        for price_range, keywords in self.price_keywords.items():
            if any(keyword in query for keyword in keywords):
                info['price_preference'] = price_range
                break
        
        # Price range from numbers
        price_match = re.search(r'\$?(\d+)', query)
        if price_match:
            price = int(price_match.group(1))
            if price < 20:
                info['price_preference'] = 'budget'
            elif price <= 40:
                info['price_preference'] = 'moderate'
            else:
                info['price_preference'] = 'premium'
            info['budget'] = price
        
        # Relationship detection
        for rel_type, keywords in self.relationship_keywords.items():
            if any(keyword in query for keyword in keywords):
                info['relationship'] = rel_type
                break
        
        # Category detection
        categories = product_service.get_all_categories()
        for category in categories:
            if category.lower() in query:
                info['category'] = category
                break
        
        return info
    
    def _is_greeting(self, query):
        """Check if query is a greeting"""
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'help me']
        return any(greeting in query for greeting in greetings)
    
    def _is_follow_up_question(self, query):
        """Check if query is a follow-up question"""
        follow_ups = ['what about', 'how about', 'any other', 'something else', 'different']
        return any(phrase in query for phrase in follow_ups)
    
    def _is_specific_request(self, query):
        """Check if query is asking for something specific"""
        specific_words = ['show me', 'find', 'looking for', 'need', 'want', 'recommend']
        return any(word in query for word in specific_words)
    
    def _handle_greeting(self, context):
        """Handle greeting messages"""
        responses = [
            "Hello! I'm here to help you find the perfect gift. Who are you shopping for?",
            "Hi there! I can help you discover amazing gifts. What's the occasion?",
            "Welcome to our gift advisor! Tell me about the person you're shopping for."
        ]
        
        import random
        response = random.choice(responses)
        
        # Get some general recommendations
        recommendations = self._get_general_recommendations()
        
        return {
            "response": response,
            "recommendations": recommendations
        }
    
    def _handle_follow_up(self, query, context):
        """Handle follow-up questions"""
        preferences = context['preferences']
        
        # Modify previous search
        if 'price' in query and preferences.get('price_preference'):
            # Change price preference
            if 'cheaper' in query or 'budget' in query:
                preferences['price_preference'] = 'budget'
            elif 'expensive' in query or 'premium' in query:
                preferences['price_preference'] = 'premium'
        
        # Get new recommendations based on updated preferences
        recommendations = self._generate_smart_recommendations(preferences)
        
        response = "Here are some different options you might like:"
        
        return {
            "response": response,
            "recommendations": recommendations
        }
    
    def _handle_specific_request(self, extracted_info, context):
        """Handle specific requests"""
        # Combine with context
        combined_preferences = {**context['preferences'], **extracted_info}
        
        # Generate targeted recommendations
        recommendations = self._generate_smart_recommendations(combined_preferences)
        
        # Generate personalized response
        response = self._generate_personalized_response(combined_preferences)
        
        return {
            "response": response,
            "recommendations": recommendations
        }
    
    def _handle_general_inquiry(self, extracted_info, context):
        """Handle general inquiries"""
        # Update context and provide recommendations
        recommendations = self._generate_smart_recommendations(extracted_info)
        
        if not extracted_info:
            response = "I'd love to help you find the perfect gift! Could you tell me more about the person or occasion?"
        else:
            response = "Based on what you're looking for, here are my recommendations:"
        
        return {
            "response": response,
            "recommendations": recommendations
        }
    
    def _generate_smart_recommendations(self, preferences, limit=3):
        """Generate intelligent recommendations based on preferences and data analysis"""
        products = product_service.get_all_products()
        combos = product_service.get_all_combos()
        all_items = []
        
        # Convert products and combos to unified format
        for product in products:
            all_items.append({**product, 'type': 'product'})
        
        for combo in combos:
            all_items.append({**combo, 'type': 'combo'})
        
        # Score each item based on preferences
        scored_items = []
        for item in all_items:
            score = self._calculate_item_score(item, preferences)
            if score > 0:
                scored_items.append((item, score))
        
        # Sort by score and return top items
        scored_items.sort(key=lambda x: x[1], reverse=True)
        recommendations = [item for item, score in scored_items[:limit]]
        
        # Format recommendations for frontend
        formatted_recommendations = []
        for item in recommendations:
            formatted_recommendations.append({
                "id": item["id"],
                "name": item["name"],
                "price": item["price"],
                "image": item["image"],
                "description": item["description"],
                "type": item["type"]
            })
        
        return formatted_recommendations
    
    def _calculate_item_score(self, item, preferences):
        """Calculate score for an item based on user preferences"""
        score = 1.0  # Base score
        
        # Category matching
        if preferences.get('category') and item['category'] == preferences['category']:
            score += 3.0
        
        # Age-based scoring
        age_group = preferences.get('age_group')
        if age_group and age_group in self.recommendation_rules['age_based']:
            if item['category'] in self.recommendation_rules['age_based'][age_group]:
                score += 2.0
        
        # Gender-based scoring
        gender = preferences.get('gender')
        if gender and gender in self.recommendation_rules['gender_based']:
            if item['category'] in self.recommendation_rules['gender_based'][gender]:
                score += 1.5
        
        # Price preference scoring
        price_pref = preferences.get('price_preference')
        if price_pref and price_pref in self.analyzed_data['price_ranges']:
            price_range = self.analyzed_data['price_ranges'][price_pref]
            if price_range['min'] <= item['price'] <= price_range['max']:
                score += 2.0
            else:
                # Penalize items outside preferred price range
                score -= 1.0
        
        # Occasion-based scoring
        occasion = preferences.get('occasion')
        if occasion:
            if occasion == 'creative' and 'Arts' in item['category']:
                score += 2.0
            elif occasion == 'education' and 'Educational' in item['category']:
                score += 2.0
            elif occasion == 'play' and 'Toys' in item['category']:
                score += 2.0
        
        # Boost for combos on special occasions
        if item['type'] == 'combo' and preferences.get('occasion') in ['birthday', 'christmas']:
            score += 1.0
        
        return max(0, score)  # Ensure non-negative score
    
    def _generate_personalized_response(self, preferences):
        """Generate a personalized response based on preferences"""
        response_parts = ["I've found some great options"]
        
        if preferences.get('age_group'):
            age_descriptions = {
                'toddler': 'for little ones',
                'child': 'for children',
                'teen': 'for teenagers',
                'adult': 'for adults'
            }
            response_parts.append(age_descriptions[preferences['age_group']])
        
        if preferences.get('occasion'):
            response_parts.append(f"for {preferences['occasion']}")
        
        if preferences.get('price_preference'):
            price_descriptions = {
                'budget': 'that are budget-friendly',
                'moderate': 'in a moderate price range',
                'premium': 'for those looking for premium quality'
            }
            response_parts.append(price_descriptions[preferences['price_preference']])
        
        if preferences.get('gender'):
            response_parts.append(f"that {preferences['gender']}s typically love")
        
        response = " ".join(response_parts) + ". Here are my top recommendations:"
        
        return response
    
    def _get_general_recommendations(self, limit=3):
        """Get general recommendations for new users"""
        # Get most popular items across all categories
        products = product_service.get_all_products()
        combos = product_service.get_all_combos()
        
        # Simple popularity-based selection
        recommendations = []
        
        # Add a combo
        if combos:
            recommendations.append({
                "id": combos[0]["id"],
                "name": combos[0]["name"],
                "price": combos[0]["price"],
                "image": combos[0]["image"],
                "description": combos[0]["description"],
                "type": "combo"
            })
        
        # Add products from different categories
        added_categories = set()
        for product in products:
            if len(recommendations) >= limit:
                break
            
            if product['category'] not in added_categories:
                recommendations.append({
                    "id": product["id"],
                    "name": product["name"],
                    "price": product["price"],
                    "image": product["image"],
                    "description": product["description"],
                    "type": "product"
                })
                added_categories.add(product['category'])
        
        return recommendations
    
    def get_analytics_summary(self):
        """Get analytics summary for admin purposes"""
        if not self.analyzed_data:
            return "No data analyzed yet."
        
        summary = {
            "total_categories": len(self.analyzed_data['category_popularity']),
            "most_popular_category": max(self.analyzed_data['category_popularity'].items(), 
                                       key=lambda x: x[1])[0],
            "age_preferences": dict(self.recommendation_rules['age_based']),
            "gender_preferences": dict(self.recommendation_rules['gender_based']),
            "price_distribution": {
                k: v['count'] for k, v in self.recommendation_rules['price_based'].items()
            }
        }
        
        return summary

# Create singleton instance
enhanced_chatbot_service = EnhancedChatbotService()