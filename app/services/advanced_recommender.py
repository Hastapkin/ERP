import re

class AdvancedRecommender:
    """Advanced product recommendation system - SMART UPGRADED VERSION"""
    
    def __init__(self, products=None, categories=None, combos=None):
        self.products = products or []
        self.categories = categories or []
        self.combos = combos or []
        
        # SMART ANALYSIS CAPABILITIES - NEW
        self.smart_keywords = {
            'art': ['art', 'drawing', 'painting', 'creative', 'sketch', 'color', 'craft', 'artistic', 'create'],
            'science': ['science', 'experiment', 'chemistry', 'STEM', 'discovery', 'lab', 'educational', 'learn'],
            'sports': ['sports', 'athletic', 'exercise', 'active', 'outdoor', 'ball', 'fitness', 'physical'],
            'music': ['music', 'singing', 'instrument', 'karaoke', 'sound', 'piano', 'guitar', 'musical'],
            'gaming': ['game', 'gaming', 'electronic', 'console', 'handheld', 'video', 'digital'],
            'reading': ['book', 'story', 'read', 'tale', 'literature', 'novel', 'stories'],
            'building': ['building', 'construction', 'blocks', 'build', 'assemble', 'lego'],
            'tech': ['tech', 'technology', 'gadget', 'device', 'smart', 'bluetooth', 'digital']
        }
        
        # AGE-APPROPRIATE SCORING - NEW
        self.age_scores = {
            'toddler': {'Arts & Crafts': 0.9, 'Toys': 1.0, 'Books': 0.7, 'Electronics': 0.2, 'Clothes': 0.8},
            'child': {'Arts & Crafts': 1.0, 'Toys': 1.0, 'Books': 0.9, 'Electronics': 0.4, 'Sports': 0.7, 'Clothes': 0.6},
            'tween': {'Arts & Crafts': 0.8, 'Toys': 0.9, 'Books': 0.8, 'Electronics': 0.7, 'Sports': 0.8, 'Clothes': 0.7},
            'teen': {'Electronics': 1.0, 'Clothes': 1.0, 'Arts & Crafts': 0.6, 'Books': 0.7, 'Sports': 0.8, 'Toys': 0.4},
            'adult': {'Electronics': 1.0, 'Books': 1.0, 'Arts & Crafts': 0.7, 'Clothes': 0.9, 'Sports': 0.8, 'Toys': 0.2}
        }
        
        # OCCASION PREFERENCES - NEW
        self.occasion_boosts = {
            'birthday': {'boost': 1.3, 'categories': ['Toys', 'Arts & Crafts', 'Electronics', 'Books']},
            'christmas': {'boost': 1.4, 'categories': ['Toys', 'Electronics', 'Books', 'Arts & Crafts']},
            'graduation': {'boost': 1.2, 'categories': ['Electronics', 'Books', 'Clothes']}
        }
    
    def set_products(self, products, categories, combos):
        """Update product data"""
        self.products = products
        self.categories = categories
        self.combos = combos
    
    def analyze_query_smart(self, query):
        """Smart query analysis - CORE INTELLIGENCE"""
        query_lower = query.lower()
        
        # Extract age information
        age_info = {}
        
        # Specific age patterns
        age_patterns = [
            r'(\d+)\s*(?:year|yr)s?\s*old',
            r'age\s*(\d+)',
            r'(\d+)[- ]year[- ]old'
        ]
        
        for pattern in age_patterns:
            match = re.search(pattern, query_lower)
            if match:
                age = int(match.group(1))
                if age <= 3:
                    age_info = {'group': 'toddler', 'specific_age': age, 'confidence': 0.9}
                elif age <= 8:
                    age_info = {'group': 'child', 'specific_age': age, 'confidence': 0.9}
                elif age <= 12:
                    age_info = {'group': 'tween', 'specific_age': age, 'confidence': 0.9}
                elif age <= 17:
                    age_info = {'group': 'teen', 'specific_age': age, 'confidence': 0.9}
                else:
                    age_info = {'group': 'adult', 'specific_age': age, 'confidence': 0.9}
                break
        
        # Age group keywords if no specific age found
        if not age_info:
            age_keywords = {
                'baby': 'toddler', 'toddler': 'toddler', 'infant': 'toddler',
                'child': 'child', 'kid': 'child', 'children': 'child',
                'tween': 'tween', 'preteen': 'tween',
                'teen': 'teen', 'teenager': 'teen', 'adolescent': 'teen',
                'adult': 'adult', 'grown': 'adult'
            }
            
            for keyword, group in age_keywords.items():
                if keyword in query_lower:
                    age_info = {'group': group, 'confidence': 0.7}
                    break
        
        # Extract interests
        interests = []
        for interest, keywords in self.smart_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                interests.append(interest)
        
        # Extract budget information
        budget_info = {}
        budget_patterns = [
            r'under\s*\$?(\d+)',
            r'below\s*\$?(\d+)',
            r'less\s+than\s*\$?(\d+)',
            r'around\s*\$?(\d+)',
            r'about\s*\$?(\d+)',
            r'budget.*?\$?(\d+)',
            r'\$(\d+)'
        ]
        
        for pattern in budget_patterns:
            match = re.search(pattern, query_lower)
            if match:
                amount = float(match.group(1))
                budget_info = {
                    'max_amount': amount,
                    'category': 'low' if amount <= 25 else 'medium' if amount <= 60 else 'high',
                    'confidence': 0.8
                }
                break
        
        # Budget category keywords
        if not budget_info:
            if any(word in query_lower for word in ['cheap', 'budget', 'affordable', 'inexpensive']):
                budget_info = {'category': 'low', 'confidence': 0.6}
            elif any(word in query_lower for word in ['expensive', 'premium', 'high-end', 'luxury']):
                budget_info = {'category': 'high', 'confidence': 0.6}
        
        # Extract occasion
        occasion = None
        occasions = {
            'birthday': ['birthday', 'bday', 'b-day', 'born'],
            'christmas': ['christmas', 'xmas', 'holiday', 'festive'],
            'graduation': ['graduation', 'graduate', 'grad', 'commencement']
        }
        
        for occ, keywords in occasions.items():
            if any(keyword in query_lower for keyword in keywords):
                occasion = occ
                break
        
        # Extract relationship
        relationship = None
        relationships = {
            'child': ['son', 'daughter', 'child', 'kid'],
            'family': ['mom', 'dad', 'mother', 'father', 'sister', 'brother', 'nephew', 'niece', 'cousin'],
            'friend': ['friend', 'buddy', 'pal', 'bestie'],
            'romantic': ['boyfriend', 'girlfriend', 'husband', 'wife', 'partner']
        }
        
        for rel_type, keywords in relationships.items():
            if any(keyword in query_lower for keyword in keywords):
                relationship = rel_type
                break
        
        return {
            'age_info': age_info,
            'interests': interests,
            'budget_info': budget_info,
            'occasion': occasion,
            'relationship': relationship
        }

    def get_recommendations(self, query, conversation_history, limit=3):
        """Get personalized recommendations with smart analysis - UPGRADED CORE METHOD"""
        try:
            # Analyze conversation history for additional context
            all_text = query
            if conversation_history and len(conversation_history) > 0:
                # Get recent user messages for context
                recent_messages = []
                for msg in conversation_history[-6:]:  # Last 3 exchanges
                    if msg.get('role') == 'user':
                        recent_messages.append(msg['parts'][0]['text'])
                
                # Combine with current query for analysis
                all_text = ' '.join(recent_messages + [query])
            
            # Smart analysis of combined context
            analysis = self.analyze_query_smart(all_text)
            
            # Score all products with smart logic
            scored_products = []
            for product in self.products:
                score, reasons = self._calculate_smart_score(product, analysis)
                scored_products.append((product, score, reasons, 'product'))
            
            # Score combos with bonus
            for combo in self.combos:
                score, reasons = self._calculate_smart_score(combo, analysis)
                combo_score = score * 1.2  # Combo bonus
                reasons.append("Special gift bundle")
                scored_products.append((combo, combo_score, reasons, 'combo'))
            
            # Sort by score
            scored_products.sort(key=lambda x: x[1], reverse=True)
            
            # Select diverse items avoiding same category
            diverse_items = self._select_diverse_smart(scored_products, limit)
            
            # Format with smart explanations
            return self._format_with_explanations(diverse_items, analysis)
            
        except Exception as e:
            print(f"Error in smart recommendations: {e}")
            return self._get_basic_recommendations(limit)
    
    def _calculate_smart_score(self, item, analysis):
        """Calculate smart score for item with detailed reasoning"""
        score = 1.0
        reasons = []
        
        # Age appropriateness scoring
        age_info = analysis.get('age_info', {})
        if age_info.get('group'):
            age_group = age_info['group']
            category = item.get('category', '')
            
            if age_group in self.age_scores and category in self.age_scores[age_group]:
                age_score = self.age_scores[age_group][category]
                score *= (1 + age_score)
                
                if age_score > 0.7:
                    if age_info.get('specific_age'):
                        reasons.append(f"Great for {age_info['specific_age']}-year-olds")
                    else:
                        reasons.append(f"Perfect for {age_group}s")
        
        # Interest matching scoring
        interests = analysis.get('interests', [])
        item_name = item.get('name', '').lower()
        item_description = item.get('description', '').lower()
        
        for interest in interests:
            if interest in self.smart_keywords:
                keywords = self.smart_keywords[interest]
                
                # Check name and description for interest keywords
                name_matches = sum(1 for keyword in keywords if keyword in item_name)
                desc_matches = sum(1 for keyword in keywords if keyword in item_description)
                
                if name_matches > 0:
                    score *= 2.5  # Strong boost for name match
                    reasons.append(f"Perfect for {interest} lovers")
                elif desc_matches > 0:
                    score *= 1.8  # Good boost for description match
                    reasons.append(f"Great for {interest} interests")
        
        # Budget compatibility scoring
        budget_info = analysis.get('budget_info', {})
        item_price = item.get('price', 0)
        
        if budget_info.get('max_amount'):
            max_budget = budget_info['max_amount']
            if item_price <= max_budget:
                score *= 1.5  # Boost for within budget
                reasons.append(f"Within ${max_budget:.0f} budget")
            elif item_price <= max_budget * 1.1:  # Slightly over budget
                score *= 1.2
                reasons.append(f"Close to ${max_budget:.0f} budget")
            elif item_price > max_budget * 1.3:  # Way over budget
                score *= 0.3  # Heavy penalty
        
        elif budget_info.get('category'):
            budget_cat = budget_info['category']
            if budget_cat == 'low' and item_price <= 25:
                score *= 1.3
                reasons.append("Budget-friendly option")
            elif budget_cat == 'medium' and 20 <= item_price <= 60:
                score *= 1.2
                reasons.append("Good value for money")
            elif budget_cat == 'high' and item_price >= 50:
                score *= 1.1
                reasons.append("Premium quality item")
        
        # Occasion appropriateness
        occasion = analysis.get('occasion')
        if occasion and occasion in self.occasion_boosts:
            occasion_data = self.occasion_boosts[occasion]
            category = item.get('category', '')
            
            if category in occasion_data['categories']:
                score *= occasion_data['boost']
                reasons.append(f"Perfect for {occasion}")
        
        # Relationship appropriateness
        relationship = analysis.get('relationship')
        if relationship:
            if relationship == 'child' and any(word in item_name for word in ['kid', 'child', 'young']):
                score *= 1.2
                reasons.append("Great for kids")
            elif relationship == 'teen' and item.get('category') in ['Electronics', 'Clothes']:
                score *= 1.1
                reasons.append("Teen-appropriate")
        
        return score, reasons
    
    def _select_diverse_smart(self, scored_items, limit):
        """Select diverse items avoiding same category repetition"""
        if len(scored_items) <= limit:
            return scored_items
        
        selected = []
        seen_categories = set()
        
        # First pass: Select high-scoring items from different categories
        for item, score, reasons, item_type in scored_items:
            if len(selected) >= limit:
                break
                
            category = item.get('category', 'Unknown')
            
            # Prefer diversity but allow same category if score is significantly higher
            if (category not in seen_categories or 
                score > 4.0 or  # Very high score overrides diversity
                len(seen_categories) >= len(self.categories)):  # All categories seen
                
                selected.append((item, score, reasons, item_type))
                seen_categories.add(category)
        
        # Second pass: Fill remaining slots with highest scoring items
        for item, score, reasons, item_type in scored_items:
            if len(selected) >= limit:
                break
            if (item, score, reasons, item_type) not in selected:
                selected.append((item, score, reasons, item_type))
        
        return selected[:limit]
    
    def _format_with_explanations(self, items, analysis):
        """Format items with smart explanations and confidence levels"""
        formatted = []
        
        for item, score, reasons, item_type in items:
            # Determine confidence level based on score
            if score > 5.0:
                confidence = "Highly recommended"
            elif score > 3.0:
                confidence = "Good match"
            elif score > 2.0:
                confidence = "Consider this option"
            else:
                confidence = "Popular choice"
            
            # Create relevance explanation
            relevance_scores = {}
            if reasons:
                # Use top 2 reasons for strengths
                relevance_scores['strengths'] = ', '.join(reasons[:2])
                relevance_scores['confidence'] = confidence
                
                # Add considerations if any
                if len(reasons) > 2:
                    relevance_scores['additional'] = ', '.join(reasons[2:3])
            else:
                relevance_scores['suggestion'] = "Popular choice"
                relevance_scores['confidence'] = confidence
            
            formatted.append({
                "id": item["id"],
                "name": item["name"],
                "price": item["price"],
                "image": item["image"],
                "description": item["description"],
                "type": item_type,
                "relevance_scores": relevance_scores,
                "smart_score": round(score, 1)  # For debugging
            })
        
        return formatted
    
    def _get_basic_recommendations(self, limit=3):
        """Fallback recommendations when analysis fails"""
        try:
            recommendations = []
            
            # Get variety of products and combos
            seen_categories = set()
            all_items = []
            
            # Add products
            for product in self.products[:limit*2]:
                all_items.append((product, 'product'))
            
            # Add combos
            for combo in self.combos[:limit]:
                all_items.append((combo, 'combo'))
            
            # Select diverse items
            for item, item_type in all_items:
                if len(recommendations) >= limit:
                    break
                    
                category = item.get('category', '')
                if category not in seen_categories or len(seen_categories) >= len(self.categories):
                    recommendations.append({
                        "id": item["id"],
                        "name": item["name"],
                        "price": item["price"],
                        "image": item["image"],
                        "description": item["description"],
                        "type": item_type,
                        "relevance_scores": {"suggestion": "Popular choice"}
                    })
                    seen_categories.add(category)
        
            return recommendations[:limit]
        except:
            return []

    # LEGACY METHODS - Keep for backward compatibility
    def _is_category_related_to_interest(self, category, interest):
        """Legacy method - kept for compatibility"""
        category_to_interest_map = {
            'Arts & Crafts': ['art', 'creative', 'drawing', 'painting'],
            'Toys': ['gaming', 'play', 'fun', 'children'],
            'Books': ['reading', 'knowledge', 'education', 'learning'],
            'Electronics': ['technology', 'gaming', 'music', 'movies'],
            'Clothes': ['fashion', 'style', 'clothing'],
            'Sports': ['sports', 'fitness', 'outdoors', 'exercise']
        }
        
        if not category:
            return False
            
        return interest in category_to_interest_map.get(category, []) or interest.lower() in category.lower()
    
    def _is_product_suitable_for_age(self, product, age_group):
        """Legacy method - kept for compatibility"""
        category = product.get('category', '')
        
        age_group_categories = {
            'toddler': ['Toys', 'Arts & Crafts'],
            'child': ['Toys', 'Arts & Crafts', 'Books', 'Sports'],
            'teen': ['Electronics', 'Books', 'Clothes', 'Sports'],
            'adult': ['Electronics', 'Books', 'Clothes', 'Sports']
        }
        
        return category in age_group_categories.get(age_group, [])
    
    def _is_product_in_budget(self, product, budget):
        """Legacy method - kept for compatibility"""
        price = product.get('price', 0)
        
        budget_ranges = {
            'low': (0, 25),
            'medium': (20, 60),
            'high': (50, float('inf'))
        }
        
        min_price, max_price = budget_ranges.get(budget, (0, float('inf')))
        return min_price <= price <= max_price