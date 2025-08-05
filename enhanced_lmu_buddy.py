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

class EnhancedLMUBuddy:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.data = self.load_lmu_data()
        self.embeddings = self.load_or_compute_embeddings()
        self.conversation_history = []
        self.user_preferences = {}
        self.user_context = {
            'name': None,
            'clubs': [],
            'major': None,
            'year': None,
            'favorite_topics': [],
            'recent_queries': []
        }
        self.query_frequency = {}  # Track how often specific queries are asked
        self.lmu_personality = {
            'casual': {
                'greetings': ['Yo!', 'Hey there!', 'What\'s good?', 'Sup!'],
                'excitement': ['🔥', '✨', '💯', '👏', '🎉'],
                'agreement': ['Facts!', 'Period!', 'No cap!', 'Literally!'],
                'emphasis': ['literally', 'actually', 'honestly', 'fr fr'],
                'lmc_slang': ['the bluff', 'the bluff life', 'bluff vibes', 'bluff culture']
            },
            'formal': {
                'greetings': ['Greetings!', 'Hello!', 'Good day!', 'Welcome!'],
                'excitement': ['Excellent!', 'Wonderful!', 'Fantastic!', 'Outstanding!'],
                'agreement': ['Indeed!', 'Absolutely!', 'Certainly!', 'Precisely!'],
                'emphasis': ['indeed', 'certainly', 'precisely', 'undoubtedly'],
                'lmc_slang': ['Loyola Marymount University', 'our esteemed institution', 'the university community']
            },
            'neutral': {
                'greetings': ['Hey!', 'Hi there!', 'Hello!', 'Welcome!'],
                'excitement': ['Great!', 'Awesome!', 'Nice!', 'Cool!'],
                'agreement': ['Definitely!', 'Absolutely!', 'For sure!', 'Totally!'],
                'emphasis': ['definitely', 'absolutely', 'for sure', 'totally'],
                'lmc_slang': ['LMU', 'campus', 'the bluff', 'our school']
            }
        }
        
        # LMU-specific knowledge base
        self.lmu_insights = {
            'campus_culture': [
                "LMU's Jesuit values emphasize 'cura personalis' - care for the whole person",
                "The bluff location gives us amazing views of LA and the ocean",
                "We're known for our strong film school and connections to Hollywood",
                "The campus is super walkable and everything is close together",
                "We have a strong sense of community and school spirit"
            ],
            'student_life': [
                "Greek life is huge here - about 30% of students are involved",
                "The Lair is the main dining spot and social hub",
                "Sunset Strip is just down the hill for nightlife",
                "Venice Beach and Santa Monica are super close",
                "We have amazing weather year-round"
            ],
            'academic_tips': [
                "Office hours are your best friend - professors are super accessible",
                "The library has amazing study spots with ocean views",
                "Take advantage of LA internships and networking opportunities",
                "Study abroad programs are popular and well-supported",
                "Research opportunities are available even for undergrads"
            ],
            'hidden_gems': [
                "The rooftop of Burns Fine Arts has the best sunset views",
                "The meditation garden behind Sacred Heart Chapel is peaceful",
                "The Lion's Den has the best smoothie bowls",
                "The bluff trail behind campus is perfect for walks",
                "The library's 3rd floor is the quietest study spot"
            ]
        }
        
        # Event emoji mapping for better visual formatting
        self.event_emojis = {
            'arts': '🎭',
            'music': '🎵',
            'sports': '🏀',
            'academic': '📚',
            'social': '🎉',
            'cultural': '🌍',
            'professional': '💼',
            'spiritual': '🙏',
            'food': '🍕',
            'movie': '🎬',
            'workshop': '🔧',
            'lecture': '🎤',
            'party': '🎊',
            'meeting': '🤝',
            'volunteer': '❤️',
            'fitness': '💪',
            'gaming': '🎮',
            'dance': '💃',
            'theater': '🎭',
            'comedy': '😂'
        }
        
        # Fun LMU trivia for sprinkling into responses
        self.lmu_trivia = [
            "Did you know LMU's campus has been used in over 30 major Hollywood films? Perfect backdrop for your day!",
            "The bluff location gives us the best sunset views in LA - no wonder we're called 'the bluff'!",
            "LMU's film school alumni have won Oscars and worked on blockbuster movies!",
            "Our campus is so beautiful that it's been featured in countless TV shows and commercials!",
            "The bluff trail behind campus is a hidden gem that most students don't discover until senior year!",
            "LMU's library has ocean views from almost every study spot - talk about motivation!",
            "The meditation garden behind Sacred Heart Chapel is where many students find their zen!",
            "Our campus is so close to the ocean that you can sometimes smell the sea breeze!",
            "LMU's location on the bluff means we get the best weather in LA - no smog up here!",
            "The rooftop of Burns Fine Arts has the most Instagram-worthy sunset views on campus!"
        ]
        
        # Multiple dining options for variety
        self.dining_variations = {
            'quick_bite': [
                "🌮 The Hungry Lion for amazing tacos",
                "🥪 Subway for quick sandwiches",
                "🍕 Pizza Hut Express for grab-and-go slices",
                "🥗 Fresh & Co for healthy salads"
            ],
            'sit_down': [
                "🍕 The Lair for the full dining experience",
                "☕ Starbucks for coffee and pastries",
                "🍜 Panda Express for Asian cuisine",
                "🍔 Burger Studio for classic American food"
            ],
            'healthy': [
                "🥗 The Blend Bar for smoothie bowls",
                "🥪 Fresh & Co for organic options",
                "🍎 The Market for fresh fruits and snacks",
                "🥤 Juice It Up for fresh juices"
            ],
            'late_night': [
                "🌙 Late Night Café for midnight cravings",
                "🍕 The Lair (late hours) for pizza",
                "☕ Starbucks for late-night caffeine",
                "🍦 The Den for ice cream and snacks"
            ]
        }
        
        # Engaging closing prompts
        self.closing_prompts = {
            'casual': [
                "What LMU magic can I help you with next? 🔥",
                "Need campus hacks or secret spots? Just ask! 🦁",
                "Want the tea on something else? I'm here for it! ✨",
                "What's on your mind about LMU? Let's chat! 💯",
                "Need more bluff wisdom? Hit me up! 🎉"
            ],
            'formal': [
                "How else may I assist you with your LMU experience?",
                "Is there anything else you'd like to know about our campus?",
                "What other aspects of university life would you like to explore?",
                "How may I continue to be of service to you?",
                "What additional information would be helpful to you?"
            ],
            'neutral': [
                "What else would you like to know about LMU? 🦁",
                "Need help with anything else campus-related? ✨",
                "What's next on your LMU exploration list? 🔥",
                "Want to discover more about campus life? 💫",
                "What other LMU topics interest you? 🎯"
            ]
        }
    
    def load_lmu_data(self):
        """Load LMU data from JSON file"""
        try:
            with open('enhanced_lmu_data.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create default data if file doesn't exist
            return self.create_default_data()
    
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
        """Load pre-computed embeddings or compute new ones"""
        try:
            with open('lmu_embeddings.pkl', 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return self.compute_embeddings()
    
    def compute_embeddings(self):
        """Compute embeddings for all LMU data"""
        all_texts = []
        text_mapping = []
        
        # Process professors
        for prof in self.data.get('professors', []):
            text = f"{prof.get('name', '')} {prof.get('department', '')} {' '.join(prof.get('tags', []))} {' '.join(prof.get('courses', []))}"
            all_texts.append(text)
            text_mapping.append(('professor', prof))
        
        # Process courses
        for course in self.data.get('courses', []):
            text = f"{course.get('code', '')} {course.get('name', '')} {course.get('department', '')} {course.get('description', '')}"
            all_texts.append(text)
            text_mapping.append(('course', course))
        
        # Process dining
        for dining in self.data.get('dining', []):
            text = f"{dining.get('name', '')} {dining.get('type', '')} {' '.join(dining.get('features', []))} {' '.join(dining.get('popular_items', []))}"
            all_texts.append(text)
            text_mapping.append(('dining', dining))
        
        # Process housing
        for housing in self.data.get('housing', []):
            text = f"{housing.get('name', '')} {housing.get('type', '')} {' '.join(housing.get('features', []))} {' '.join(housing.get('pros', []))}"
            all_texts.append(text)
            text_mapping.append(('housing', housing))
        
        # Process events
        for event in self.data.get('events', []):
            text = f"{event.get('name', '')} {event.get('type', '')} {event.get('description', '')} {event.get('location', '')}"
            all_texts.append(text)
            text_mapping.append(('event', event))
        
        # Process organizations
        for org in self.data.get('organizations', []):
            text = f"{org.get('name', '')} {org.get('type', '')} {org.get('description', '')} {' '.join(org.get('events', []))}"
            all_texts.append(text)
            text_mapping.append(('organization', org))
        
        # Process facilities
        for facility in self.data.get('facilities', []):
            text = f"{facility.get('name', '')} {facility.get('type', '')} {' '.join(facility.get('features', []))} {' '.join(facility.get('popular_spots', []))}"
            all_texts.append(text)
            text_mapping.append(('facility', facility))
        
        if all_texts:
            embeddings = self.model.encode(all_texts)
            
            # Save embeddings
            with open('lmu_embeddings.pkl', 'wb') as f:
                pickle.dump({
                    'embeddings': embeddings,
                    'text_mapping': text_mapping
                }, f)
            
            return {
                'embeddings': embeddings,
                'text_mapping': text_mapping
            }
        else:
            return {
                'embeddings': np.array([]),
                'text_mapping': []
            }
    
    def semantic_search(self, query, top_k=3):
        """Perform semantic search on LMU data"""
        if not self.embeddings['embeddings'].size:
            return []
        
        query_embedding = self.model.encode([query])
        similarities = cosine_similarity(query_embedding, self.embeddings['embeddings'])[0]
        
        # Get top k results
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.3:  # Threshold for relevance
                category, data = self.embeddings['text_mapping'][idx]
                results.append({
                    'category': category,
                    'data': data,
                    'similarity': similarities[idx]
                })
        
        return results
    
    def get_professor_info(self, query):
        """Get specific professor information"""
        search_results = self.semantic_search(query, top_k=1)
        for result in search_results:
            if result['category'] == 'professor':
                return result['data']
        return None
    
    def get_course_info(self, query):
        """Get specific course information"""
        search_results = self.semantic_search(query, top_k=1)
        for result in search_results:
            if result['category'] == 'course':
                return result['data']
        return None
    
    def get_upcoming_events(self, days=7):
        """Get upcoming events within specified days"""
        current_date = datetime.now()
        upcoming_events = []
        
        for event in self.data.get('events', []):
            event_date = datetime.strptime(event.get('date', ''), '%Y-%m-%d')
            if current_date <= event_date <= current_date + timedelta(days=days):
                upcoming_events.append(event)
        
        return upcoming_events
    
    def analyze_user_tone(self, user_input):
        """Enhanced tone analysis with more sophisticated detection"""
        user_input_lower = user_input.lower()
        
        # Enhanced formal indicators
        formal_indicators = [
            'please', 'thank you', 'would you', 'could you', 'may i', 'excuse me', 'pardon',
            'kindly', 'appreciate', 'grateful', 'respectfully', 'sincerely', 'regards'
        ]
        
        # Enhanced informal indicators
        informal_indicators = [
            'yo', 'hey', 'whats up', 'sup', 'bro', 'dude', 'omg', 'lol', 'fr', 'ngl', 'tbh',
            'literally', 'actually', 'honestly', 'deadass', 'no cap', 'period', 'slay',
            'vibe', 'mood', 'same', 'mood', 'relatable', 'facts', 'tea', 'spill'
        ]
        
        # Academic/formal context indicators
        academic_indicators = [
            'professor', 'course', 'assignment', 'syllabus', 'office hours', 'academic',
            'research', 'study', 'exam', 'final', 'midterm', 'grade', 'gpa'
        ]
        
        # Social/casual context indicators
        social_indicators = [
            'party', 'weekend', 'fun', 'hangout', 'friends', 'social', 'event',
            'food', 'eat', 'drink', 'nightlife', 'club', 'bar', 'restaurant'
        ]
        
        formal_count = sum(1 for indicator in formal_indicators if indicator in user_input_lower)
        informal_count = sum(1 for indicator in informal_indicators if indicator in user_input_lower)
        academic_count = sum(1 for indicator in academic_indicators if indicator in user_input_lower)
        social_count = sum(1 for indicator in social_indicators if indicator in user_input_lower)
        
        # Check for emoji usage
        emoji_count = len([char for char in user_input if ord(char) > 127])
        
        # Check for punctuation patterns
        exclamation_count = user_input.count('!')
        question_count = user_input.count('?')
        caps_count = sum(1 for char in user_input if char.isupper())
        
        # Check for slang and abbreviations
        slang_patterns = ['u ', 'ur ', 'yr ', 'r u ', 'w/', 'w/o', 'bc', 'b/c', 'imo', 'tbh']
        slang_count = sum(1 for pattern in slang_patterns if pattern in user_input_lower)
        
        # Determine tone with more sophisticated logic
        if formal_count > informal_count and academic_count > social_count:
            return 'formal'
        elif (informal_count > formal_count or emoji_count > 0 or exclamation_count > 1 or 
              slang_count > 0 or social_count > academic_count):
            return 'casual'
        elif len(user_input.split()) > 20 and caps_count < len(user_input) * 0.1:
            return 'formal'
        else:
            return 'neutral'
    
    def get_lmu_insight(self, category, tone='neutral'):
        """Get a relevant LMU insight based on category and tone"""
        insights = self.lmu_insights.get(category, [])
        if insights:
            insight = random.choice(insights)
            personality = self.lmu_personality.get(tone, self.lmu_personality['neutral'])
            
            if tone == 'casual':
                return f"💡 **Bluff Wisdom**: {insight} {random.choice(personality['excitement'])}"
            elif tone == 'formal':
                return f"💡 **Campus Insight**: {insight}"
            else:
                return f"💡 **Campus Insight**: {insight} 🦁"
        return ""
    
    def track_query_frequency(self, query):
        """Track how often specific queries are asked to avoid repetition"""
        query_lower = query.lower().strip()
        self.query_frequency[query_lower] = self.query_frequency.get(query_lower, 0) + 1
        return self.query_frequency[query_lower]
    
    def is_repeated_query(self, query):
        """Check if this is a repeated query that needs diversification"""
        query_lower = query.lower().strip()
        return self.query_frequency.get(query_lower, 0) > 1
    
    def get_personalized_greeting(self, tone='neutral'):
        """Get personalized greeting based on user context"""
        personality = self.lmu_personality.get(tone, self.lmu_personality['neutral'])
        
        if self.user_context['name']:
            if tone == 'casual':
                return f"Yo {self.user_context['name']}! "
            elif tone == 'formal':
                return f"Greetings {self.user_context['name']}! "
            else:
                return f"Hey {self.user_context['name']}! "
        
        return random.choice(personality['greetings']) + " "
    
    def add_contextual_recommendation(self, query, tone='neutral'):
        """Add personalized recommendations based on user context"""
        query_lower = query.lower()
        
        # Check if user is in specific clubs/organizations
        if self.user_context['clubs']:
            club = self.user_context['clubs'][0]  # Use first club for now
            if 'film' in club.lower() and any(word in query_lower for word in ['event', 'activity', 'fun']):
                return f"Since you're in the {club}, check out the upcoming film screenings at the Burns Fine Arts Center! 🎬"
            elif 'business' in club.lower() and any(word in query_lower for word in ['career', 'professional', 'networking']):
                return f"As a {club} member, you might be interested in the upcoming networking events! 💼"
        
        # Check if user has a specific major
        if self.user_context['major']:
            if 'science' in self.user_context['major'].lower() and any(word in query_lower for word in ['food', 'eat', 'dining']):
                return f"Hey, if you're heading to science classes, grab food at the Lion's Den - it's right near the science building! 🧪"
            elif 'arts' in self.user_context['major'].lower() and any(word in query_lower for word in ['study', 'quiet', 'library']):
                return f"Since you're in the arts, the Burns Fine Arts library is perfect for your creative projects! 🎨"
        
        return ""
    
    def sprinkle_lmu_trivia(self, tone='neutral'):
        """Randomly add fun LMU trivia to responses"""
        if random.random() < 0.3:  # 30% chance to add trivia
            trivia = random.choice(self.lmu_trivia)
            personality = self.lmu_personality.get(tone, self.lmu_personality['neutral'])
            
            if tone == 'casual':
                return f"\n\n💭 **Fun Fact**: {trivia} {random.choice(personality['excitement'])}"
            elif tone == 'formal':
                return f"\n\n💡 **Interesting Note**: {trivia}"
            else:
                return f"\n\n💭 **Fun Fact**: {trivia} 🦁"
        
        return ""
    
    def get_engaging_closing_prompt(self, tone='neutral'):
        """Get an engaging closing prompt based on tone"""
        prompts = self.closing_prompts.get(tone, self.closing_prompts['neutral'])
        return random.choice(prompts)
    
    def extract_user_context(self, user_input):
        """Extract user context from conversation to enable personalized recommendations"""
        user_input_lower = user_input.lower()
        
        # Extract name if mentioned
        if "my name is" in user_input_lower or "i'm" in user_input_lower or "i am" in user_input_lower:
            # Simple name extraction - could be enhanced with NLP
            words = user_input.split()
            for i, word in enumerate(words):
                if word.lower() in ['name', 'is', 'am', 'i\'m'] and i + 1 < len(words):
                    potential_name = words[i + 1].strip('.,!?')
                    if len(potential_name) > 1 and potential_name.isalpha():
                        self.user_context['name'] = potential_name
                        break
        
        # Extract major if mentioned
        major_keywords = ['major', 'studying', 'study', 'degree', 'field']
        for keyword in major_keywords:
            if keyword in user_input_lower:
                # Extract major from context
                words = user_input.split()
                for i, word in enumerate(words):
                    if word.lower() == keyword and i + 1 < len(words):
                        potential_major = words[i + 1].strip('.,!?')
                        if len(potential_major) > 2:
                            self.user_context['major'] = potential_major
                            break
        
        # Extract clubs/organizations if mentioned
        club_keywords = ['club', 'organization', 'member', 'join', 'part of']
        for keyword in club_keywords:
            if keyword in user_input_lower:
                # Extract club name from context
                words = user_input.split()
                for i, word in enumerate(words):
                    if word.lower() in club_keywords and i + 1 < len(words):
                        potential_club = words[i + 1].strip('.,!?')
                        if len(potential_club) > 2 and potential_club not in self.user_context['clubs']:
                            self.user_context['clubs'].append(potential_club)
                            break
        
        # Extract year if mentioned
        year_keywords = ['freshman', 'sophomore', 'junior', 'senior', 'first year', 'second year', 'third year', 'fourth year']
        for keyword in year_keywords:
            if keyword in user_input_lower:
                self.user_context['year'] = keyword
                break
        
        # Track favorite topics based on query frequency
        topic_keywords = {
            'academic': ['professor', 'course', 'study', 'class', 'exam'],
            'social': ['event', 'party', 'club', 'organization', 'friend'],
            'dining': ['food', 'eat', 'dining', 'restaurant', 'cafe'],
            'facilities': ['library', 'gym', 'study', 'building', 'facility']
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in user_input_lower for keyword in keywords):
                if topic not in self.user_context['favorite_topics']:
                    self.user_context['favorite_topics'].append(topic)
                break
    
    def format_event_with_emoji(self, event, tone='neutral'):
        """Format event with appropriate emoji and engaging details"""
        event_type = event.get('type', '').lower()
        emoji = self.event_emojis.get(event_type, '📅')
        
        # Find the best matching emoji
        for key, value in self.event_emojis.items():
            if key in event_type:
                emoji = value
                break
        
        # Add engaging details based on event type
        engaging_details = ""
        if 'free' in event.get('description', '').lower():
            engaging_details = " (FREE!)"
        elif 'pizza' in event.get('description', '').lower():
            engaging_details = " (FREE pizza!)"
        elif 'concert' in event_type or 'music' in event_type:
            engaging_details = " (Live music!)"
        elif 'sports' in event_type:
            engaging_details = " (Go Lions!)"
        
        return f"{emoji} **{event['name']}**{engaging_details} ({event['date']})\n📍 {event['location']}\n📝 {event['description'][:100]}...\n"
    
    def get_diverse_dining_response(self, query, tone='neutral'):
        """Get diverse dining recommendations to avoid repetition"""
        query_lower = query.lower()
        personality = self.lmu_personality.get(tone, self.lmu_personality['neutral'])
        
        # Check if this is a repeated dining query and add playful response
        if self.is_repeated_query(query):
            if tone == 'casual':
                response = f"You asked twice! Hungry much? 😂 Here are some fresh spots:\n\n"
            elif tone == 'formal':
                response = "I notice you've asked about dining options before. Here are some additional recommendations:\n\n"
            else:
                response = "You asked twice! Hungry much? 😂 Here are some fresh spots:\n\n"
        else:
            if tone == 'casual':
                response = "LMU's got you covered food-wise! 🌮\n\n"
            elif tone == 'formal':
                response = "LMU offers several excellent dining options:\n\n"
            else:
                response = "LMU's got you covered food-wise! 🌮\n\n"
        
        # Determine dining preference from query
        if any(word in query_lower for word in ['quick', 'fast', 'grab']):
            options = self.dining_variations['quick_bite']
        elif any(word in query_lower for word in ['sit', 'relax', 'chill']):
            options = self.dining_variations['sit_down']
        elif any(word in query_lower for word in ['healthy', 'fresh', 'organic']):
            options = self.dining_variations['healthy']
        elif any(word in query_lower for word in ['late', 'night', 'midnight']):
            options = self.dining_variations['late_night']
        else:
            # Mix different types for variety
            all_options = []
            for category in self.dining_variations.values():
                all_options.extend(category)
            options = random.sample(all_options, min(4, len(all_options)))
        
        for option in options[:3]:
            response += f"• {option}\n"
        
        if tone == 'casual':
            response += f"\nWhat vibe you looking for—quick bite or chill hangout? {random.choice(personality['excitement'])}"
        elif tone == 'formal':
            response += "\nWhich type of dining experience interests you most?"
        else:
            response += "\nWhat vibe you looking for—quick bite or chill hangout? 🦁"
        
        return response
    
    def generate_response(self, user_input):
        """Enhanced response generation with better context awareness and LMU-specific knowledge"""
        user_input_lower = user_input.lower()
        
        # Track query frequency for diversification
        self.track_query_frequency(user_input)
        
        # Analyze user tone
        user_tone = self.analyze_user_tone(user_input)
        
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Update user context with recent queries
        self.user_context['recent_queries'].append(user_input_lower)
        if len(self.user_context['recent_queries']) > 10:
            self.user_context['recent_queries'].pop(0)
        
        # Extract user context from conversation
        self.extract_user_context(user_input_lower)
        
        # Check for specific query types with enhanced detection
        if any(word in user_input_lower for word in ['professor', 'teacher', 'instructor', 'faculty', 'dr.', 'prof.']):
            return self.handle_professor_query(user_input, user_tone)
        elif any(word in user_input_lower for word in ['course', 'class', 'subject', 'syllabus', 'assignment', 'exam']):
            return self.handle_course_query(user_input, user_tone)
        elif any(word in user_input_lower for word in ['food', 'eat', 'dining', 'restaurant', 'lair', 'lions den', 'cafe']):
            return self.handle_dining_query(user_input, user_tone)
        elif any(word in user_input_lower for word in ['housing', 'dorm', 'apartment', 'live', 'residence', 'room']):
            return self.handle_housing_query(user_input, user_tone)
        elif any(word in user_input_lower for word in ['event', 'activity', 'weekend', 'party', 'social', 'fun']):
            return self.handle_event_query(user_input, user_tone)
        elif any(word in user_input_lower for word in ['organization', 'club', 'greek', 'sorority', 'fraternity', 'group']):
            return self.handle_organization_query(user_input, user_tone)
        elif any(word in user_input_lower for word in ['facility', 'library', 'study', 'gym', 'center', 'building']):
            return self.handle_facility_query(user_input, user_tone)
        elif any(word in user_input_lower for word in ['news', 'announcement', 'update', 'information']):
            return self.handle_news_query(user_input, user_tone)
        elif any(word in user_input_lower for word in ['parking', 'car', 'shuttle', 'transportation', 'commute']):
            return self.handle_transportation_query(user_input, user_tone)
        elif any(word in user_input_lower for word in ['weather', 'sunset', 'view', 'bluff', 'campus']):
            return self.handle_campus_life_query(user_input, user_tone)
        else:
            # Check if this is an unknown or too broad query
            if len(user_input.split()) < 3 or any(word in user_input_lower for word in ['what', 'how', 'why', 'when', 'where']):
                return self.handle_unknown_query(user_input, user_tone)
            else:
                return self.handle_general_query(user_input, user_tone)
    
    def handle_professor_query(self, query, tone='neutral'):
        """Enhanced professor query handler with better LMU-specific insights"""
        prof_info = self.get_professor_info(query)
        
        # Get personality elements
        personality = self.lmu_personality.get(tone, self.lmu_personality['neutral'])
        
        # Tone-specific greetings and language
        if tone == 'formal':
            greeting = "I'd be happy to provide information about"
            rating_text = "Student Rating"
            difficulty_text = "Course Difficulty"
            tip_start = "Recommendation"
            not_found = "I apologize, but I couldn't locate specific professor information for your query."
        elif tone == 'casual':
            greeting = "Yo, here's the tea on"
            rating_text = "Rating"
            difficulty_text = "How hard"
            tip_start = "Pro tip"
            not_found = "Oof, couldn't find that prof in my database."
        else:
            greeting = "Here's what I found about"
            rating_text = "Rating"
            difficulty_text = "Difficulty"
            tip_start = "Pro tip"
            not_found = "I couldn't find specific professor information for that query."
        
        if prof_info:
            response = f"👨‍🏫 **{prof_info['name']}** ({prof_info['department']})\n\n"
            response += f"⭐ {rating_text}: {prof_info['rating']}/5.0\n"
            response += f"📊 {difficulty_text}: {prof_info['difficulty']}/5.0\n"
            response += f"💬 Reviews: {prof_info['reviews']}\n\n"
            response += f"🏷️ Tags: {', '.join(prof_info['tags'])}\n"
            response += f"📚 Courses: {', '.join(prof_info['courses'])}\n\n"
            
            # Add intimate LMU knowledge based on tone
            if tone == 'casual':
                response += f"💡 {tip_start}: {prof_info['name']} is known for being super chill in office hours. Students say they're really approachable and actually care about your success. Plus, they usually curve generously! {random.choice(personality['excitement'])}\n\n"
                response += "🎯 **Student Gossip**: Rumor has it they're working on some groundbreaking research in their field. Might be worth asking about in class!"
            elif tone == 'formal':
                response += f"💡 {tip_start}: Professor {prof_info['name']} maintains excellent office hours and is known for their dedication to student success. Many students report significant academic growth in their courses.\n\n"
                response += "📚 **Academic Note**: They are actively engaged in research and often welcome undergraduate participation in their projects."
            else:
                response += f"💡 {tip_start}: Check Rate My Professor for detailed reviews and student experiences! 🦁\n\n"
                response += "🎓 **Campus Insight**: This professor is well-respected in their department and often mentors students beyond the classroom."
            
            # Add contextual recommendations and trivia
            response += self.add_contextual_recommendation(query, tone)
            response += self.sprinkle_lmu_trivia(tone)
            response += f"\n\n{self.get_lmu_insight('academic_tips', tone)}"
            response += f"\n\n{self.get_engaging_closing_prompt(tone)}"
            
            return response
        
        # Search for professors by department or other criteria
        search_results = self.semantic_search(query, top_k=3)
        if search_results:
            if tone == 'casual':
                response = "🔍 Here are some profs that might be what you're looking for:\n\n"
            elif tone == 'formal':
                response = "🔍 Here are some professors that might match your query:\n\n"
            else:
                response = "🔍 Here are some professors that might match your query:\n\n"
                
            for result in search_results:
                if result['category'] == 'professor':
                    prof = result['data']
                    response += f"• **{prof['name']}** ({prof['department']}) - Rating: {prof['rating']}/5.0\n"
            
            if tone == 'casual':
                response += f"\n💡 Try asking about a specific prof by name! I know all the tea on campus faculty 😏 {random.choice(personality['excitement'])}"
            elif tone == 'formal':
                response += "\n💡 Please try asking about a specific professor by name for more detailed information."
            else:
                response += "\n💡 Try asking about a specific professor by name!"
            return response
        
        return not_found
    
    def handle_course_query(self, query, tone='neutral'):
        """Enhanced course query handler with better LMU-specific insights"""
        course_info = self.get_course_info(query)
        
        # Get personality elements
        personality = self.lmu_personality.get(tone, self.lmu_personality['neutral'])
        
        # Tone-specific language
        if tone == 'formal':
            tip_start = "Recommendation"
            not_found = "I apologize, but I couldn't locate specific course information for your query."
        elif tone == 'casual':
            tip_start = "Pro tip"
            not_found = "Oof, couldn't find that course in my database."
        else:
            tip_start = "Pro tip"
            not_found = "I couldn't find specific course information for that query."
        
        if course_info:
            response = f"📚 **{course_info['code']} - {course_info['name']}**\n\n"
            response += f"🏛️ Department: {course_info['department']}\n"
            response += f"⭐ Rating: {course_info['rating']}/5.0\n"
            response += f"📊 Difficulty: {course_info['difficulty']}/5.0\n"
            response += f"💬 Reviews: {course_info['reviews']}\n\n"
            response += f"📝 Description: {course_info['description']}\n\n"
            
            if tone == 'casual':
                response += f"💡 {tip_start}: This class is {random.choice(['pretty chill', 'kinda challenging', 'super interesting', 'definitely worth taking'])}! Students say the workload is manageable and the professor is {random.choice(['super helpful', 'really approachable', 'great at explaining things', 'always available for help'])}. {random.choice(personality['excitement'])}\n\n"
                response += "🎯 **Student Insight**: Make sure to go to office hours - it's literally the key to success in this class!"
            elif tone == 'formal':
                response += f"💡 {tip_start}: This course has received positive feedback from students regarding its academic rigor and instructor accessibility. Regular attendance at office hours is highly recommended for optimal performance.\n\n"
                response += "📚 **Academic Note**: The course structure allows for meaningful engagement with the subject matter."
            else:
                response += f"💡 {tip_start}: Students generally find this course engaging and well-structured. Office hours are highly recommended! 🦁\n\n"
                response += "🎓 **Campus Insight**: This course is popular among students and often fills up quickly during registration."
            
            # Add contextual recommendations and trivia
            response += self.add_contextual_recommendation(query, tone)
            response += self.sprinkle_lmu_trivia(tone)
            response += f"\n\n{self.get_lmu_insight('academic_tips', tone)}"
            response += f"\n\n{self.get_engaging_closing_prompt(tone)}"
            return response
        
        # Search for courses by department or other criteria
        search_results = self.semantic_search(query, top_k=3)
        if search_results:
            response = "🔍 Here are some courses that might match your query:\n\n"
            for result in search_results:
                if result['category'] == 'course':
                    course = result['data']
                    response += f"• **{course['code']}** - {course['name']} (Rating: {course['rating']}/5.0)\n"
            
            if tone == 'casual':
                response += f"\n💡 Try asking about a specific course by code or name! I know all the deets {random.choice(personality['excitement'])}"
            else:
                response += "\n💡 Try asking about a specific course by code or name!"
            return response
        
        return not_found
    
    def handle_dining_query(self, query, tone='neutral'):
        """Enhanced dining query handler with LMU-specific food knowledge"""
        search_results = self.semantic_search(query, top_k=3)
        personality = self.lmu_personality.get(tone, self.lmu_personality['neutral'])
        
        # Check if this is a repeated query and use diverse response
        if self.is_repeated_query(query):
            response = self.get_diverse_dining_response(query, tone)
            response += self.add_contextual_recommendation(query, tone)
            response += self.sprinkle_lmu_trivia(tone)
            response += f"\n\n{self.get_engaging_closing_prompt(tone)}"
            return response
        
        if search_results:
            best_result = search_results[0]
            if best_result['category'] == 'dining':
                dining_info = best_result['data']
                
                if tone == 'casual':
                    response = f"🍕 **{dining_info['name']}** - The {dining_info['type']} Spot! 🍕\n\n"
                    response += f"📍 Location: {dining_info['location']}\n"
                    response += f"⭐ Rating: {dining_info['rating']}/5.0\n"
                    response += f"💰 Price Range: {dining_info['price_range']}\n\n"
                    response += f"🔥 **Must-Try Items:**\n"
                    for item in dining_info.get('popular_items', [])[:3]:
                        response += f"• {item}\n"
                    response += f"\n💡 **Pro Tip**: {dining_info['name']} is {random.choice(['always packed during lunch', 'best during off-peak hours', 'perfect for late-night cravings', 'great for group hangouts'])}! {random.choice(personality['excitement'])}\n\n"
                    response += "🎯 **Student Gossip**: Rumor has it they're planning to add some new menu items next semester!"
                elif tone == 'formal':
                    response = f"🍕 **{dining_info['name']}** - {dining_info['type']} Establishment 🍕\n\n"
                    response += f"📍 Location: {dining_info['location']}\n"
                    response += f"⭐ Rating: {dining_info['rating']}/5.0\n"
                    response += f"💰 Price Range: {dining_info['price_range']}\n\n"
                    response += f"📋 **Popular Menu Items:**\n"
                    for item in dining_info.get('popular_items', [])[:3]:
                        response += f"• {item}\n"
                    response += f"\n💡 **Recommendation**: {dining_info['name']} is known for its consistent quality and student-friendly pricing.\n\n"
                    response += "📚 **Note**: This establishment is popular among students and faculty alike."
                else:
                    response = f"🍕 **{dining_info['name']}** - {dining_info['type']} 🍕\n\n"
                    response += f"📍 Location: {dining_info['location']}\n"
                    response += f"⭐ Rating: {dining_info['rating']}/5.0\n"
                    response += f"💰 Price Range: {dining_info['price_range']}\n\n"
                    response += f"🔥 **Popular Items:**\n"
                    for item in dining_info.get('popular_items', [])[:3]:
                        response += f"• {item}\n"
                    response += f"\n💡 **Pro Tip**: {dining_info['name']} is a great spot for {random.choice(['lunch with friends', 'quick meals between classes', 'late-night study snacks', 'group dining'])}! 🦁\n\n"
                    response += "🎯 **Campus Insight**: This place is always buzzing with students!"
                
                response += f"\n\n{self.get_lmu_insight('student_life', tone)}"
                return response
        
        # General dining recommendations with diverse options
        response = self.get_diverse_dining_response(query, tone)
        response += self.add_contextual_recommendation(query, tone)
        response += self.sprinkle_lmu_trivia(tone)
        response += f"\n\n{self.get_lmu_insight('student_life', tone)}"
        return response
    
    def handle_housing_query(self, query, tone='neutral'):
        """Enhanced housing query handler with LMU-specific dorm knowledge"""
        search_results = self.semantic_search(query, top_k=3)
        personality = self.lmu_personality.get(tone, self.lmu_personality['neutral'])
        
        if search_results:
            best_result = search_results[0]
            if best_result['category'] == 'housing':
                housing_info = best_result['data']
                
                if tone == 'casual':
                    response = f"🏠 **{housing_info['name']}** - {housing_info['type']} Life! 🏠\n\n"
                    response += f"📍 Location: {housing_info['location']}\n"
                    response += f"⭐ Rating: {housing_info['rating']}/5.0\n"
                    response += f"💰 Cost: {housing_info['cost']}\n\n"
                    response += f"🔥 **What Students Love:**\n"
                    for pro in housing_info.get('pros', [])[:3]:
                        response += f"• {pro}\n"
                    response += f"\n💡 **Pro Tip**: {housing_info['name']} is {random.choice(['super social and fun', 'perfect for quiet study', 'great for making friends', 'convenient to everything'])}! {random.choice(personality['excitement'])}\n\n"
                    response += "🎯 **Student Gossip**: This dorm has the best RA's on campus!"
                elif tone == 'formal':
                    response = f"🏠 **{housing_info['name']}** - {housing_info['type']} Residence 🏠\n\n"
                    response += f"📍 Location: {housing_info['location']}\n"
                    response += f"⭐ Rating: {housing_info['rating']}/5.0\n"
                    response += f"💰 Cost: {housing_info['cost']}\n\n"
                    response += f"✅ **Key Features:**\n"
                    for pro in housing_info.get('pros', [])[:3]:
                        response += f"• {pro}\n"
                    response += f"\n💡 **Recommendation**: {housing_info['name']} offers excellent amenities and a supportive living environment.\n\n"
                    response += "📚 **Note**: This residence hall is highly regarded among students."
                else:
                    response = f"🏠 **{housing_info['name']}** - {housing_info['type']} 🏠\n\n"
                    response += f"📍 Location: {housing_info['location']}\n"
                    response += f"⭐ Rating: {housing_info['rating']}/5.0\n"
                    response += f"💰 Cost: {housing_info['cost']}\n\n"
                    response += f"✅ **Pros:**\n"
                    for pro in housing_info.get('pros', [])[:3]:
                        response += f"• {pro}\n"
                    response += f"\n💡 **Pro Tip**: {housing_info['name']} is known for being {random.choice(['very social', 'quiet and studious', 'convenient to classes', 'great community'])}! 🦁\n\n"
                    response += "🎯 **Campus Insight**: Students here really love the community!"
                
                response += self.add_contextual_recommendation(query, tone)
                response += self.sprinkle_lmu_trivia(tone)
                response += f"\n\n{self.get_lmu_insight('student_life', tone)}"
                response += f"\n\n{self.get_engaging_closing_prompt(tone)}"
                return response
        
        # General housing recommendations
        if tone == 'casual':
            response = "🏠 **LMU Housing - Where to Live Your Best Life** 🏠\n\n"
            response += "**Freshman Dorms:**\n"
            response += "• Del Rey North/South - classic freshman experience\n"
            response += "• Rosecrans - newer, more modern vibes\n"
            response += "• Huesman - smaller, more intimate community\n\n"
            response += "**Upperclassmen Options:**\n"
            response += "• Palm South - apartment-style living\n"
            response += "• Leavey 4/5 - suite-style with ocean views\n"
            response += "• Off-campus apartments in Playa Vista\n\n"
            response += f"💡 **Pro Tip**: Apply for housing early - the good spots fill up fast! {random.choice(personality['excitement'])}"
        elif tone == 'formal':
            response = "🏠 **LMU Housing Information** 🏠\n\n"
            response += "**First-Year Residence Halls:**\n"
            response += "• Del Rey North and South - traditional dormitory experience\n"
            response += "• Rosecrans Hall - contemporary living facilities\n"
            response += "• Huesman Hall - intimate residential community\n\n"
            response += "**Upper-Class Housing Options:**\n"
            response += "• Palm South - apartment-style accommodations\n"
            response += "• Leavey 4/5 - suite-style residences with scenic views\n"
            response += "• Off-campus housing opportunities in surrounding areas\n\n"
            response += "💡 **Recommendation**: Submit housing applications promptly as spaces are limited."
        else:
            response = "🏠 **LMU Housing Guide** 🏠\n\n"
            response += "**Freshman Dorms:**\n"
            response += "• Del Rey North/South - traditional freshman experience\n"
            response += "• Rosecrans - newer, more modern facilities\n"
            response += "• Huesman - smaller, more intimate setting\n\n"
            response += "**Upperclassmen Housing:**\n"
            response += "• Palm South - apartment-style living\n"
            response += "• Leavey 4/5 - suite-style with great views\n"
            response += "• Off-campus options in Playa Vista area\n\n"
            response += "💡 **Pro Tip**: Apply early for the best housing options! 🦁"
        
        response += self.add_contextual_recommendation(query, tone)
        response += self.sprinkle_lmu_trivia(tone)
        response += f"\n\n{self.get_lmu_insight('student_life', tone)}"
        response += f"\n\n{self.get_engaging_closing_prompt(tone)}"
        return response
    
    def handle_event_query(self, query, tone='neutral'):
        """Enhanced event query handler with LMU-specific event knowledge"""
        upcoming_events = self.get_upcoming_events(14)  # Next 2 weeks
        personality = self.lmu_personality.get(tone, self.lmu_personality['neutral'])
        
        if upcoming_events:
            if tone == 'casual':
                response = "🎉 **What's Popping at LMU - Next 2 Weeks** 🎉\n\n"
                for event in upcoming_events[:5]:
                    response += self.format_event_with_emoji(event, tone)
                    response += "\n"
                response += f"💡 **Pro Tip**: Follow @lmu_events on Instagram for the latest updates! {random.choice(personality['excitement'])}\n\n"
                response += "🎯 **Want to RSVP to any? Or looking for specific club meetups?**"
            elif tone == 'formal':
                response = "🎉 **Upcoming LMU Events - Next Two Weeks** 🎉\n\n"
                for event in upcoming_events[:5]:
                    response += self.format_event_with_emoji(event, tone)
                    response += "\n"
                response += "💡 **Recommendation**: Monitor the official LMU events calendar for current information.\n\n"
                response += "📋 **Would you like information about RSVP procedures or specific event details?**"
            else:
                response = "🎉 **Upcoming LMU Events** 🎉\n\n"
                for event in upcoming_events[:5]:
                    response += self.format_event_with_emoji(event, tone)
                    response += "\n"
                response += "💡 **Pro Tip**: Check the LMU events calendar regularly! 🦁\n\n"
                response += "🎯 **Want to RSVP to any? Or looking for specific club meetups?**"
        else:
            if tone == 'casual':
                response = "🎉 **LMU Events Scene** 🎉\n\n"
                response += "**What's Always Happening:**\n"
                response += "• 🏛️ Greek life mixers and formals\n"
                response += "• 🌍 Cultural events and celebrations\n"
                response += "• 📚 Academic lectures and workshops\n"
                response += "• 🏀 Sports games and tailgates\n"
                response += "• 🎬 Movie nights and social events\n\n"
                response += f"💡 **Pro Tip**: Join clubs and organizations to stay in the loop! {random.choice(personality['excitement'])}"
            elif tone == 'formal':
                response = "🎉 **LMU Events and Activities** 🎉\n\n"
                response += "**Regular Programming:**\n"
                response += "• 🏛️ Greek life social events and formal functions\n"
                response += "• 🌍 Cultural celebrations and diversity programs\n"
                response += "• 📚 Academic lectures and professional development workshops\n"
                response += "• 🏀 Athletic competitions and school spirit events\n"
                response += "• 🎬 Entertainment and social programming\n\n"
                response += "💡 **Recommendation**: Engage with campus organizations for comprehensive event information."
            else:
                response = "🎉 **LMU Events & Activities** 🎉\n\n"
                response += "**Regular Events:**\n"
                response += "• 🏛️ Greek life mixers and formals\n"
                response += "• 🌍 Cultural events and celebrations\n"
                response += "• 📚 Academic lectures and workshops\n"
                response += "• 🏀 Sports games and school spirit events\n"
                response += "• 🎬 Social events and entertainment\n\n"
                response += "💡 **Pro Tip**: Get involved in campus organizations! 🦁"
        
        response += self.add_contextual_recommendation(query, tone)
        response += self.sprinkle_lmu_trivia(tone)
        response += f"\n\n{self.get_lmu_insight('student_life', tone)}"
        return response
    
    def handle_organization_query(self, query, tone='neutral'):
        """Enhanced organization query handler with LMU-specific club knowledge"""
        search_results = self.semantic_search(query, top_k=3)
        personality = self.lmu_personality.get(tone, self.lmu_personality['neutral'])
        
        if search_results:
            best_result = search_results[0]
            if best_result['category'] == 'organization':
                org_info = best_result['data']
                
                if tone == 'casual':
                    response = f"🏛️ **{org_info['name']}** - {org_info['type']} Vibes! 🏛️\n\n"
                    response += f"📝 {org_info['description']}\n\n"
                    response += f"🔥 **What They Do:**\n"
                    for event in org_info.get('events', [])[:3]:
                        response += f"• {event}\n"
                    response += f"\n💡 **Pro Tip**: {org_info['name']} is {random.choice(['super active and fun', 'great for networking', 'perfect for making friends', 'really impactful on campus'])}! {random.choice(personality['excitement'])}\n\n"
                    response += "🎯 **Student Gossip**: They're always planning something exciting!"
                elif tone == 'formal':
                    response = f"🏛️ **{org_info['name']}** - {org_info['type']} Organization 🏛️\n\n"
                    response += f"📝 {org_info['description']}\n\n"
                    response += f"📋 **Activities and Events:**\n"
                    for event in org_info.get('events', [])[:3]:
                        response += f"• {event}\n"
                    response += f"\n💡 **Recommendation**: {org_info['name']} provides excellent opportunities for leadership development and community engagement.\n\n"
                    response += "📚 **Note**: This organization is well-respected within the campus community."
                else:
                    response = f"🏛️ **{org_info['name']}** - {org_info['type']} 🏛️\n\n"
                    response += f"📝 {org_info['description']}\n\n"
                    response += f"🎯 **Activities:**\n"
                    for event in org_info.get('events', [])[:3]:
                        response += f"• {event}\n"
                    response += f"\n💡 **Pro Tip**: {org_info['name']} is known for being {random.choice(['very active', 'great for networking', 'fun and engaging', 'impactful'])}! 🦁\n\n"
                    response += "🎯 **Campus Insight**: Students love being part of this organization!"
                
                response += self.add_contextual_recommendation(query, tone)
                response += self.sprinkle_lmu_trivia(tone)
                response += f"\n\n{self.get_lmu_insight('campus_culture', tone)}"
                response += f"\n\n{self.get_engaging_closing_prompt(tone)}"
                return response
        
        # General organization recommendations
        if tone == 'casual':
            response = "🏛️ **LMU Organizations - Get Involved!** 🏛️\n\n"
            response += "**Greek Life (Huge Here):**\n"
            response += "• About 30% of students are involved\n"
            response += "• Great for social life and leadership\n"
            response += "• Rush season is intense but worth it\n\n"
            response += "**Academic & Professional:**\n"
            response += "• Pre-professional clubs for every major\n"
            response += "• Honor societies and academic groups\n"
            response += "• Networking and career development\n\n"
            response += "**Cultural & Social:**\n"
            response += "• Cultural clubs celebrating diversity\n"
            response += "• Service organizations and volunteer groups\n"
            response += "• Special interest clubs for every hobby\n\n"
            response += f"💡 **Pro Tip**: Go to the involvement fair in September! {random.choice(personality['excitement'])}"
        elif tone == 'formal':
            response = "🏛️ **LMU Student Organizations** 🏛️\n\n"
            response += "**Greek Life Organizations:**\n"
            response += "• Approximately 30% of student body participation\n"
            response += "• Leadership development and social engagement opportunities\n"
            response += "• Structured recruitment process during designated periods\n\n"
            response += "**Academic and Professional Organizations:**\n"
            response += "• Discipline-specific professional development groups\n"
            response += "• Honor societies recognizing academic achievement\n"
            response += "• Career preparation and networking opportunities\n\n"
            response += "**Cultural and Service Organizations:**\n"
            response += "• Cultural diversity celebration and awareness groups\n"
            response += "• Community service and volunteer organizations\n"
            response += "• Special interest and hobby-based clubs\n\n"
            response += "💡 **Recommendation**: Attend the annual involvement fair for comprehensive information."
        else:
            response = "🏛️ **LMU Student Organizations** 🏛️\n\n"
            response += "**Greek Life:**\n"
            response += "• About 30% of students are involved\n"
            response += "• Great for social life and leadership development\n"
            response += "• Rush season happens in the fall\n\n"
            response += "**Academic & Professional:**\n"
            response += "• Clubs for every major and career path\n"
            response += "• Honor societies and academic groups\n"
            response += "• Networking and professional development\n\n"
            response += "**Cultural & Social:**\n"
            response += "• Cultural clubs and diversity organizations\n"
            response += "• Service and volunteer groups\n"
            response += "• Special interest clubs for hobbies\n\n"
            response += "💡 **Pro Tip**: Check out the involvement fair! 🦁"
        
        response += f"\n\n{self.get_lmu_insight('campus_culture', tone)}"
        return response
    
    def handle_facility_query(self, query, tone='neutral'):
        """Enhanced facility query handler with LMU-specific facility knowledge"""
        search_results = self.semantic_search(query, top_k=3)
        personality = self.lmu_personality.get(tone, self.lmu_personality['neutral'])
        
        if search_results:
            best_result = search_results[0]
            if best_result['category'] == 'facility':
                facility_info = best_result['data']
                
                if tone == 'casual':
                    response = f"🏢 **{facility_info['name']}** - {facility_info['type']} Spot! 🏢\n\n"
                    response += f"📍 Location: {facility_info['location']}\n"
                    response += f"⭐ Rating: {facility_info['rating']}/5.0\n\n"
                    response += f"🔥 **What's Cool Here:**\n"
                    for feature in facility_info.get('features', [])[:3]:
                        response += f"• {feature}\n"
                    response += f"\n💡 **Pro Tip**: {facility_info['name']} is {random.choice(['perfect for studying', 'great for hanging out', 'awesome for events', 'super convenient'])}! {random.choice(personality['excitement'])}\n\n"
                    response += "🎯 **Student Gossip**: This is definitely one of the best spots on campus!"
                elif tone == 'formal':
                    response = f"🏢 **{facility_info['name']}** - {facility_info['type']} Facility 🏢\n\n"
                    response += f"📍 Location: {facility_info['location']}\n"
                    response += f"⭐ Rating: {facility_info['rating']}/5.0\n\n"
                    response += f"📋 **Available Features:**\n"
                    for feature in facility_info.get('features', [])[:3]:
                        response += f"• {feature}\n"
                    response += f"\n💡 **Recommendation**: {facility_info['name']} provides excellent resources and amenities for student use.\n\n"
                    response += "📚 **Note**: This facility is highly utilized by the campus community."
                else:
                    response = f"🏢 **{facility_info['name']}** - {facility_info['type']} 🏢\n\n"
                    response += f"📍 Location: {facility_info['location']}\n"
                    response += f"⭐ Rating: {facility_info['rating']}/5.0\n\n"
                    response += f"✅ **Features:**\n"
                    for feature in facility_info.get('features', [])[:3]:
                        response += f"• {feature}\n"
                    response += f"\n💡 **Pro Tip**: {facility_info['name']} is known for being {random.choice(['great for studying', 'perfect for socializing', 'very convenient', 'really nice'])}! 🦁\n\n"
                    response += "🎯 **Campus Insight**: Students love using this facility!"
                
                response += self.add_contextual_recommendation(query, tone)
                response += self.sprinkle_lmu_trivia(tone)
                response += f"\n\n{self.get_lmu_insight('hidden_gems', tone)}"
                response += f"\n\n{self.get_engaging_closing_prompt(tone)}"
                return response
        
        # General facility recommendations
        if tone == 'casual':
            response = "🏢 **LMU Facilities - Where to Be** 🏢\n\n"
            response += "**Study Spots:**\n"
            response += "• Hannon Library - 3rd floor is the quietest\n"
            response += "• Burns Fine Arts rooftop - best sunset views\n"
            response += "• The bluff trail - perfect for outdoor studying\n\n"
            response += "**Fitness & Recreation:**\n"
            response += "• Burns Recreation Center - full gym and pool\n"
            response += "• Outdoor basketball and tennis courts\n"
            response += "• Hiking trails behind campus\n\n"
            response += "**Social Spaces:**\n"
            response += "• The Lair - main dining and hangout spot\n"
            response += "• Sacred Heart Chapel - peaceful meditation garden\n"
            response += "• Various lounges throughout campus\n\n"
            response += f"💡 **Pro Tip**: The library's ocean view study rooms are everything! {random.choice(personality['excitement'])}"
        elif tone == 'formal':
            response = "🏢 **LMU Campus Facilities** 🏢\n\n"
            response += "**Academic Facilities:**\n"
            response += "• Hannon Library - comprehensive study spaces and research resources\n"
            response += "• Burns Fine Arts Center - rooftop study areas with scenic views\n"
            response += "• Outdoor study locations along the bluff trail\n\n"
            response += "**Recreational Facilities:**\n"
            response += "• Burns Recreation Center - comprehensive fitness and aquatic facilities\n"
            response += "• Outdoor athletic courts and playing fields\n"
            response += "• Natural hiking trails and outdoor recreation areas\n\n"
            response += "**Social and Community Spaces:**\n"
            response += "• The Lair - primary dining and social gathering facility\n"
            response += "• Sacred Heart Chapel - spiritual and contemplative spaces\n"
            response += "• Various student lounges and common areas\n\n"
            response += "💡 **Recommendation**: The library's ocean-view study rooms provide excellent academic environments."
        else:
            response = "🏢 **LMU Campus Facilities** 🏢\n\n"
            response += "**Study Areas:**\n"
            response += "• Hannon Library - 3rd floor is the quietest\n"
            response += "• Burns Fine Arts rooftop - amazing sunset views\n"
            response += "• The bluff trail - great for outdoor studying\n\n"
            response += "**Fitness & Recreation:**\n"
            response += "• Burns Recreation Center - full gym and pool\n"
            response += "• Outdoor basketball and tennis courts\n"
            response += "• Hiking trails behind campus\n\n"
            response += "**Social Spaces:**\n"
            response += "• The Lair - main dining and hangout area\n"
            response += "• Sacred Heart Chapel - peaceful meditation garden\n"
            response += "• Various lounges throughout campus\n\n"
            response += "💡 **Pro Tip**: The library's ocean view study rooms are amazing! 🦁"
        
        response += self.add_contextual_recommendation(query, tone)
        response += self.sprinkle_lmu_trivia(tone)
        response += f"\n\n{self.get_lmu_insight('hidden_gems', tone)}"
        response += f"\n\n{self.get_engaging_closing_prompt(tone)}"
        return response
    
    def handle_news_query(self, query, tone='neutral'):
        """Enhanced news query handler with LMU-specific current events"""
        personality = self.lmu_personality.get(tone, self.lmu_personality['neutral'])
        
        if tone == 'casual':
            response = "📰 **LMU News & Updates - What's Good** 📰\n\n"
            response += "**Campus Happenings:**\n"
            response += "• New dining options coming to the Lair next semester\n"
            response += "• Construction on the new student center is almost done\n"
            response += "• Basketball team is killing it this season\n"
            response += "• Film school students winning major awards\n\n"
            response += "**Student Life Updates:**\n"
            response += "• New clubs and organizations forming\n"
            response += "• Greek life recruitment numbers are up\n"
            response += "• Study abroad programs expanding\n"
            response += "• Career fair dates announced\n\n"
            response += f"💡 **Pro Tip**: Follow @lmu_news on Instagram for real-time updates! {random.choice(personality['excitement'])}"
        elif tone == 'formal':
            response = "📰 **LMU News and Announcements** 📰\n\n"
            response += "**Campus Developments:**\n"
            response += "• Enhanced dining facilities scheduled for next academic term\n"
            response += "• New student center construction nearing completion\n"
            response += "• Athletic programs achieving notable success\n"
            response += "• Film and television program receiving industry recognition\n\n"
            response += "**Student Affairs Updates:**\n"
            response += "• New student organizations being established\n"
            response += "• Greek life participation showing positive trends\n"
            response += "• International study opportunities expanding\n"
            response += "• Professional development events being scheduled\n\n"
            response += "💡 **Recommendation**: Monitor official LMU communication channels for current information."
        else:
            response = "📰 **LMU News & Updates** 📰\n\n"
            response += "**Campus News:**\n"
            response += "• New dining options coming to campus\n"
            response += "• Student center construction almost complete\n"
            response += "• Basketball team having a great season\n"
            response += "• Film school students winning awards\n\n"
            response += "**Student Life:**\n"
            response += "• New clubs and organizations starting up\n"
            response += "• Greek life recruitment going well\n"
            response += "• Study abroad programs expanding\n"
            response += "• Career fair dates announced\n\n"
            response += "💡 **Pro Tip**: Follow LMU social media for updates! 🦁"
        
        response += self.add_contextual_recommendation(query, tone)
        response += self.sprinkle_lmu_trivia(tone)
        response += f"\n\n{self.get_lmu_insight('campus_culture', tone)}"
        response += f"\n\n{self.get_engaging_closing_prompt(tone)}"
        return response
    
    def handle_general_query(self, query, tone='neutral'):
        """Enhanced general query handler with sophisticated LMU-specific knowledge and context awareness"""
        search_results = self.semantic_search(query, top_k=2)
        personality = self.lmu_personality.get(tone, self.lmu_personality['neutral'])
        
        # Check conversation history for context
        recent_context = ""
        if len(self.conversation_history) > 2:
            recent_topics = []
            for msg in self.conversation_history[-4:]:
                if msg["role"] == "user":
                    user_input_lower = msg["content"].lower()
                    if any(word in user_input_lower for word in ['professor', 'course', 'academic']):
                        recent_topics.append('academic')
                    elif any(word in user_input_lower for word in ['food', 'dining', 'eat']):
                        recent_topics.append('dining')
                    elif any(word in user_input_lower for word in ['event', 'party', 'social']):
                        recent_topics.append('social')
                    elif any(word in user_input_lower for word in ['housing', 'dorm', 'live']):
                        recent_topics.append('housing')
            
            if recent_topics:
                most_common = max(set(recent_topics), key=recent_topics.count)
                if most_common == 'academic':
                    recent_context = "academic"
                elif most_common == 'dining':
                    recent_context = "dining"
                elif most_common == 'social':
                    recent_context = "social"
                elif most_common == 'housing':
                    recent_context = "housing"
        
        if search_results:
            # Use the most relevant result
            best_result = search_results[0]
            category = best_result['category']
            data = best_result['data']
            
            if category == 'professor':
                return self.handle_professor_query(query, tone)
            elif category == 'course':
                return self.handle_course_query(query, tone)
            elif category == 'dining':
                return self.handle_dining_query(query, tone)
            elif category == 'housing':
                return self.handle_housing_query(query, tone)
            elif category == 'event':
                return self.handle_event_query(query, tone)
            elif category == 'organization':
                return self.handle_organization_query(query, tone)
            elif category == 'facility':
                return self.handle_facility_query(query, tone)
        
        # Enhanced tone-aware responses with context awareness and LMU-specific knowledge
        if len(self.conversation_history) > 2:
            if tone == 'formal':
                response = "I appreciate your continued engagement with our LMU campus assistant! As your dedicated academic companion, I'm equipped to provide comprehensive information about all aspects of university life, including academic matters, dining establishments, study facilities, social events, Greek life organizations, and transportation options. "
                
                if recent_context == "academic":
                    response += "Given our previous discussion about academic matters, I'd be happy to provide more detailed information about specific courses, professors, or study resources. "
                elif recent_context == "dining":
                    response += "Since we've been discussing dining options, I can offer additional insights about campus food services, meal plans, or nearby dining establishments. "
                elif recent_context == "social":
                    response += "Building on our conversation about social activities, I can provide information about upcoming events, student organizations, or campus life opportunities. "
                elif recent_context == "housing":
                    response += "Following our discussion about housing, I can offer more details about residence life, housing policies, or living arrangements. "
                
                response += "I'm continuously updating my knowledge base to serve our campus community more effectively and provide the most current and relevant information."
                
            elif tone == 'casual':
                response = f"Yo, that's a great question! As your LMU Buddy, I'm literally here for everything campus-related. Whether you need the tea on professors, want to know about the best food spots, need study location recommendations, or want to know what's popping this weekend - I got you! "
                
                if recent_context == "academic":
                    response += "Since we've been talking about classes and stuff, I can definitely help you find the best professors or figure out which courses to take! "
                elif recent_context == "dining":
                    response += "Building on our food talk, I know all the best spots and when to hit them to avoid the crowds! "
                elif recent_context == "social":
                    response += "Following up on the social scene, I can tell you about the latest events and which organizations are worth checking out! "
                elif recent_context == "housing":
                    response += "Since we've been discussing housing, I can give you the real scoop on which dorms are the best and what to expect! "
                
                response += f"I'm constantly learning more about our amazing campus and all the little secrets that make LMU special. {random.choice(personality['excitement'])}"
                
            else:
                response = "🤔 That's a great question! As your LMU Buddy, I'm here to help with everything campus-related. "
                
                if recent_context == "academic":
                    response += "Since we've been talking about academics, I can help you find great professors, courses, or study resources! "
                elif recent_context == "dining":
                    response += "Building on our food discussion, I know all the best dining spots and tips! "
                elif recent_context == "social":
                    response += "Following our social talk, I can tell you about upcoming events and campus activities! "
                elif recent_context == "housing":
                    response += "Since we've been discussing housing, I can give you insights about residence life! "
                
                response += "Try asking me about professors, courses, food spots, study locations, weekend events, Greek life, or parking tips! I'm constantly learning more about our amazing campus. 🦁✨"
        else:
            if tone == 'formal':
                response = "Greetings! I am your LMU campus assistant, designed to provide comprehensive information about all aspects of university life. I can assist you with academic inquiries, dining recommendations, facility information, event schedules, organizational details, transportation options, and much more. "
                response += "Our campus offers a unique blend of academic excellence, vibrant student life, and beautiful surroundings on the bluff overlooking Los Angeles. "
                response += "How may I be of service to you today?"
                
            elif tone == 'casual':
                response = f"Yo! I'm your LMU Buddy - your AI campus companion! I know literally everything about LMU, from the best professors and courses to the hidden food spots and upcoming events. "
                response += "I'm basically your personal campus insider who's been programmed with all the tea about life on the bluff! "
                response += f"What do you want to know about LMU? {random.choice(personality['excitement'])}"
                
            else:
                response = "👋 Hey! I'm your LMU Buddy - your AI campus companion! I can help you with everything from finding the best professors and courses to discovering great food spots and upcoming events. "
                response += "I'm specifically designed to know all about LMU and life on the bluff - from academic tips to campus secrets! "
                response += "What would you like to know about LMU? 🦁✨"
        
        # Add relevant LMU insights based on the query
        query_lower = query.lower()
        if any(word in query_lower for word in ['help', 'assist', 'support']):
            response += f"\n\n{self.get_lmu_insight('campus_culture', tone)}"
        elif any(word in query_lower for word in ['study', 'learn', 'academic']):
            response += f"\n\n{self.get_lmu_insight('academic_tips', tone)}"
        elif any(word in query_lower for word in ['fun', 'enjoy', 'experience']):
            response += f"\n\n{self.get_lmu_insight('student_life', tone)}"
        elif any(word in query_lower for word in ['secret', 'hidden', 'unknown']):
            response += f"\n\n{self.get_lmu_insight('hidden_gems', tone)}"
        else:
            # Add a random insight for general queries
            insight_categories = ['campus_culture', 'student_life', 'academic_tips', 'hidden_gems']
            random_category = random.choice(insight_categories)
            response += f"\n\n{self.get_lmu_insight(random_category, tone)}"
        
        # Add contextual recommendations and trivia
        response += self.add_contextual_recommendation(query, tone)
        response += self.sprinkle_lmu_trivia(tone)
        
        # Add engaging closing prompt
        response += f"\n\n{self.get_engaging_closing_prompt(tone)}"
        
        return response
    
    def handle_unknown_query(self, query, tone='neutral'):
        """Handle unknown or too broad queries with helpful redirection"""
        personality = self.lmu_personality.get(tone, self.lmu_personality['neutral'])
        
        if tone == 'casual':
            response = f"That's a great question! I'm still learning, but here are some things I can help you with: {random.choice(personality['excitement'])}\n\n"
            response += "🎯 **Try asking me about:**\n"
            response += "• 'What's popping this week?' (for events)\n"
            response += "• 'Where should I eat on campus?' (for dining)\n"
            response += "• 'Show me some good professors' (for academics)\n"
            response += "• 'What clubs should I join?' (for organizations)\n"
            response += "• 'Where can I study?' (for facilities)\n\n"
            response += "💡 **Pro Tip**: Be specific and I'll give you the best info! For official stuff, check out the LMU website."
        elif tone == 'formal':
            response = "That's an excellent question! While I'm continuously expanding my knowledge base, I can provide information on the following topics:\n\n"
            response += "📋 **Available Information:**\n"
            response += "• Academic matters (professors, courses, study resources)\n"
            response += "• Campus facilities and services\n"
            response += "• Dining options and meal plans\n"
            response += "• Student organizations and activities\n"
            response += "• Transportation and parking information\n\n"
            response += "💡 **Recommendation**: For official university information, please consult the LMU website or contact the appropriate department."
        else:
            response = "That's a great question! I'm still learning, but you might check out the official LMU website or try asking me about:\n\n"
            response += "🎯 **Popular topics:**\n"
            response += "• 'What's happening this week?' (for events)\n"
            response += "• 'Where should I eat on campus?' (for dining)\n"
            response += "• 'Show me some good professors' (for academics)\n"
            response += "• 'What clubs should I join?' (for organizations)\n"
            response += "• 'Where can I study?' (for facilities)\n\n"
            response += "💡 **Pro Tip**: Be specific and I'll give you the best info! 🦁"
        
        response += self.sprinkle_lmu_trivia(tone)
        response += f"\n\n{self.get_engaging_closing_prompt(tone)}"
        return response
    
    def handle_transportation_query(self, query, tone='neutral'):
        """Handle transportation and parking queries with LMU-specific knowledge"""
        personality = self.lmu_personality.get(tone, self.lmu_personality['neutral'])
        
        if tone == 'casual':
            response = "🚗 **LMU Transportation & Parking Guide** 🚗\n\n"
            response += "**Parking Drama (It's Real):**\n"
            response += "• Get there early (like 8 AM early) or you're SOL\n"
            response += "• The main lots fill up by 9 AM on weekdays\n"
            response += "• Pro tip: Park at the Playa Vista shuttle lot - it's free with your student ID!\n\n"
            response += "**Shuttle Service:**\n"
            response += "• Runs every 15 minutes during peak hours\n"
            response += "• Free with your student ID\n"
            response += "• Saves you from the parking ticket stress! 🎫\n\n"
            response += "**Alternative Options:**\n"
            response += "• Uber/Lyft from nearby areas\n"
            response += "• Bike racks are available throughout campus\n"
            response += "• Walking from nearby apartments is totally doable\n\n"
            response += f"💡 **Pro Tip**: Download the LMU app for real-time shuttle tracking! {random.choice(personality['excitement'])}"
        elif tone == 'formal':
            response = "🚗 **LMU Transportation & Parking Information** 🚗\n\n"
            response += "**Parking Facilities:**\n"
            response += "• Main campus lots are available for students with valid permits\n"
            response += "• Early arrival is recommended as lots fill quickly during peak hours\n"
            response += "• Alternative parking is available at the Playa Vista shuttle location\n\n"
            response += "**Shuttle Service:**\n"
            response += "• Regular service every 15 minutes during academic hours\n"
            response += "• Complimentary access with valid student identification\n"
            response += "• Provides convenient transportation to and from campus\n\n"
            response += "**Additional Transportation Options:**\n"
            response += "• Ride-sharing services are readily available\n"
            response += "• Bicycle facilities are provided throughout campus\n"
            response += "• Walking access is available from nearby residential areas\n\n"
            response += "💡 **Recommendation**: Utilize the LMU mobile application for real-time shuttle tracking."
        else:
            response = "🚗 **LMU Transportation & Parking Guide** 🚗\n\n"
            response += "**Parking:**\n"
            response += "• Arrive early (before 9 AM) for best parking availability\n"
            response += "• Main lots fill up quickly during weekdays\n"
            response += "• Playa Vista shuttle lot is a great alternative - free with student ID!\n\n"
            response += "**Shuttle Service:**\n"
            response += "• Runs every 15 minutes during peak hours\n"
            response += "• Free with your student ID\n"
            response += "• Convenient way to avoid parking hassles\n\n"
            response += "**Other Options:**\n"
            response += "• Uber/Lyft available from nearby areas\n"
            response += "• Bike racks throughout campus\n"
            response += "• Walking distance from many nearby apartments\n\n"
            response += "💡 **Pro Tip**: Use the LMU app for real-time shuttle tracking! 🦁"
        
        response += self.add_contextual_recommendation(query, tone)
        response += self.sprinkle_lmu_trivia(tone)
        response += f"\n\n{self.get_lmu_insight('student_life', tone)}"
        response += f"\n\n{self.get_engaging_closing_prompt(tone)}"
        return response
    
    def handle_campus_life_query(self, query, tone='neutral'):
        """Handle campus life and general LMU experience queries"""
        personality = self.lmu_personality.get(tone, self.lmu_personality['neutral'])
        
        if tone == 'casual':
            response = "🌅 **Life on the Bluff - LMU Campus Vibes** 🌅\n\n"
            response += "**The Views:**\n"
            response += "• Literally the best sunset views in LA from the bluff\n"
            response += "• You can see the ocean, downtown, and the Hollywood sign\n"
            response += "• Perfect for Instagram pics and study breaks\n\n"
            response += "**The Weather:**\n"
            response += "• Basically perfect year-round (we're spoiled)\n"
            response += "• Rarely gets too hot or too cold\n"
            response += "• Ocean breeze keeps everything fresh\n\n"
            response += "**The Community:**\n"
            response += "• Super tight-knit campus community\n"
            response += "• Everyone knows everyone (in a good way)\n"
            response += "• Strong school spirit and pride\n\n"
            response += f"💡 **Pro Tip**: The bluff trail behind campus is perfect for sunset walks! {random.choice(personality['excitement'])}"
        elif tone == 'formal':
            response = "🌅 **LMU Campus Life Overview** 🌅\n\n"
            response += "**Campus Location:**\n"
            response += "• Situated on a bluff with panoramic views of Los Angeles\n"
            response += "• Offers vistas of the Pacific Ocean, downtown skyline, and surrounding areas\n"
            response += "• Provides an ideal setting for academic and recreational activities\n\n"
            response += "**Climate:**\n"
            response += "• Mediterranean climate with mild temperatures throughout the year\n"
            response += "• Consistent weather patterns conducive to outdoor activities\n"
            response += "• Ocean breezes provide natural climate control\n\n"
            response += "**Community Atmosphere:**\n"
            response += "• Close-knit academic community with strong interpersonal connections\n"
            response += "• Collaborative environment fostering meaningful relationships\n"
            response += "• Vibrant campus culture with active student engagement\n\n"
            response += "💡 **Recommendation**: The bluff trail offers excellent opportunities for outdoor recreation and reflection."
        else:
            response = "🌅 **Life on the Bluff - LMU Campus Experience** 🌅\n\n"
            response += "**The Views:**\n"
            response += "• Amazing sunset views from the bluff overlooking LA\n"
            response += "• You can see the ocean, downtown, and the Hollywood sign\n"
            response += "• Perfect for photos and peaceful study breaks\n\n"
            response += "**The Weather:**\n"
            response += "• Great weather year-round - we're lucky!\n"
            response += "• Rarely too extreme in either direction\n"
            response += "• Ocean breeze keeps the air fresh\n\n"
            response += "**The Community:**\n"
            response += "• Close-knit campus where people really connect\n"
            response += "• Strong sense of community and school pride\n"
            response += "• Everyone is friendly and supportive\n\n"
            response += "💡 **Pro Tip**: The bluff trail is perfect for sunset walks! 🦁"
        
        response += self.add_contextual_recommendation(query, tone)
        response += self.sprinkle_lmu_trivia(tone)
        response += f"\n\n{self.get_lmu_insight('campus_culture', tone)}"
        response += f"\n\n{self.get_lmu_insight('hidden_gems', tone)}"
        response += f"\n\n{self.get_engaging_closing_prompt(tone)}"
        return response

def create_enhanced_chat_interface():
    """Create the enhanced chat interface"""
    st.markdown("""
    <div class="main-header">
        <h1>🤖 Enhanced LMU Buddy - Your AI Campus Companion</h1>
        <p>Powered by advanced AI with comprehensive LMU knowledge!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize Enhanced LMU Buddy
    if 'enhanced_lmu_buddy' not in st.session_state:
        with st.spinner("Loading LMU Buddy... This may take a moment on first run."):
            st.session_state.enhanced_lmu_buddy = EnhancedLMUBuddy()
    
    # Chat interface
    st.markdown("### 💬 Chat with Enhanced LMU Buddy")
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message">{message["content"]}</div>', unsafe_allow_html=True)
    
    # Chat input
    user_input = st.text_input("What LMU magic can I help you with? 🔥", key="enhanced_chat_input")
    
    if st.button("Send", key="enhanced_send_button") and user_input:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Get AI response
        with st.spinner("LMU Buddy is thinking..."):
            ai_response = st.session_state.enhanced_lmu_buddy.generate_response(user_input)
        st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
        
        st.rerun()
    
    # Quick access buttons
    st.markdown("### 🚀 Quick Access")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📚 Academic**")
        if st.button("Find Professors", key="find_professors"):
            st.session_state.chat_history.append({"role": "user", "content": "Show me some good professors"})
            ai_response = st.session_state.enhanced_lmu_buddy.generate_response("Show me some good professors")
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            st.rerun()
        
        if st.button("Popular Courses", key="popular_courses"):
            st.session_state.chat_history.append({"role": "user", "content": "What are some popular courses?"})
            ai_response = st.session_state.enhanced_lmu_buddy.generate_response("What are some popular courses?")
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            st.rerun()
    
    with col2:
        st.markdown("**🎉 Campus Life**")
        if st.button("Upcoming Events", key="upcoming_events"):
            st.session_state.chat_history.append({"role": "user", "content": "What events are coming up?"})
            ai_response = st.session_state.enhanced_lmu_buddy.generate_response("What events are coming up?")
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            st.rerun()
        
        if st.button("Best Food Spots", key="best_food"):
            st.session_state.chat_history.append({"role": "user", "content": "Where should I eat on campus?"})
            ai_response = st.session_state.enhanced_lmu_buddy.generate_response("Where should I eat on campus?")
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            st.rerun()
    
    # Data insights
    st.markdown("### 📊 LMU Data Insights")
    
    buddy = st.session_state.enhanced_lmu_buddy
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Professors", len(buddy.data.get('professors', [])))
    with col2:
        st.metric("Courses", len(buddy.data.get('courses', [])))
    with col3:
        st.metric("Dining Options", len(buddy.data.get('dining', [])))
    with col4:
        st.metric("Organizations", len(buddy.data.get('organizations', [])))
    
    # Feedback system
    st.markdown("### 👍 How was your experience?")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("👍 Great!", key="feedback_great"):
            st.success("Thanks! LMU Buddy is learning and improving! 🦁")
    with col2:
        if st.button("👎 Could be better", key="feedback_better"):
            st.info("Thanks for the feedback! We're constantly working to improve.")
    with col3:
        if st.button("🔄 Clear Chat", key="clear_enhanced_chat"):
            st.session_state.chat_history = []
            st.rerun()

if __name__ == "__main__":
    create_enhanced_chat_interface()