from .product_service import product_service

class ChatbotService:
    def __init__(self):
        self.occasions = ["birthday", "anniversary", "graduation", "wedding", "holiday", "christmas", 
                         "valentine's day", "mother's day", "father's day", "thank you", "congratulations"]
        self.age_groups = ["children", "kids", "teenagers", "teens", "adults", "elderly", "seniors"]
        self.relations = ["friend", "boyfriend", "girlfriend", "husband", "wife", "mom", "dad", 
                         "mother", "father", "brother", "sister", "grandparent", "colleague", "boss", "teacher"]
    
    def process_query(self, query):
        """Process user query and generate a response with recommendations"""
        query = query.lower()
        
        # Check if query is empty
        if not query.strip():
            return {
                "response": "Hello! I can help you find the perfect gift. What occasion are you shopping for?",
                "recommendations": []
            }
        
        # Identify key information from query
        occasion = self._detect_occasion(query)
        age_group = self._detect_age_group(query)
        relation = self._detect_relation(query)
        category = self._detect_category(query)
        
        # Generate recommendations based on extracted information
        recommendations = self._generate_recommendations(occasion, age_group, relation, category)
        
        # Generate response text
        response = self._generate_response(occasion, age_group, relation, category, recommendations)
        
        return {
            "response": response,
            "recommendations": recommendations
        }
    
    def _detect_occasion(self, query):
        """Detect occasion from query"""
        for occasion in self.occasions:
            if occasion in query:
                return occasion
        return None
    
    def _detect_age_group(self, query):
        """Detect age group from query"""
        for age in self.age_groups:
            if age in query:
                return age
        
        # Check for numeric ages
        import re
        age_numbers = re.findall(r'\b(\d+)\s*(?:year|yr)s?\s*old\b', query)
        if age_numbers:
            age = int(age_numbers[0])
            if age < 13:
                return "children"
            elif age < 20:
                return "teenagers"
            elif age < 65:
                return "adults"
            else:
                return "seniors"
        
        return None
    
    def _detect_relation(self, query):
        """Detect relationship from query"""
        for relation in self.relations:
            if relation in query:
                return relation
        return None
    
    def _detect_category(self, query):
        """Detect product category from query"""
        categories = product_service.get_all_categories()
        for category in categories:
            if category.lower() in query.lower():
                return category
        return None
    
    def _generate_recommendations(self, occasion, age_group, relation, category, limit=3):
        """Generate product recommendations based on detected parameters"""
        products = product_service.get_all_products()
        combos = product_service.get_all_combos()
        
        # Filter by category if specified
        if category:
            products = [p for p in products if p["category"] == category]
            combos = [c for c in combos if c["category"] == category]
        
        # Prioritize combos for specific occasions
        if occasion and occasion in ["birthday", "anniversary", "graduation", "wedding", "holiday"]:
            # First look for combos that match the occasion
            matching_combos = [c for c in combos if occasion.lower() in c["name"].lower() or 
                              occasion.lower() in c["description"].lower()]
            
            if matching_combos:
                # Return combos that match occasion
                return matching_combos[:limit]
        
        # Mix of products and combos
        recommendations = []
        
        # Add up to 2 combos
        for combo in combos[:2]:
            if len(recommendations) < limit:
                recommendations.append({
                    "id": combo["id"],
                    "name": combo["name"],
                    "price": combo["price"],
                    "image": combo["image"],
                    "description": combo["description"],
                    "type": "combo"
                })
        
        # Fill the rest with products
        for product in products:
            if len(recommendations) < limit:
                recommendations.append({
                    "id": product["id"],
                    "name": product["name"],
                    "price": product["price"],
                    "image": product["image"],
                    "description": product["description"],
                    "type": "product"
                })
        
        return recommendations
    
    def _generate_response(self, occasion, age_group, relation, category, recommendations):
        """Generate chatbot response text"""
        if not any([occasion, age_group, relation, category]) or not recommendations:
            return "I'd be happy to help you find the perfect gift! Could you tell me more about the occasion, who it's for, or what type of gift you're looking for?"
        
        response_parts = ["Here are some recommendations for you"]
        
        if occasion:
            response_parts.append(f"for {occasion}")
        
        if relation:
            response_parts.append(f"for your {relation}")
        
        if age_group:
            response_parts.append(f"in the {age_group} category")
        
        if category:
            response_parts.append(f"from our {category} collection")
        
        response = " ".join(response_parts) + "."
        
        return response

# Create singleton instance
chatbot_service = ChatbotService()