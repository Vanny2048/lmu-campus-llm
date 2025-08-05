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

class EnhancedLMUBuddy:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.data = self.load_lmu_data()
        self.embeddings = self.load_or_compute_embeddings()
        self.conversation_history = []
        
    def load_lmu_data(self):
        """Load LMU data from JSON file"""
        try:
            with open('lmu_data.json', 'r') as f:
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
                pickle.dump((embeddings, text_mapping), f)
            
            return embeddings, text_mapping
        else:
            return np.array([]), []
    
    def semantic_search(self, query, top_k=3):
        """Perform semantic search on LMU data"""
        if not self.embeddings[0].size:
            return []
        
        query_embedding = self.model.encode([query])
        similarities = cosine_similarity(query_embedding, self.embeddings[0])[0]
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.3:  # Threshold for relevance
                category, data = self.embeddings[1][idx]
                results.append({
                    'category': category,
                    'data': data,
                    'similarity': similarities[idx]
                })
        
        return results
    
    def get_professor_info(self, query):
        """Get specific professor information"""
        query_lower = query.lower()
        
        for prof in self.data.get('professors', []):
            if prof['name'].lower() in query_lower or any(course.lower() in query_lower for course in prof.get('courses', [])):
                return prof
        
        return None
    
    def get_course_info(self, query):
        """Get specific course information"""
        query_lower = query.lower()
        
        for course in self.data.get('courses', []):
            if course['code'].lower() in query_lower or course['name'].lower() in query_lower:
                return course
        
        return None
    
    def get_upcoming_events(self, days=7):
        """Get upcoming events within specified days"""
        today = datetime.now()
        upcoming = []
        
        for event in self.data.get('events', []):
            try:
                event_date = datetime.strptime(event['date'], '%Y-%m-%d')
                if event_date >= today and event_date <= today + timedelta(days=days):
                    upcoming.append(event)
            except:
                continue
        
        return sorted(upcoming, key=lambda x: x['date'])
    
    def analyze_user_tone(self, user_input):
        """Analyze user's tone to mirror it in responses"""
        user_input_lower = user_input.lower()
        
        # Check for formal indicators
        formal_indicators = ['please', 'thank you', 'would you', 'could you', 'may i', 'excuse me', 'pardon']
        informal_indicators = ['yo', 'hey', 'whats up', 'sup', 'bro', 'dude', 'omg', 'lol', 'fr', 'ngl', 'tbh']
        
        formal_count = sum(1 for indicator in formal_indicators if indicator in user_input_lower)
        informal_count = sum(1 for indicator in informal_indicators if indicator in user_input_lower)
        
        # Check for emoji usage
        emoji_count = len([char for char in user_input if ord(char) > 127])
        
        # Check for punctuation patterns
        exclamation_count = user_input.count('!')
        question_count = user_input.count('?')
        
        # Determine tone
        if formal_count > informal_count or (len(user_input.split()) > 15 and emoji_count == 0):
            return 'formal'
        elif informal_count > formal_count or emoji_count > 0 or exclamation_count > 1:
            return 'casual'
        else:
            return 'neutral'

    def generate_response(self, user_input):
        """Generate intelligent response based on user input with tone mirroring"""
        user_input_lower = user_input.lower()
        
        # Analyze user tone
        user_tone = self.analyze_user_tone(user_input)
        
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Check for specific query types
        if any(word in user_input_lower for word in ['professor', 'teacher', 'instructor']):
            return self.handle_professor_query(user_input, user_tone)
        elif any(word in user_input_lower for word in ['course', 'class', 'subject']):
            return self.handle_course_query(user_input, user_tone)
        elif any(word in user_input_lower for word in ['food', 'eat', 'dining', 'restaurant']):
            return self.handle_dining_query(user_input, user_tone)
        elif any(word in user_input_lower for word in ['housing', 'dorm', 'apartment', 'live']):
            return self.handle_housing_query(user_input, user_tone)
        elif any(word in user_input_lower for word in ['event', 'activity', 'weekend', 'party']):
            return self.handle_event_query(user_input, user_tone)
        elif any(word in user_input_lower for word in ['organization', 'club', 'greek', 'sorority', 'fraternity']):
            return self.handle_organization_query(user_input, user_tone)
        elif any(word in user_input_lower for word in ['facility', 'library', 'study', 'gym']):
            return self.handle_facility_query(user_input, user_tone)
        elif any(word in user_input_lower for word in ['news', 'announcement', 'update']):
            return self.handle_news_query(user_input, user_tone)
        else:
            return self.handle_general_query(user_input, user_tone)
    
    def handle_professor_query(self, query, tone='neutral'):
        """Handle professor-related queries with tone-aware responses"""
        prof_info = self.get_professor_info(query)
        
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
                response += f"💡 {tip_start}: {prof_info['name']} is known for being super chill in office hours. Students say they're really approachable and actually care about your success. Plus, they usually curve generously! 🦁\n\n"
                response += "🎯 **Student Gossip**: Rumor has it they're working on some groundbreaking research in their field. Might be worth asking about in class!"
            elif tone == 'formal':
                response += f"💡 {tip_start}: Professor {prof_info['name']} maintains excellent office hours and is known for their dedication to student success. Many students report significant academic growth in their courses.\n\n"
                response += "📚 **Academic Note**: They are actively engaged in research and often welcome undergraduate participation in their projects."
            else:
                response += f"💡 {tip_start}: Check Rate My Professor for detailed reviews and student experiences! 🦁\n\n"
                response += "🎓 **Campus Insight**: This professor is well-respected in their department and often mentors students beyond the classroom."
            
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
                response += "\n💡 Try asking about a specific prof by name! I know all the tea on campus faculty 😏"
            elif tone == 'formal':
                response += "\n💡 Please try asking about a specific professor by name for more detailed information."
            else:
                response += "\n💡 Try asking about a specific professor by name!"
            return response
        
        return not_found
    
    def handle_course_query(self, query, tone='neutral'):
        """Handle course-related queries with tone-aware responses"""
        course_info = self.get_course_info(query)
        
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
            response = f"📚 **{course_info['code']}: {course_info['name']}**\n\n"
            response += f"🏫 Department: {course_info['department']}\n"
            response += f"📝 Credits: {course_info['credits']}\n"
            response += f"⭐ Rating: {course_info['rating']}/5.0\n\n"
            response += f"📖 Description: {course_info['description']}\n\n"
            response += f"👨‍🏫 Professors: {', '.join(course_info['professors'])}\n"
            response += f"📋 Prerequisites: {course_info['prerequisites']}\n\n"
            
            # Add intimate LMU knowledge based on tone
            if tone == 'casual':
                response += f"💡 {tip_start}: This class is actually pretty popular! Students say the workload is manageable and the professors are super helpful. Plus, it's a great way to meet people in your major! 🦁\n\n"
                response += "🎯 **Student Gossip**: Rumor has it this course is getting updated next semester with some really cool new content!"
            elif tone == 'formal':
                response += f"💡 {tip_start}: This course is highly regarded among students for its comprehensive curriculum and supportive faculty. It serves as an excellent foundation for advanced studies in the field.\n\n"
                response += "📚 **Academic Note**: The course is being updated next semester to incorporate the latest developments in the field."
            else:
                response += f"💡 {tip_start}: Check the course catalog for current availability and schedules! 🦁\n\n"
                response += "🎓 **Campus Insight**: This course is popular among students and known for its engaging content."
            
            return response
        
        # Search for courses by department or topic
        search_results = self.semantic_search(query, top_k=3)
        if search_results:
            if tone == 'casual':
                response = "🔍 Here are some courses that might be what you're looking for:\n\n"
            elif tone == 'formal':
                response = "🔍 Here are some courses that might interest you:\n\n"
            else:
                response = "🔍 Here are some courses that might interest you:\n\n"
                
            for result in search_results:
                if result['category'] == 'course':
                    course = result['data']
                    response += f"• **{course['code']}**: {course['name']} ({course['department']})\n"
            
            if tone == 'casual':
                response += "\n💡 Ask about a specific course code for more details! I know all the tea on campus classes 😏"
            elif tone == 'formal':
                response += "\n💡 Please ask about a specific course code for more detailed information."
            else:
                response += "\n💡 Ask about a specific course code for more details!"
            return response
        
        return not_found
    
    def handle_dining_query(self, query, tone='neutral'):
        """Handle dining-related queries with intimate LMU knowledge"""
        search_results = self.semantic_search(query, top_k=3)
        
        # Tone-specific language
        if tone == 'formal':
            response = "🍽️ Here are the premier dining establishments on campus:\n\n"
            tip_start = "Recommendation"
            insider_tip = "**Campus Insight**: The culinary team at LMU consistently receives high marks for quality and variety."
        elif tone == 'casual':
            response = "🍕 Alright, here's the real tea on campus food:\n\n"
            tip_start = "Pro tip"
            insider_tip = "**Student Gossip**: The Lair's pizza is lowkey better than most delivery places, and the staff is super nice!"
        else:
            response = "🍕 Here are the best dining options on campus:\n\n"
            tip_start = "Pro tip"
            insider_tip = "**Campus Secret**: The Lair's pizza is surprisingly good, and the staff remembers regulars!"
        
        if search_results:
            for result in search_results:
                if result['category'] == 'dining':
                    dining = result['data']
                    response += f"🏪 **{dining['name']}** ({dining['type']})\n"
                    response += f"🕐 Hours: {dining['hours']}\n"
                    response += f"⭐ Rating: {dining['rating']}/5.0\n"
                    response += f"🍽️ Popular: {', '.join(dining['popular_items'][:3])}\n"
                    response += f"✨ Features: {', '.join(dining['features'][:2])}\n\n"
            
            # Add intimate LMU knowledge
            if tone == 'casual':
                response += f"💡 {tip_start}: The Lair is always a safe bet for variety, and Lion's Den has the best smoothie bowls! But here's the real hack - go to the Lair at 11:45 AM or 5:45 PM to beat the rush. The staff is super chill and will hook you up with extra toppings if you're nice! 🦁\n\n"
                response += insider_tip + "\n\n"
                response += "🎯 **Hidden Gem**: The coffee cart near the library has the best iced lattes on campus, and the barista knows everyone's order by heart!"
            elif tone == 'formal':
                response += f"💡 {tip_start}: The Lair offers excellent variety and quality, while the Lion's Den provides healthy alternatives perfect for busy students. Optimal dining times are 11:45 AM and 5:45 PM to avoid peak crowds.\n\n"
                response += insider_tip + "\n\n"
                response += "📚 **Academic Note**: Many students find the quiet atmosphere at the Lion's Den conducive to studying during off-peak hours."
            else:
                response += f"💡 {tip_start}: The Lair is always a safe bet for variety, and Lion's Den has the best smoothie bowls! 🦁\n\n"
                response += insider_tip + "\n\n"
                response += "🎓 **Campus Tip**: The coffee cart near the library has amazing iced lattes and the barista is super friendly!"
            
            return response
        
        # Fallback with intimate knowledge
        if tone == 'casual':
            return "🍕 Yo, the best food spots on campus? Hands down, it's the Lair! Their pizza is actually fire, and the smoothie bowls at the Lion's Den are perfect for those early morning classes. But here's the real tea - go 15 minutes before the lunch crowd hits to avoid the line, and the staff will literally remember your name if you go regularly. Plus, the coffee cart near the library? That barista is a legend and makes the best iced lattes on campus! 🦁"
        elif tone == 'formal':
            return "🍽️ The premier dining establishment on campus is undoubtedly the Lair, which offers exceptional variety and quality. The Lion's Den provides excellent healthy alternatives, particularly their smoothie bowls which are perfect for early morning classes. I recommend visiting 15 minutes before peak dining hours to avoid crowds. The staff is consistently friendly and accommodating to regular patrons."
        else:
            return "🍕 The best food spots on campus? Hands down, it's the Lair! Their pizza is legendary, and the smoothie bowls at the Lion's Den are perfect for those early morning classes. Pro tip: avoid the rush by going 15 minutes before the lunch crowd hits! The staff is super friendly and remembers regulars. Plus, the coffee cart near the library has amazing iced lattes! 🦁"
    
    def handle_housing_query(self, query, tone='neutral'):
        """Handle housing-related queries with tone-aware responses"""
        search_results = self.semantic_search(query, top_k=3)
        
        # Tone-specific language
        if tone == 'formal':
            response = "🏠 Here's comprehensive information about LMU housing options:\n\n"
            tip_start = "Recommendation"
            insider_tip = "**Campus Insight**: Housing assignments are prioritized based on class standing and special circumstances."
        elif tone == 'casual':
            response = "🏠 Alright, here's the real tea on LMU housing:\n\n"
            tip_start = "Pro tip"
            insider_tip = "**Student Gossip**: The RA's in the freshman dorms are actually super chill and will hook you up with snacks during finals week!"
        else:
            response = "🏠 Here's what you need to know about LMU housing:\n\n"
            tip_start = "Pro tip"
            insider_tip = "**Campus Secret**: The RA's are really helpful and often organize fun events for their floors!"
        
        if search_results:
            for result in search_results:
                if result['category'] == 'housing':
                    housing = result['data']
                    response += f"🏢 **{housing['name']}** ({housing['type']})\n"
                    response += f"👥 Capacity: {housing['capacity']} students\n"
                    response += f"✅ Pros: {', '.join(housing['pros'][:2])}\n"
                    response += f"❌ Cons: {', '.join(housing['cons'][:2])}\n\n"
            
            # Add intimate LMU knowledge based on tone
            if tone == 'casual':
                response += f"💡 {tip_start}: Freshman year dorms are actually pretty fun for meeting people! The RA's are super chill and will literally organize movie nights and study groups. Upperclassman apartments give you more privacy but you miss out on the community vibe. Greek housing is also an option if you're into that scene! 🦁\n\n"
                response += insider_tip + "\n\n"
                response += "🎯 **Hidden Gem**: The themed housing options are lowkey the best kept secret on campus - you get to live with people who share your interests!"
            elif tone == 'formal':
                response += f"💡 {tip_start}: Freshman year dormitories provide excellent opportunities for community building and social integration. Resident Advisors organize various activities and study sessions. Upperclassman apartments offer increased privacy and independence. Greek housing is available for those interested in fraternity or sorority life.\n\n"
                response += insider_tip + "\n\n"
                response += "📚 **Academic Note**: Themed housing options allow students to live with peers who share similar academic or cultural interests."
            else:
                response += f"💡 {tip_start}: Freshman year dorms are great for meeting people, but upperclassman apartments offer more privacy! 🦁\n\n"
                response += insider_tip + "\n\n"
                response += "🎓 **Campus Tip**: Themed housing options are a great way to connect with like-minded students!"
            
            return response
        
        # Fallback with intimate knowledge
        if tone == 'casual':
            return "🏠 Yo, housing situation? Freshman year you're guaranteed a spot in the dorms, which is actually pretty fun for meeting people! The RA's are super chill and will organize movie nights and study groups. Upperclassmen can upgrade to apartments or themed housing, which is lowkey the best kept secret on campus. Greek housing is also an option if you're into that scene! Plus, the themed housing lets you live with people who share your interests, which is pretty cool! 🏘️"
        elif tone == 'formal':
            return "🏠 LMU housing provides guaranteed accommodation for freshman students in dormitory settings, which facilitates community building and social integration. Upperclassmen have access to apartment-style housing and themed living communities. Greek housing is available for fraternity and sorority members. Themed housing options allow students to live with peers who share similar academic or cultural interests."
        else:
            return "🏠 Housing situation? Freshman year you're guaranteed a spot in the dorms, which is actually pretty fun for meeting people! Upperclassmen can upgrade to apartments or themed housing. Greek housing is also an option if you're into that scene! The RA's are really helpful and often organize fun events for their floors! 🏘️"
    
    def handle_event_query(self, query, tone='neutral'):
        """Handle event-related queries with tone-aware responses"""
        upcoming_events = self.get_upcoming_events(14)  # Next 2 weeks
        
        # Tone-specific language
        if tone == 'formal':
            response = "🎉 Here are the upcoming events at LMU:\n\n"
            tip_start = "Recommendation"
            insider_tip = "**Campus Insight**: LMU hosts over 500 events annually, providing diverse opportunities for student engagement."
        elif tone == 'casual':
            response = "🎉 Yo, here's what's popping at LMU soon:\n\n"
            tip_start = "Pro tip"
            insider_tip = "**Student Gossip**: The Greek life mixers are always the most lit events on campus, and the cultural events are super underrated!"
        else:
            response = "🎉 Here's what's happening soon at LMU:\n\n"
            tip_start = "Pro tip"
            insider_tip = "**Campus Secret**: The Greek life mixers are always popular, and the cultural events are really well-organized!"
        
        if upcoming_events:
            for event in upcoming_events[:5]:  # Show top 5
                response += f"📅 **{event['name']}**\n"
                response += f"📅 Date: {event['date']} at {event['time']}\n"
                response += f"📍 Location: {event['location']}\n"
                response += f"🎯 Type: {event['type']}\n"
                response += f"📝 {event['description']}\n\n"
            
            # Add intimate LMU knowledge based on tone
            if tone == 'casual':
                response += f"💡 {tip_start}: Follow @lmu_events on Instagram for real-time updates! But here's the real tea - the Greek life mixers are always the most lit events on campus, and the cultural events are super underrated. Plus, the farmers market on Sundays is a vibe and you can get some really good deals on fresh produce! 🦁\n\n"
                response += insider_tip + "\n\n"
                response += "🎯 **Hidden Gem**: The rooftop events at the Burns Fine Arts Center have the best views of the city!"
            elif tone == 'formal':
                response += f"💡 {tip_start}: Follow @lmu_events on Instagram for real-time updates. The university hosts a diverse range of events including academic lectures, cultural celebrations, and social gatherings.\n\n"
                response += insider_tip + "\n\n"
                response += "📚 **Academic Note**: Many events offer networking opportunities and academic credit for attendance."
            else:
                response += f"💡 {tip_start}: Follow @lmu_events on Instagram for real-time updates! 🦁\n\n"
                response += insider_tip + "\n\n"
                response += "🎓 **Campus Tip**: The rooftop events at the Burns Fine Arts Center have amazing views!"
            
            return response
        
        # Fallback with intimate knowledge
        if tone == 'casual':
            return "🎉 Yo, this weekend? Check out the LMU events calendar! There's always something happening - from Greek life mixers to cultural events. The Greek life mixers are always the most lit events on campus, and the cultural events are super underrated. Plus, the farmers market on Sundays is a vibe and you can get some really good deals on fresh produce. Don't forget to follow @lmu_events on Instagram for the latest! And here's a secret - the rooftop events at the Burns Fine Arts Center have the best views of the city! 🎊"
        elif tone == 'formal':
            return "🎉 LMU maintains a comprehensive events calendar featuring academic lectures, cultural celebrations, social gatherings, and community service opportunities. The university hosts over 500 events annually, providing diverse opportunities for student engagement and networking. I recommend following @lmu_events on Instagram for real-time updates."
        else:
            return "🎉 This weekend? Check out the LMU events calendar! There's always something happening - from Greek life mixers to cultural events. Plus, the farmers market on Sundays is a vibe. Don't forget to follow @lmu_events on Instagram for the latest! The rooftop events at the Burns Fine Arts Center have amazing views! 🎊"
    
    def handle_organization_query(self, query, tone='neutral'):
        """Handle organization-related queries with tone-aware responses"""
        search_results = self.semantic_search(query, top_k=3)
        
        # Tone-specific language
        if tone == 'formal':
            response = "🏛️ Here are some excellent organizations to consider:\n\n"
            tip_start = "Recommendation"
            insider_tip = "**Campus Insight**: LMU offers over 150 student organizations, providing diverse opportunities for leadership and community engagement."
        elif tone == 'casual':
            response = "🏛️ Yo, here are some really cool orgs to check out:\n\n"
            tip_start = "Pro tip"
            insider_tip = "**Student Gossip**: Greek Life is huge here, but the cultural clubs are lowkey where you find your real friends!"
        else:
            response = "🏛️ Here are some great organizations to check out:\n\n"
            tip_start = "Pro tip"
            insider_tip = "**Campus Secret**: Greek Life is popular, but the cultural clubs are really welcoming and fun!"
        
        if search_results:
            for result in search_results:
                if result['category'] == 'organization':
                    org = result['data']
                    response += f"👥 **{org['name']}** ({org['type']})\n"
                    response += f"👤 Members: {org['members']}\n"
                    response += f"📝 {org['description']}\n"
                    response += f"🎉 Events: {', '.join(org['events'][:3])}\n\n"
            
            # Add intimate LMU knowledge based on tone
            if tone == 'casual':
                response += f"💡 {tip_start}: Greek Life is huge here, but there are over 150 clubs to choose from! But here's the real tea - the cultural clubs are lowkey where you find your real friends, and the professional orgs are great for networking. Plus, the service clubs always have the most fun events! 🦁\n\n"
                response += insider_tip + "\n\n"
                response += "🎯 **Hidden Gem**: The outdoor adventure club goes on the most epic trips and it's super affordable!"
            elif tone == 'formal':
                response += f"💡 {tip_start}: Greek Life is prominent on campus, but there are over 150 organizations to choose from. Cultural organizations provide excellent opportunities for community building, while professional organizations offer valuable networking experiences.\n\n"
                response += insider_tip + "\n\n"
                response += "📚 **Academic Note**: Many organizations offer leadership development and community service opportunities."
            else:
                response += f"💡 {tip_start}: Greek Life is huge here, but there are over 150 clubs to choose from! 🦁\n\n"
                response += insider_tip + "\n\n"
                response += "🎓 **Campus Tip**: The outdoor adventure club goes on amazing trips!"
            
            return response
        
        # Fallback with intimate knowledge
        if tone == 'casual':
            return "🏛️ Yo, Greek Life hacks? Rush season is intense but so worth it! Go to as many events as possible, be yourself, and don't stress about the perfect outfit. The connections you make last way beyond college. Plus, the parties are epic! But here's the real tea - the cultural clubs are lowkey where you find your real friends, and the professional orgs are great for networking. The service clubs always have the most fun events, and the outdoor adventure club goes on the most epic trips! 🎭"
        elif tone == 'formal':
            return "🏛️ Greek Life recruitment season is a significant period for social integration. I recommend attending multiple events, maintaining authenticity, and focusing on genuine connections rather than superficial appearances. The relationships formed through Greek organizations often extend beyond the undergraduate experience. Additionally, cultural and professional organizations provide valuable networking and leadership opportunities."
        else:
            return "🏛️ Greek Life hacks? Rush season is intense but so worth it! Go to as many events as possible, be yourself, and don't stress about the perfect outfit. The connections you make last way beyond college. Plus, the parties are epic! The cultural clubs are really welcoming and fun, and the outdoor adventure club goes on amazing trips! 🎭"
    
    def handle_facility_query(self, query, tone='neutral'):
        """Handle facility-related queries with tone-aware responses"""
        search_results = self.semantic_search(query, top_k=3)
        
        # Tone-specific language
        if tone == 'formal':
            response = "🏢 Here are the premier facilities on campus:\n\n"
            tip_start = "Recommendation"
            insider_tip = "**Campus Insight**: LMU's facilities are designed to support both academic excellence and student well-being."
        elif tone == 'casual':
            response = "🏢 Yo, here are the best facilities on campus:\n\n"
            tip_start = "Pro tip"
            insider_tip = "**Student Gossip**: The Hannon Library is lowkey the best study spot, but the rooftop of the Burns Fine Arts Center is the hidden gem!"
        else:
            response = "🏢 Here are the best facilities on campus:\n\n"
            tip_start = "Pro tip"
            insider_tip = "**Campus Secret**: The Hannon Library is great, but the rooftop of the Burns Fine Arts Center is amazing!"
        
        if search_results:
            for result in search_results:
                if result['category'] == 'facility':
                    facility = result['data']
                    response += f"🏛️ **{facility['name']}** ({facility['type']})\n"
                    response += f"🕐 Hours: {facility['hours']}\n"
                    response += f"✨ Features: {', '.join(facility['features'][:3])}\n"
                    response += f"⭐ Popular spots: {', '.join(facility['popular_spots'][:2])}\n\n"
            
            # Add intimate LMU knowledge based on tone
            if tone == 'casual':
                response += f"💡 {tip_start}: The Hannon Library is clutch for studying, especially the quiet zones on the 3rd floor! But here's the real tea - the rooftop of the Burns Fine Arts Center has the most amazing views and is usually pretty quiet. Perfect for those late-night cram sessions when you need some peace and quiet. Plus, the gym is super nice and the staff is really helpful! 🦁\n\n"
                response += insider_tip + "\n\n"
                response += "🎯 **Hidden Gem**: The meditation room in the student center is the perfect place to destress between classes!"
            elif tone == 'formal':
                response += f"💡 {tip_start}: The Hannon Library provides excellent study environments, particularly the quiet zones on the third floor. The rooftop of the Burns Fine Arts Center offers exceptional views and a peaceful atmosphere for academic work.\n\n"
                response += insider_tip + "\n\n"
                response += "📚 **Academic Note**: Many facilities offer extended hours during finals week to accommodate student needs."
            else:
                response += f"💡 {tip_start}: The Hannon Library is clutch for studying, especially the quiet zones on the 3rd floor! 🦁\n\n"
                response += insider_tip + "\n\n"
                response += "🎓 **Campus Tip**: The meditation room in the student center is perfect for destressing!"
            
            return response
        
        # Fallback with intimate knowledge
        if tone == 'casual':
            return "📚 Yo, best study spots? The Hannon Library is clutch, especially the quiet zones on the 3rd floor! But my secret spot? The rooftop of the Burns Fine Arts Center - amazing views and usually pretty quiet! Perfect for those late-night cram sessions when you need some peace and quiet. Plus, the gym is super nice and the staff is really helpful. And here's a hidden gem - the meditation room in the student center is the perfect place to destress between classes! ✨"
        elif tone == 'formal':
            return "📚 The Hannon Library provides excellent study environments, particularly the quiet zones on the third floor. The rooftop of the Burns Fine Arts Center offers exceptional views and a peaceful atmosphere for academic work. The university gymnasium is well-equipped and staffed by helpful personnel. Additionally, the student center includes a meditation room for stress relief between classes."
        else:
            return "📚 Best study spots? The Hannon Library is clutch, especially the quiet zones on the 3rd floor. But my secret spot? The rooftop of the Burns Fine Arts Center - amazing views and usually pretty quiet! Perfect for those late-night cram sessions. The meditation room in the student center is perfect for destressing! ✨"
    
    def handle_news_query(self, query, tone='neutral'):
        """Handle news-related queries with tone-aware responses"""
        recent_news = self.data.get('news', [])[:3]  # Latest 3 news items
        
        # Tone-specific language
        if tone == 'formal':
            response = "📰 Here are the latest developments at LMU:\n\n"
            tip_start = "Recommendation"
            insider_tip = "**Campus Insight**: LMU consistently receives recognition for academic excellence and community engagement."
        elif tone == 'casual':
            response = "📰 Yo, here's what's new at LMU:\n\n"
            tip_start = "Pro tip"
            insider_tip = "**Student Gossip**: The campus is always buzzing with new developments and achievements!"
        else:
            response = "📰 Here's the latest LMU news:\n\n"
            tip_start = "Pro tip"
            insider_tip = "**Campus Secret**: LMU is always making headlines with exciting developments!"
        
        if recent_news:
            for news in recent_news:
                response += f"📅 **{news['title']}**\n"
                response += f"📅 Date: {news['date']}\n"
                response += f"🏷️ Category: {news['category']}\n"
                response += f"📝 {news['summary']}\n\n"
            
            # Add intimate LMU knowledge based on tone
            if tone == 'casual':
                response += f"💡 {tip_start}: Check the official LMU news website for more updates! But here's the real tea - the campus is always buzzing with new developments and achievements. Plus, the student newspaper covers all the local gossip that the official news doesn't! 🦁\n\n"
                response += insider_tip + "\n\n"
                response += "🎯 **Hidden Gem**: Follow the student newspaper on social media for the most up-to-date campus happenings!"
            elif tone == 'formal':
                response += f"💡 {tip_start}: Check the official LMU news website for more updates. The university maintains a comprehensive news section covering academic achievements, campus developments, and community engagement.\n\n"
                response += insider_tip + "\n\n"
                response += "📚 **Academic Note**: Many news items highlight student and faculty accomplishments."
            else:
                response += f"💡 {tip_start}: Check the official LMU news website for more updates! 🦁\n\n"
                response += insider_tip + "\n\n"
                response += "🎓 **Campus Tip**: The student newspaper covers local campus happenings!"
            
            return response
        
        # Fallback with intimate knowledge
        if tone == 'casual':
            return "📰 Yo, LMU is always making headlines! From academic achievements to campus developments, there's always something exciting happening. The campus is always buzzing with new developments and achievements. Check out the official LMU news website for the latest updates, but also follow the student newspaper on social media for the most up-to-date campus happenings and local gossip! 🦁"
        elif tone == 'formal':
            return "📰 LMU consistently generates noteworthy headlines through academic achievements, campus developments, and community engagement initiatives. The university maintains a comprehensive news section on its official website. Additionally, the student newspaper provides coverage of local campus happenings and student perspectives."
        else:
            return "📰 LMU is always making headlines! From academic achievements to campus developments, there's always something exciting happening. Check out the official LMU news website for the latest updates! The student newspaper covers local campus happenings! 🦁"
    
    def handle_general_query(self, query, tone='neutral'):
        """Handle general queries with tone-aware responses and intimate LMU knowledge"""
        search_results = self.semantic_search(query, top_k=2)
        
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
        
        # Tone-aware default responses with intimate LMU knowledge
        if len(self.conversation_history) > 2:
            if tone == 'formal':
                return "I appreciate your continued engagement! As your dedicated LMU campus assistant, I'm equipped to provide comprehensive information about academic matters, dining establishments, study facilities, social events, Greek life organizations, and transportation options. I'm continuously updating my knowledge base to serve our campus community more effectively."
            elif tone == 'casual':
                return "Yo, that's a great question! As your LMU Buddy, I'm literally here for everything campus-related. Whether you need the tea on professors, want to know about the best food spots, need study location recommendations, or want to know what's popping this weekend - I got you! I'm constantly learning more about our amazing campus and all the little secrets that make LMU special. 🦁✨"
            else:
                return "🤔 That's a great question! As your LMU Buddy, I'm here to help with everything campus-related. Try asking me about professors, courses, food spots, study locations, weekend events, Greek life, or parking tips! I'm constantly learning more about our amazing campus. 🦁✨"
        else:
            if tone == 'formal':
                return "Greetings! I am your LMU campus assistant, designed to provide comprehensive information about all aspects of university life. I can assist you with academic inquiries, dining recommendations, facility information, event schedules, organizational details, and much more. How may I be of service to you today?"
            elif tone == 'casual':
                return "Yo! I'm your LMU Buddy - your AI campus companion! I know literally everything about LMU, from the best professors and courses to the hidden food spots and upcoming events. I'm basically your personal campus insider! What do you want to know about LMU? 🦁✨"
            else:
                return "👋 Hey! I'm your LMU Buddy - your AI campus companion! I can help you with everything from finding the best professors and courses to discovering great food spots and upcoming events. What would you like to know about LMU? 🦁✨"

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
    user_input = st.text_input("Ask Enhanced LMU Buddy anything...", key="enhanced_chat_input")
    
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