class AdvancedRecommender:
    """Advanced product recommendation system"""
    
    def __init__(self, products=None, categories=None, combos=None):
        self.products = products or []
        self.categories = categories or []
        self.combos = combos or []
    
    def set_products(self, products, categories, combos):
        """Update product data"""
        self.products = products
        self.categories = categories
        self.combos = combos
    
    def get_recommendations(self, query, conversation_history, limit=3):
        """Get personalized recommendations based on conversation context"""
        try:
            # Import locally to avoid circular import
            from app.services.context_analyzer import ContextAnalyzer
            context_analyzer = ContextAnalyzer()
        except ImportError as e:
            print(f"Failed to import ContextAnalyzer: {e}")
            return self._get_basic_recommendations(limit)
        
        try:
            # Analyze the latest query
            query_analysis = context_analyzer.analyze_query(query)
            
            # Analyze the entire conversation for context  
            context_analysis = context_analyzer.analyze_conversation(conversation_history)
            
            # Combine analyses
            combined_analysis = {**context_analysis, **query_analysis}
            
            # Score and rank products
            scored_products = []
            for product in self.products:
                score = self._calculate_product_score(product, combined_analysis)
                scored_products.append((product, score, 'product'))
            
            # Score and rank combos
            for combo in self.combos:
                score = self._calculate_combo_score(combo, combined_analysis)
                scored_products.append((combo, score, 'combo'))
            
            # Sort by score
            scored_products.sort(key=lambda x: x[1], reverse=True)
            
            # Ensure diverse recommendations
            diverse_recommendations = self._ensure_diverse_recommendations(scored_products, limit)
            
            # Format recommendations for display
            formatted_recommendations = []
            for item, _, item_type in diverse_recommendations:
                formatted_recommendations.append({
                    "id": item["id"],
                    "name": item["name"],
                    "price": item["price"],
                    "image": item["image"],
                    "description": item["description"],
                    "type": item_type,
                    "relevance_scores": self._get_relevance_details(item, combined_analysis)
                })
            
            return formatted_recommendations
        except Exception as e:
            print(f"Error in get_recommendations: {e}")
            return self._get_basic_recommendations(limit)
    
    def _get_basic_recommendations(self, limit=3):
        """Fallback method when context analyzer is not available"""
        recommendations = []
        
        # Mix products and combos
        all_items = []
        for product in self.products[:limit]:
            all_items.append((product, 'product'))
        for combo in self.combos[:limit]:
            all_items.append((combo, 'combo'))
        
        # Take first few items
        for item, item_type in all_items[:limit]:
            recommendations.append({
                "id": item["id"],
                "name": item["name"],
                "price": item["price"],
                "image": item["image"],
                "description": item["description"],
                "type": item_type,
                "relevance_scores": {"suggestion": "Popular item"}
            })
        
        return recommendations
    
    def _calculate_product_score(self, product, analysis):
        """Calculate relevance score for a product based on user preferences"""
        score = 0.0
        
        # Start with base score
        base_score = 1.0
        score += base_score
        
        # Category match
        if analysis.get('interests'):
            for interest in analysis['interests']:
                if self._is_category_related_to_interest(product['category'], interest):
                    score += 2.0
        
        # Age group match
        if analysis.get('age_group'):
            age_group = analysis['age_group']
            if self._is_product_suitable_for_age(product, age_group):
                score += 1.5
        
        # Budget match
        if analysis.get('budget'):
            budget = analysis['budget']
            if self._is_product_in_budget(product, budget):
                score += 1.0
        
        # Occasion match
        if analysis.get('occasion'):
            for occasion in analysis['occasion']:
                if self._is_product_suitable_for_occasion(product, occasion):
                    score += 1.5
        
        # Relationship appropriateness
        if analysis.get('relationship'):
            for relationship in analysis['relationship']:
                if self._is_product_suitable_for_relationship(product, relationship):
                    score += 1.0
        
        return score
    
    def _calculate_combo_score(self, combo, analysis):
        """Calculate relevance score for a combo based on user preferences"""
        # Start with higher base score for combos as they're generally better gifts
        score = 2.0
        
        # Occasion match is very important for combos
        if analysis.get('occasion'):
            for occasion in analysis['occasion']:
                if self._is_combo_suitable_for_occasion(combo, occasion):
                    score += 2.5
        
        # Budget match - combos are often more expensive
        if analysis.get('budget'):
            budget = analysis['budget']
            if (budget == 'medium' and combo['price'] < 60) or (budget == 'high'):
                score += 1.5
        
        # Relationship appropriateness
        if analysis.get('relationship'):
            for relationship in analysis['relationship']:
                if self._is_combo_suitable_for_relationship(combo, relationship):
                    score += 1.5
        
        return score
    
    def _ensure_diverse_recommendations(self, scored_items, limit):
        """Ensure recommendations are diverse (not all from same category)"""
        if not scored_items:
            return []
        
        # Always include top item
        recommendations = [scored_items[0]]
        seen_categories = {scored_items[0][0].get('category')}
        
        # Handle case with very few items
        if len(scored_items) <= limit:
            return scored_items
        
        # Try to add diverse recommendations
        for item, score, item_type in scored_items[1:]:
            if len(recommendations) >= limit:
                break
                
            category = item.get('category')
            
            # If we haven't seen this category yet, or we've seen all categories
            if category not in seen_categories or len(seen_categories) >= min(3, len(self.categories)):
                recommendations.append((item, score, item_type))
                seen_categories.add(category)
        
        # If we still need more recommendations, add the highest scored remaining ones
        remaining_items = [item for item in scored_items if item not in recommendations]
        recommendations.extend(remaining_items[:limit - len(recommendations)])
        
        return recommendations[:limit]
    
    def _get_relevance_details(self, item, analysis):
        """Get detailed relevance information for user interface"""
        relevance = {}
        
        # Add relevance details
        if analysis.get('age_group'):
            if item.get('category') in self._get_suitable_categories_for_age(analysis['age_group']):
                relevance['age_match'] = f"Good for {analysis['age_group']}s"
        
        if analysis.get('interests'):
            matching_interests = []
            for interest in analysis['interests']:
                if self._is_category_related_to_interest(item.get('category'), interest):
                    matching_interests.append(interest)
            if matching_interests:
                relevance['interest_match'] = f"Matches interests: {', '.join(matching_interests)}"
        
        if analysis.get('occasion'):
            matching_occasions = []
            for occasion in analysis['occasion']:
                if self._is_product_suitable_for_occasion(item, occasion) or \
                   (item.get('type') == 'combo' and self._is_combo_suitable_for_occasion(item, occasion)):
                    matching_occasions.append(self._format_occasion_name(occasion))
            if matching_occasions:
                relevance['occasion_match'] = f"Perfect for: {', '.join(matching_occasions)}"
        
        if analysis.get('budget'):
            budget = analysis['budget']
            if self._is_product_in_budget(item, budget):
                budget_descriptions = {
                    'low': 'Budget-friendly option',
                    'medium': 'Mid-range price point',
                    'high': 'Premium quality item'
                }
                relevance['budget_match'] = budget_descriptions.get(budget, '')
        
        return relevance
    
    def _is_category_related_to_interest(self, category, interest):
        """Check if a product category is related to a user interest"""
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
        """Check if a product is suitable for an age group"""
        category = product.get('category', '')
        
        age_group_categories = {
            'toddler': ['Toys', 'Arts & Crafts'],
            'child': ['Toys', 'Arts & Crafts', 'Books', 'Sports'],
            'teen': ['Electronics', 'Books', 'Clothes', 'Sports'],
            'adult': ['Electronics', 'Books', 'Clothes', 'Sports']
        }
        
        return category in age_group_categories.get(age_group, [])
    
    def _get_suitable_categories_for_age(self, age_group):
        """Get suitable categories for an age group"""
        age_group_categories = {
            'toddler': ['Toys', 'Arts & Crafts'],
            'child': ['Toys', 'Arts & Crafts', 'Books', 'Sports'],
            'teen': ['Electronics', 'Books', 'Clothes', 'Sports'],
            'adult': ['Electronics', 'Books', 'Clothes', 'Sports']
        }
        
        return age_group_categories.get(age_group, [])
    
    def _is_product_in_budget(self, product, budget):
        """Check if a product is within a budget range"""
        price = product.get('price', 0)
        
        budget_ranges = {
            'low': (0, 20),
            'medium': (20, 50),
            'high': (50, float('inf'))
        }
        
        min_price, max_price = budget_ranges.get(budget, (0, float('inf')))
        return min_price <= price <= max_price
    
    def _is_product_suitable_for_occasion(self, product, occasion):
        """Check if a product is suitable for an occasion"""
        occasion_categories = {
            'birthday': ['Toys', 'Arts & Crafts', 'Electronics', 'Clothes'],
            'christmas': ['Toys', 'Arts & Crafts', 'Electronics', 'Books'],
            'graduation': ['Electronics', 'Books', 'Clothes'],
            'wedding': ['Home', 'Kitchen', 'Decor'],
            'anniversary': ['Jewelry', 'Fashion', 'Electronics'],
            'valentines': ['Jewelry', 'Fashion', 'Electronics'],
            'mothers_day': ['Fashion', 'Beauty', 'Home'],
            'fathers_day': ['Electronics', 'Sports', 'Tools'],
            'back_to_school': ['Books', 'Stationery', 'Electronics']
        }
        
        category = product.get('category', '')
        return category in occasion_categories.get(occasion, []) or \
               any(keyword in product.get('name', '').lower() for keyword in [occasion, self._format_occasion_name(occasion).lower()])
    
    def _is_combo_suitable_for_occasion(self, combo, occasion):
        """Check if a combo is suitable for an occasion"""
        occasion_keywords = {
            'birthday': ['birthday', 'celebration', 'special'],
            'christmas': ['christmas', 'holiday', 'festive'],
            'graduation': ['graduation', 'achievement', 'success'],
            'wedding': ['wedding', 'couple', 'love'],
            'anniversary': ['anniversary', 'love', 'romance'],
            'valentines': ['valentine', 'love', 'romance'],
            'mothers_day': ['mother', 'mom', 'mum'],
            'fathers_day': ['father', 'dad'],
            'back_to_school': ['school', 'student', 'education']
        }
        
        occasion_words = occasion_keywords.get(occasion, [])
        return any(word in combo.get('name', '').lower() for word in occasion_words) or \
               any(word in combo.get('description', '').lower() for word in occasion_words)
    
    def _is_product_suitable_for_relationship(self, product, relationship):
        """Check if a product is suitable for a relationship type"""
        relationship_categories = {
            'friend': ['Arts & Crafts', 'Books', 'Toys', 'Sports'],
            'romantic_partner': ['Electronics', 'Jewelry', 'Fashion'],
            'parent': ['Books', 'Home', 'Electronics'],
            'child': ['Toys', 'Books', 'Arts & Crafts'],
            'sibling': ['Electronics', 'Sports', 'Clothes'],
            'extended_family': ['Books', 'Home', 'Food'],
            'colleague': ['Books', 'Office', 'Stationery'],
            'teacher': ['Books', 'Office', 'Stationery']
        }
        
        category = product.get('category', '')
        return category in relationship_categories.get(relationship, [])
    
    def _is_combo_suitable_for_relationship(self, combo, relationship):
        """Check if a combo is suitable for a relationship type"""
        relationship_keywords = {
            'friend': ['friend', 'friendship', 'special'],
            'romantic_partner': ['love', 'romantic', 'special'],
            'parent': ['parent', 'mom', 'dad', 'mother', 'father'],
            'child': ['child', 'kid', 'children'],
            'sibling': ['brother', 'sister', 'sibling'],
            'extended_family': ['family', 'relative'],
            'colleague': ['colleague', 'office', 'professional'],
            'teacher': ['teacher', 'appreciation', 'thanks']
        }
        
        relationship_words = relationship_keywords.get(relationship, [])
        return any(word in combo.get('name', '').lower() for word in relationship_words) or \
               any(word in combo.get('description', '').lower() for word in relationship_words)
    
    def _format_occasion_name(self, occasion):
        """Format occasion name for display"""
        occasion_formats = {
            'birthday': 'Birthday',
            'christmas': 'Christmas',
            'graduation': 'Graduation',
            'wedding': 'Wedding',
            'anniversary': 'Anniversary',
            'valentines': "Valentine's Day",
            'mothers_day': "Mother's Day",
            'fathers_day': "Father's Day",
            'thanksgiving': 'Thanksgiving',
            'halloween': 'Halloween',
            'new_year': 'New Year',
            'easter': 'Easter',
            'back_to_school': 'Back to School',
            'baby_shower': 'Baby Shower',
            'housewarming': 'Housewarming',
            'retirement': 'Retirement',
            'get_well': 'Get Well',
            'thank_you': 'Thank You',
            'congratulations': 'Congratulations'
        }
        
        return occasion_formats.get(occasion, occasion.title())