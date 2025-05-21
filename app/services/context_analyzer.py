class ContextAnalyzer:
    """Analyze conversation context and extract useful information"""
    
    def __init__(self):
        # Age-related keywords
        self.age_keywords = {
            'toddler': ['baby', 'toddler', 'infant', 'little one', '0-3', '1-3', 'ages 1', 'ages 2', 'ages 3'],
            'child': ['child', 'kid', 'young', 'little', 'elementary', 'ages 4', 'ages 5', 'ages 6', 'ages 7', 'ages 8', 'ages 9', 'ages 10', 'ages 11', 'ages 12'],
            'teen': ['teen', 'teenager', 'adolescent', 'middle school', 'high school', 'ages 13', 'ages 14', 'ages 15', 'ages 16', 'ages 17', 'ages 18', 'ages 19'],
            'adult': ['adult', 'grown-up', 'grown up', 'man', 'woman', 'guy', 'lady', 'gentleman', 'ages 20', '20s', '30s', '40s', '50s']
        }
        
        # Occasion-related keywords
        self.occasion_keywords = {
            'birthday': ['birthday', 'bday', 'b-day', 'born', 'birth', 'anniversary of birth'],
            'wedding': ['wedding', 'marriage', 'bride', 'groom', 'getting married'],
            'graduation': ['graduation', 'graduate', 'graduated', 'graduating', 'grad', 'commencement'],
            'anniversary': ['anniversary', 'married', 'wedding anniversary', 'years together'],
            'christmas': ['christmas', 'xmas', 'holiday season', 'december 25', 'santa', 'winter holiday'],
            'valentines': ['valentine', "valentine's", 'valentines', 'feb 14', 'february 14', 'romance'],
            'mothers_day': ['mother', 'mom', "mother's day", 'mothers day', 'mommy'],
            'fathers_day': ['father', 'dad', "father's day", 'fathers day', 'daddy'],
            'thanksgiving': ['thanksgiving', 'turkey day', 'thanks giving', 'november'],
            'halloween': ['halloween', 'spooky', 'costume', 'october 31', 'trick or treat'],
            'new_year': ['new year', 'years eve', 'january 1', 'year ahead'],
            'easter': ['easter', 'paschal', 'resurrection sunday'],
            'back_to_school': ['back to school', 'school year', 'semester', 'class'],
            'baby_shower': ['baby shower', 'expecting', 'pregnant', 'newborn'],
            'housewarming': ['housewarming', 'new home', 'new house', 'moved', 'moving'],
            'retirement': ['retirement', 'retired', 'retiring', 'pension'],
            'get_well': ['get well', 'recovery', 'hospital', 'sick', 'health'],
            'thank_you': ['thank you', 'thanks', 'appreciation', 'grateful'],
            'congratulations': ['congrats', 'congratulations', 'achievement', 'success', 'accomplished', 'promotion']
        }
        
        # Relationship-related keywords
        self.relationship_keywords = {
            'friend': ['friend', 'pal', 'buddy', 'mate', 'bestie', 'best friend', 'friendship'],
            'romantic_partner': ['boyfriend', 'girlfriend', 'partner', 'significant other', 'husband', 'wife', 'spouse', 'fiancé', 'fiancée', 'lover'],
            'parent': ['mom', 'mother', 'dad', 'father', 'parent', 'mother-in-law', 'father-in-law'],
            'child': ['son', 'daughter', 'child', 'stepson', 'stepdaughter'],
            'sibling': ['brother', 'sister', 'sibling', 'stepbrother', 'stepsister', 'bro', 'sis'],
            'extended_family': ['grandma', 'grandmother', 'grandpa', 'grandfather', 'grandparent', 'aunt', 'uncle', 'cousin', 'niece', 'nephew'],
            'colleague': ['colleague', 'coworker', 'boss', 'supervisor', 'manager', 'employee', 'workmate'],
            'teacher': ['teacher', 'professor', 'instructor', 'educator', 'mentor', 'tutor'],
            'acquaintance': ['acquaintance', 'neighbor', 'classmate', 'roommate']
        }
        
        # Interest-related keywords
        self.interest_keywords = {
            'art': ['art', 'drawing', 'painting', 'sketch', 'creative', 'artistic', 'crafts', 'crafting'],
            'music': ['music', 'singing', 'song', 'band', 'concert', 'instrument', 'piano', 'guitar', 'drum'],
            'sports': ['sports', 'athletic', 'exercise', 'workout', 'fitness', 'basketball', 'football', 'soccer', 'baseball', 'tennis', 'golf', 'swimming'],
            'reading': ['book', 'reading', 'novel', 'author', 'literature', 'story', 'stories'],
            'cooking': ['cooking', 'baking', 'recipe', 'chef', 'food', 'cuisine', 'kitchen'],
            'gaming': ['game', 'gaming', 'video game', 'gamer', 'play station', 'xbox', 'nintendo', 'console'],
            'technology': ['tech', 'technology', 'computer', 'programming', 'coding', 'software', 'hardware', 'gadget'],
            'fashion': ['fashion', 'clothing', 'style', 'outfit', 'dress', 'clothes', 'accessory', 'accessories'],
            'travel': ['travel', 'traveling', 'journey', 'trip', 'adventure', 'destination', 'tourist', 'tourism'],
            'gardening': ['garden', 'gardening', 'plant', 'flower', 'nature', 'outdoor', 'landscaping'],
            'movies': ['movie', 'film', 'cinema', 'theater', 'actress', 'actor', 'director', 'hollywood'],
            'science': ['science', 'scientific', 'chemistry', 'physics', 'biology', 'experiment', 'lab'],
            'history': ['history', 'historical', 'ancient', 'vintage', 'antique', 'collector'],
            'animals': ['animal', 'pet', 'dog', 'cat', 'bird', 'fish', 'wildlife', 'zoo']
        }
        
        # Budget-related keywords
        self.budget_keywords = {
            'low': ['cheap', 'inexpensive', 'low budget', 'budget', 'affordable', 'low price', 'low cost', 'under 20', 'less than 20', 'less than $20', 'under $20'],
            'medium': ['mid price', 'medium budget', 'moderate price', 'reasonable price', 'mid-range', 'around 30', 'between 20 and 50', 'between $20 and $50'],
            'high': ['expensive', 'high-end', 'premium', 'luxury', 'high quality', 'over 50', 'more than 50', 'above 50', 'over $50', 'more than $50', 'above $50']
        }
        
        # Sentiment keywords
        self.sentiment_keywords = {
            'positive': ['love', 'like', 'enjoy', 'favorite', 'interested', 'passionate', 'fascinated', 'exciting'],
            'negative': ['dislike', 'hate', 'boring', 'not interested', 'avoid', 'doesn\'t like', 'doesn\'t enjoy']
        }
    
    def analyze_query(self, query):
        """Analyze a single query for relevant information"""
        query = query.lower()
        result = {
            'age_group': self._detect_age_group(query),
            'occasion': self._detect_occasion(query),
            'relationship': self._detect_relationship(query),
            'interests': self._detect_interests(query),
            'budget': self._detect_budget(query),
            'sentiment': self._detect_sentiment(query),
            'specific_age': self._detect_specific_age(query)
        }
        return {k: v for k, v in result.items() if v}  # Remove None values
    
    def analyze_conversation(self, history):
        """Analyze full conversation history for context"""
        combined_text = ' '.join([message['parts'][0]['text'].lower() for message in history if message['role'] == 'user'])
        
        # First analyze complete conversation
        results = self.analyze_query(combined_text)
        
        # Then analyze most recent messages with higher weight
        if len(history) >= 2:
            recent_messages = history[-2:]
            recent_text = ' '.join([message['parts'][0]['text'].lower() for message in recent_messages if message['role'] == 'user'])
            recent_results = self.analyze_query(recent_text)
            
            # Recent results override earlier results
            results.update(recent_results)
        
        return results
    
    def _detect_age_group(self, text):
        """Detect age group from text"""
        for age_group, keywords in self.age_keywords.items():
            if any(keyword in text.split() or keyword in text for keyword in keywords):
                return age_group
        return None
    
    def _detect_specific_age(self, text):
        """Extract specific age numbers"""
        import re
        age_patterns = [
            r'(\d+)\s*(?:year|yr)s?\s*old',  # "10 years old", "10 yr old"
            r'(?:age|aged)\s*(\d+)',         # "age 10", "aged 10"
            r'(\d+)[- ]year[- ]old',         # "10-year-old", "10 year old"
            r'(?:turning|turned)\s*(\d+)'    # "turning 10", "turned 10"
        ]
        
        for pattern in age_patterns:
            match = re.search(pattern, text)
            if match:
                return int(match.group(1))
        return None
    
    def _detect_occasion(self, text):
        """Detect occasion from text"""
        detected = []
        for occasion, keywords in self.occasion_keywords.items():
            if any(keyword in text.split() or keyword in text for keyword in keywords):
                detected.append(occasion)
        return detected if detected else None
    
    def _detect_relationship(self, text):
        """Detect relationship from text"""
        detected = []
        for relation, keywords in self.relationship_keywords.items():
            if any(keyword in text.split() or keyword in text for keyword in keywords):
                detected.append(relation)
        return detected if detected else None
    
    def _detect_interests(self, text):
        """Detect interests from text"""
        detected = []
        for interest, keywords in self.interest_keywords.items():
            if any(keyword in text.split() or keyword in text for keyword in keywords):
                detected.append(interest)
        return detected if detected else None
    
    def _detect_budget(self, text):
        """Detect budget range from text"""
        # First check for specific dollar amounts
        import re
        amount_pattern = r'\$?\d+(?:\.\d+)?'
        amounts = re.findall(amount_pattern, text)
        
        if amounts:
            # Convert to float and find the most relevant one
            amounts = [float(amount.replace('$', '')) for amount in amounts]
            
            # Look for budget indicators near the amounts
            budget_indicators = ['budget', 'spend', 'cost', 'price', 'under', 'below', 'less than', 'around', 'about', 'approximately']
            
            for indicator in budget_indicators:
                if indicator in text:
                    # Find the closest amount to this indicator
                    indicator_pos = text.find(indicator)
                    closest_amount = None
                    min_distance = float('inf')
                    
                    for amount in amounts:
                        amount_str = str(amount)
                        if '$' + amount_str in text:
                            amount_str = '$' + amount_str
                        elif amount_str + '$' in text:
                            amount_str = amount_str + '$'
                        
                        amount_pos = text.find(amount_str)
                        distance = abs(indicator_pos - amount_pos)
                        
                        if distance < min_distance:
                            min_distance = distance
                            closest_amount = amount
                    
                    if closest_amount is not None:
                        if closest_amount < 20:
                            return 'low'
                        elif closest_amount < 50:
                            return 'medium'
                        else:
                            return 'high'
        
        # If no specific amounts, check for budget keywords
        for budget, keywords in self.budget_keywords.items():
            if any(keyword in text for keyword in keywords):
                return budget
        
        return None
    
    def _detect_sentiment(self, text):
        """Detect sentiment toward interests/activities"""
        for sentiment, keywords in self.sentiment_keywords.items():
            if any(keyword in text for keyword in keywords):
                return sentiment
        return None