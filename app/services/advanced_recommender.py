import re

class AdvancedRecommender:
    """FIXED: Data-driven product recommendation system with consistent results"""
    
    def __init__(self, products=None, categories=None, combos=None):
        self.products = products or []
        self.categories = categories or []
        self.combos = combos or []
        
        # Get data insights from product_service
        self.product_service = None
        
        # SMART ANALYSIS CAPABILITIES - ENHANCED INTEREST KEYWORDS
        self.smart_keywords = {
            'art': ['art', 'drawing', 'painting', 'creative', 'sketch', 'color', 'craft', 'artistic', 'create', 'coloring', 'poster'],
            'building': ['building', 'construction', 'blocks', 'build', 'assemble', 'lego', 'brick', 'tower', 'structure', 'construct', 'wooden', 'train'],
            'science': ['science', 'experiment', 'chemistry', 'STEM', 'discovery', 'lab', 'educational', 'learn'],
            'sports': ['sports', 'athletic', 'exercise', 'active', 'outdoor', 'ball', 'fitness', 'physical'],
            'music': ['music', 'singing', 'instrument', 'karaoke', 'sound', 'piano', 'guitar', 'musical'],
            'gaming': ['game', 'gaming', 'electronic', 'console', 'handheld', 'video', 'digital'],
            'reading': ['book', 'story', 'read', 'tale', 'literature', 'novel', 'stories'],
            'toys': ['toy', 'play', 'fun', 'game', 'puzzle', 'figure', 'doll', 'car', 'truck'],
            'tech': ['tech', 'technology', 'gadget', 'device', 'smart', 'bluetooth', 'digital', 'electronic']
        }
        
        # OCCASION PREFERENCES
        self.occasion_boosts = {
            'birthday': {'boost': 1.3, 'categories': ['Toys', 'Arts & Crafts', 'Electronics', 'Books']},
            'christmas': {'boost': 1.4, 'categories': ['Toys', 'Electronics', 'Books', 'Arts & Crafts']},
            'graduation': {'boost': 1.2, 'categories': ['Electronics', 'Books', 'Clothes']}
        }
    
    def set_products(self, products, categories, combos):
        """Update product data and get data insights"""
        self.products = products
        self.categories = categories
        self.combos = combos
        
        # Get reference to product_service for data insights
        try:
            from app.services.product_service import product_service
            self.product_service = product_service
            print("✅ Connected to data-driven product service")
        except ImportError:
            print("⚠️ Product service not available - using basic recommendations")
    
    def analyze_query_smart(self, query):
        """Smart query analysis with comprehensive pattern matching"""
        query_lower = query.lower()
        print(f"🔍 ANALYZING QUERY: '{query}' -> '{query_lower}'")

        # Extract budget information with comprehensive patterns
        budget_info = {}

        # RANGE budget patterns (between X and Y)
        range_budget_patterns = [
            r'between\s*(\d+(?:\.\d+)?)\$\s*and\s*(\d+(?:\.\d+)?)\$',
            r'between\s*\$(\d+(?:\.\d+)?)\s*and\s*\$(\d+(?:\.\d+)?)',
            r'from\s*(\d+(?:\.\d+)?)\$\s*to\s*(\d+(?:\.\d+)?)\$',
            r'from\s*\$(\d+(?:\.\d+)?)\s*to\s*\$(\d+(?:\.\d+)?)',
            r'(\d+(?:\.\d+)?)\$\s*to\s*(\d+(?:\.\d+)?)\$',
            r'\$(\d+(?:\.\d+)?)\s*to\s*\$(\d+(?:\.\d+)?)',
            r'between\s*(\d+(?:\.\d+)?)\s*and\s*(\d+(?:\.\d+)?)',
        ]

        max_budget_patterns = [
            r'under\s*\$?(\d+(?:\.\d+)?)',
            r'below\s*\$?(\d+(?:\.\d+)?)',
            r'less\s+than\s*\$?(\d+(?:\.\d+)?)',
            r'around\s*\$?(\d+(?:\.\d+)?)',
            r'about\s*\$?(\d+(?:\.\d+)?)',
            r'budget.*?\$?(\d+(?:\.\d+)?)',
            r'\$(\d+(?:\.\d+)?)\s*budget',
            r'max.*?\$?(\d+(?:\.\d+)?)',
            r'maximum.*?\$?(\d+(?:\.\d+)?)',
            r'within\s*\$?(\d+(?:\.\d+)?)',
            r'within\s*(\d+(?:\.\d+)?)\$',
        ]

        min_budget_patterns = [
            r'above\s*\$?(\d+(?:\.\d+)?)',
            r'over\s*\$?(\d+(?:\.\d+)?)',
            r'more\s+than\s*\$?(\d+(?:\.\d+)?)',
            r'at\s+least\s*\$?(\d+(?:\.\d+)?)',
            r'minimum.*?\$?(\d+(?:\.\d+)?)',
            r'min.*?\$?(\d+(?:\.\d+)?)',
        ]

        # Check for RANGE budget first (highest priority)
        for pattern in range_budget_patterns:
            match = re.search(pattern, query_lower)
            if match:
                min_amount = float(match.group(1))
                max_amount = float(match.group(2))
                
                if min_amount > max_amount:
                    min_amount, max_amount = max_amount, min_amount
                
                budget_info = {
                    'type': 'range',
                    'min_amount': min_amount,
                    'max_amount': max_amount,
                    'category': 'low' if max_amount <= 25 else 'medium' if max_amount <= 60 else 'high',
                    'confidence': 0.95
                }
                print(f"🔍 FOUND RANGE BUDGET: ${min_amount} - ${max_amount}")
                break

        # Check for MAXIMUM budget if no range found
        if not budget_info:
            for pattern in max_budget_patterns:
                match = re.search(pattern, query_lower)
                if match:
                    amount = float(match.group(1))
                    budget_info = {
                        'type': 'max',
                        'max_amount': amount,
                        'category': 'low' if amount <= 25 else 'medium' if amount <= 60 else 'high',
                        'confidence': 0.9
                    }
                    print(f"🔍 FOUND MAX BUDGET: ${amount}")
                    break

        # Check for MINIMUM budget if no max budget found
        if not budget_info:
            for pattern in min_budget_patterns:
                match = re.search(pattern, query_lower)
                if match:
                    amount = float(match.group(1))
                    budget_info = {
                        'type': 'min',
                        'min_amount': amount,
                        'category': 'low' if amount <= 25 else 'medium' if amount <= 60 else 'high',
                        'confidence': 0.9
                    }
                    print(f"🔍 FOUND MIN BUDGET: ${amount}")
                    break

        # Check for general dollar amounts if no specific budget found
        if not budget_info:
            dollar_pattern = r'\$(\d+(?:\.\d+)?)'
            match = re.search(dollar_pattern, query_lower)
            if match:
                amount = float(match.group(1))
                budget_info = {
                    'type': 'max',
                    'max_amount': amount,
                    'category': 'low' if amount <= 25 else 'medium' if amount <= 60 else 'high',
                    'confidence': 0.6
                }
                print(f"🔍 FOUND GENERAL BUDGET: ${amount}")

        # Budget category keywords - if no specific amount found
        if not budget_info:
            if any(word in query_lower for word in ['cheap', 'budget', 'affordable', 'inexpensive', 'low cost']):
                budget_info = {'type': 'max', 'category': 'low', 'max_amount': 25, 'confidence': 0.7}
            elif any(word in query_lower for word in ['expensive', 'premium', 'high-end', 'luxury']):
                budget_info = {'type': 'min', 'category': 'high', 'min_amount': 50, 'confidence': 0.7}

        # Extract age information
        age_info = {}
        
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
        
        if not age_info:
            age_keywords = {
                'baby': 'toddler', 'toddler': 'toddler', 'infant': 'toddler',
                'child': 'child', 'kid': 'child', 'children': 'child',
                'teenager': 'teen', 'teen': 'teen', 'adolescent': 'teen',
                'adult': 'adult', 'grown': 'adult', 'grownup': 'adult'
            }
            
            for keyword, group in age_keywords.items():
                if re.search(r'\b' + keyword + r'\b', query_lower):
                    age_info = {'group': group, 'confidence': 0.7}
                    print(f"🔍 FOUND AGE GROUP: {group} from keyword '{keyword}'")
                    break
            
            if not age_info and re.search(r'\btween\b', query_lower):
                age_info = {'group': 'tween', 'confidence': 0.7}
                print(f"🔍 FOUND AGE GROUP: tween")

        print(f"🔍 AGE DETECTION COMPLETE: {age_info}")
        
        # Extract interests with ENHANCED detection
        interests = []
        for interest, keywords in self.smart_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                interests.append(interest)
        
        # SPECIAL CASE: "building toys" should map to 'building' interest
        if 'building' in query_lower and 'toy' in query_lower:
            if 'building' not in interests:
                interests.append('building')
        
        # SPECIAL CASE: "construction" should map to 'building'  
        if 'construction' in query_lower:
            if 'building' not in interests:
                interests.append('building')
        
        print(f"🔍 DETECTED INTERESTS: {interests}")
        
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
        
        # Extract relationship information
        relationship = None
        relationships = {
            'child': ['son', 'daughter', 'child', 'kid', 'boy', 'girl', 'children'],
            'family': ['mom', 'dad', 'mother', 'father', 'sister', 'brother', 'nephew', 'niece', 'cousin'],
            'friend': ['friend', 'buddy', 'pal', 'bestie'],
            'romantic': ['boyfriend', 'girlfriend', 'husband', 'wife', 'partner']
        }

        for rel_type, keywords in relationships.items():
            if any(keyword in query_lower for keyword in keywords):
                relationship = rel_type
                print(f"🔍 FOUND RELATIONSHIP: {rel_type}")
                break
            
        # Extract gender information
        gender = None
        if any(word in query_lower for word in ['boy', 'son', 'male', 'man', 'gentleman', 'guy']):
            gender = 'male'
            print(f"🔍 FOUND GENDER: male")
        elif any(word in query_lower for word in ['girl', 'daughter', 'female', 'woman', 'lady', 'gal']):
            gender = 'female'
            print(f"🔍 FOUND GENDER: female")

        if gender and not age_info:
            if any(word in query_lower for word in ['boy', 'girl', 'son', 'daughter']):
                age_info = {'group': 'child', 'confidence': 0.7}
                print(f"🔍 INFERRED AGE GROUP: child (from gender)")

        result = {
            'age_info': age_info,
            'interests': interests,
            'budget_info': budget_info,
            'occasion': occasion,
            'relationship': relationship,
            'gender': gender
        }
        
        print(f"📊 ANALYSIS COMPLETE: {result}")
        return result

    def get_recommendations(self, query, conversation_history, limit=3):
        """FIXED: Get personalized recommendations with CONSISTENT results"""
        try:
            print(f"🔍 STARTING FIXED ANALYSIS for query: '{query}'")
            
            # Analyze current query
            current_analysis = self.analyze_query_smart(query)
            print(f"📊 CURRENT QUERY ANALYSIS: {current_analysis}")
            
            # Supplement with history if needed
            if conversation_history and len(conversation_history) > 0:
                recent_messages = []
                for msg in conversation_history[-4:]:
                    if msg.get('role') == 'user':
                        recent_messages.append(msg['parts'][0]['text'])
                
                all_text = ' '.join(recent_messages + [query])
                history_analysis = self.analyze_query_smart(all_text)
                
                final_analysis = current_analysis.copy()
                
                for key, value in history_analysis.items():
                    if not current_analysis.get(key) and value:
                        if key == 'gender':
                            gender_terms = ['male', 'female', 'boy', 'girl', 'man', 'woman', 'son', 'daughter', 'guy', 'lady']
                            if any(term in query.lower() for term in gender_terms):
                                print(f"🚫 IGNORING GENDER from history - current query mentions gender")
                                continue
                        
                        print(f"📝 SUPPLEMENTING {key} from history: {value}")
                        final_analysis[key] = value
                        
                analysis = final_analysis
            else:
                analysis = current_analysis
            
            print(f"📊 FINAL ANALYSIS USED: {analysis}")
            
            # 🎯 FIXED: Score INDIVIDUAL products first, then combos separately
            scored_products = []
            scored_combos = []
            
            # Score individual products
            for product in self.products:
                score, reasons = self._calculate_data_driven_score(product, analysis)
                scored_products.append((product, score, reasons, 'product'))
            
            # Score combos with REDUCED bonus to avoid dominating
            for combo in self.combos:
                score, reasons = self._calculate_data_driven_score(combo, analysis)
                combo_score = score * 1.05  # REDUCED from 1.2 to 1.05
                reasons.append("Special gift bundle")
                scored_combos.append((combo, combo_score, reasons, 'combo'))
            
            # 🎯 FIXED: Prioritize individual products for consistency
            all_scored = scored_products + scored_combos
            all_scored.sort(key=lambda x: x[1], reverse=True)
            
            # 🎯 FIXED: Select mostly individual products with max 1 combo
            selected_items = []
            combo_count = 0
            
            for item, score, reasons, item_type in all_scored:
                if len(selected_items) >= limit:
                    break
                
                # Limit combos to max 1
                if item_type == 'combo':
                    if combo_count >= 1:
                        continue
                    combo_count += 1
                
                selected_items.append((item, score, reasons, item_type))
            
            # If we need more items and don't have enough, fill with top products
            if len(selected_items) < limit:
                for item, score, reasons, item_type in scored_products:
                    if len(selected_items) >= limit:
                        break
                    if (item, score, reasons, item_type) not in selected_items:
                        selected_items.append((item, score, reasons, item_type))
            
            # Select diverse items from the selected pool
            diverse_items = self._select_diverse_smart(selected_items, limit)
            
            # Format with smart explanations
            return self._format_with_explanations(diverse_items, analysis)
            
        except Exception as e:
            print(f"Error in FIXED recommendations: {e}")
            return self._get_basic_recommendations(limit)
    
    def _calculate_data_driven_score(self, item, analysis):
        """ENHANCED: Calculate score using REAL historical data from product_service"""
        score = 1.0
        reasons = []
        
        # GET ITEM DETAILS
        item_name = item.get('name', '').lower()
        item_description = item.get('description', '').lower()
        item_category = item.get('category', '').lower()
        item_price = item.get('price', 0)
        
        print(f"   🔍 SCORING: {item.get('name', 'Unknown')} (${item_price})")
        
        # 🎯 DATA-DRIVEN AGE APPROPRIATENESS
        age_info = analysis.get('age_info', {})
        if age_info.get('group') and self.product_service:
            age_group = age_info['group']
            category = item.get('category', '')
            
            # Use REAL age preferences from historical data
            age_score = self.product_service.get_age_category_score(age_group, category)
            
            if age_score > 0.7:
                score *= (1 + age_score * 1.5)  # REDUCED multiplier
                if age_info.get('specific_age'):
                    reasons.append(f"Proven popular with {age_info['specific_age']}-year-olds")
                else:
                    reasons.append(f"Top choice for {age_group}s based on purchase history")
            elif age_score > 0.5:
                score *= (1 + age_score * 0.8)  # REDUCED multiplier
                reasons.append(f"Good fit for {age_group}s")
            else:
                score *= 0.9  # LESS penalty
                
            print(f"      AGE SCORE: {age_group} + {category} = {age_score:.2f} -> Score: {score:.2f}")
        
        # 🎯 DATA-DRIVEN GENDER PREFERENCES
        gender = analysis.get('gender')
        if gender and self.product_service:
            product_name = item.get('name', '')
            gender_preference = self.product_service.get_gender_preference(product_name)
            
            gender_multipliers = {
                'male': {
                    'strongly_male': 1.5, 'male_leaning': 1.2, 'neutral': 1.0,  # REDUCED multipliers
                    'female_leaning': 0.8, 'strongly_female': 0.6  # LESS penalty
                },
                'female': {
                    'strongly_female': 1.5, 'female_leaning': 1.2, 'neutral': 1.0,  # REDUCED multipliers  
                    'male_leaning': 0.8, 'strongly_male': 0.6  # LESS penalty
                }
            }
            
            if gender in gender_multipliers and gender_preference in gender_multipliers[gender]:
                multiplier = gender_multipliers[gender][gender_preference]
                score *= multiplier
                
                if multiplier >= 1.3:
                    reasons.append(f"Top choice for {gender}s (data-proven)")
                elif multiplier >= 1.1:
                    reasons.append(f"Popular with {gender}s")
                elif multiplier <= 0.7:
                    reasons.append(f"May be better for opposite gender")
            
            print(f"      GENDER SCORE: {gender} + {product_name} + {gender_preference} = {score:.2f}")
        
        # 🎯 DATA-DRIVEN CATEGORY POPULARITY  
        if self.product_service:
            category = item.get('category', '')
            category_stats = self.product_service.get_category_stats(category)
            
            popularity_boost = 1 + (category_stats['popularity_score'] * 0.2)  # REDUCED boost
            happiness_boost = 1 + ((category_stats['happiness_rate'] - 0.5) * 0.3)  # REDUCED boost
            
            score *= popularity_boost * happiness_boost
            
            if category_stats['happiness_rate'] > 0.7:
                reasons.append(f"High satisfaction category ({category_stats['total_purchases']} happy customers)")
            elif category_stats['happiness_rate'] > 0.5:
                reasons.append(f"Good customer feedback")
            
            print(f"      CATEGORY SCORE: {category} = pop:{category_stats['popularity_score']:.2f}, happy:{category_stats['happiness_rate']:.2f} -> Score: {score:.2f}")
        
        # 🎯 ENHANCED INTEREST MATCHING with stronger scoring
        interests = analysis.get('interests', [])
        interest_matched = False
        
        for interest in interests:
            if interest in self.smart_keywords:
                keywords = self.smart_keywords[interest]
                
                name_matches = sum(1 for keyword in keywords if keyword in item_name)
                desc_matches = sum(1 for keyword in keywords if keyword in item_description)
                
                if name_matches > 0:
                    score *= 4.0  # INCREASED from 2.0 for strong name match
                    reasons.append(f"Perfect match for {interest} lovers")
                    interest_matched = True
                elif desc_matches > 0:
                    score *= 2.5  # INCREASED from 1.5 for description match
                    reasons.append(f"Great for {interest} interests")
                    interest_matched = True
        
        # PENALTY for products that don't match specified interests
        if interests and not interest_matched:
            # Check if product category conflicts with interests
            item_category_lower = item_category.lower()
            
            # If user wants building toys but product is Arts & Crafts (and not building-related)
            if 'building' in interests:
                if 'arts' in item_category_lower or 'craft' in item_category_lower:
                    building_keywords = self.smart_keywords.get('building', [])
                    if not any(keyword in item_name for keyword in building_keywords):
                        score *= 0.3  # Heavy penalty for non-building Arts & Crafts
                        reasons.append("May not match building interests")
            
            # Similar logic for other interests
            elif 'art' in interests:
                if 'toy' in item_category_lower:
                    art_keywords = self.smart_keywords.get('art', [])
                    if not any(keyword in item_name for keyword in art_keywords):
                        score *= 0.4  # Penalty for non-art toys
                        reasons.append("May not match art interests")
        
        print(f"      INTEREST SCORE: {interests} + {item.get('name', 'Unknown')} = {score:.2f}")
        
        # 🎯 BUDGET ANALYSIS (Most important for consistency)
        budget_info = analysis.get('budget_info', {})
        if budget_info:
            if budget_info.get('type') == 'range':
                min_budget = budget_info['min_amount']
                max_budget = budget_info['max_amount']
                
                if min_budget <= item_price <= max_budget:
                    score *= 3.0  # STRONG boost for budget match
                    reasons.append(f"Perfect fit: ${min_budget:.0f}-${max_budget:.0f} range")
                elif item_price < min_budget:
                    score *= 0.3 if item_price < min_budget * 0.85 else 1.1
                    reasons.append("Below requested range" if item_price < min_budget * 0.85 else "Close to range")
                else:
                    score *= 0.2 if item_price > max_budget * 1.15 else 1.2
                    reasons.append("Over range" if item_price > max_budget * 1.15 else "Slightly over range")
            
            elif budget_info.get('type') == 'max':
                max_budget = budget_info['max_amount']
                if item_price <= max_budget:
                    score *= 2.5  # STRONG boost for budget match
                    reasons.append(f"Within ${max_budget:.0f} budget")
                elif item_price <= max_budget * 1.15:
                    score *= 1.2
                    reasons.append(f"Slightly over ${max_budget:.0f} budget")
                else:
                    score *= 0.1  # HEAVY penalty for way over budget
                    reasons.append(f"Over ${max_budget:.0f} budget")
            
            elif budget_info.get('type') == 'min':
                min_budget = budget_info['min_amount']
                if item_price >= min_budget:
                    score *= 2.0
                    reasons.append(f"Above ${min_budget:.0f} as requested")
                elif item_price >= min_budget * 0.85:
                    score *= 1.2
                    reasons.append(f"Close to ${min_budget:.0f} minimum")
                else:
                    score *= 0.2
                    reasons.append(f"Below ${min_budget:.0f} minimum")
        
        # 🎯 OCCASION APPROPRIATENESS
        occasion = analysis.get('occasion')
        if occasion and occasion in self.occasion_boosts:
            occasion_data = self.occasion_boosts[occasion]
            category = item.get('category', '')
            
            if category in occasion_data['categories']:
                score *= occasion_data['boost']
                reasons.append(f"Perfect for {occasion}")
        
        print(f"      FINAL SCORE: {score:.2f}")
        return score, reasons
    
    def _select_diverse_smart(self, scored_items, limit):
        """Select diverse items avoiding same category repetition"""
        if len(scored_items) <= limit:
            return scored_items
        
        selected = []
        seen_categories = set()
        
        for item, score, reasons, item_type in scored_items:
            if len(selected) >= limit:
                break
                
            category = item.get('category', 'Unknown')
            
            if (category not in seen_categories or 
                score > 6.0 or  # INCREASED threshold for high scores
                len(seen_categories) >= len(self.categories)):
                
                selected.append((item, score, reasons, item_type))
                seen_categories.add(category)
        
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
            if score > 8.0:
                confidence = "🎯 Highly recommended (data-proven)"
            elif score > 5.0:
                confidence = "✅ Excellent match"
            elif score > 3.0:
                confidence = "👍 Good choice"
            else:
                confidence = "📋 Popular option"
            
            relevance_scores = {}
            if reasons:
                relevance_scores['strengths'] = ', '.join(reasons[:2])
                relevance_scores['confidence'] = confidence
                
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
                "smart_score": round(score, 1)
            })
        
        return formatted
    
    def _get_basic_recommendations(self, limit=3):
        """Fallback recommendations when analysis fails"""
        try:
            recommendations = []
            seen_categories = set()
            
            # Prioritize individual products for basic recommendations too
            for product in self.products[:limit*2]:
                if len(recommendations) >= limit:
                    break
                    
                category = product.get('category', '')
                if category not in seen_categories or len(seen_categories) >= len(self.categories):
                    recommendations.append({
                        "id": product["id"],
                        "name": product["name"],
                        "price": product["price"],
                        "image": product["image"],
                        "description": product["description"],
                        "type": "product",
                        "relevance_scores": {"suggestion": "Popular choice"}
                    })
                    seen_categories.add(category)
        
            return recommendations[:limit]
        except:
            return []

    # LEGACY METHODS - Keep for backward compatibility
    def _get_gender_preference(self, product_name):
        """Legacy method - now uses data-driven approach"""
        if self.product_service:
            return self.product_service.get_gender_preference(product_name)
        return 'neutral'
    
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
        """Legacy method - now uses data-driven approach"""
        if self.product_service:
            category = product.get('category', '')
            return self.product_service.get_age_category_score(age_group, category) > 0.5
        
        # Fallback to simple logic
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