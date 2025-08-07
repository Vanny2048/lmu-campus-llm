import streamlit as st
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
import random
from typing import Dict, List, Any, Tuple
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedLMUBuddyV2:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.data = self.load_lmu_data()
        self.reddit_data = self.load_reddit_data()
        self.rmp_data = self.load_rmp_data()
        
        # Initialize LMU tea before computing embeddings
        self.lmu_tea = {
            'campus_landmarks': [
                "Malone? Girl that building smells like burnt circuits fr fr",
                "HLP is giving Hogwarts vibes with all those stairs",
                "The bluff views are literally unmatched, especially at sunset",
                "Sacred Heart Chapel is peaceful but the bells are LOUD",
                "Burns Fine Arts rooftop has the best sunset views period",
                "The library's 3rd floor is the quietest spot on campus",
                "The meditation garden behind Sacred Heart is so underrated"
            ],
            'caf_reviews': [
                "The omelette guy is the only reason I wake up for breakfast",
                "That pasta line better be worth it today",
                "The smoothie bowls at Lion's Den are actually fire",
                "Pizza at the Lair is mid but the garlic knots? *chef's kiss*",
                "Coffee at Starbucks is overpriced but the line is always long",
                "The salad bar is actually pretty good ngl",
                "Breakfast burritos are the move before 8am classes"
            ],
            'dorm_rumors': [
                "Nobody uses the showers on 2nd floor Hannon because ghost",
                "McCarthy thinks they're better than Del Rey but ok 👀",
                "Doheny has the best views but the elevators are always broken",
                "Palm South is lowkey the best dorm for social life",
                "Rosecrans is quiet but the rooms are actually nice",
                "Hannon 4th floor has the best study lounges",
                "Del Rey South has the best food options nearby"
            ],
            'professor_tea': [
                "If you're taking Calc with Bro. Martin… godspeed",
                "Dr. Walsh is cool if you participate, mid if you don't",
                "The Film School professors are actually industry legends",
                "Business professors are hit or miss but mostly hit",
                "Psychology professors are all pretty chill",
                "Engineering professors are tough but fair",
                "English professors are passionate but grade hard"
            ],
            'events_opinions': [
                "TNL lineup lookin mid this week but maybe free pizza?",
                "Basketball games are actually so fun, the energy is unmatched",
                "Greek life mixers are chaotic but in a good way",
                "Cultural events are always well-organized and interesting",
                "The farmers market on Sundays is a vibe",
                "Movie nights on the bluff are underrated",
                "Career fairs are stressful but necessary"
            ],
            'admin_complaints': [
                "They said cura personalis but my advising appointment is 3 weeks out???",
                "Parking is literally the worst, I'm always late to class",
                "Registration is a nightmare every semester",
                "The wifi in Malone is actually unusable",
                "Why are the printers always broken?",
                "The bookstore is overpriced, Amazon is the move",
                "Advising office never answers their phone"
            ],
            'campus_slang': [
                "The bluff life hits different",
                "Bluff vibes are unmatched",
                "HLP = Hannon Library Problems",
                "Malone moment = when technology fails you",
                "Bluff culture = the unique LMU experience",
                "Cura personalis = care for the whole person (but not your schedule)",
                "Lion's Den = the best food spot on campus",
                "The Lair = main dining and social hub"
            ]
        }
        
        self.embeddings = self.load_or_compute_embeddings()
        self.conversation_history = []
        self.user_preferences = {}
        self.user_context = {
            'name': None,
            'clubs': [],
            'major': None,
            'year': None,
            'favorite_topics': [],
            'recent_queries': [],
            'dorm': None,
            'tone_preference': 'neutral'
        }
        
        # Enhanced tone detection patterns
        self.tone_patterns = {
            'casual': {
                'indicators': [
                    r'\b(yo|hey|sup|what\'s up|wassup|fr fr|literally|actually|honestly|ngl|tbh|imo|idk|lol|omg|wtf|fml|smh)\b',
                    r'\b(bro|sis|girl|dude|fam|bestie|queen|king|slay|vibe|mood|tea|gossip|drama|beef|mid|fire|lit|bussin|no cap|period)\b',
                    r'[!]{2,}',  # Multiple exclamation marks
                    r'[?]{2,}',  # Multiple question marks
                    r'[A-Z]{3,}',  # ALL CAPS
                    r'[a-z]+[A-Z]+[a-z]+',  # camelCase
                    r'[0-9]+[a-z]+',  # numbers with letters
                ],
                'emoji_usage': ['🔥', '✨', '💯', '👏', '🎉', '😭', '😤', '😩', '😍', '🤡', '💀', '😅', '😭', '😤', '😩', '😍', '🤡', '💀', '😅'],
                'sentence_endings': ['!', '...', '??', '!!!', '?!', '!?'],
                'contractions': ['don\'t', 'can\'t', 'won\'t', 'it\'s', 'that\'s', 'you\'re', 'they\'re', 'we\'re', 'i\'m', 'he\'s', 'she\'s']
            },
            'formal': {
                'indicators': [
                    r'\b(indeed|certainly|precisely|undoubtedly|furthermore|moreover|consequently|therefore|thus|hence|accordingly)\b',
                    r'\b(respectfully|professionally|appropriately|adequately|sufficiently|comprehensively|thoroughly)\b',
                    r'[A-Z][a-z]+ [A-Z][a-z]+',  # Proper nouns
                    r'\b(Mr\.|Mrs\.|Dr\.|Prof\.|Professor|University|Department|Administration)\b',
                    r'[;:]',  # Semicolons and colons
                    r'[()]',  # Parentheses
                    r'\b(approximately|approximately|approximately|approximately)\b'
                ],
                'emoji_usage': [],
                'sentence_endings': ['.'],
                'contractions': []
            },
            'academic': {
                'indicators': [
                    r'\b(research|study|analysis|methodology|hypothesis|conclusion|evidence|data|statistics|correlation|causation)\b',
                    r'\b(according to|based on|research shows|studies indicate|evidence suggests|data reveals)\b',
                    r'\b(however|nevertheless|nonetheless|conversely|alternatively|similarly|likewise)\b',
                    r'[0-9]+%',  # Percentages
                    r'\b(et al\.|i\.e\.|e\.g\.|vs\.|etc\.)\b',
                    r'[[]\d+[]]',  # Citations
                ],
                'emoji_usage': [],
                'sentence_endings': ['.'],
                'contractions': []
            }
        }
        
        # LMU-specific authentic knowledge from Reddit/RMP
        # (Already initialized in __init__)
        
        # Gen-Z personality traits
        self.genz_personality = {
            'greetings': ['Yo!', 'Hey bestie!', 'What\'s good?', 'Sup!', 'Hey there!', 'What\'s up?'],
            'excitement': ['🔥', '✨', '💯', '👏', '🎉', '😭', '😤', '😩', '😍', '🤡', '💀', '😅'],
            'agreement': ['Facts!', 'Period!', 'No cap!', 'Literally!', 'Actually!', 'Honestly!', 'Fr fr!'],
            'emphasis': ['literally', 'actually', 'honestly', 'fr fr', 'no cap', 'period', 'slay'],
            'disagreement': ['Nah', 'Not really', 'I mean...', 'Kinda', 'Mid', 'Meh'],
            'surprise': ['Wait what?', 'No way!', 'Shut up!', 'Stop it!', 'You\'re kidding!'],
            'filler_words': ['like', 'literally', 'actually', 'honestly', 'basically', 'obviously', 'clearly'],
            'slang': ['tea', 'gossip', 'drama', 'beef', 'vibe', 'mood', 'slay', 'queen', 'king', 'bestie', 'fam', 'bro', 'sis', 'girl', 'dude']
        }
        
        # Event emoji mapping
        self.event_emojis = {
            'arts': '🎭', 'music': '🎵', 'sports': '🏀', 'academic': '📚', 'social': '🎉',
            'cultural': '🌍', 'professional': '💼', 'spiritual': '🙏', 'food': '🍕',
            'movie': '🎬', 'workshop': '🔧', 'lecture': '🎤', 'party': '🎊', 'meeting': '🤝'
        }
    
    def load_lmu_data(self):
        """Load existing LMU data"""
        try:
            with open('enhanced_lmu_data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning("enhanced_lmu_data.json not found, using default data")
            return self.create_default_data()
    
    def load_reddit_data(self):
        """Load Reddit scraped data"""
        try:
            with open('lmu_reddit_data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning("lmu_reddit_data.json not found, using default tea")
            return {'campus_tea': [], 'slang': []}
    
    def load_rmp_data(self):
        """Load RateMyProfessors scraped data"""
        try:
            with open('lmu_rmp_data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning("lmu_rmp_data.json not found, using default professor data")
            return {'professors': [], 'professor_tea': []}
    
    def create_default_data(self):
        """Create default LMU data structure"""
        return {
            'professors': [],
            'courses': [],
            'dining': [],
            'housing': [],
            'events': [],
            'organizations': [],
            'facilities': [],
            'news': []
        }
    
    def load_or_compute_embeddings(self):
        """Load or compute embeddings for semantic search"""
        try:
            with open('lmu_embeddings.pkl', 'rb') as f:
                data = pickle.load(f)
                # Handle both old and new format
                if isinstance(data, dict):
                    return data
                else:
                    # Old format, recompute
                    return self.compute_embeddings()
        except FileNotFoundError:
            return self.compute_embeddings()
    
    def compute_embeddings(self):
        """Compute embeddings for all LMU data"""
        logger.info("Computing embeddings for LMU data...")
        
        all_texts = []
        text_mapping = []
        
        # Add existing data
        for category, items in self.data.items():
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict):
                        text = ' '.join(str(v) for v in item.values() if v)
                        all_texts.append(text)
                        text_mapping.append({'category': category, 'item': item})
        
        # Add Reddit tea
        for tea in self.reddit_data.get('campus_tea', []):
            text = f"{tea.get('content', '')} {tea.get('details', '')}"
            all_texts.append(text)
            text_mapping.append({'category': 'reddit_tea', 'item': tea})
        
        # Add RMP professor tea
        for tea in self.rmp_data.get('professor_tea', []):
            text = f"{tea.get('professor', '')} {tea.get('tea_content', '')} {tea.get('details', '')}"
            all_texts.append(text)
            text_mapping.append({'category': 'rmp_tea', 'item': tea})
        
        # Add LMU tea
        for category, items in self.lmu_tea.items():
            for item in items:
                all_texts.append(item)
                text_mapping.append({'category': f'lmu_tea_{category}', 'item': item})
        
        if not all_texts:
            return {'embeddings': [], 'mapping': []}
        
        # Compute embeddings
        embeddings = self.model.encode(all_texts)
        
        # Save embeddings
        with open('lmu_embeddings.pkl', 'wb') as f:
            pickle.dump({'embeddings': embeddings, 'mapping': text_mapping}, f)
        
        return {'embeddings': embeddings, 'mapping': text_mapping}
    
    def analyze_user_tone(self, user_input: str) -> Dict[str, float]:
        """Advanced tone analysis using multiple indicators"""
        text = user_input.lower()
        
        tone_scores = {
            'casual': 0.0,
            'formal': 0.0,
            'academic': 0.0
        }
        
        # Analyze patterns for each tone
        for tone, patterns in self.tone_patterns.items():
            score = 0.0
            
            # Check indicators
            for pattern in patterns['indicators']:
                try:
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    score += len(matches) * 0.1
                except re.error:
                    # Skip invalid regex patterns
                    continue
            
            # Check emoji usage
            emoji_count = sum(1 for emoji in patterns['emoji_usage'] if emoji in user_input)
            score += emoji_count * 0.2
            
            # Check sentence endings
            for ending in patterns['sentence_endings']:
                if ending in user_input:
                    score += 0.1
            
            # Check contractions
            contraction_count = sum(1 for contraction in patterns['contractions'] if contraction in text)
            score += contraction_count * 0.05
            
            # Check ALL CAPS
            caps_count = len(re.findall(r'[A-Z]{3,}', user_input))
            score += caps_count * 0.1
            
            # Check exclamation/question marks
            exclamation_count = user_input.count('!')
            question_count = user_input.count('?')
            score += (exclamation_count + question_count) * 0.05
            
            tone_scores[tone] = min(score, 1.0)  # Cap at 1.0
        
        # Normalize scores
        total_score = sum(tone_scores.values())
        if total_score > 0:
            tone_scores = {k: v/total_score for k, v in tone_scores.items()}
        
        return tone_scores
    
    def get_dominant_tone(self, tone_scores: Dict[str, float]) -> str:
        """Get the dominant tone from scores"""
        if not tone_scores:
            return 'neutral'
        
        max_tone = max(tone_scores.items(), key=lambda x: x[1])
        if max_tone[1] > 0.4:  # Threshold for dominant tone
            return max_tone[0]
        return 'neutral'
    
    def mirror_user_tone(self, user_input: str, response: str) -> str:
        """Mirror the user's tone in the response"""
        tone_scores = self.analyze_user_tone(user_input)
        dominant_tone = self.get_dominant_tone(tone_scores)
        
        # Adjust response based on tone
        if dominant_tone == 'casual':
            response = self.make_casual(response)
        elif dominant_tone == 'formal':
            response = self.make_formal(response)
        elif dominant_tone == 'academic':
            response = self.make_academic(response)
        
        return response
    
    def make_casual(self, text: str) -> str:
        """Make text more casual and Gen-Z like"""
        # Add casual greetings
        greetings = random.choice(self.genz_personality['greetings'])
        
        # Add emojis
        emojis = random.sample(self.genz_personality['excitement'], min(3, len(self.genz_personality['excitement'])))
        
        # Add filler words
        filler_words = random.sample(self.genz_personality['filler_words'], min(2, len(self.genz_personality['filler_words'])))
        
        # Add emphasis
        emphasis = random.choice(self.genz_personality['emphasis'])
        
        # Transform text
        text = f"{greetings} {text}"
        
        # Add emojis at the end
        text += f" {' '.join(emojis)}"
        
        # Add emphasis
        if random.random() < 0.3:
            text += f" {emphasis}!"
        
        return text
    
    def make_formal(self, text: str) -> str:
        """Make text more formal"""
        # Remove casual elements
        text = re.sub(r'[!]{2,}', '.', text)  # Replace multiple ! with .
        text = re.sub(r'[?]{2,}', '?', text)  # Replace multiple ? with single ?
        
        # Add formal elements
        formal_starters = ['Indeed,', 'Certainly,', 'I understand that', 'It appears that']
        if random.random() < 0.3:
            text = f"{random.choice(formal_starters)} {text.lower()}"
        
        return text
    
    def make_academic(self, text: str) -> str:
        """Make text more academic"""
        # Add academic connectors
        connectors = ['Furthermore,', 'Moreover,', 'Additionally,', 'It should be noted that']
        if random.random() < 0.3:
            text = f"{random.choice(connectors)} {text}"
        
        return text
    
    def get_authentic_lmu_tea(self, query: str) -> str:
        """Get authentic LMU tea based on query"""
        query_lower = query.lower()
        
        # Check for specific topics
        if any(word in query_lower for word in ['malone', 'building', 'smell', 'circuit']):
            return random.choice(self.lmu_tea['campus_landmarks'])
        
        if any(word in query_lower for word in ['caf', 'food', 'dining', 'lair', 'pizza', 'omelette']):
            return random.choice(self.lmu_tea['caf_reviews'])
        
        if any(word in query_lower for word in ['dorm', 'roommate', 'hannon', 'mccarthy', 'del rey', 'ghost']):
            return random.choice(self.lmu_tea['dorm_rumors'])
        
        if any(word in query_lower for word in ['professor', 'prof', 'teacher', 'bro martin', 'dr walsh']):
            return random.choice(self.lmu_tea['professor_tea'])
        
        if any(word in query_lower for word in ['tnl', 'event', 'party', 'basketball', 'game']):
            return random.choice(self.lmu_tea['events_opinions'])
        
        if any(word in query_lower for word in ['admin', 'advising', 'registration', 'parking', 'wifi']):
            return random.choice(self.lmu_tea['admin_complaints'])
        
        if any(word in query_lower for word in ['bluff', 'lmu', 'campus', 'culture', 'slang']):
            return random.choice(self.lmu_tea['campus_slang'])
        
        # Return random tea if no specific match
        all_tea = []
        for category, items in self.lmu_tea.items():
            all_tea.extend(items)
        
        return random.choice(all_tea) if all_tea else "LMU is literally the best campus ever! 🔥"
    
    def semantic_search(self, query: str, top_k: int = 3) -> List[Dict]:
        """Enhanced semantic search with Reddit and RMP data"""
        if not self.embeddings or not isinstance(self.embeddings, dict) or 'embeddings' not in self.embeddings:
            return []
        
        # Encode query
        query_embedding = self.model.encode([query])
        
        # Compute similarities
        similarities = cosine_similarity(query_embedding, self.embeddings['embeddings'])[0]
        
        # Get top matches
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.3:  # Threshold for relevance
                mapping = self.embeddings['mapping'][idx]
                results.append({
                    'category': mapping['category'],
                    'item': mapping['item'],
                    'similarity': float(similarities[idx])
                })
        
        return results
    
    def generate_response(self, user_input: str) -> str:
        """Generate enhanced response with tone mirroring and authentic LMU knowledge"""
        # Analyze user tone
        tone_scores = self.analyze_user_tone(user_input)
        dominant_tone = self.get_dominant_tone(tone_scores)
        
        # Update user context
        self.extract_user_context(user_input)
        
        # Get relevant information
        search_results = self.semantic_search(user_input)
        
        # Generate base response
        response = self.generate_base_response(user_input, search_results, dominant_tone)
        
        # Add authentic LMU tea
        if random.random() < 0.4:  # 40% chance to add tea
            tea = self.get_authentic_lmu_tea(user_input)
            response += f"\n\n{tea}"
        
        # Mirror user tone
        response = self.mirror_user_tone(user_input, response)
        
        # Add conversation history
        self.conversation_history.append({
            'user': user_input,
            'assistant': response,
            'tone': dominant_tone,
            'timestamp': datetime.now().isoformat()
        })
        
        return response
    
    def generate_base_response(self, user_input: str, search_results: List[Dict], tone: str) -> str:
        """Generate base response based on search results and tone"""
        query_lower = user_input.lower()
        
        # Handle specific query types
        if any(word in query_lower for word in ['professor', 'prof', 'teacher']):
            return self.handle_professor_query(user_input, tone)
        
        if any(word in query_lower for word in ['food', 'eat', 'dining', 'caf', 'lair']):
            return self.handle_dining_query(user_input, tone)
        
        if any(word in query_lower for word in ['dorm', 'housing', 'room', 'live']):
            return self.handle_housing_query(user_input, tone)
        
        if any(word in query_lower for word in ['event', 'party', 'tnl', 'weekend']):
            return self.handle_event_query(user_input, tone)
        
        if any(word in query_lower for word in ['study', 'library', 'quiet', 'spot']):
            return self.handle_study_query(user_input, tone)
        
        # Use search results if available
        if search_results:
            best_result = search_results[0]
            if best_result['similarity'] > 0.5:
                return self.format_search_result(best_result, tone)
        
        # Fallback to general response
        return self.handle_general_query(user_input, tone)
    
    def handle_professor_query(self, user_input: str, tone: str) -> str:
        """Handle professor-related queries with RMP data"""
        # Check RMP data first
        if self.rmp_data.get('professor_tea'):
            tea = random.choice(self.rmp_data['professor_tea'])
            return f"Omg {tea['tea_content']}! {tea['details']}"
        
        # Fallback to existing data
        professors = self.data.get('professors', [])
        if professors:
            prof = random.choice(professors)
            return f"Professor {prof.get('name', 'Unknown')} in {prof.get('department', 'Unknown')} is pretty solid! They teach {', '.join(prof.get('courses', [])[:2])}"
        
        return "Professors here are generally pretty good! Office hours are your best friend fr fr 🔥"
    
    def handle_dining_query(self, user_input: str, tone: str) -> str:
        """Handle dining-related queries"""
        # Use authentic caf reviews
        caf_reviews = self.lmu_tea['caf_reviews']
        if caf_reviews:
            return random.choice(caf_reviews)
        
        # Fallback to existing data
        dining = self.data.get('dining', [])
        if dining:
            place = random.choice(dining)
            return f"The {place.get('name', 'Lair')} is actually pretty good! {place.get('description', 'Great food and vibes')}"
        
        return "The Lair is the main spot for food! Pizza is mid but the garlic knots? *chef's kiss* ✨"
    
    def handle_housing_query(self, user_input: str, tone: str) -> str:
        """Handle housing-related queries"""
        # Use authentic dorm rumors
        dorm_rumors = self.lmu_tea['dorm_rumors']
        if dorm_rumors:
            return random.choice(dorm_rumors)
        
        # Fallback to existing data
        housing = self.data.get('housing', [])
        if housing:
            dorm = random.choice(housing)
            return f"{dorm.get('name', 'The dorms')} are actually pretty nice! {dorm.get('description', 'Good vibes and community')}"
        
        return "Hannon has the best study lounges but McCarthy thinks they're better than Del Rey 👀"
    
    def handle_event_query(self, user_input: str, tone: str) -> str:
        """Handle event-related queries"""
        # Use authentic event opinions
        event_opinions = self.lmu_tea['events_opinions']
        if event_opinions:
            return random.choice(event_opinions)
        
        # Fallback to existing data
        events = self.data.get('events', [])
        if events:
            event = random.choice(events)
            return f"{event.get('name', 'Events')} are always fun! {event.get('description', 'Great way to meet people')}"
        
        return "TNL lineup lookin mid this week but maybe free pizza? 🍕"
    
    def handle_study_query(self, user_input: str, tone: str) -> str:
        """Handle study-related queries"""
        # Use authentic campus landmarks
        landmarks = self.lmu_tea['campus_landmarks']
        study_spots = [spot for spot in landmarks if any(word in spot.lower() for word in ['library', 'quiet', 'study', '3rd floor'])]
        
        if study_spots:
            return random.choice(study_spots)
        
        return "The library's 3rd floor is the quietest spot on campus! Perfect for those late-night cram sessions 📚"
    
    def handle_general_query(self, user_input: str, tone: str) -> str:
        """Handle general queries"""
        # Use authentic campus tea
        all_tea = []
        for category, items in self.lmu_tea.items():
            all_tea.extend(items)
        
        if all_tea:
            return random.choice(all_tea)
        
        return "LMU is literally the best campus ever! The bluff views are unmatched and the community is so supportive 🔥"
    
    def format_search_result(self, result: Dict, tone: str) -> str:
        """Format search result based on tone"""
        item = result['item']
        
        if isinstance(item, dict):
            if 'name' in item:
                return f"{item['name']} is actually pretty good! {item.get('description', 'Great vibes')}"
            elif 'content' in item:
                return item['content']
            elif 'tea_content' in item:
                return item['tea_content']
        
        return str(item)
    
    def extract_user_context(self, user_input: str):
        """Extract and update user context from input"""
        text = user_input.lower()
        
        # Extract major
        majors = ['cs', 'computer science', 'business', 'psychology', 'film', 'english', 'engineering']
        for major in majors:
            if major in text:
                self.user_context['major'] = major
                break
        
        # Extract year
        years = ['freshman', 'sophomore', 'junior', 'senior', 'first year', 'second year', 'third year', 'fourth year']
        for year in years:
            if year in text:
                self.user_context['year'] = year
                break
        
        # Extract dorm
        dorms = ['hannon', 'mccarthy', 'del rey', 'doheny', 'palm', 'rosecrans']
        for dorm in dorms:
            if dorm in text:
                self.user_context['dorm'] = dorm
                break
        
        # Update recent queries
        self.user_context['recent_queries'].append(user_input)
        if len(self.user_context['recent_queries']) > 5:
            self.user_context['recent_queries'].pop(0)

def create_enhanced_chat_interface():
    """Create the enhanced chat interface"""
    st.markdown("### 🤖 Enhanced LMU Buddy V2")
    st.markdown("**Now with authentic campus tea from Reddit & RateMyProfessors!**")
    
    # Initialize buddy
    if 'enhanced_buddy_v2' not in st.session_state:
        with st.spinner("Loading Enhanced LMU Buddy V2..."):
            st.session_state.enhanced_buddy_v2 = EnhancedLMUBuddyV2()
    
    buddy = st.session_state.enhanced_buddy_v2
    
    # Display tone analysis
    if st.session_state.get('last_user_input'):
        tone_scores = buddy.analyze_user_tone(st.session_state.last_user_input)
        st.markdown(f"**Tone Analysis:** {buddy.get_dominant_tone(tone_scores).title()}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Casual", f"{tone_scores.get('casual', 0):.1%}")
        with col2:
            st.metric("Formal", f"{tone_scores.get('formal', 0):.1%}")
        with col3:
            st.metric("Academic", f"{tone_scores.get('academic', 0):.1%}")
    
    # Chat interface
    user_input = st.text_input("Ask Enhanced LMU Buddy V2 anything...", key="enhanced_v2_input")
    
    if st.button("Send", key="enhanced_v2_send") and user_input:
        st.session_state.last_user_input = user_input
        
        with st.spinner("LMU Buddy is thinking..."):
            response = buddy.generate_response(user_input)
        
        # Display conversation
        st.markdown("### 💬 Conversation")
        st.markdown(f"**You:** {user_input}")
        st.markdown(f"**LMU Buddy:** {response}")
        
        # Show user context
        if buddy.user_context['major'] or buddy.user_context['dorm']:
            st.markdown("### 👤 Your Context")
            context_info = []
            if buddy.user_context['major']:
                context_info.append(f"Major: {buddy.user_context['major']}")
            if buddy.user_context['dorm']:
                context_info.append(f"Dorm: {buddy.user_context['dorm']}")
            if buddy.user_context['year']:
                context_info.append(f"Year: {buddy.user_context['year']}")
            
            st.markdown(", ".join(context_info))
    
    # Quick access buttons
    st.markdown("### 🚀 Quick Access")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🍕 Food Tea", key="food_tea_v2"):
            st.session_state.last_user_input = "Tell me about the food on campus"
            response = buddy.generate_response("Tell me about the food on campus")
            st.markdown(f"**LMU Buddy:** {response}")
    
    with col2:
        if st.button("👻 Dorm Gossip", key="dorm_gossip_v2"):
            st.session_state.last_user_input = "What's the tea about the dorms?"
            response = buddy.generate_response("What's the tea about the dorms?")
            st.markdown(f"**LMU Buddy:** {response}")
    
    with col3:
        if st.button("👨‍🏫 Professor Tea", key="prof_tea_v2"):
            st.session_state.last_user_input = "Tell me about the professors"
            response = buddy.generate_response("Tell me about the professors")
            st.markdown(f"**LMU Buddy:** {response}")

if __name__ == "__main__":
    # Test the enhanced buddy
    buddy = EnhancedLMUBuddyV2()
    
    test_inputs = [
        "Yo what's the best food on campus?",
        "Could you please provide information about the dining facilities?",
        "What are the optimal study locations for academic pursuits?",
        "The wifi in Malone is literally unusable fr fr",
        "What's the tea about the dorms?"
    ]
    
    for test_input in test_inputs:
        print(f"\nInput: {test_input}")
        response = buddy.generate_response(test_input)
        print(f"Response: {response}")
        print("-" * 50)